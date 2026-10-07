#!/usr/bin/env python3
"""Busca e publica respostas de comentários do Instagram via Graph API oficial.

Sem dependências externas (só stdlib).

Cada perfil (perfis/<perfil>/) tem seu próprio .env com o token da conta.
Com --perfil, o script carrega perfis/<perfil>/.env e grava em comentarios/<perfil>/.
Variáveis já definidas no ambiente têm prioridade sobre o .env.

Variáveis de ambiente:
  IG_ACCESS_TOKEN  token da conta profissional (obrigatório)
  IG_USER_ID       id da conta IG (padrão: "me", funciona com Instagram Login)
  IG_USERNAME      @ da conta, sem @ (usado para detectar respostas próprias;
                   se vazio, é buscado na API)
  IG_API_HOST      graph.instagram.com (Instagram Login, padrão)
                   ou graph.facebook.com (Facebook Login / Página vinculada)
  IG_API_VERSION   padrão v24.0

Uso:
  python3 scripts/ig_comments.py --perfil tecnologia fetch [--dias 3] [--posts 15] [--saida ARQ]
  python3 scripts/ig_comments.py --perfil tecnologia publicar ARQ.json [--confirmar] [--intervalo 4]
"""

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA_PERFIS = RAIZ / "perfis"
PASTA_COMENTARIOS = RAIZ / "comentarios"


class ApiError(RuntimeError):
    pass


def _carregar_perfil(perfil):
    pasta = PASTA_PERFIS / perfil
    if not pasta.is_dir():
        existentes = sorted(d.name for d in PASTA_PERFIS.iterdir() if d.is_dir() and not d.name.startswith("_"))
        sys.exit(f"Perfil '{perfil}' não existe. Perfis: {', '.join(existentes)}")
    env = pasta / ".env"
    if env.exists():
        for linha in env.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))


def _config():
    token = os.environ.get("IG_ACCESS_TOKEN")
    if not token:
        sys.exit("IG_ACCESS_TOKEN não definido (perfis/<perfil>/.env). Veja docs/setup-meta.md.")
    host = os.environ.get("IG_API_HOST", "graph.instagram.com")
    versao = os.environ.get("IG_API_VERSION", "v24.0")
    return {
        "token": token,
        "base": f"https://{host}/{versao}",
        "user_id": os.environ.get("IG_USER_ID", "me"),
        "username": os.environ.get("IG_USERNAME", "").lstrip("@").lower(),
    }


def _request(cfg, metodo, caminho, params=None, tentativas=3):
    params = dict(params or {})
    params["access_token"] = cfg["token"]
    url = f"{cfg['base']}/{caminho.lstrip('/')}"
    dados = None
    if metodo == "GET":
        url += "?" + urllib.parse.urlencode(params)
    else:
        dados = urllib.parse.urlencode(params).encode()

    for tentativa in range(tentativas):
        req = urllib.request.Request(url, data=dados, method=metodo)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            corpo = e.read().decode(errors="replace")
            # 429 / 5xx: tenta de novo com backoff; o resto é erro definitivo
            if e.code == 429 or e.code >= 500:
                if tentativa < tentativas - 1:
                    time.sleep(2 ** (tentativa + 1))
                    continue
            raise ApiError(f"HTTP {e.code} em {caminho}: {corpo}") from None
        except urllib.error.URLError as e:
            if tentativa < tentativas - 1:
                time.sleep(2 ** (tentativa + 1))
                continue
            raise ApiError(f"Falha de rede em {caminho}: {e.reason}") from None


def _paginar(cfg, caminho, params, limite):
    itens = []
    resp = _request(cfg, "GET", caminho, params)
    while True:
        itens.extend(resp.get("data", []))
        proximo = resp.get("paging", {}).get("next")
        if len(itens) >= limite or not proximo:
            return itens[:limite]
        with urllib.request.urlopen(proximo, timeout=30) as r:
            resp = json.loads(r.read().decode())


def _parse_ts(ts):
    # Formato da Graph API: 2026-10-07T12:34:56+0000
    return dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z")


