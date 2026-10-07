# Configurar acesso à API do Instagram

O passo a passo completo, clique a clique, está em
**[`CONECTAR-INSTAGRAM.md`](../CONECTAR-INSTAGRAM.md)** na raiz do repositório.

Esta página é só a referência técnica.

## Permissões usadas

| Permissão | Para quê |
|---|---|
| `instagram_business_basic` | ler perfil e posts |
| `instagram_business_manage_comments` | ler, responder e ocultar comentários |
| `instagram_business_manage_messages` | DM para quem comentou (private reply) |

Em modo de desenvolvimento o app só interage com contas que têm função no app.
Para DM a seguidores reais: verificação da empresa + App Review (acesso avançado)
+ app publicado. Detalhes na seção "Fase 1 × Fase 2" do guia.

## Variáveis lidas por `scripts/ig_comments.py`

| Variável | Padrão | Observação |
|---|---|---|
| `IG_ACCESS_TOKEN` | — | obrigatório |
| `IG_USERNAME` | buscado na API | @ da conta, sem @ |
| `IG_USER_ID` | `me` | obrigatório só com Facebook Login |
| `IG_API_HOST` | `graph.instagram.com` | `graph.facebook.com` se usar Facebook Login + Página |
| `IG_API_VERSION` | `v26.0` | |

Onde ficam:
- **Local:** `perfis/<perfil>/.env` (modelo em `perfis/_modelo/.env.example`, fora do git).
- **Nuvem:** variáveis do ambiente com sufixo do perfil, ex. `IG_ACCESS_TOKEN_TECNOLOGIA`.
  O sufixo vence a variável genérica.

## Renovar token

`GET https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=<TOKEN>`
(token com mais de 24 h e ainda válido; dura mais 60 dias).

## Ferramentas

A Meta tem um MCP oficial de *devtools* (`mcp.facebook.com/devtools`) para
gerenciar apps, webhooks e App Review pelo Claude. Não acessa posts nem comentários.

## Erros

`190` = token inválido/vencido · `10`/`200` = permissão faltando ·
DM falhando só para alguns = pessoa sem função no app (modo dev) ou comentário com mais de 7 dias.
