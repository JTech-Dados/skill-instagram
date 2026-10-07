---
name: instagram-comentarios
description: Triagem e resposta de comentários do Instagram com a voz da marca e aprovação humana — busca comentários pela Graph API, classifica, rascunha respostas, e só publica o que foi aprovado. Use quando pedirem para responder comentários, ver comentários pendentes, moderar, ocultar spam ou "cuidar do engajamento".
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

## 1. Buscar

```bash
python3 scripts/ig_comments.py --perfil <perfil> fetch --dias 3
```

- Precisa de `IG_ACCESS_TOKEN` em `perfis/<perfil>/.env` (ver `docs/setup-meta.md`). Se faltar,
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
| `resposta` | texto (só se `acao = responder`) |
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
- O script grava `publicado_em` / `erro` em cada linha — reporte falhas.
- Itens `escalar` viram uma lista para o usuário resolver pessoalmente.

## Limites da API (para explicar ao usuário quando perguntar)

- Só funciona com conta **Profissional** (Business ou Criador).
- Responder publicamente e ocultar: sim. Excluir: só comentários nos próprios posts.
- Resposta privada (DM a partir de comentário): possível via Graph API, mas só
  dentro da janela de 7 dias e uma por comentário — não implementado aqui.
- Volume: mantenha bem abaixo do rate limit; o script espera entre envios.
