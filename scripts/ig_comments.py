#!/usr/bin/env python3
"""Busca comentários do Instagram, publica respostas aprovadas e envia DM a quem
comentou (private reply), via Graph API oficial.

Sem dependências externas (só stdlib).

Cada perfil (perfis/<perfil>/) tem seu próprio .env com o token da conta.
Com --perfil, o script carrega perfis/<perfil>/.env e grava em comentarios/<perfil>/.
Variáveis já definidas no ambiente têm prioridade sobre o .env. Na nuvem (sem .env),
use variáveis com o sufixo do perfil: IG_ACCESS_TOKEN_TECNOLOGIA, IG_USERNAME_MATERNIDADE...

Variáveis de ambiente:
  IG_ACCESS_TOKEN  token da conta profissional (obrigatório)
  IG_USER_ID       id da conta IG (padrão: "me", funciona com Instagram Login)
  IG_USERNAME      @ da conta, sem @ (usado para detectar respostas próprias;
                   se vazio, é buscado na API)
  IG_API_HOST      graph.instagram.com (Instagram Login, padrão)
                   ou graph.facebook.com (Facebook Login / Página vinculada)
  IG_API_VERSION   padrão v26.0

Uso:
  python3 scripts/ig_comments.py --perfil tecnologia fetch [--dias 3] [--posts 15] [--saida ARQ]
  python3 scripts/ig_comments.py --perfil tecnologia campanha [--nome NOME] [--dias 7]
  python3 scripts/ig_comments.py --perfil tecnologia publicar ARQ.json [--confirmar] [--intervalo 4]

Itens do rascunho (acao = "responder") podem ter "resposta" (pública), "dm"
(mensagem privada para quem comentou) ou os dois. A DM usa o recurso de
"private reply": 1 por comentário, até 7 dias depois do comentário.
"""

import argparse
import datetime as dt
import json
import os
import random
import re
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
    # variáveis com sufixo do perfil (ex.: IG_ACCESS_TOKEN_TECNOLOGIA) vencem as genéricas
    sufixo = "_" + re.sub(r"\W", "_", perfil).upper()
    for chave in ("IG_ACCESS_TOKEN", "IG_USERNAME", "IG_USER_ID", "IG_API_HOST", "IG_API_VERSION"):
        if os.environ.get(chave + sufixo):
            os.environ[chave] = os.environ[chave + sufixo]
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
        sys.exit("IG_ACCESS_TOKEN não definido (perfis/<perfil>/.env ou IG_ACCESS_TOKEN_<PERFIL>). Veja docs/setup-meta.md.")
    host = os.environ.get("IG_API_HOST", "graph.instagram.com")
    versao = os.environ.get("IG_API_VERSION", "v26.0")
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


def _pasta_saida(args):
    pasta = PASTA_COMENTARIOS / args.perfil if args.perfil else PASTA_COMENTARIOS
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def _carregar_historico(pasta):
    arq = pasta / "historico.json"
    return json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else []


def _registrar_historico(pasta, item):
    historico = _carregar_historico(pasta)
    historico.append({
        "comment_id": item.get("comment_id"),
        "username": item.get("username"),
        "media_id": item.get("media_id"),
        "acao": item.get("acao"),
        "campanha": item.get("campanha"),
        "dm": bool(item.get("dm_enviada_em")),
        "em": item.get("publicado_em"),
    })
    (pasta / "historico.json").write_text(json.dumps(historico, ensure_ascii=False, indent=2), encoding="utf-8")


def _shortcode(url_ou_id):
    m = re.search(r"/(?:p|reel|reels|tv)/([^/?#]+)", url_ou_id or "")
    return m.group(1) if m else None


