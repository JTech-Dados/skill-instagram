# Pendências

Status do harness de Instagram e o que falta para ele rodar de verdade nas duas
contas. Marque `[x]` ao concluir e anote a data.

Legenda: 👤 = precisa de vocês (não dá para o Claude fazer) · 🤖 = o Claude faz
quando pedirem.

## 1. Repositório

- [x] 🤖 Criar a branch base `main` com README e licença MIT (2026-10-07)
- [x] 🤖 Abrir o PR da branch do harness para `main` (2026-10-07)
- [x] 👤 Revisar e fazer merge do PR — JTech-Dados/skill-instagram#1 (2026-10-07)
- [ ] 👤 Conferir no GitHub se `main` está como branch padrão (Settings → Default branch)
- [ ] 👤 Confirmar a licença: ficou **MIT** (aberta). Se o repo for privado/comercial
      e não quiserem permitir reuso, trocar por "Todos os direitos reservados".

## 2. Definir os nichos (em aberto)

Preencher os campos `<...>`. Enquanto estiverem vazios, as skills perguntam antes
de criar.

### Tecnologia — `perfis/tecnologia/perfil.md`
- [ ] 👤 Recorte do nicho (ex.: dados, carreira em TI, IA no dia a dia, dev iniciante...)
- [ ] 👤 @ da conta e promessa do perfil
- [ ] 👤 Público: quem é, 3 dores, 3 desejos, objeções
- [ ] 👤 Pilares de conteúdo e % de cada
- [ ] 👤 Voz e tom, emojis, "nunca dizer"
- [ ] 👤 Oferta/CTA principal (se houver)
- [ ] 👤 Identidade visual: cores (hex) e fontes
- [ ] 👤 FAQ — `perfis/tecnologia/faq.md`

### Maternidade — `perfis/maternidade/perfil.md`
- [ ] 👤 Recorte do nicho (ex.: primeira viagem, 0–2 anos, mãe que trabalha, amamentação...)
- [ ] 👤 @ da conta e promessa do perfil
- [ ] 👤 Público: quem é, 3 dores, 3 desejos, objeções
- [ ] 👤 Pilares de conteúdo e % de cada
- [ ] 👤 Voz e tom, emojis, "nunca dizer"
- [ ] 👤 Oferta/CTA principal (se houver)
- [ ] 👤 Identidade visual: cores (hex) e fontes
- [ ] 👤 FAQ — `perfis/maternidade/faq.md`
- [ ] 👤 **Regras de compliance**: nicho sensível. Definir limites (ex.: não
      orientar sobre medicação/dosagem, não substituir pediatra, cuidado com
      exposição de imagem de criança) e frases de aviso padrão.

🤖 Atalho: dá para mandar os dados soltos no chat (ou um áudio transcrito) que o
Claude organiza nos arquivos.

## 3. Acesso à API do Instagram (para comentários)

Passo a passo em `docs/setup-meta.md`. Repetir para **cada** conta.

- [ ] 👤 Converter as duas contas para Profissional (Criador ou Empresa)
- [ ] 👤 Criar o app em developers.facebook.com (um app pode servir as duas contas)
- [ ] 👤 Adicionar as contas como testadoras e aceitar o convite no Instagram
- [ ] 👤 Gerar token de longa duração com `instagram_business_basic` +
      `instagram_business_manage_comments` + `instagram_business_manage_messages`
      (esta última é a da DM para quem comentou)
- [ ] 👤 Criar `perfis/tecnologia/.env` e `perfis/maternidade/.env` a partir de
      `perfis/_modelo/.env.example` (nunca commitar)
- [ ] 👤 Anotar a data de expiração dos tokens (60 dias) — ver item 5
- [ ] 🤖 Primeiro teste real: `python3 scripts/ig_comments.py --perfil <perfil> fetch --dias 7`
      (até agora só foi testado com a API simulada)
- [x] 🤖 Atualizar a versão padrão da Graph API para `v26.0` (2026-10-07)
- [ ] 🤖 Primeira campanha real "comentou → DM" num reel de teste, com 1–2 contas
      amigas comentando (só testado com API simulada)

## 4. Primeiras entregas (depois do item 2)

- [ ] 🤖 Calendário do 1º mês de cada conta (`conteudo/<perfil>/calendario-AAAA-MM.md`)
- [ ] 🤖 1 carrossel piloto por conta, com PNGs, para validar voz e visual
- [ ] 👤 Revisar os pilotos e ajustar `perfil.md` com o que não soou como vocês
- [ ] 🤖 1ª rodada de comentários com aprovação manual (depois do item 3)
- [ ] 👤 Alimentar o `faq.md` com as perguntas reais que aparecerem
- [ ] 👤 Para cada post com "comenta X": preencher `perfis/<perfil>/campanhas.json`
      (link do post, palavra-chave, texto da DM com o link)

## 5. Melhorias futuras (avaliar)

- [ ] 🤖 Script para renovar o token antes de vencer (`refresh_access_token`)
- [ ] 🤖 Ajustar `templates/carrossel.html` à identidade de cada conta (ou um
      template por perfil) quando as cores/fontes forem definidas
- [x] 🤖 Envio de DM a partir de comentário ("comenta GUIA") — comando `campanha`
      + campo `dm` (2026-10-07)
- [ ] 👤🤖 DM **instantânea** (segundos após o comentário): webhook `comments` +
      n8n ou endpoint próprio, reaproveitando `campanhas.json`. Hoje é em lote
- [ ] 👤🤖 Agendamento: decidir se usa Metricool (MCP já conectado na sessão) ou outro
- [ ] 👤🤖 Respostas em tempo real com n8n + webhook (ver
      `docs/ferramentas-comentarios.md`) — só depois de calibrar a voz no modo manual
- [ ] 🤖 Relatório simples de desempenho por pilar (o que gera mais salvamento/comentário)
- [x] 🤖 Avaliar last30days e Chatwoot lendo o código (2026-10-07) — ver
      `docs/ferramentas-comentarios.md`
- [ ] 👤 Instalar a skill last30days na máquina de vocês (sem cookies do navegador)
      e testar uma pesquisa por nicho
- [x] 🤖 Passo de tendências antes da pauta na skill `instagram-conteudo` (2026-10-07)
- [ ] 👤🤖 Chatwoot para DMs em equipe — só quando o volume de DMs justificar
      (não trata comentários)
- [ ] 🤖 SessionStart hook para instalar o Playwright automaticamente nas sessões na nuvem
