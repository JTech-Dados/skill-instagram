# CLAUDE.md

Harness de Instagram: duas skills em `.claude/skills/` (`instagram-conteudo`,
`instagram-comentarios`) alimentadas por um perfil em `perfis/<perfil>/` (`perfil.md` + `faq.md`).
Perfis atuais: `tecnologia` (conta do dono do repo) e `maternidade` (conta da esposa). `_modelo` é só template.

- Idioma de tudo (conteúdo, código, commits): português do Brasil.
- Se o pedido não disser qual perfil, pergunte. Nunca misture voz, FAQ ou
  conteúdo entre perfis.
- Antes de criar conteúdo ou responder comentário, leia `perfis/<perfil>/perfil.md`.
  Campos `<...>` em aberto: pergunte — não invente.
- Nunca rode `scripts/ig_comments.py publicar ... --confirmar` sem aprovação
  explícita do usuário na conversa atual. Nunca publique/agende post sem OK.
- Nunca commite `.env`, tokens ou `comentarios/**/*.json`.
- Só Graph API oficial; não sugerir bibliotecas de API privada (instagrapi etc.).
- Scripts Python: só stdlib, exceto Playwright no render de carrossel.
- Pendências do projeto: `.claude/pendencias.md` — atualize ao concluir algo.
- Peças novas vão em `conteudo/<perfil>/AAAA-MM-DD-<slug>/`, a partir de `conteudo/_modelo/`.
