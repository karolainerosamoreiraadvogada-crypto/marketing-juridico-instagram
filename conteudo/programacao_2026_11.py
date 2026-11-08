"""Programação de novembro/2026 (escrita pelo Claude com a skill marketing-juridico).

Segue o plano de alcance de 13/10/2026: Reels de 20 a 25 s (até 12 palavras por tela),
carrosséis salváveis, série "Regularize seu imóvel" (4 partes), toque local (Billings)
e teste de horário às 18h (16/11 e 27/11). Finados (02/11) e Consciência Negra (20/11)
já estão na fila (conteudo/datas_comemorativas_2026.py).

Fontes conferidas em 26/10/2026 no planalto.gov.br e no al.sp.gov.br:
Lei 6.015/1973 (arts. 17, 19, 176, 186, 188, 216-A e 216-B), Código Civil (arts. 108,
1.238, 1.240, 1.245 e 1.246), Lei 13.465/2017, Lei 8.213/1991 (arts. 18, 26, 29-A, 58 e 86),
Lei 9.250/1995 (art. 23), Lei 11.196/2005 (art. 39), LC 123/2006 e LC 238/2026 (21/10/2026)
e Lei estadual SP 13.579/2009 (Billings).

Execute com:  python -m conteudo.programacao_2026_11
Grava os JSON em posts/fila/ (nada vai ao GitHub sem a aprovação da Dra. Dirciléia).
"""
import json

from agente.config import PASTA_FILA

CONFERIDO = "conferido em 26/10/2026"
SERIE = "Série Regularize seu imóvel · parte {} de 4"
TAGS_FIXAS = ["#saobernardodocampo", "#abcpaulista", "#advocacia"]

