# Reaproveitamento (uma ideia, vários formatos)

Transforma uma peça pronta em outros formatos sem repetir o texto palavra por
palavra. Entrada: uma pasta `conteudo/<perfil>/<peça>/` ou um texto/link colado
(post antigo, roteiro, artigo, live, transcrição).

Saída: subpastas na pasta da peça original, ex.:
`conteudo/<perfil>/2026-10-07-sono-bebe/reels/`, `.../stories/`.

## Regras

1. **Mesma ideia central, ângulo novo.** Cada formato tem um gancho próprio
   (gere 3 opções com `ganchos.md`). Nunca reaproveite a capa como gancho do Reel.
2. **Respeite o formato** (`formatos.md`): o que é lista no carrossel vira
   sequência de cenas no Reel e enquete/caixinha nos Stories.
3. **Espaçamento:** publique a versão nova pelo menos 7–14 dias depois da
   original, ou no mesmo dia em formatos complementares (Reel puxando para o carrossel).
4. **Humanizer** em todas as versões.
5. Só aproveite o que performou bem ou o que o usuário escolher —
   reaproveitar post fraco multiplica post fraco.

## Mapa de conversões

| De → Para | Como fazer |
|---|---|
| Carrossel → Reels | 1 slide-chave vira o gancho falado; 3–5 slides viram cenas de 3–5 s; CTA "o passo a passo completo tá no carrossel fixado" |
| Carrossel → Stories | Slide 1 como pergunta (enquete) · 2–3 slides como telas · caixinha "qual sua dúvida?" · link para o post |
| Reels → Carrossel | Transcreva a fala; cada bloco vira 1 slide; acrescente o detalhe que não coube no vídeo |
| Reels → Legenda longa | A história por trás do vídeo, em primeira pessoa |
| Post → "Comenta X" | Transforme o material extra (checklist, guia) em isca: CTA "comenta X que eu te mando" + entrada em `campanhas.json` |
| Comentários/DMs → Pauta | Perguntas repetidas em `comentarios/<perfil>/` viram FAQ em carrossel ou série de Reels |
| Post de um perfil → outro perfil | **Proibido.** Tecnologia e maternidade não compartilham conteúdo |

## Entrega

Para cada formato gerado: `roteiro.md` + `legenda.md` (modelo em
`conteudo/_modelo/`) e, no `roteiro.md` da peça original, uma seção
"Derivados" listando o que foi criado e a data sugerida de cada um.
