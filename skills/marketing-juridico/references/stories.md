# Stories descontraídos (todo sábado, às 14h)

Objetivo: aproximar o público, gerar interação e mostrar o lado leve do Direito,
sem perder a sobriedade exigida pela OAB. Uma sequência de **2 a 4 telas** por sábado.

## Formatos (alternar a cada semana)

| Formato | Tela 1 | Telas seguintes |
|---|---|---|
| **Mito ou verdade?** | Afirmação popular ("Quem paga IPTU vira dono do imóvel") | Resposta ("MITO!") + explicação curta e correta |
| **Juridiquês x português** | Termo técnico ("Averbação") | Tradução simples, com exemplo do dia a dia |
| **Você sabia?** | Curiosidade jurídica verdadeira e verificável | Explicação + "salve para lembrar" |
| **Complete a frase** | "Quem não registra..." | "...não é dono." + explicação |
| **Expectativa x realidade** | Expectativa ("Comprei, assinei, é meu!") | Realidade ("Só com o registro na matrícula") |

## Tom permitido (OAB)

- Leve, simpático e bem-humorado, **nunca debochado**.
- Humor sobre **situações e mitos**, nunca sobre pessoas: sem piadas com clientes,
  colegas, juízes, servidores, partes ou instituições.
- Sem memes com rostos de celebridades, marcas ou personagens (direito de imagem e autoral).
- Sem promessas, sem preços, sem "chame no direct", sem urgência.
- A informação jurídica continua **100% correta**: o humor é a embalagem, não o conteúdo.
- Chamadas permitidas: "Sabia disso?", "Salve para lembrar", "Compartilhe com quem precisa",
  "Envie sua dúvida pela caixinha" (a caixinha de perguntas, quando houver, é adicionada
  manualmente e as respostas devem ser genéricas, nunca consultoria de caso concreto).

## Visual

- Formato 1080 x 1920 (9:16). Áreas seguras: nada nos 250 px de cima (barra do perfil)
  nem nos 340 px de baixo (campo de resposta).
- Mesma paleta do perfil; fundo creme ou vinho alternando entre as telas.
- Tipografia grande e expressiva: etiqueta do formato em caixa alta, afirmação em Bodoni,
  resposta com destaque em terracota ("MITO!" / "VERDADE!").
- Indicação "toque para ver a resposta" na primeira tela.

## JSON (formato "stories")

```json
{
  "formato": "stories",
  "data_publicacao": "AAAA-MM-DD (sábado)",
  "area": "Direito Imobiliário",
  "tipo": "mito_verdade | juridiques | voce_sabia | complete | expectativa",
  "quadros": [
    {"etiqueta": "MITO OU VERDADE?", "titulo": "Quem paga o IPTU vira dono do imóvel.", "texto": "", "rodape": "toque para ver a resposta"},
    {"etiqueta": "RESPOSTA", "destaque": "MITO!", "titulo": "Pagar IPTU não transfere a propriedade.", "texto": "..."}
  ],
  "fontes": ["..."]
}
```

