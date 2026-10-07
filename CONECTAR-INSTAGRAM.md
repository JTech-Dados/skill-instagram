# Conectar o Instagram — passo a passo

Guia para ligar as contas (tecnologia e maternidade) ao harness, do zero.
Escrito para quem nunca mexeu no painel da Meta.

> **Antes de começar**
> - Só precisa disto para **comentários e DM**. Criar conteúdo já funciona sem conectar nada.
> - A Meta muda nomes de menus com frequência. Se algum botão não estiver
>   exatamente com o nome abaixo, procure o equivalente — a lógica é a mesma.
> - Custo: **zero**. A API do Instagram não cobra.
> - Tempo: ~30–60 min na primeira conta, ~10 min na segunda.

## Visão geral

```
Conta do Instagram          Site da Meta (developers)         Claude
──────────────────          ─────────────────────────         ──────
1. virar Profissional  ──►  2. conta de desenvolvedor
                            3. criar o app (1 só p/ as 2 contas)
4. aceitar convite     ◄──  4. adicionar a conta como testadora
5. liberar mensagens        6. gerar o token  ─────────────►  7. guardar o token
                                                              8. testar
```

Faça os passos 1, 4, 5, 6 e 7 **para cada conta**. Os passos 2 e 3 são feitos uma vez só.

---

## Passo 1 — Transformar a conta em Profissional (no celular)

Faça em cada conta (a sua e a da sua esposa).

1. Abra o Instagram → seu **perfil** → menu **☰** (canto superior direito).
2. **Configurações e atividade** → **Tipo de conta e ferramentas**
   (em algumas versões: **Para profissionais**).
3. **Mudar para conta profissional** → escolha **Criador de conteúdo**
   (recomendado para perfis pessoais) ou **Empresa**.
4. Escolha a categoria (ex.: "Criador digital", "Blogueiro(a)", "Educação").
5. Pode pular a conexão com Página do Facebook — **não é necessária**.

✅ Pronto quando aparecer "Painel profissional" no seu perfil.

---

## Passo 2 — Criar a conta de desenvolvedor da Meta (uma vez)

Feito por quem vai administrar (ex.: você).

1. No computador, acesse **https://developers.facebook.com**.
2. Clique em **Começar** (ou **Get Started**) e entre com sua conta do Facebook.
   - Não tem Facebook? Crie um — a Meta exige para o painel de desenvolvedor.
3. Confirme e-mail/telefone se pedir e aceite os termos.
4. Em "Qual é a sua função?", escolha **Desenvolvedor** (ou qualquer opção — não muda nada).

✅ Pronto quando você vir o painel **Meus apps**.

---

## Passo 3 — Criar o app (uma vez, serve para as duas contas)

1. Em **Meus apps** → **Criar app**.
2. **Nome do app:** `skill-instagram` (ou o que quiser — ninguém de fora vê).
   **E-mail de contato:** o seu.
3. **Caso de uso:** marque **"Gerenciar mensagens e conteúdo no Instagram"**
   (pode aparecer como "Instagram API" ou "Manage messaging & content on Instagram").
4. **Portfólio empresarial:** escolha **"Não quero conectar um portfólio agora"**
   (dá para conectar depois — só será necessário na Fase 2).
5. Revise e clique em **Criar app**. Pode pedir sua senha do Facebook.

✅ Pronto quando abrir o **Painel do app** com o caso de uso do Instagram.

---

## Passo 4 — Adicionar cada conta do Instagram como testadora

### 4a. No site da Meta (você faz)

1. No painel do app, menu lateral → **Funções do app** → **Funções**.
2. **Adicionar pessoas** → escolha **Testador do Instagram**.
3. Digite o **@ da conta** (sem o @) → **Adicionar**.
4. Repita para a outra conta.

### 4b. No Instagram (cada dono da conta faz)

O convite **não aparece no app do celular de forma confiável** — use o navegador:

1. Entre em **https://www.instagram.com** com a conta convidada.
2. **Configurações** → **Apps e sites** → aba **Convites de testador**.
3. **Aceitar** o convite do app `skill-instagram`.

✅ Pronto quando o convite sumir e, no painel da Meta, a conta aparecer sem "pendente".

---

## Passo 5 — Liberar o acesso às mensagens (no celular)

Necessário para a DM automática ("comentou → recebe o link").

1. Instagram → perfil → **☰** → **Configurações e atividade**.
2. **Mensagens e respostas ao story** → **Ferramentas conectadas**
   (em algumas versões: **Controles de mensagens** → **Ferramentas conectadas**).
3. Ative **Permitir acesso a mensagens**.

---

## Passo 6 — Gerar o token (a "senha" da API)

1. No painel do app → **Casos de uso** → no do Instagram clique em **Personalizar**.
2. Abra **Configuração da API com login do Instagram**
   (ou "API setup with Instagram login").
3. Em **Permissões**, confirme que estão adicionadas:
   - `instagram_business_basic`
   - `instagram_business_manage_comments` — ler, responder e ocultar comentários
   - `instagram_business_manage_messages` — mandar a DM para quem comentou
4. Em **Gerar tokens de acesso** → **Adicionar conta** → faça login com a conta
   do Instagram → autorize tudo.
5. Ao lado da conta, clique em **Gerar token** → **copie** o token.
   - Ele é um texto longo começando com `IG...`.
   - **Não cole no chat, e-mail ou WhatsApp.** Vá direto para o passo 7.
6. Anote **a data de hoje + 60 dias** — é quando o token vence (ver "Renovar" abaixo).

Repita os itens 4–6 para a segunda conta.

---

## Passo 7 — Guardar o token onde o Claude encontra

Escolha **uma** das opções.

