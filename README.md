# skill-instagram

Harness para o Claude Code produzir conteúdo de Instagram para **mais de uma
conta/nicho** (hoje: `tecnologia` e `maternidade`) e cuidar dos comentários com a voz da marca — sempre com aprovação
humana antes de publicar.

## Como funciona

```
perfis/<perfil>/perfil.md ─┬─► skill instagram-conteudo   ──► conteudo/<perfil>/<data>-<peça>/
perfis/<perfil>/faq.md    ─┘                                   roteiro.md · legenda.md · slide-XX.png
perfis/<perfil>/.env      ───► skill instagram-comentarios ──► comentarios/<perfil>/rascunho-<data>.json
                                                           └─(você aprova)─► Graph API
```

| Peça | Arquivo |
|---|---|
| Perfil da marca (nicho, público, pilares, voz, compliance, visual) | `perfis/<perfil>/perfil.md` |
| Respostas aprovadas e casos que sempre escalam | `perfis/<perfil>/faq.md` |
| Token da conta (não versionado) | `perfis/<perfil>/.env` |
| Template para criar um perfil novo | `perfis/_modelo/` |
| Skill de conteúdo (pauta, carrossel, reels, stories, legenda) | `.claude/skills/instagram-conteudo/` |
| Skill de comentários (triagem, rascunho, aprovação, publicação) | `.claude/skills/instagram-comentarios/` |
| Graph API: buscar pendentes / publicar aprovados / DM para quem comentou | `scripts/ig_comments.py` |
| Campanhas "comenta X que eu te mando o link" | `perfis/<perfil>/campanhas.json` |
| Carrossel HTML → PNG 1080×1350 | `scripts/render_carrossel.py` + `templates/carrossel.html` |
| Ferramentas avaliadas (comentários, DMs, tendências) | `docs/ferramentas-comentarios.md` |
| **Conectar o Instagram (passo a passo)** | [`CONECTAR-INSTAGRAM.md`](CONECTAR-INSTAGRAM.md) |
| Referência técnica da API | `docs/setup-meta.md` |

## Começando

1. **Preencha `perfis/tecnologia/perfil.md` e `perfis/maternidade/perfil.md`**
   (e os `faq.md`). É o que faz o conteúdo soar como cada conta e não como
   "post genérico de IA". Enquanto estiverem em aberto, as skills perguntam.
   Para outra conta: copie `perfis/_modelo/` para `perfis/<novo>/`.
2. Abra o Claude Code na pasta do repo e peça, por exemplo:
   - "monta o calendário de novembro do tecnologia, 3 posts por semana"
   - "cria um carrossel de maternidade sobre <tema> e gera as imagens"
   - "roteiro de reels de 30s sobre <tema> pro tecnologia"
   - "responde os comentários da conta de maternidade dos últimos 3 dias"
   - "manda o link do guia na DM de quem comentou GUIA no último reel do tecnologia"
3. Para comentários e DM, conecte as contas seguindo
   **[`CONECTAR-INSTAGRAM.md`](CONECTAR-INSTAGRAM.md)** (criar o app na Meta, gerar o token, guardar).

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
- **Perfis não se misturam.** Voz, FAQ, token e arquivos ficam separados por pasta.
- **Dados de terceiros fora do git.** `comentarios/**/*.json` está no `.gitignore`.

## Pendências

O que falta para rodar nas duas contas está em [`.claude/pendencias.md`](.claude/pendencias.md).

## Licença

[MIT](LICENSE) © 2026 JTech-Dados.
