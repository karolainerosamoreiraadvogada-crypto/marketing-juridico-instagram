# Estratégia de engajamento (dentro da ética da OAB)

Objetivo: gerar reação (salvamentos, compartilhamentos, comentários) e atrair
seguidores **qualificados**, isto é, pessoas com o problema que a Dra. Dirciléia resolve.

## Diagnóstico do perfil (setembro de 2026)

- Cerca de 515 seguidores; de 2 a 5 curtidas por post; nenhum comentário.
- Feed disperso entre muitas áreas, sem pilar dominante.
- Chamadas "Comenta PALAVRA que te explico" não funcionaram e são zona cinzenta ética.
- Frequência irregular.

## Princípios

1. **Pilar dominante:** metade do conteúdo sobre regularização de imóveis.
2. **Gancho nos primeiros 3 segundos:** a capa responde "por que isso é sobre mim?".
3. **Conteúdo salvável:** checklists, passo a passo e comparativos geram salvamento,
   o sinal que mais pesa para o alcance.
4. **Conteúdo compartilhável:** "mande para quem está comprando um imóvel".
5. **Conversa real:** perguntas abertas no fim ("Você já passou por isso?").
6. **Toque local:** em cerca de 1 a cada 3 posts, mencione Cornélio Procópio ou o ABC.

## Formatos (alterne)

| Formato | Exemplo | Reação esperada |
|---|---|---|
| Mito x verdade | "Pagar IPTU dá direito a usucapião?" | comentários |
| Checklist | "5 documentos antes de comprar um imóvel" | salvamentos |
| Passo a passo | "Como funciona a usucapião em cartório" | salvamentos |
| Erro comum | "O erro que trava a venda do imóvel" | compartilhamentos |
| Comparativo | "Escritura x registro x matrícula" | salvamentos |
| Pergunta frequente | "Comprei com contrato de gaveta. O imóvel é meu?" | comentários |
| Situação cotidiana | "Herdou um imóvel e ninguém fez inventário?" | compartilhamentos |

## Fórmulas de título (até 8 palavras)

- "[Situação comum]? Leia antes de [ação]."
- "O que ninguém te conta sobre [tema]."
- "[Tema]: o que é e o que não é."
- "[Número] [coisas] que [público] precisa saber."
- "Você sabe a diferença entre [A] e [B]?"

## Chamadas finais permitidas

- "Salve para consultar depois."
- "Envie para quem está passando por isso."
- "Você já viveu essa situação? Conte nos comentários."
- "Siga @karolainemoreira.adv para mais conteúdos."

## Calendário padrão

- 3 posts por semana (segunda, quarta e sexta), às 21h.
- Proporção: 3 carrosséis para 1 card.
- Semana típica: 2 posts de Imobiliário + 1 das demais áreas, em rodízio.

## Plano de alcance (aprovado em 13/10/2026)

Diagnóstico (28/09 a 12/10/2026): engajamento bom (8,8% do alcance), mas alcance muito baixo
(~40 contas por post, menos de 10% dos 514 seguidores); Reels com alcance menor que carrossel;
0 comentários e 0 salvamentos. Melhor post: carrossel "Usucapião em cartório" (20,8%).

Automático (já no código):
- Localização "Cornélio Procópio" em todo post do feed (`config/perfil.yaml` > alcance).
- Máximo de 5 hashtags na publicação: as 4 mais específicas do tema + #saobernardodocampo.
  Ao escrever, liste primeiro as hashtags mais específicas.
- Story "NOVO POST NO FEED" publicado logo depois de cada carrossel e Reels
  (`python -m conteudo.produzir AAAA-MM avisos`, também no modo "tudo").

Regras de conteúdo a partir de novembro/2026:
- **Reels curtos**: capa + 2 ou 3 telas com até 12 palavras cada + encerramento. Com o teste de leitura (3 palavras/s), 3 telas dão ~30 a 38 s (novembro/2026); para 20 a 25 s, usar 2 telas.
  A frase de impacto da capa é o gancho do primeiro segundo (pergunta ou afirmação surpreendente).
- **Carrosséis "salváveis"**: checklist, passo a passo, comparativo ("X ou Y?"), documentos
  necessários. Pelo menos 1 por semana.
- **Séries** numeradas (ex.: "Regularize seu imóvel · 1 de 5") para criar hábito de retorno.
- **Toque local** em pelo menos 1 post por semana: Cornélio Procópio e ABC (bairros,
  loteamentos, IPTU do município, programas municipais de regularização; sempre com fonte).
- **Pergunta no fim da legenda** que convide a contar experiência ("Você já passou por isso?"),
  nunca oferta de serviço nem "chame no direct para orçamento" (OAB).
- **Teste de horário**: 2 posts por mês às 12h ou às 18h (campo "horario") para comparar com 21h
  no relatório de KPIs.
- **Reels com a Dra. Dirciléia** (rosto e voz): roteiro de 20 a 30 s escrito pelo Claude; ela grava
  no celular. Formato que mais amplia o alcance.

O que depende dela (lembrar nos relatórios): responder comentários e directs na primeira hora;
compartilhar o post nos Stories com enquete; nome e bio otimizados; posts em "Collab" com perfis
locais (corretores, contadores, associações), sem captação; 10 min/dia de interação com perfis do ABC.

