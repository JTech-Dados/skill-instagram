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
   - `instagram_business_manage_comments`
4. Troque o token curto por um **token de longa duração** (60 dias) e anote a data
   de expiração. Renove antes de vencer:
   `GET https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=<TOKEN>`

Para uso só na sua própria conta não é preciso App Review.

## 3. Variáveis de ambiente

Copie `.env.example` para `.env` (já está no `.gitignore`) e preencha:

```bash
IG_ACCESS_TOKEN=...
IG_USERNAME=suaconta
# IG_API_HOST=graph.facebook.com   # só se usar Facebook Login + Página
# IG_USER_ID=1784...               # obrigatório com Facebook Login
```

Carregue antes de rodar: `set -a; source .env; set +a`.

## 4. Testar

```bash
python3 scripts/ig_comments.py fetch --dias 7
```

Deve gerar `comentarios/pendentes-<data>.json`. Erro `190` = token inválido/expirado;
erro `10`/`200` = permissão faltando.

> **Nunca** commite o token. Se vazar, revogue no painel da Meta e gere outro.
