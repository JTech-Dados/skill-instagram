# skill-instagram

Harness para o Claude Code produzir conteúdo de Instagram para **um nicho
específico** e cuidar dos comentários com a voz da marca — sempre com aprovação
humana antes de publicar.

## Como funciona

```
nicho/perfil.md  ──┬──►  skill instagram-conteudo   ──►  conteudo/<data>-<peça>/
nicho/faq.md     ──┘                                      roteiro.md · legenda.md · slide-XX.png
                   └──►  skill instagram-comentarios ──►  comentarios/rascunho-<data>.json
                                                           └─(você aprova)─► Graph API
```

| Peça | Arquivo |
|---|---|
| Perfil da marca (nicho, público, pilares, voz, compliance, visual) | `nicho/perfil.md` |
| Respostas aprovadas e casos que sempre escalam | `nicho/faq.md` |
| Skill de conteúdo (pauta, carrossel, reels, stories, legenda) | `.claude/skills/instagram-conteudo/` |
| Skill de comentários (triagem, rascunho, aprovação, publicação) | `.claude/skills/instagram-comentarios/` |
| Graph API: buscar pendentes / publicar aprovados | `scripts/ig_comments.py` |
| Carrossel HTML → PNG 1080×1350 | `scripts/render_carrossel.py` + `templates/carrossel.html` |
| Ferramentas open source para comentários | `docs/ferramentas-comentarios.md` |
| Configurar token da Meta | `docs/setup-meta.md` |

## Começando

1. **Preencha `nicho/perfil.md`** (e o `faq.md`). É o que faz o conteúdo soar
   como você e não como "post genérico de IA".
2. Abra o Claude Code na pasta do repo e peça, por exemplo:
   - "monta o calendário de novembro, 3 posts por semana"
   - "cria um carrossel sobre <tema> e gera as imagens"
   - "roteiro de reels de 30s sobre <tema>"
   - "responde os comentários dos últimos 3 dias"
3. Para comentários, configure o token antes: `docs/setup-meta.md`.

### Dependências

- Python 3.10+
- Carrossel em PNG: `pip install -r requirements.txt && playwright install chromium`
  (ou defina `CHROMIUM_PATH` para um Chromium já instalado).
- Comentários: só a biblioteca padrão + `IG_ACCESS_TOKEN`.

## Princípios

- **Nada é publicado sem OK humano.** O script de publicação roda em modo
  simulação por padrão; `--confirmar` só depois da aprovação.
- **Só API oficial.** Nada de automação por login/senha — risco de ban.
- **Sem fatos inventados.** Números marcados com `[FONTE?]`; preço/links só da FAQ.
- **Dados de terceiros fora do git.** `comentarios/*.json` está no `.gitignore`.
