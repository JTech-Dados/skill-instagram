---
name: instagram-conteudo
description: Cria conteúdo de Instagram para um dos perfis em perfis/ (tecnologia, maternidade) — pauta/calendário com tendências, carrossel, roteiro de Reels, Stories, legenda com hashtags, otimização de bio/perfil, reaproveitamento de conteúdo entre formatos e revisão "tirar cara de IA". Use quando pedirem post, carrossel, reels, ideias de pauta, calendário editorial, legenda, gancho, bio, melhorar o perfil, reaproveitar/transformar um post, humanizar texto ou "conteúdo pro insta".
---

# Criação de conteúdo para Instagram

Harness para produzir conteúdo consistente com a marca. Toda peça nasce do
perfil do nicho e termina numa pasta em `conteudo/<perfil>/` pronta para revisão.

## 0. Escolher o perfil (sempre primeiro)

Há mais de um perfil em `perfis/` (hoje: `tecnologia` e `maternidade`; ignore `_modelo`).
Se o pedido não deixar claro para qual conta é, **pergunte**. Nunca misture
voz, FAQ ou conteúdo de um perfil no outro. Abaixo, `<perfil>` é a pasta escolhida.

## 0.1 Carregar contexto

1. Leia `perfis/<perfil>/perfil.md`. Se houver campos `<...>` não preenchidos que afetem
   a peça pedida (público, voz, pilares, compliance), **pergunte antes** — no
   máximo 3 perguntas objetivas. Não invente o nicho.
2. Leia `references/formatos.md` (specs de cada formato),
   `references/ganchos.md` (fórmulas de gancho) e `references/humanizer.md`
   (revisão anti-"cara de IA", obrigatória em todo texto entregue).
3. Liste `conteudo/<perfil>/` para não repetir temas recentes.

## 1. Escolher o modo

| Pedido | Modo | Saída |
|---|---|---|
| "ideias", "pauta", "calendário" | **Pauta** | `conteudo/<perfil>/calendario-AAAA-MM.md` |
| "carrossel", "post" | **Carrossel** | pasta da peça com `roteiro.md` + `legenda.md` (+ PNGs opcionais) |
| "reels", "vídeo", "roteiro" | **Reels** | pasta da peça com `roteiro.md` + `legenda.md` |
| "stories", "sequência" | **Stories** | pasta da peça com `roteiro.md` |
| "legenda" para algo pronto | **Legenda** | `legenda.md` |
| "bio", "melhorar o perfil", "destaques" | **Perfil** — siga `references/perfil-otimizacao.md` | `conteudo/<perfil>/perfil-otimizado-AAAA-MM-DD.md` |
| "reaproveitar", "transformar em reels/stories" | **Reaproveitar** — siga `references/reaproveitamento.md` | subpastas na pasta da peça original |
| "humaniza", "tá com cara de IA", texto colado para revisar | **Humanizer** — só `references/humanizer.md` | texto revisado + antes/depois dos trechos ajustados |

Pasta da peça: `conteudo/<perfil>/AAAA-MM-DD-<slug>/` (copie a estrutura de `conteudo/_modelo/`).

## 2. Processo por peça

1. **Briefing (escreva no topo do `roteiro.md`)**
   - Pilar (de `perfil.md`) e objetivo: alcance, salvamento, compartilhamento, comentário ou conversão.
   - Dor/desejo específico do público que a peça ataca.
   - Uma única ideia central em 1 frase. Se não cabe em 1 frase, divida em duas peças.
2. **Ganchos:** gere 5 opções usando fórmulas diferentes de `ganchos.md`, escolha
   a melhor e explique em 1 linha por quê. Mantenha as outras 4 no arquivo como alternativas.
3. **Corpo:** siga a spec do formato em `formatos.md`. Use o vocabulário do público.
4. **CTA:** um só, alinhado ao objetivo (salvar ≠ comentar ≠ link da bio).
   Para gerar comentários, prefira pergunta fechada ou palavra-chave
   ("comenta GUIA que te mando") — isso alimenta a skill `instagram-comentarios`.
5. **Legenda:** ver `formatos.md#legenda`.
6. **Humanizer:** aplique `references/humanizer.md` em slides/roteiro e legenda.
   Anote no `roteiro.md` quantos trechos mudaram e 2–3 exemplos antes → depois.
7. **Checklist final:** rode `references/checklist.md` e marque no `roteiro.md`.
   Se algum item de compliance falhar, corrija antes de entregar.

## 3. Modo Pauta (calendário)

**Antes de montar, pesquise tendências** (passo recomendado, pule se o usuário dispensar):

1. Se a skill `last30days` estiver instalada (ver `docs/ferramentas-comentarios.md`),
   rode-a com 2–3 temas do nicho, escritos como o público pesquisaria
   (ex.: "sono do bebê 4 meses", "IA para quem trabalha com planilha").
   Peça Reddit + YouTube; Instagram/TikTok só se houver `SCRAPECREATORS_API_KEY`.
   **Nunca autorize leitura de cookies do navegador** (`--no-browser-cookies`).
2. Sem a skill, use a busca web disponível com o mesmo recorte dos últimos 30 dias.
3. Salve um resumo em `conteudo/<perfil>/tendencias-AAAA-MM.md`: 5–10 assuntos em
   alta, as perguntas/dores que mais aparecem (palavras do público) e os links.
4. Use esse arquivo para escolher temas e ganchos — cite no briefing de cada peça
   qual tendência ela aproveita. Tendência que fere o compliance do perfil fica de fora.

- Peça ao usuário: período, frequência (posts/semana) e datas importantes.
- Distribua os pilares conforme a % em `perfil.md`.
- Varie formatos (carrossel / reels / stories) e alterne objetivos.
- Para cada item: data, pilar, formato, ideia central, gancho provisório, CTA
  e a tendência de origem (se houver).
- Se o CTA for "comenta X que eu te mando", anote o link/material a entregar —
  vira uma entrada em `perfis/<perfil>/campanhas.json` quando o post sair.
- Inclua 2–3 "séries" recorrentes (ex.: "Mito ou Verdade às quartas") — séries
  facilitam produção e criam hábito no público.

## 4. Visual do carrossel (opcional)

Quando o usuário quiser as imagens:

1. Gere `slides.json` na pasta da peça (formato no comentário do topo de
   `templates/carrossel.html`), copiando cores e fontes de
   `perfil.md > Identidade visual` para o campo `tema`.
2. Rode `python3 scripts/render_carrossel.py conteudo/<perfil>/<pasta>` → gera
   `slide-01.png ...` em 1080×1350.
3. Abra os PNGs (Read) e confira: texto cortado, contraste, slide com texto demais.

Se um MCP de imagem/design estiver conectado (Canva, Figma, Higgsfield...), ofereça
como alternativa — mas o fluxo HTML→PNG funciona sem nenhuma conta externa.

## 5. Publicar / agendar

Esta skill **não publica sozinha**. Se o usuário pedir para agendar e houver um
MCP de agendamento conectado (ex.: Metricool), mostre a peça final e só agende
após OK explícito.

## Regras

- Nunca inventar dados, estatísticas ou depoimentos. Se a peça precisa de um
  número, marque `[FONTE?]` e peça ao usuário.
- Respeitar a seção "Regras e compliance do nicho" acima de qualquer gancho.
- Português do Brasil, a menos que `perfil.md` diga outra coisa.