def _buscar_pendentes(cfg, dias, n_posts, ja_tratados):
    username = cfg["username"]
    if not username:
        username = _request(cfg, "GET", cfg["user_id"], {"fields": "username"})["username"].lower()

    corte = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=dias)
    posts = _paginar(
        cfg,
        f"{cfg['user_id']}/media",
        {"fields": "id,caption,permalink,timestamp,comments_count", "limit": 25},
        n_posts,
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
            if autor == username or c["id"] in ja_tratados or _parse_ts(c["timestamp"]) < corte:
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
    return pendentes, len(posts)


def cmd_fetch(args):
    cfg = _config()
    pasta = _pasta_saida(args)
    ja_tratados = {h["comment_id"] for h in _carregar_historico(pasta)}
    pendentes, n_posts = _buscar_pendentes(cfg, args.dias, args.posts, ja_tratados)
    saida = Path(args.saida) if args.saida else pasta / f"pendentes-{dt.date.today().isoformat()}.json"
    saida.write_text(json.dumps(pendentes, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(pendentes)} comentário(s) pendente(s) em {n_posts} post(s) → {saida}")


def cmd_campanha(args):
    if not args.perfil:
        sys.exit("campanha exige --perfil.")
    arq = PASTA_PERFIS / args.perfil / "campanhas.json"
    if not arq.exists():
        sys.exit(f"{arq} não existe. Copie perfis/_modelo/campanhas.json e preencha.")
    campanhas = [c for c in json.loads(arq.read_text(encoding="utf-8"))["campanhas"] if c.get("ativa")]
    if args.nome:
        campanhas = [c for c in campanhas if c.get("nome") == args.nome]
    if not campanhas:
        sys.exit("Nenhuma campanha ativa encontrada.")

    cfg = _config()
    pasta = _pasta_saida(args)
    historico = _carregar_historico(pasta)
    ja_tratados = {h["comment_id"] for h in historico}
    pendentes, _ = _buscar_pendentes(cfg, min(args.dias, 7), args.posts, ja_tratados)

    rascunho = []
    for camp in campanhas:
        alvo = str(camp["post"])
        codigo = _shortcode(alvo)
        palavra = (camp.get("palavra_chave") or "").strip().lower()
        # 1 DM por pessoa por campanha, contando o que já foi enviado antes
        receberam = {
            (h.get("username") or "").lower()
            for h in historico if h.get("dm") and h.get("campanha") == camp["nome"]
        }
        for c in pendentes:
            mesmo_post = c["media_id"] == alvo or (codigo and _shortcode(c["media_permalink"]) == codigo)
            if not mesmo_post:
                continue
            if palavra and palavra not in c["texto"].lower():
                continue
            pessoa = (c["username"] or "").lower()
            if pessoa in receberam:
                continue
            receberam.add(pessoa)
            rascunho.append({
                **c,
                "categoria": "palavra_chave",
                "campanha": camp["nome"],
                "acao": "responder",
                "resposta": random.choice(camp.get("respostas_publicas") or [""]),
                "dm": camp["dm"].replace("{username}", c["username"] or ""),
                "motivo": f"campanha {camp['nome']}",
                "aprovado": False,
            })

    if not rascunho:
        print("Ninguém novo para receber DM.")
        return
    saida = pasta / f"campanha-{dt.datetime.now().strftime('%Y-%m-%d-%H%M%S')}.json"
    saida.write_text(json.dumps(rascunho, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(rascunho)} pessoa(s) para receber DM → {saida}")
    print("Revise, marque \"aprovado\": true e rode: publicar <arquivo> --confirmar")


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
            print(f"[responder] {alvo}")
            if i.get("resposta"):
                print(f"    pública → {i['resposta']}")
            if i.get("dm"):
                print(f"    DM      → {i['dm']}")
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
    pasta = _pasta_saida(args)
    falhas = 0
    for n, i in enumerate(fila):
        if not i.get("comment_id"):
            i["erro"] = "sem comment_id (comentário inserido à mão)"
            falhas += 1
            continue
        try:
            agora = lambda: dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
            if i["acao"] == "responder":
                if not i.get("resposta") and not i.get("dm"):
                    raise ApiError("item sem 'resposta' nem 'dm'")
                # cada etapa grava seu carimbo: se falhar no meio, não repete o que já foi
                if i.get("resposta") and not i.get("reply_id"):
                    resp = _request(cfg, "POST", f"{i['comment_id']}/replies", {"message": i["resposta"]})
                    i["reply_id"] = resp.get("id")
                if i.get("dm") and not i.get("dm_enviada_em"):
                    _request(cfg, "POST", f"{cfg['user_id']}/messages", {
                        "recipient": json.dumps({"comment_id": i["comment_id"]}),
                        "message": json.dumps({"text": i["dm"]}, ensure_ascii=False),
                    })
                    i["dm_enviada_em"] = agora()
            else:
                _request(cfg, "POST", i["comment_id"], {"hide": "true"})
            i["publicado_em"] = agora()
            i.pop("erro", None)
            _registrar_historico(pasta, i)
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

    c = sub.add_parser("campanha", help="monta rascunho de DMs para quem comentou em post de campanha")
    c.add_argument("--nome", help="só esta campanha (padrão: todas as ativas)")
    c.add_argument("--dias", type=int, default=7, help="janela (máx. 7, limite da private reply)")
    c.add_argument("--posts", type=int, default=15, help="nº de posts recentes (padrão 15)")
    c.set_defaults(func=cmd_campanha)

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
