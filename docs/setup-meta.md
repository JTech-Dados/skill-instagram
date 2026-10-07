# Configurar acesso à API do Instagram

Necessário só para a skill de comentários (`scripts/ig_comments.py`). A skill de
conteúdo funciona sem nada disso.

## 1. Conta

Converta o perfil para **Profissional** (Criador ou Empresa):
Configurações → Tipo de conta e ferramentas → Mudar para conta profissional.

## 2. App na Meta

1. Acesse <https://developers.facebook.com/apps> → **Criar app** → caso de uso
   "Gerenciar mensagens e conteúdo no Instagram".
2. Em **Instagram → Configuração da API com login do Instagram**, adicione sua
   conta como testadora (Funções do app) e aceite o convite no Instagram
   (Configurações → Apps e sites).
3. Gere o token com as permissões:
   - `instagram_business_basic`
   - `instagram_business_manage_comments` (responder/ocultar)
   - `instagram_business_manage_messages` (DM para quem comentou — campanhas)
4. Troque o token curto por um **token de longa duração** (60 dias) e anote a data
   de expiração. Renove antes de vencer:
   `GET https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=<TOKEN>`

Para uso só na sua própria conta não é preciso App Review.

Dica: a Meta tem um MCP oficial de *devtools* (`mcp.facebook.com/devtools`) para
gerenciar apps, webhooks e App Review pelo Claude. Pode ajudar nesta etapa; ele
não acessa posts nem comentários.

Custo: a API do Instagram não cobra por chamada nem por mensagem.

Repita os passos para cada conta (tecnologia e maternidade) — cada uma tem seu token.

## 3. Variáveis de ambiente

Para cada perfil, copie `perfis/_modelo/.env.example` para `perfis/<perfil>/.env`
(já está no `.gitignore`) e preencha:

```bash
IG_ACCESS_TOKEN=...
IG_USERNAME=suaconta
# IG_API_HOST=graph.facebook.com   # só se usar Facebook Login + Página
# IG_USER_ID=1784...               # obrigatório com Facebook Login
```

O script carrega esse arquivo sozinho quando recebe `--perfil <perfil>`.

## 4. Testar

```bash
python3 scripts/ig_comments.py --perfil tecnologia fetch --dias 7
```

Deve gerar `comentarios/tecnologia/pendentes-<data>.json`. Erro `190` = token inválido/expirado;
erro `10`/`200` = permissão faltando.

> **Nunca** commite o token. Se vazar, revogue no painel da Meta e gere outro.
