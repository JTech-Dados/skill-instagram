# Ferramentas para comentários, DMs e pesquisa de pauta

Levantamento revisado em 2026-10-07. "Código verificado" = clonamos o repositório
e lemos o código; o resto é com base na documentação pública.

## Decisão atual

| Necessidade | Usamos | Por quê |
|---|---|---|
| Responder/ocultar comentários com aprovação | `scripts/ig_comments.py` + skill `instagram-comentarios` | ~390 linhas, só stdlib, token só vai para a Meta. Dá para ler tudo |
| **Comentou → recebe o link na DM** | `ig_comments.py campanha` + `perfis/<perfil>/campanhas.json` | Usa o recurso oficial de *private reply*. Nenhuma ferramenta de terceiros necessária |
| Pesquisa de tendências para a pauta | `last30days-skill` (opcional) | Só lê conteúdo público, não toca na conta |
| Humanizer, bio/perfil, reaproveitamento | Modos da skill `instagram-conteudo` | Ideias do instagram-skills, reescritas em PT-BR por perfil |
| Caixa de entrada de DMs em equipe (futuro) | Chatwoot | Maduro, mas **não** trata comentários |

## Custo da API oficial

A API do Instagram (Graph API / Instagram Platform) **não cobra por chamada nem
por mensagem**. Responder comentário, ocultar e mandar DM a partir de comentário
é gratuito. O que existe são limites de uso (rate limit por conta) e regras:
DM a partir de comentário só 1 por comentário, até 7 dias.
Quem cobra são as plataformas por cima (ManyChat, n8n Cloud, Chatwoot Cloud,
ScrapeCreators...). Confirme sempre no painel da Meta — política de preço pode mudar.

## Verificação de código (2026-10-07)

### last30days-skill — [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill)

- **Maturidade:** ~64 mil estrelas, MIT, v3.26.0, commit do dia anterior à revisão, 2.700+ testes.
- **O que faz:** pesquisa um tema em Reddit, YouTube, HN, GitHub, X, TikTok, Reels etc.
  e devolve um resumo com fontes, ordenado por engajamento.
- **Pontos de atenção encontrados no código:**
  - Pode **ler cookies do navegador** (Chrome/Firefox/Safari) para acessar o X com a
    sua sessão. Só com consentimento explícito no setup; dá para negar
    (`--no-browser-cookies`, `FROM_BROWSER=off`). **Nossa regra: sempre negar.**
  - Sugere instalar ferramentas extras (yt-dlp, CLIs via `npm -g`, `curl | bash` do Grok).
    São opcionais — só instale o que entender.
  - Instagram/TikTok dependem do **ScrapeCreators** (serviço pago de coleta de
    terceiros). Opcional.
  - Não achamos telemetria nem `eval`/`shell=True` no código Python.
- **Teste:** o motor rodou (`--quick --no-browser-cookies`, Python 3.13). Aqui as
  fontes deram 403 por causa do proxy do nosso ambiente de nuvem, não do projeto.
- **Veredito: pode usar hoje**, na máquina de vocês, sem cookies, começando com
  Reddit + YouTube (grátis). Instalação: plugin do Claude Code
  (`/plugin marketplace add mvanhorn/last30days-skill` e depois `/plugin install last30days`).

### Chatwoot — [chatwoot/chatwoot](https://github.com/chatwoot/chatwoot)

- **Maturidade:** ~38 mil estrelas, MIT no núcleo (pasta `enterprise/` com licença
  própria — inclui o agente de IA Captain), Ruby on Rails, desenvolvimento ativo.
- **Instagram no código:** o canal assina só os webhooks
  `messages`, `message_reactions` e `messaging_seen`
  (`app/models/channel/instagram.rb`). **Não assina `comments`.**
- **Veredito:** **não resolve "comentou → DM" nem responde comentários.** Serve
  para atender DMs em equipe (uma caixa por conta). Exige servidor (Docker,
  Postgres, Redis) ou plano pago na nuvem. Deixar para quando o volume de DMs justificar.

### instagram-skills — [sergebulaev/instagram-skills](https://github.com/sergebulaev/instagram-skills)

- **Maturidade:** ~300 estrelas, MIT, commit do dia anterior à revisão. Mesmo
  autor do linkedin-skills.
- **O que é:** 9 skills de **criação** (legenda, carrossel, calendário, hashtags,
  extrair gancho, humanizer, otimizar perfil, ler o nicho, reaproveitar).
  **Não responde comentários nem manda DM.**
- **Código:** ~1.600 linhas de Python, fácil de auditar. Só fala com
  `api.publora.com` (agendar/publicar), `api.apify.com` (dados públicos de
  hashtags/perfis) e `api.pixfaro.com` (imagens) — e só se houver chave, todas
  pagas e opcionais. Não usa login/senha do Instagram, sem telemetria. Só roda
  comando externo se o usuário configurar `INSTAGRAM_SKILLS_CUSTOM_POSTER`.
- **Ressalvas:** a aprovação antes de publicar é convenção escrita, não trava
  no código; regras do humanizer pensadas para inglês; não conhece nossos perfis.
- **Veredito:** seguro, mas **não instalado** para não competir com a skill
  `instagram-conteudo`. Trouxemos as ideias, reescritas em português e por perfil:
  `humanizer.md`, `perfil-otimizacao.md` e `reaproveitamento.md`
  (em `.claude/skills/instagram-conteudo/references/`).

### MCPs

- **Oficiais da Meta** (`mcp.facebook.com`): existem para **Ads** e para
  **devtools** (gerenciar app, webhooks, App Review). **Não há MCP oficial para
  Instagram orgânico** (posts, comentários, DMs). O de devtools pode ajudar na
  configuração do app — ver `docs/setup-meta.md`.
- **De terceiros** (luminarylane, AleemHaider, mikusnuz/meta-mcp, CLABS...):
  usam a API oficial, mas são projetos pequenos (alguns com < 10 estrelas) e o
  token dá controle total da conta. **Não usar sem ler o código** e fixar versão.
  Não trazem nada que o nosso script não faça.

### Outras opções

| Ferramenta | Situação |
|---|---|
| [n8n](https://n8n.io/workflows/18455-reply-to-instagram-comments-and-send-dms-with-facebook-graph-api-and-gemini/) + webhook `comments` | Caminho para **tempo real** (DM segundos após o comentário). Exige servidor público HTTPS. Licença *fair-code*. Reaproveita `campanhas.json` e as regras do perfil |
| [InstaAuto / insta-p8](https://github.com/ayuuxh2/insta-p8) | Clone do estilo ManyChat; não revisado |
| Postiz | Só agendamento |
| ManyChat (pago, não open source) | Referência de mercado para "comenta X"; alternativa sem código |

## Evitar

Qualquer ferramenta que use **login e senha** ou automatize o navegador
(InstaPy, `instagrapi`, extensões). Violam os Termos de Uso e são a causa mais
comum de bloqueio de conta. O próprio autor do InstaPy diz ter sido banido pela Meta.

## Tempo real vs. em lote

Hoje a campanha roda **em lote**: vocês pedem "manda o link pra quem comentou
no reel X", aprovam e o script envia. Rodando 2–3x por dia, todo mundo recebe
dentro da janela de 7 dias. Se quiserem DM instantânea, o próximo passo é o
webhook `comments` (n8n ou um endpoint próprio) — ver pendências.
