# Datas comemorativas e estações do ano

Pedido da Dra. Dirciléia (02/10/2026): publicações criativas em cada estação do ano e nas
datas comemorativas mais relevantes. O calendário completo, com ocasião, área, formato,
ideia e base legal de partida, está em `conteudo/calendario.py`
(`python -m conteudo.calendario 2027`).

## Regras de publicação
- O post sai **no próprio dia** da data, às 21h. Em segunda, quarta ou sexta, ocupa o post
  do dia; nos outros dias, é um post extra (o GitHub roda o feed todos os dias às 21h).
- Ocasiões de clima descontraído (ex.: Festa Junina) vão para os Stories do sábado, às 14h.
- Ao montar a programação do mês, consultar `calendario.datas(ano, mes)` e reservar essas
  datas antes de distribuir os demais temas.

## Design
- Campo `data_comemorativa` no post: `{"dia": "20", "mes": "Novembro", "nome": "Consciência Negra"}`.
- Carrossel: selo de calendário no canto superior direito (dia em Bodoni itálico terracota,
  mês espaçado) e o nome da ocasião no lugar da área, na capa.
- Reels: dia grande e mês acima da etiqueta da capa; a etiqueta mostra a ocasião.
- Nome da ocasião curto (até ~24 caracteres) para caber na área segura do Reels.

## Conteúdo
- A data é o gancho; o corpo é sempre informativo, com base legal conferida.
- Abrir a legenda com uma frase sobre a data (homenagem sóbria) e conectar ao tema jurídico.
- Ocasiões delicadas (Finados, Consciência Negra, Pessoa com Deficiência): tom respeitoso,
  sem humor, sem atribuir identidade a pessoas das fotos; preferir imagens simbólicas.
- Natal e Ano-Novo: votos breves e elegantes + conteúdo útil.

## Ética da OAB (Provimento 205/2021)
- Proibido: promoções, descontos, "presente" em serviços, sorteios, Black Friday de
  honorários, chamadas como "aproveite" ou "agende já".
- Evitar "garantido/garantida" (o revisor acusa promessa de resultado); usar "reconhecido",
  "previsto em lei", "assegurado pela lei" quando for direito.
- A base legal do calendário é ponto de partida: conferir de novo no mês da publicação.