### Opção A — No seu computador (recomendado para começar)

Com o repositório clonado e o Claude Code aberto na pasta:

1. Copie o modelo para cada perfil:
   ```bash
   cp perfis/_modelo/.env.example perfis/tecnologia/.env
   cp perfis/_modelo/.env.example perfis/maternidade/.env
   ```
2. Abra cada `.env` num editor e preencha:
   ```
   IG_ACCESS_TOKEN=IG...(token da conta)
   IG_USERNAME=usuario_da_conta
   ```
3. Esses arquivos estão no `.gitignore` — **nunca vão para o GitHub**.

### Opção B — No Claude Code na nuvem (claude.ai/code)

1. Na sessão, abra o **menu do ambiente** na barra de título → **Editar**.
2. Em **variáveis de ambiente** (ou **Network secrets / API credentials**, se aparecer), adicione:
   ```
   IG_ACCESS_TOKEN_TECNOLOGIA=IG...
   IG_USERNAME_TECNOLOGIA=usuario_tecnologia
   IG_ACCESS_TOKEN_MATERNIDADE=IG...
   IG_USERNAME_MATERNIDADE=usuario_maternidade
   ```
3. Salve e **abra uma sessão nova** (as variáveis só valem em sessões novas).
4. Quem tem acesso ao ambiente consegue usar o token — use um ambiente só seu.

---

## Passo 8 — Testar

Peça ao Claude:

> "busca os comentários da conta de tecnologia dos últimos 7 dias"

Ou rode direto:

```bash
python3 scripts/ig_comments.py --perfil tecnologia fetch --dias 7
```

✅ Funcionou se aparecer `N comentário(s) pendente(s) em M post(s)`.

Depois, teste a DM:

1. Poste um reel/post de teste com "comenta TESTE".
2. Peça para uma **conta testadora** (ver Fase 1 abaixo) comentar "TESTE".
3. Peça ao Claude: *"manda o link X na DM de quem comentou TESTE no último post do tecnologia"*.
4. Aprove e confira se a DM chegou.

---

## Fase 1 (teste) × Fase 2 (seguidores reais) — leia isto

O app nasce em **modo de desenvolvimento**. Nesse modo, a Meta só deixa o app
interagir com **contas que têm função no app** (as que você adicionou no passo 4).
Na prática:

| | Fase 1 — modo desenvolvimento | Fase 2 — modo publicado |
|---|---|---|
| Buscar e responder comentários | ✅ nas suas contas* | ✅ |
| **DM para quem comentou** | Só para quem tem função no app (adicione 1–2 amigos como **Testador do Instagram** para testar) | ✅ para qualquer seguidor |
| O que precisa | Nada além deste guia | **Verificação da empresa** + **App Review** da permissão `instagram_business_manage_messages` (e possivelmente `..._manage_comments`) + mudar o app para **Publicado/Live** |
| Prazo | Hoje | Dias a algumas semanas (a Meta costuma pedir vídeo mostrando o uso) |

\* Se o `fetch` não trouxer comentários de pessoas sem função no app, é a
mesma restrição — vale para a Fase 2.

**Resumo:** dá para montar e testar tudo hoje com contas testadoras. Para
mandar o link para **todo mundo** que comentar, é preciso passar pelo App
Review. As regras exatas de acesso mudam — confirme no painel
(**Revisão do app → Permissões e recursos**) qual nível cada permissão exige.

### Como pedir o App Review (resumo)

1. **Configurações do app → Básico:** preencha URL da política de privacidade
   (pode ser uma página simples), ícone, categoria.
2. Conecte um **portfólio empresarial** e faça a **verificação da empresa**
   (Configurações do negócio → Central de segurança). Pode pedir CNPJ ou documento.
3. **Revisão do app → Permissões e recursos:** solicite **Acesso avançado** para
   `instagram_business_manage_messages` (e as outras que o painel indicar).
4. Para cada uma, explique o uso ("responder a quem comenta palavra-chave
   enviando o material prometido no post") e grave um vídeo de tela mostrando o fluxo.
5. Depois de aprovado, mude o app para **Publicado (Live)** no topo do painel.

---

## Renovar o token (a cada ~60 dias)

O token vence. Antes de vencer (e pelo menos 24 h depois de gerado), peça ao
Claude para renovar, ou rode no navegador/terminal:

```
https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=SEU_TOKEN
```

A resposta traz um `access_token` novo — troque no `.env` ou nas variáveis do ambiente.
Se vencer, basta gerar outro no passo 6.

## Problemas comuns

| Erro / sintoma | Causa provável | O que fazer |
|---|---|---|
| `IG_ACCESS_TOKEN não definido` | Token não está no `.env` / variáveis | Passo 7. Na nuvem, abra sessão nova |
| `HTTP 400 ... code 190` | Token inválido ou vencido | Gere outro (passo 6) |
| `code 10` ou `code 200` | Falta permissão | Passo 6.3; gere o token de novo depois de adicionar |
| DM falha para alguns usuários | Usuário sem função no app (Fase 1) ou comentário com mais de 7 dias | Fase 2, ou comente de novo |
| DM falha para todos | Passo 5 não feito, ou falta `..._manage_messages` | Passos 5 e 6 |
| Convite de testador não aparece | Procurando no app do celular | Use instagram.com no navegador (passo 4b) |
| "Conta pessoal não suportada" | Conta não é Profissional | Passo 1 |

## Segurança

- Token = acesso total às mensagens e comentários da conta. Trate como senha.
- Nunca cole o token no chat, em issue, em commit ou em print.
- Vazou? Em **instagram.com → Configurações → Apps e sites → Ativos**, remova
  o app `skill-instagram` (isso derruba o token). Depois refaça os passos 4b e 6.
