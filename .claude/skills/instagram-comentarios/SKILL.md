---
name: instagram-comentarios
description: Triagem e resposta de comentários do Instagram com a voz da marca e aprovação humana — busca comentários pela Graph API, classifica, rascunha respostas, envia link na DM para quem comentou (campanha "comenta X que eu te mando") e só publica o que foi aprovado. Use quando pedirem para responder comentários, mandar link/DM para quem comentou, rodar campanha de palavra-chave, moderar, ocultar spam ou "cuidar do engajamento".
---

# Resposta de comentários (human-in-the-loop)

Fluxo em 4 etapas. **Nada é publicado sem aprovação explícita do usuário.**

```
buscar  →  classificar + rascunhar  →  revisar/aprovar  →  publicar
(script)        (você, Claude)           (usuário)         (script)
```

## 0. Escolher o perfil (sempre primeiro)

Há mais de um perfil em `perfis/` (hoje: `tecnologia` e `maternidade`; ignore `_modelo`).
Se o pedido não deixar claro para qual conta é, **pergunte**. Nunca misture
voz, FAQ ou conteúdo de um perfil no outro. Abaixo, `<perfil>` é a pasta escolhida.

## 0.1 Contexto

1. Leia `perfis/<perfil>/perfil.md` (voz, tom, emojis, "Nunca dizer", compliance).
2. Leia `perfis/<perfil>/faq.md` (respostas aprovadas e situações que sempre escalam).
3. Leia `references/categorias.md` (como classificar e o que fazer em cada caso).

## Atalho: campanha "comentou → recebe o link na DM"

Use quando o pedido for mandar algo na DM para quem comentou num post/reel.

1. Confira `perfis/<perfil>/campanhas.json`. Se a campanha não existir, pergunte
   ao usuário o link do post, a palavra-chave (ou "qualquer comentário"), o
   texto da DM com o link e 2–3 respostas públicas curtas; grave com `ativa: true`.
   O texto da DM segue a voz do `perfil.md`.
2. Monte o rascunho (só comentários dos últimos 7 dias — limite da Meta):
   ```bash
   python3 scripts/ig_comments.py --perfil <perfil> campanha [--nome <campanha>]
   ```
   Gera `comentarios/<perfil>/campanha-<data-hora>.json` com 1 item por pessoa
   (quem já recebeu DM nessa campanha fica de fora).
3. Mostre o resumo (`@usuário | comentário | resposta pública | DM`) e peça OK.
   Com OK, marque `aprovado: true` e siga para a etapa 4 (Publicar).
4. Comentários fora da palavra-chave no mesmo post continuam no fluxo normal abaixo.

Regras da DM (private reply): 1 mensagem por comentário, até 7 dias depois dele.
Respostas seguintes só se a pessoa responder a DM. Exige a permissão
`instagram_business_manage_messages` no token (ver `CONECTAR-INSTAGRAM.md`).

## 1. Buscar

```bash
python3 scripts/ig_comments.py --perfil <perfil> fetch --dias 3
```

- Precisa de `IG_ACCESS_TOKEN` em `perfis/<perfil>/.env` (ver `CONECTAR-INSTAGRAM.md`). Se faltar,
  avise o usuário e pare — não tente outra forma de acesso.
- Gera `comentarios/<perfil>/pendentes-AAAA-MM-DD.json` só com comentários que ainda não
  têm resposta da própria conta.
- Sem token, mas o usuário colou comentários no chat? Monte o mesmo JSON à mão
  (campos `comment_id` vazio) e siga — a etapa 4 fica manual.

## 2. Classificar e rascunhar

Para cada comentário do arquivo de pendentes, preencha:

| campo | valor |
|---|---|
| `categoria` | uma de `references/categorias.md` |
| `acao` | `responder` · `ocultar` · `ignorar` · `escalar` |
| `resposta` | texto público (opcional se houver `dm`) |
| `dm` | mensagem privada para quem comentou (opcional; ver regras da DM acima) |
| `motivo` | 1 linha justificando a ação |
| `aprovado` | sempre `false` nesta etapa |

Salve como `comentarios/<perfil>/rascunho-AAAA-MM-DD.json` (mesma estrutura dos
pendentes + esses campos).

Regras de escrita da resposta:
- Curta: 1–2 frases, máx. ~200 caracteres. Comentário não é post.
- Comece pelo nome/@ só quando soar natural; varie as aberturas — respostas
  idênticas em série parecem bot.
- Use a legenda do post (`media_caption`) como contexto.
- Fatos (preço, link, prazo, política) **só** do `faq.md` do perfil. Não sabe? `escalar`.
- Responda no idioma do comentário.
- Sempre que fizer sentido, devolva uma pergunta — conversa nos comentários
  aumenta o alcance do post.
- Nunca discutir, ironizar ou expor alguém publicamente.

## 3. Revisar com o usuário

Mostre um resumo em tabela: `@usuário | comentário | ação | resposta proposta`.
Agrupe por ação (escalar primeiro, depois responder, ocultar, ignorar).

O usuário pode: aprovar tudo, aprovar por linha, editar texto, mudar ação.
Atualize o JSON: `aprovado: true` só nas linhas aprovadas.

## 4. Publicar

```bash
python3 scripts/ig_comments.py --perfil <perfil> publicar comentarios/<perfil>/rascunho-AAAA-MM-DD.json              # simulação
python3 scripts/ig_comments.py --perfil <perfil> publicar comentarios/<perfil>/rascunho-AAAA-MM-DD.json --confirmar
```

- Rode primeiro sem `--confirmar` e mostre o que seria enviado.
- Só rode com `--confirmar` depois do OK do usuário **nesta conversa**.
- O script grava `reply_id`, `dm_enviada_em`, `publicado_em` / `erro` em cada linha
  e registra o que foi feito em `comentarios/<perfil>/historico.json` (o `fetch`
  e a `campanha` pulam o que já está lá). Rodar de novo após falha retoma sem
  duplicar a resposta pública nem a DM. Reporte falhas.
- Itens `escalar` viram uma lista para o usuário resolver pessoalmente.

## Limites da API (para explicar ao usuário quando perguntar)

- Só funciona com conta **Profissional** (Business ou Criador).
- Responder publicamente e ocultar: sim. Excluir: só comentários nos próprios posts.
- DM a partir de comentário (private reply): 1 por comentário, até 7 dias.
  Implementado (campo `dm`); exige `instagram_business_manage_messages`.
- Volume: mantenha bem abaixo do rate limit; o script espera entre envios.