POSTS = [
    # ------------------------------------------------------------------ 04/11
    {
        "id": "2026-11-04_serie-1-matricula",
        "data_publicacao": "2026-11-04", "formato": "carrossel", "area": "Direito Imobiliário",
        "titulo": "Por onde começar? Pela *matrícula*.",
        "subtitulo": SERIE.format(1),
        "foto": "assets/fotos/escolhidas/pexels-6862446.jpg",
        "slides": [
            {"titulo": "Cada imóvel tem a sua",
             "texto": "Todo imóvel registrado tem uma matrícula própria no Cartório de Registro de Imóveis "
                      "(Lei 6.015/1973, art. 176, § 1º, I)."},
            {"titulo": "O que ela mostra",
             "texto": "Quem é o dono, a descrição do imóvel e se há penhora, hipoteca ou outra restrição "
                      "registrada."},
            {"titulo": "Qualquer pessoa pode pedir",
             "texto": "A certidão pode ser pedida no cartório sem informar o motivo do pedido (art. 17)."},
            {"titulo": "A certidão completa",
             "texto": "A certidão de inteiro teor reproduz toda a matrícula e basta para comprovar a "
                      "propriedade, os ônus e as restrições do imóvel (art. 19, § 11)."},
            {"titulo": "O primeiro passo",
             "texto": "Com a certidão em mãos, dá para saber o que falta para o imóvel ficar regular no seu "
                      "nome."},
        ],
        "chamada_final": "Você já tem a certidão atualizada do seu imóvel?",
        "legenda": "Começa hoje a série Regularize seu imóvel, em 4 partes. Salve para acompanhar.\n\n"
                   "Parte 1: o primeiro passo é a matrícula. Todo imóvel registrado tem uma matrícula própria "
                   "no Cartório de Registro de Imóveis, com o nome do dono, a descrição do imóvel e as "
                   "restrições registradas, como penhora ou hipoteca.\n\nQualquer pessoa pode pedir a "
                   "certidão, sem precisar explicar o motivo. A certidão de inteiro teor reproduz toda a "
                   "matrícula e basta para comprovar a propriedade, os ônus e as restrições do imóvel.\n\n"
                   "Com ela em mãos, fica claro o que falta para o imóvel ficar regular no seu nome.\n\n"
                   "Na parte 2: os caminhos para regularizar.\n\nVocê já tem a certidão atualizada do seu "
                   "imóvel? Conte nos comentários.",
        "hashtags": ["#matricula", "#regularizacaodeimoveis", "#registrodeimoveis", "#cartorio"] + TAGS_FIXAS,
        "fontes": [f"Lei 6.015/1973, arts. 17, 19, § 11, e 176, § 1º, I ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 06/11
    {
        "id": "2026-11-06_reel-cnis",
        "data_publicacao": "2026-11-06", "formato": "reel", "area": "Direito Previdenciário",
        "titulo": "Vai se aposentar? Confira o *CNIS* antes",
        "subtitulo": "O extrato que o INSS usa",
        "video_capa": "assets/videos/pexels-7546130.mp4", "video_final": "assets/videos/pexels-5798910.mp4",
        "trilha": "assets/audio/pixabay-590331-inspiring-emotional.mp3",
        "slides": [
            {"titulo": "O que é",
             "texto": "O INSS usa o CNIS para calcular o benefício e o tempo de contribuição.",
             "video": "assets/videos/pexels-6964001.mp4"},
            {"titulo": "Faltou um vínculo?",
             "texto": "Com carteira de trabalho e holerites, você pode pedir a correção.",
             "video": "assets/videos/pexels-7550648.mp4"},
            {"titulo": "Trabalho insalubre?",
             "texto": "Peça à empresa o PPP, o perfil profissiográfico previdenciário.",
             "video": "assets/videos/pexels-7247861.mp4"},
        ],
        "chamada_final": "Conferir antes evita surpresas no pedido.",
        "legenda": "Antes de pedir a aposentadoria, confira o seu CNIS, o Cadastro Nacional de Informações "
                   "Sociais.\n\n1. É com as informações do CNIS que o INSS calcula o benefício e comprova o "
                   "tempo de contribuição (Lei 8.213/1991, art. 29-A).\n2. Se faltar algum vínculo ou salário, "
                   "o segurado pode pedir, a qualquer momento, a inclusão ou a correção, com documentos como "
                   "carteira de trabalho, holerites e contratos (art. 29-A, § 2º).\n3. Se você trabalhou "
                   "exposto a agentes nocivos, a empresa deve fornecer o PPP, o perfil profissiográfico "
                   "previdenciário (art. 58, § 4º).\n\nVocê já conferiu o seu CNIS? Conte nos comentários.",
        "hashtags": ["#cnis", "#aposentadoria", "#inss", "#direitoprevidenciario"] + TAGS_FIXAS,
        "fontes": [f"Lei 8.213/1991, arts. 29-A, caput e § 2º, e 58, § 4º ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 09/11
    {
        "id": "2026-11-09_serie-2-caminhos",
        "data_publicacao": "2026-11-09", "formato": "carrossel", "area": "Direito Imobiliário",
        "titulo": "Os *caminhos* para regularizar o seu imóvel",
        "subtitulo": SERIE.format(2),
        "foto": "assets/fotos/escolhidas/pexels-36575138.jpg",
        "slides": [
            {"titulo": "Escritura e registro",
             "texto": "Comprou de quem consta na matrícula? Lavre a escritura e registre no cartório "
                      "(Código Civil, arts. 108 e 1.245)."},
            {"titulo": "Adjudicação compulsória",
             "texto": "Pagou pela promessa de compra e não recebeu a escritura? O pedido pode ser feito no "
                      "Registro de Imóveis (Lei 6.015/1973, art. 216-B)."},
            {"titulo": "Usucapião",
             "texto": "Mora no imóvel há anos, como dono, mesmo sem escritura? Pode caber a usucapião, "
                      "inclusive em cartório (art. 216-A)."},
            {"titulo": "REURB",
             "texto": "O bairro inteiro é um loteamento irregular? A regularização fundiária urbana pode "
                      "titular os moradores (Lei 13.465/2017)."},
        ],
        "chamada_final": "Qual desses caminhos é o mais parecido com o seu caso?",
        "legenda": "Parte 2 da série Regularize seu imóvel: os caminhos.\n\nCada situação tem um caminho "
                   "próprio na lei:\n\n1. Escritura e registro, quando quem vende consta como dono na "
                   "matrícula.\n2. Adjudicação compulsória, quando a promessa de compra foi paga e a "
                   "escritura definitiva não saiu. Pode ser feita no próprio Registro de Imóveis.\n3. "
                   "Usucapião, para quem tem a posse do imóvel há anos, como dono. Também pode ser pedida em "
                   "cartório.\n4. REURB, para núcleos urbanos informais, como loteamentos irregulares.\n\n"
                   "Descobrir qual é o caminho certo depende da análise dos documentos.\n\nNa parte 3: os "
                   "prazos do cartório.\n\nQual desses caminhos é o mais parecido com a sua situação?",
        "hashtags": ["#regularizacaodeimoveis", "#usucapiao", "#adjudicacaocompulsoria", "#reurb"] + TAGS_FIXAS,
        "fontes": [f"Código Civil, arts. 108 e 1.245 ({CONFERIDO})",
                   f"Lei 6.015/1973, arts. 216-A e 216-B ({CONFERIDO})", f"Lei 13.465/2017 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 11/11
    {
        "id": "2026-11-11_reel-usucapiao-prazos",
        "data_publicacao": "2026-11-11", "formato": "reel", "area": "Direito Imobiliário",
        "titulo": "Usucapião: 3 prazos da *lei*",
        "subtitulo": "Do mais longo ao mais curto",
        "video_capa": "assets/videos/pexels-8208901.mp4", "video_final": "assets/videos/pexels-7646544.mp4",
        "trilha": "assets/audio/pixabay-409347-inspiring-cinematic.mp3",
        "slides": [
            {"titulo": "15 anos",
             "texto": "Posse contínua e sem oposição, mesmo sem título nem boa-fé.",
             "video": "assets/videos/pexels-7646797.mp4"},
            {"titulo": "10 anos",
             "texto": "Se você mora no imóvel ou fez nele obras produtivas.",
             "video": "assets/videos/pexels-7986204.mp4"},
            {"titulo": "5 anos",
             "texto": "Área urbana de até 250 m², usada como moradia, sem outro imóvel.",
             "video": "assets/videos/pexels-7647330.mp4"},
        ],
        "chamada_final": "Cada caso exige análise dos requisitos.",
        "legenda": "Muita gente acha que a usucapião sempre exige 15 anos. Não é bem assim.\n\n1. 15 anos: "
                   "posse contínua e sem oposição, mesmo sem título e sem boa-fé (Código Civil, art. 1.238).\n"
                   "2. 10 anos: o mesmo caso, quando o possuidor mora no imóvel ou nele realizou obras ou "
                   "serviços de caráter produtivo (art. 1.238, parágrafo único).\n3. 5 anos: área urbana de "
                   "até 250 m², usada como moradia da pessoa ou da família, por quem não é dono de outro "
                   "imóvel (art. 1.240).\n\nHá outras modalidades, e cada uma tem requisitos próprios.\n\n"
                   "Você conhecia esses prazos? Conte nos comentários.",
        "hashtags": ["#usucapiao", "#regularizacaodeimoveis", "#direitoimobiliario", "#posse"] + TAGS_FIXAS,
        "fontes": [f"Código Civil, arts. 1.238 e 1.240 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 13/11
    {
        "id": "2026-11-13_reel-isencao-ir-venda-imovel",
        "data_publicacao": "2026-11-13", "formato": "reel", "area": "Direito Tributário",
        "titulo": "Vendeu um imóvel? O IR pode ser *isento*",
        "subtitulo": "Duas isenções previstas em lei",
        "video_capa": "assets/videos/pexels-8293116.mp4", "video_final": "assets/videos/pexels-7414173.mp4",
        "trilha": "assets/audio/pixabay-576594-upbeat-corporate.mp3",
        "slides": [
            {"titulo": "Único imóvel",
             "texto": "Vendido por até R$ 440 mil, sem outra venda em 5 anos.",
             "video": "assets/videos/pexels-7247823.mp4"},
            {"titulo": "Comprou outro em 180 dias",
             "texto": "Residencial vendido e valor aplicado em outro residencial: isento.",
             "video": "assets/videos/pexels-7817162.mp4"},
            {"titulo": "Atenção",
             "texto": "A isenção da recompra vale uma vez a cada 5 anos.",
             "video": "assets/videos/pexels-13511897.mp4"},
        ],
        "chamada_final": "Informação antes da venda faz diferença.",
        "legenda": "Quem vende um imóvel com lucro, em regra, paga imposto de renda sobre o ganho de capital. "
                   "Mas a lei prevê isenções:\n\n1. Único imóvel: é isento o ganho na venda do único imóvel "
                   "do vendedor, por até R$ 440 mil, se não houve outra venda nos últimos 5 anos (Lei "
                   "9.250/1995, art. 23).\n2. Recompra em 180 dias: é isento o ganho na venda de imóvel "
                   "residencial quando o valor é aplicado, em até 180 dias do contrato, na compra de outro "
                   "imóvel residencial no Brasil. Se só parte do valor for aplicada, a isenção é proporcional "
                   "(Lei 11.196/2005, art. 39).\n3. Essa isenção da recompra pode ser usada uma vez a cada 5 "
                   "anos (art. 39, § 5º).\n\nVocê sabia dessas isenções? Conte nos comentários.",
        "hashtags": ["#impostoderenda", "#ganhodecapital", "#direitotributario", "#vendadeimovel"] + TAGS_FIXAS,
        "fontes": [f"Lei 9.250/1995, art. 23 ({CONFERIDO})", f"Lei 11.196/2005, art. 39 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 16/11 (teste: 18h)
    {
        "id": "2026-11-16_billings-mananciais",
        "data_publicacao": "2026-11-16", "horario": "18h", "formato": "carrossel", "area": "Direito Imobiliário",
        "titulo": "Imóvel perto da *Billings*? A lei tem regras próprias",
        "subtitulo": "O que muda nas áreas de manancial de São Bernardo do Campo.",
        "foto": "assets/fotos/escolhidas/pexels-9325480.jpg",
        "slides": [
            {"titulo": "Uma lei para a Billings",
             "texto": "A Lei estadual 13.579/2009 definiu a Área de Proteção e Recuperação dos Mananciais da "
                      "Billings, que abrange partes de São Bernardo do Campo (arts. 1º e 9º)."},
            {"titulo": "Alvará do Estado e do município",
             "texto": "Loteamentos, obras e ampliações nessa área dependem de alvará dos órgãos ambientais do "
                      "Estado e do município (art. 59)."},
            {"titulo": "O esgoto é condição",
             "texto": "Para regularizar uma edificação, a lei exige a ligação à rede pública de esgoto, onde "
                      "ela for exigida (art. 75, I)."},
            {"titulo": "Lote mínimo especial",
             "texto": "Só para fins de regularização, a lei admite lote mínimo de 125 m² em algumas subáreas "
                      "(art. 75, parágrafo único)."},
            {"titulo": "Interesse social",
             "texto": "Assentamentos de interesse social sem saneamento podem receber programas de "
                      "recuperação, os PRIS (arts. 32 e 33)."},
        ],
        "chamada_final": "Você sabia que a Billings tem uma lei própria?",
        "legenda": "Boa parte de São Bernardo do Campo fica na bacia da represa Billings. E quem tem imóvel "
                   "nessa região precisa conhecer uma lei específica.\n\nA Lei estadual 13.579/2009 definiu a "
                   "Área de Proteção e Recuperação dos Mananciais da Billings, a APRM-B. Nela:\n\n1. "
                   "Loteamentos, obras e ampliações dependem de alvará dos órgãos ambientais do Estado e do "
                   "município.\n2. A regularização de edificações exige a ligação à rede pública de esgoto, "
                   "onde ela for exigida.\n3. Só para fins de regularização, admite-se lote mínimo de 125 m² "
                   "em algumas subáreas.\n4. Assentamentos de interesse social sem saneamento podem receber "
                   "programas de recuperação, os PRIS.\n\nAntes de comprar ou regularizar, vale verificar se o "
                   "imóvel está na área de manancial.\n\nVocê sabia que a Billings tem uma lei própria? Conte "
                   "nos comentários.",
        "hashtags": ["#billings", "#mananciais", "#regularizacaodeimoveis", "#direitoimobiliario"] + TAGS_FIXAS,
        "fontes": [f"Lei estadual SP 13.579/2009, arts. 1º, 9º, 32, 33, 59 e 75 ({CONFERIDO}, al.sp.gov.br)"],
    },
    # ------------------------------------------------------------------ 18/11
    {
        "id": "2026-11-18_reel-auxilio-acidente",
        "data_publicacao": "2026-11-18", "formato": "reel", "area": "Direito Previdenciário",
        "titulo": "Auxílio-acidente: você *conhece*?",
        "subtitulo": "Indenização paga pelo INSS",
        "video_capa": "assets/videos/pexels-4352133.mp4", "video_final": "assets/videos/pexels-8814513.mp4",
        "trilha": "assets/audio/pixabay-595943-upbeat-corporate.mp3",
        "slides": [
            {"titulo": "Quem tem direito",
             "texto": "Empregados, domésticos, avulsos e segurados especiais.",
             "video": "assets/videos/pexels-7516761.mp4"},
            {"titulo": "Quando",
             "texto": "Sequela de acidente que reduziu a capacidade para o seu trabalho.",
             "video": "assets/videos/pexels-6624500.mp4"},
            {"titulo": "Como é pago",
             "texto": "Sem carência, mesmo trabalhando, até a véspera da aposentadoria.",
             "video": "assets/videos/pexels-7413807.mp4"},
        ],
        "chamada_final": "Informação certa evita perder direitos.",
        "legenda": "O auxílio-acidente é uma indenização paga pelo INSS e ainda é pouco conhecido.\n\n1. Quem "
                   "tem direito: o segurado empregado, o empregado doméstico, o trabalhador avulso e o "
                   "segurado especial (Lei 8.213/1991, art. 18, § 1º).\n2. Quando: depois da consolidação "
                   "das lesões de um acidente de qualquer natureza, se ficarem sequelas que reduzam a "
                   "capacidade para o trabalho que a pessoa exercia (art. 86).\n3. Como é pago: não exige "
                   "carência (art. 26, I), corresponde a 50% do salário de benefício e é devido mesmo que a "
                   "pessoa continue trabalhando, até a véspera da aposentadoria (art. 86, §§ 1º e 2º).\n\n"
                   "Você conhecia esse benefício? Compartilhe com quem precisa saber.",
        "hashtags": ["#auxilioacidente", "#inss", "#direitoprevidenciario", "#acidentedetrabalho"] + TAGS_FIXAS,
        "fontes": [f"Lei 8.213/1991, arts. 18, § 1º, 26, I, e 86 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 23/11
    {
        "id": "2026-11-23_serie-3-prazos-cartorio",
        "data_publicacao": "2026-11-23", "formato": "carrossel", "area": "Direito Imobiliário",
        "titulo": "Quanto tempo o cartório tem para *registrar*?",
        "subtitulo": SERIE.format(3),
        "foto": "assets/fotos/escolhidas/pexels-8406965.jpg",
        "slides": [
            {"titulo": "Prazo geral: 10 dias",
             "texto": "Depois do protocolo, o cartório tem, em regra, 10 dias para registrar ou emitir nota "
                      "devolutiva com as exigências (Lei 6.015/1973, art. 188)."},
            {"titulo": "Casos simples: 5 dias",
             "texto": "Sem exigências, a escritura de compra e venda sem cláusulas especiais e a averbação de "
                      "construção devem ser registradas em 5 dias (art. 188, § 1º, I)."},
            {"titulo": "Exigências cumpridas",
             "texto": "Se o título voltar com as exigências cumpridas, dentro do prazo da prenotação, o prazo "
                      "também é de 5 dias (art. 188, § 1º, III)."},
            {"titulo": "Certidões",
             "texto": "Inteiro teor eletrônica: até 4 horas. Situação jurídica atualizada: até 1 dia. Demais "
                      "certidões: até 5 dias (art. 19, § 10)."},
            {"titulo": "Prazo descumprido",
             "texto": "O descumprimento dos prazos sujeita o cartório às penalidades da lei, conforme as "
                      "regras do CNJ (art. 188, § 2º)."},
        ],
        "chamada_final": "Você sabia que o cartório tem prazos definidos em lei?",
        "legenda": "Parte 3 da série Regularize seu imóvel: os prazos do cartório.\n\nDesde a Lei 14.382/2022, "
                   "a Lei de Registros Públicos fixa prazos claros:\n\n1. Em regra, 10 dias do protocolo para "
                   "registrar ou emitir a nota devolutiva com as exigências.\n2. 5 dias para a escritura de "
                   "compra e venda sem cláusulas especiais e para a averbação de construção, quando não há "
                   "exigências.\n3. 5 dias também para o título que volta com as exigências cumpridas, dentro "
                   "do prazo da prenotação.\n4. Certidões: até 4 horas para o inteiro teor eletrônico (com o "
                   "número da matrícula e no horário de expediente), até 1 dia para a situação jurídica "
                   "atualizada e até 5 dias nos demais casos, contados do pagamento.\n\nNa parte 4, a última: "
                   "por que registrar logo.\n\nVocê sabia desses prazos? Conte nos comentários.",
        "hashtags": ["#cartorio", "#registrodeimoveis", "#regularizacaodeimoveis", "#escritura"] + TAGS_FIXAS,
        "fontes": [f"Lei 6.015/1973, arts. 19, § 10, e 188, com a redação da Lei 14.382/2022 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 25/11
    {
        "id": "2026-11-25_reel-mei-novo-limite",
        "data_publicacao": "2026-11-25", "formato": "reel", "area": "Direito Empresarial",
        "titulo": "MEI: o limite vai *subir*",
        "subtitulo": "Nova lei de outubro de 2026",
        "video_capa": "assets/videos/pexels-7288127.mp4", "video_final": "assets/videos/pexels-6565543.mp4",
        "trilha": "assets/audio/pixabay-583436-trailer-energetic.mp3",
        "slides": [
            {"titulo": "Em 2027",
             "texto": "O limite anual de faturamento do MEI passa para R$ 110 mil.",
             "video": "assets/videos/pexels-5404980.mp4"},
            {"titulo": "A partir de 2028",
             "texto": "O limite sobe para R$ 140 mil por ano.",
             "video": "assets/videos/pexels-7308223.mp4"},
            {"titulo": "Empregados",
             "texto": "O MEI poderá ter até 2 empregados.",
             "video": "assets/videos/pexels-6602213.mp4"},
        ],
        "chamada_final": "Informação certa ajuda a planejar o negócio.",
        "legenda": "Novidade para quem é MEI: a Lei Complementar 238, publicada em 21 de outubro de 2026, "
                   "muda as regras.\n\n1. Em 2027, o limite anual de receita bruta do MEI passa de R$ 81 mil "
                   "para R$ 110 mil (art. 2º).\n2. A partir de 2028, o limite passa a ser de R$ 140 mil por "
                   "ano (arts. 1º e 10, I).\n3. A partir de 2027, o MEI poderá ter até 2 empregados, com "
                   "salário mínimo ou o piso da categoria (art. 1º, que alterou o art. 18-C da Lei do Simples "
                   "Nacional).\n\nEm 2026, continua valendo o limite de R$ 81 mil. A própria lei condiciona a "
                   "ampliação à previsão nas leis orçamentárias de 2027 a 2029 (art. 3º).\n\nVocê é MEI? Conte "
                   "nos comentários o que essa mudança significa para o seu negócio.",
        "hashtags": ["#mei", "#microempreendedor", "#simplesnacional", "#direitoempresarial"] + TAGS_FIXAS,
        "fontes": [f"LC 238/2026, arts. 1º, 2º, 3º e 10 ({CONFERIDO})", f"LC 123/2006, art. 18-A ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 27/11 (teste: 18h)
    {
        "id": "2026-11-27_mei-remissao-dividas",
        "data_publicacao": "2026-11-27", "horario": "18h", "formato": "carrossel", "area": "Direito Tributário",
        "titulo": "MEI com dívida? A nova lei *perdoa* débitos",
        "subtitulo": "Entenda a remissão da Lei Complementar 238/2026.",
        "foto": "assets/fotos/escolhidas/pexels-6205772.jpg",
        "slides": [
            {"titulo": "O que é a remissão",
             "texto": "É o perdão integral das dívidas com a União de quem está enquadrado como MEI "
                      "(LC 238/2026, art. 5º)."},
            {"titulo": "Quais dívidas",
             "texto": "As contribuições mensais do MEI ao INSS, com juros, multas e encargos, inscritas ou não "
                      "em dívida ativa, até 13 de outubro de 2026 (art. 5º, § 1º)."},
            {"titulo": "Quando vale",
             "texto": "Os efeitos começam em 1º de janeiro de 2027, com regulamentação da Procuradoria-Geral "
                      "da Fazenda Nacional (arts. 9º e 10, II)."},
            {"titulo": "As contrapartidas",
             "texto": "Manter em dia as contribuições dos 6 meses seguintes à entrada em vigor da lei e "
                      "desistir de eventuais ações judiciais sobre essas dívidas (arts. 5º, § 4º, e 6º)."},
            {"titulo": "Sem devolução",
             "texto": "Valores já pagos antes da lei não são devolvidos nem compensados (art. 5º, § 3º)."},
        ],
        "chamada_final": "Você conhece algum MEI com dívidas em atraso?",
        "legenda": "A Lei Complementar 238/2026, publicada em 21 de outubro, trouxe uma notícia importante "
                   "para quem é MEI e está com as contribuições em atraso.\n\n1. A lei concede remissão, ou "
                   "seja, perdão integral, das dívidas com a União de quem está enquadrado como MEI.\n2. "
                   "Entram as contribuições mensais do MEI ao INSS, com juros, multas e encargos, inscritas ou "
                   "não em dívida ativa, até 13 de outubro de 2026.\n3. Os efeitos começam em 1º de janeiro de "
                   "2027, e a Procuradoria-Geral da Fazenda Nacional vai regulamentar o procedimento.\n4. "
                   "Contrapartidas: manter em dia as contribuições que vencerem nos 6 meses seguintes à "
                   "entrada em vigor da lei, sob pena de cancelamento, e desistir de ações judiciais sobre "
                   "essas dívidas.\n5. O que já foi pago não é devolvido nem compensado.\n\nCompartilhe com "
                   "quem é MEI.",
        "hashtags": ["#mei", "#remissao", "#direitotributario", "#dividaativa"] + TAGS_FIXAS,
        "fontes": [f"LC 238/2026, arts. 5º, 6º, 9º e 10 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 30/11
    {
        "id": "2026-11-30_serie-4-registre-logo",
        "data_publicacao": "2026-11-30", "formato": "carrossel", "area": "Direito Imobiliário",
        "titulo": "Comprou? Registre *logo*.",
        "subtitulo": SERIE.format(4),
        "foto": "assets/fotos/escolhidas/pexels-29094497.jpg",
        "slides": [
            {"titulo": "Sem registro, não é seu",
             "texto": "Enquanto o título não é registrado, o vendedor continua sendo considerado o dono "
                      "(Código Civil, art. 1.245, § 1º)."},
            {"titulo": "Quem chega primeiro",
             "texto": "O número de ordem no protocolo define a prioridade do título no cartório "
                      "(Lei 6.015/1973, art. 186)."},
            {"titulo": "Vale desde o protocolo",
             "texto": "O registro produz efeitos desde que o título é apresentado e prenotado no protocolo "
                      "(Código Civil, art. 1.246)."},
            {"titulo": "Por que isso importa",
             "texto": "Se o mesmo imóvel for negociado duas vezes, a prioridade é, em regra, de quem levou o "
                      "título ao cartório primeiro."},
            {"titulo": "Fim da série",
             "texto": "Matrícula, caminhos, prazos e registro: com essas etapas, o imóvel fica regular no seu "
                      "nome."},
        ],
        "chamada_final": "Qual parte da série foi mais útil para você?",
        "legenda": "Parte 4, a última da série Regularize seu imóvel: registre logo.\n\nAssinar a escritura não "
                   "basta. Enquanto o título não é registrado, o vendedor continua sendo considerado o dono "
                   "(Código Civil, art. 1.245, § 1º).\n\nNo cartório, vale a ordem de chegada: o número de "
                   "ordem no protocolo define a prioridade do título (Lei 6.015/1973, art. 186), e o registro "
                   "produz efeitos desde a prenotação (Código Civil, art. 1.246). Se o mesmo imóvel for "
                   "negociado duas vezes, a prioridade é, em regra, de quem levou o título ao cartório "
                   "primeiro.\n\nRecapitulando a série: 1. matrícula, 2. caminhos, 3. prazos e 4. registro. "
                   "Salve os quatro posts.\n\nQual parte da série foi mais útil para você?",
        "hashtags": ["#registrodeimoveis", "#escritura", "#regularizacaodeimoveis", "#cartorio"] + TAGS_FIXAS,
        "fontes": [f"Código Civil, arts. 1.245, § 1º, e 1.246 ({CONFERIDO})",
                   f"Lei 6.015/1973, art. 186 ({CONFERIDO})"],
    },
]

STORIES = [
    {"id": "2026-11-07_stories-mito-usucapiao-15-anos", "data_publicacao": "2026-11-07", "tipo": "mito_verdade",
     "area": "Direito Imobiliário",
     "quadros": [
         {"etiqueta": "MITO OU VERDADE?", "titulo": "Usucapião só depois de 15 anos.",
          "rodape": "toque para ver a resposta"},
         {"etiqueta": "RESPOSTA", "destaque": "Mito!", "titulo": "A lei prevê prazos *menores*.",
          "texto": "10 anos para quem mora no imóvel e 5 anos em área urbana de até 250 m² usada como "
                   "moradia, por quem não tem outro imóvel (Código Civil, arts. 1.238 e 1.240)."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "Cada caso tem o seu *prazo*.",
          "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"Código Civil, arts. 1.238, parágrafo único, e 1.240 ({CONFERIDO})"]},
    {"id": "2026-11-14_stories-juridiques-prenotacao", "data_publicacao": "2026-11-14", "tipo": "juridiques",
     "area": "Direito Imobiliário",
     "quadros": [
         {"etiqueta": "JURIDIQUÊS X PORTUGUÊS", "titulo": "*Prenotação*",
          "texto": "Você já ouviu essa palavra no cartório?", "rodape": "toque para traduzir"},
         {"etiqueta": "EM PORTUGUÊS", "titulo": "É o *protocolo* do seu título no cartório.",
          "texto": "Ele marca a ordem de chegada: o número de ordem define a prioridade do título "
                   "(Lei 6.015/1973, art. 186)."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "Comprou? Protocole e *registre*.",
          "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"Lei 6.015/1973, art. 186; Código Civil, art. 1.246 ({CONFERIDO})"]},
    {"id": "2026-11-21_stories-certidao-4-horas", "data_publicacao": "2026-11-21", "tipo": "voce_sabia",
     "area": "Direito Imobiliário",
     "quadros": [
         {"etiqueta": "VOCÊ SABIA?",
          "titulo": "A certidão eletrônica da matrícula pode sair em até *4 horas*.",
          "rodape": "toque para entender"},
         {"etiqueta": "EXPLICANDO", "titulo": "É a certidão de *inteiro teor*.",
          "texto": "Pedida no horário de expediente, com o número da matrícula, contadas as horas do "
                   "pagamento (Lei 6.015/1973, art. 19, § 10, I)."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "Situação jurídica: até *1 dia*.",
          "texto": "Certidão da situação jurídica atualizada. Demais certidões: até 5 dias.", "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"Lei 6.015/1973, art. 19, § 10 ({CONFERIDO})"]},
    {"id": "2026-11-28_stories-mei-empregados", "data_publicacao": "2026-11-28", "tipo": "complete",
     "area": "Direito Empresarial",
     "quadros": [
         {"etiqueta": "COMPLETE A FRASE", "titulo": "A partir de 2027, o MEI poderá ter até…",
          "rodape": "toque para ver a resposta"},
         {"etiqueta": "RESPOSTA", "destaque": "2 empregados!",
          "titulo": "Com salário mínimo ou piso da *categoria*.",
          "texto": "Lei Complementar 238/2026, que alterou o art. 18-C da Lei do Simples Nacional."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "E o limite sobe para *R$ 110 mil* em 2027.",
          "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"LC 238/2026, arts. 1º, 2º e 10, II ({CONFERIDO})"]},
]


def gravar():
    PASTA_FILA.mkdir(parents=True, exist_ok=True)
    for p in POSTS + [dict(s, formato="stories") for s in STORIES]:
        arq = PASTA_FILA / f"{p['id']}.json"
        if arq.exists():  # preserva o que já foi produzido (imagens, vídeo, testes)
            antigo = json.loads(arq.read_text(encoding="utf-8"))
            p = {**{k: antigo[k] for k in ("imagens", "video", "musica", "testes_video", "alertas_oab",
                                           "story_aviso") if k in antigo}, **p}
        arq.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(POSTS), len(STORIES)


if __name__ == "__main__":
    print(gravar())
