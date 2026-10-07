# CLAUDE.md

Harness de Instagram: duas skills em `.claude/skills/` (`instagram-conteudo`,
`instagram-comentarios`) alimentadas por `nicho/perfil.md` e `nicho/faq.md`.

- Idioma de tudo (conteúdo, código, commits): português do Brasil.
- Antes de criar conteúdo ou responder comentário, leia `nicho/perfil.md`.
  Se o nicho ainda não estiver preenchido, pergunte — não invente.
- Nunca rode `scripts/ig_comments.py publicar ... --confirmar` sem aprovação
  explícita do usuário na conversa atual. Nunca publique/agende post sem OK.
- Nunca commite `.env`, tokens ou `comentarios/*.json`.
- Só Graph API oficial; não sugerir bibliotecas de API privada (instagrapi etc.).
- Scripts Python: só stdlib, exceto Playwright no render de carrossel.
- Peças novas vão em `conteudo/AAAA-MM-DD-<slug>/`, a partir de `conteudo/_modelo/`.
