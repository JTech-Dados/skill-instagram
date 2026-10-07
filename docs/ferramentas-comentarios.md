# Ferramentas open source para responder comentários do Instagram

Levantamento de outubro/2026. Antes de adotar qualquer uma, confira licença,
data do último commit e se usa a **API oficial** (Graph API) — ver "Evitar" no fim.

## Resumo

| Ferramenta | Tipo | O que faz com comentários | Quando usar |
|---|---|---|---|
| **Este repo** (`scripts/ig_comments.py` + skill `instagram-comentarios`) | CLI Python + skill do Claude | Busca pendentes, Claude rascunha, você aprova, script publica/oculta | Ponto de partida: zero infra, aprovação humana em tudo |
| **[n8n](https://n8n.io) + template [18455](https://n8n.io/workflows/18455-reply-to-instagram-comments-and-send-dms-with-facebook-graph-api-and-gemini/)** | Automação self-hosted (licença *fair-code*, não OSI) | Recebe webhook da Meta, gera resposta com LLM, responde e opcionalmente manda DM; log em Sheets/Slack; filtro anti-loop | Quando quiser resposta **em tempo real** 24/7. Dá para trocar o Gemini pelo Claude no nó de IA |
| **[instagram-mcp-server (luminarylane)](https://glama.ai/mcp/servers/luminarylane/instagram-mcp-server)** | MCP server (TypeScript/npm) | `ig_get_comments`, responder e excluir comentário, publicar, insights; rate limit e backoff embutidos | Para o Claude operar o Instagram direto por ferramentas MCP, sem script |
| **[instagram-mcp (AleemHaider)](https://mcpservers.org/servers/aleemhaider/instagram-mcp)** | MCP server (Python, `pip install instagram-mcp`) | ~24 ferramentas: ler, publicar, comentar, DM, insights | Alternativa Python ao anterior, cobre também DMs |
| **[instagram-mcp-server (osborn1997)](https://glama.ai/mcp/servers/@osborn1997/instagram-mcp-server/blob/d319db9e093ae072859a0a90f41e27808521f628/README.md)** | MCP server | Ver posts, comentários, responder, mensagens | Outra opção MCP; compare manutenção antes |
| **[InstaAuto / insta-p8](https://github.com/ayuuxh2/insta-p8)** | App self-hosted | Auto-resposta em comentário + DM por palavra-chave, automações por post | Clone open source do estilo ManyChat ("comenta GUIA") |
| **[Chatwoot](https://chatwoot.com/features/instagram-integration)** | Central de atendimento open source | Caixa de entrada de **DMs** do Instagram (comentários públicos não são nativos) | Se o time precisa atender DMs em equipe, com histórico e etiquetas |
| **Postiz** | Agendador open source (AGPL) | Foco em agendamento; não gerencia comentários | Para agendar posts, não para comentários |

## Arquitetura recomendada (evolução)

1. **Agora — semiautomático (este repo).** Rode a skill 1–2x por dia:
   `fetch → Claude rascunha → você aprova → publicar`. Sem servidor, sem custo fixo,
   e você calibra a voz da marca e o `faq.md` de cada perfil com casos reais.
2. **Depois — tempo real com aprovação parcial.** Suba o n8n (Docker), assine o
   webhook `comments` da conta e reaproveite as **mesmas regras**: cole
   `perfis/<perfil>/perfil.md`, `faq.md` e `categorias.md` no prompt do nó de IA
   (um workflow por conta).
   Automatize só `elogio` e `pergunta_faq`; o resto vai para uma fila (Sheets/Slack)
   para aprovação.
3. **Opcional — MCP.** Se preferir conversar com o Claude ("responde os comentários
   de hoje"), instale um dos MCP servers acima e aponte a skill para ele em vez do
   script. As regras de aprovação continuam valendo.

## Notas sobre a API oficial

- Só contas **Profissionais** (Business ou Criador).
- Permissões: `instagram_business_basic` + `instagram_business_manage_comments`
  (Instagram Login) — ou `instagram_basic` + `instagram_manage_comments` +
  `pages_*` (Facebook Login).
- Há webhook de comentários (campo `comments`), mas exige app com endpoint HTTPS
  público e, para contas de terceiros, App Review. Para uma conta própria,
  polling a cada poucas horas (como o script faz) é suficiente.
- Versões da Graph API expiram; ajuste `IG_API_VERSION` quando a Meta avisar.

## Evitar

Bibliotecas que usam a **API privada** do app (ex.: `instagrapi`, bots de
automação por login/senha, extensões que clicam no navegador). Violam os
Termos de Uso, quebram com frequência e são a causa mais comum de
bloqueio/ban de conta. Tudo neste repo usa só a Graph API oficial.