def cmd_fetch(args):
    cfg = _config()
    username = cfg["username"]
    if not username:
        username = _request(cfg, "GET", cfg["user_id"], {"fields": "username"})["username"].lower()

    corte = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.dias)
    posts = _paginar(
        cfg,
        f"{cfg['user_id']}/media",
        {"fields": "id,caption,permalink,timestamp,comments_count", "limit": 25},
        args.posts,
    )

    pendentes = []
    for post in posts:
        if not post.get("comments_count"):
            continue
        comentarios = _paginar(
            cfg,
            f"{post['id']}/comments",
            {
                "fields": "id,text,username,timestamp,like_count,replies{id,text,username,timestamp}",
                "limit": 50,
            },
            500,
        )
        for c in comentarios:
            autor = (c.get("username") or "").lower()
            if autor == username or _parse_ts(c["timestamp"]) < corte:
                continue
            respostas = c.get("replies", {}).get("data", [])
            if any((r.get("username") or "").lower() == username for r in respostas):
                continue  # já respondido pela conta
            pendentes.append({
                "comment_id": c["id"],
                "username": c.get("username"),
                "texto": c.get("text", ""),
                "timestamp": c["timestamp"],
                "curtidas": c.get("like_count", 0),
                "media_id": post["id"],
                "media_permalink": post.get("permalink"),
                "media_caption": (post.get("caption") or "")[:500],
                "outras_respostas": [
                    {"username": r.get("username"), "texto": r.get("text")} for r in respostas
                ],
            })

    pendentes.sort(key=lambda c: c["timestamp"])
    pasta = PASTA_COMENTARIOS / args.perfil if args.perfil else PASTA_COMENTARIOS
    saida = Path(args.saida) if args.saida else (
        pasta / f"pendentes-{dt.date.today().isoformat()}.json"
    )
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(json.dumps(pendentes, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(pendentes)} comentário(s) pendente(s) em {len(posts)} post(s) → {saida}")


def cmd_publicar(args):
    arquivo = Path(args.arquivo)
    itens = json.loads(arquivo.read_text(encoding="utf-8"))
    fila = [
        i for i in itens
        if i.get("aprovado") is True
        and i.get("acao") in ("responder", "ocultar")
        and not i.get("publicado_em")
    ]
    escalar = [i for i in itens if i.get("acao") == "escalar"]

    if not fila:
        print("Nada aprovado para publicar.")
    for i in fila:
        alvo = f"@{i.get('username')}: {i.get('texto', '')[:60]!r}"
        if i["acao"] == "responder":
            print(f"[responder] {alvo}\n    → {i['resposta']}")
        else:
            print(f"[ocultar]   {alvo}")

    if escalar:
        print(f"\n{len(escalar)} item(ns) para resolver manualmente (escalar):")
        for i in escalar:
            print(f"  - @{i.get('username')}: {i.get('texto', '')[:80]!r} ({i.get('motivo', '')})")

    if not args.confirmar:
        if fila:
            print("\nSimulação. Rode com --confirmar para publicar.")
        return

    cfg = _config()
    falhas = 0
    for n, i in enumerate(fila):
        if not i.get("comment_id"):
            i["erro"] = "sem comment_id (comentário inserido à mão)"
            falhas += 1
            continue
        try:
            if i["acao"] == "responder":
                resp = _request(cfg, "POST", f"{i['comment_id']}/replies", {"message": i["resposta"]})
                i["reply_id"] = resp.get("id")
            else:
                _request(cfg, "POST", i["comment_id"], {"hide": "true"})
            i["publicado_em"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
            i.pop("erro", None)
        except ApiError as e:
            i["erro"] = str(e)
            falhas += 1
        # grava a cada item para não perder estado se o processo cair
        arquivo.write_text(json.dumps(itens, ensure_ascii=False, indent=2), encoding="utf-8")
        if n < len(fila) - 1:
            time.sleep(args.intervalo)

    print(f"\nPublicados: {len(fila) - falhas} · Falhas: {falhas} (detalhes em {arquivo})")
    if falhas:
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--perfil", help="pasta em perfis/ (ex.: tecnologia, maternidade)")
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch", help="busca comentários sem resposta")
    f.add_argument("--dias", type=int, default=3, help="janela de comentários (padrão 3)")
    f.add_argument("--posts", type=int, default=15, help="nº de posts recentes (padrão 15)")
    f.add_argument("--saida", help="arquivo de saída (padrão comentarios/<perfil>/pendentes-<data>.json)")
    f.set_defaults(func=cmd_fetch)

    pub = sub.add_parser("publicar", help="publica respostas aprovadas")
    pub.add_argument("arquivo")
    pub.add_argument("--confirmar", action="store_true", help="publica de verdade (sem isso é simulação)")
    pub.add_argument("--intervalo", type=float, default=4, help="segundos entre envios (padrão 4)")
    pub.set_defaults(func=cmd_publicar)

    args = p.parse_args()
    if args.perfil:
        _carregar_perfil(args.perfil)
    try:
        args.func(args)
    except ApiError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
