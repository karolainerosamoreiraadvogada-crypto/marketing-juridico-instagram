"""Posts de datas comemorativas e estações: outubro/2026 (Dia das Crianças) a janeiro/2027.

Escritos pelo Claude com a skill marketing-juridico. Fontes conferidas em 02/10/2026 no
planalto.gov.br: Código Civil (arts. 108, 544, 1.245, 1.394, 1.410, 1.789, 1.845, 1.846,
1.857, 1.858, 1.860, 1.862 e 1.864), Lei 8.245/1991 (arts. 48 a 50), LC 142/2013 (arts. 3º
a 5º), EC 103/2019 (art. 22), ADCT (art. 68), Decreto 4.887/2003 (arts. 2º, 3º e 17),
Lei 6.015/1973 (arts. 17, 167, 216-A e 216-B), CPC (art. 610) e Lei 14.759/2023;
STF, ADI 3.239 (julgada em 08/02/2018).

Execute com:  python -m conteudo.datas_comemorativas_2026
Grava os JSON em posts/fila/ (nada vai ao GitHub sem a aprovação da Dra. Dirciléia).
"""
import json

from agente.config import PASTA_FILA

CONFERIDO = "conferido em 02/10/2026"
TAGS_IMOB = ["#regularizacaodeimoveis", "#direitoimobiliario", "#registrodeimoveis"]
TAGS_FIXAS = ["#abcpaulista", "#advocacia", "#saobernardodocampo"]

POSTS = [
    # ------------------------------------------------------------ 12/10 Dia das Crianças
    {
        "id": "2026-10-12_dia-das-criancas-imovel-do-filho",
        "data_publicacao": "2026-10-12", "horario": "10h",  # às 21h sai o Contrato de gaveta (aprovado)
        "formato": "carrossel", "area": "Direito Imobiliário",
        "data_comemorativa": {"dia": "12", "mes": "Outubro", "nome": "Dia das Crianças"},
        "titulo": "Imóvel no nome do *filho*: os pais podem vender?",
        "subtitulo": "A proteção que a lei dá ao patrimônio das crianças.",
        "foto": "assets/fotos/escolhidas/pexels-33014349.jpg",
        "slides": [
            {"titulo": "A criança pode ser dona",
             "texto": "Um imóvel pode estar no nome de uma criança, recebido por herança ou por doação. Toda "
                      "pessoa é capaz de direitos e deveres (Código Civil, art. 1º)."},
            {"titulo": "Os pais administram",
             "texto": "Enquanto o filho é menor, os pais administram os bens dele, no exercício do poder "
                      "familiar (art. 1.689, II)."},
            {"titulo": "Vender exige autorização",
             "texto": "Os pais não podem vender nem hipotecar o imóvel do filho sem prévia autorização do juiz "
                      "(art. 1.691)."},
            {"titulo": "Só no interesse da criança",
             "texto": "A autorização depende de necessidade ou de evidente interesse do filho, demonstrados "
                      "ao juiz no pedido."},
            {"titulo": "Sem autorização, o ato é nulo",
             "texto": "A venda feita sem autorização pode ser declarada nula a pedido do próprio filho, dos "
                      "herdeiros ou do representante legal (art. 1.691, parágrafo único)."},
        ],
        "chamada_final": "Você sabia dessa proteção da lei?",
        "legenda": "Feliz Dia das Crianças! Hoje é dia de celebrar quem enche a casa de alegria.\n\nE, falando "
                   "em casa: muitas crianças são donas de imóveis, recebidos por herança ou por doação. A lei "
                   "protege esse patrimônio.\n\nEnquanto o filho é menor, os pais administram os bens dele. "
                   "Mas não podem vender nem hipotecar o imóvel sem prévia autorização do juiz, que só é dada "
                   "por necessidade ou evidente interesse da criança (Código Civil, art. 1.691).\n\nSe a venda "
                   "for feita sem essa autorização, o próprio filho, os herdeiros ou o representante legal "
                   "podem pedir que o ato seja declarado nulo.\n\nCada situação exige análise dos documentos "
                   "e do motivo do pedido.\n\nSalve este post e compartilhe com quem precisa saber disso.",
        "hashtags": ["#diadascriancas", "#imovel", "#heranca", "#alvarajudicial"] + TAGS_IMOB + TAGS_FIXAS,
        "fontes": [f"Código Civil, arts. 1º, 1.689 e 1.691 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------ 02/11 Finados
    {
        "id": "2026-11-02_finados-testamento",
        "data_publicacao": "2026-11-02", "formato": "carrossel", "area": "Direito Imobiliário",
        "data_comemorativa": {"dia": "02", "mes": "Novembro", "nome": "Dia de Finados"},
        "titulo": "Testamento: um gesto de *cuidado* com quem fica",
        "subtitulo": "Como planejar o destino dos seus bens, inclusive do imóvel.",
        "foto": "assets/fotos/escolhidas/pexels-34192102.jpg",
        "slides": [
            {"titulo": "Quem pode fazer",
             "texto": "Toda pessoa capaz pode fazer testamento a partir dos 16 anos, desde que tenha pleno "
                      "discernimento no momento do ato (Código Civil, arts. 1.857 e 1.860)."},
            {"titulo": "Existe um limite",
             "texto": "Quem tem herdeiros necessários (descendentes, ascendentes ou cônjuge) só pode dispor "
                      "de metade dos bens. A outra metade é a legítima (arts. 1.789, 1.845 e 1.846)."},
            {"titulo": "As formas comuns",
             "texto": "A lei prevê três formas de testamento ordinário: o público, o cerrado e o particular "
                      "(art. 1.862)."},
            {"titulo": "O testamento público",
             "texto": "É escrito pelo tabelião no livro de notas, lido em voz alta ao testador e a duas "
                      "testemunhas e, em seguida, assinado por todos (art. 1.864)."},
            {"titulo": "Pode ser mudado",
             "texto": "O testamento é ato personalíssimo e pode ser mudado a qualquer tempo pelo próprio "
                      "testador (art. 1.858)."},
        ],
        "chamada_final": "Você já pensou em planejar o destino dos seus bens?",
        "legenda": "No Dia de Finados, lembramos com carinho de quem partiu. A data também convida a uma "
                   "reflexão: como deixar tudo organizado para quem fica?\n\nO testamento é um dos "
                   "instrumentos para isso. Toda pessoa capaz, a partir dos 16 anos, pode fazê-lo. Quem tem "
                   "herdeiros necessários (descendentes, ascendentes ou cônjuge) pode dispor livremente de "
                   "metade dos bens; a outra metade, chamada legítima, pertence a esses herdeiros.\n\nO "
                   "testamento público é lavrado pelo tabelião, lido em voz alta na presença de duas "
                   "testemunhas e assinado por todos. E pode ser mudado a qualquer tempo.\n\nCada família tem "
                   "uma realidade, por isso o planejamento merece análise cuidadosa.\n\nSalve este post e "
                   "compartilhe com quem precisa dessa informação.",
        "hashtags": ["#testamento", "#planejamentosucessorio", "#heranca", "#diadefinados"] + TAGS_IMOB[:2]
                    + TAGS_FIXAS,
        "fontes": [f"Código Civil, arts. 1.789, 1.845, 1.846, 1.857, 1.858, 1.860, 1.862 e 1.864 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------ 20/11 Consciência Negra
    {
        "id": "2026-11-20_consciencia-negra-quilombos",
        "data_publicacao": "2026-11-20", "formato": "carrossel", "area": "Direito Imobiliário",
        "data_comemorativa": {"dia": "20", "mes": "Novembro", "nome": "Consciência Negra"},
        "titulo": "Terras quilombolas: propriedade *reconhecida* pela Constituição",
        "subtitulo": "Entenda como funciona a titulação dos territórios.",
        "foto": "assets/fotos/escolhidas/pexels-32201027.jpg",
        "slides": [
            {"titulo": "Um direito constitucional",
             "texto": "A Constituição reconhece a propriedade definitiva das terras aos remanescentes das "
                      "comunidades dos quilombos que as ocupam e determina que o Estado emita os títulos "
                      "(ADCT, art. 68)."},
            {"titulo": "Quem são",
             "texto": "Grupos com trajetória histórica própria e relações territoriais específicas, com "
                      "presunção de ancestralidade negra ligada à resistência à opressão histórica "
                      "(Decreto 4.887/2003, art. 2º)."},
            {"titulo": "A autodefinição",
             "texto": "A identidade quilombola é atestada pela autodefinição da própria comunidade, inscrita "
                      "na Fundação Cultural Palmares, que expede a certidão (art. 2º, § 1º, e art. 3º, § 4º)."},
            {"titulo": "Quem conduz a titulação",
             "texto": "O INCRA identifica, delimita, demarca e titula as terras, sem prejuízo da atuação dos "
                      "estados, do Distrito Federal e dos municípios (art. 3º)."},
            {"titulo": "Um título coletivo",
             "texto": "O título é coletivo, em nome da comunidade representada por sua associação, e não pode "
                      "ser vendido, penhorado nem adquirido por usucapião (art. 17)."},
        ],
        "chamada_final": "Você conhecia esse direito previsto na Constituição?",
        "legenda": "Hoje, 20 de novembro, é o Dia Nacional de Zumbi e da Consciência Negra, feriado nacional "
                   "desde a Lei 14.759/2023.\n\nÉ uma data para lembrar que a terra também é parte da história "
                   "e da identidade de um povo. A Constituição de 1988 reconheceu aos remanescentes das "
                   "comunidades dos quilombos a propriedade definitiva das terras que ocupam e determinou que "
                   "o Estado emita os títulos (ADCT, art. 68).\n\nO Decreto 4.887/2003 regulamenta o "
                   "procedimento: a comunidade se autodefine, obtém a certidão da Fundação Cultural Palmares "
                   "e o INCRA conduz a delimitação, a demarcação e a titulação. O título é coletivo, com "
                   "cláusulas de inalienabilidade, imprescritibilidade e impenhorabilidade. Em 2018, o Supremo "
                   "Tribunal Federal confirmou a validade do decreto (ADI 3.239).\n\nRegularizar a terra é "
                   "garantir o direito de permanecer nela.\n\nSalve e compartilhe este conhecimento.",
        "hashtags": ["#consciencianegra", "#quilombola", "#regularizacaofundiaria", "#direitoaterra"]
                    + TAGS_IMOB[:2] + TAGS_FIXAS,
        "fontes": [f"Lei 14.759/2023, art. 1º ({CONFERIDO})", f"ADCT, art. 68 ({CONFERIDO})",
                   f"Decreto 4.887/2003, arts. 2º, 3º e 17 ({CONFERIDO})",
                   "STF, ADI 3.239, julgada em 08/02/2018 (notícia oficial do STF)"],
    },
    # ------------------------------------------------------------ 03/12 Pessoa com Deficiência
    {
        "id": "2026-12-03_reel-aposentadoria-pcd",
        "data_publicacao": "2026-12-03", "formato": "reel", "area": "Direito Previdenciário",
        "data_comemorativa": {"dia": "03", "mes": "Dezembro", "nome": "Pessoa com Deficiência"},
        "titulo": "Aposentadoria da pessoa com *deficiência*",
        "subtitulo": "Regras próprias e mais favoráveis",
        "video_capa": "assets/videos/pexels-8132006.mp4", "video_final": "assets/videos/pexels-7171085.mp4",
        "trilha": "assets/audio/pixabay-409347-inspiring-cinematic.mp3",
        "slides": [
            {"titulo": "Por tempo de contribuição",
             "texto": "Deficiência grave: 25 anos de contribuição, se homem, e 20, se mulher. Moderada: 29 e 24. "
                      "Leve: 33 e 28 anos.",
             "video": "assets/videos/pexels-8132148.mp4"},
            {"titulo": "Por idade",
             "texto": "Aos 60 anos, se homem, e 55, se mulher, com 15 anos de contribuição e deficiência "
                      "comprovada durante esse período, em qualquer grau.",
             "video": "assets/videos/pexels-8132234.mp4"},
            {"titulo": "A avaliação",
             "texto": "O grau da deficiência é atestado por perícia própria do INSS, com avaliação médica e "
                      "funcional.",
             "video": "assets/videos/pexels-7546130.mp4"},
        ],
        "chamada_final": "Informação certa abre caminho para direitos.",
        "legenda": "Hoje, 3 de dezembro, é o Dia Internacional da Pessoa com Deficiência. Uma data para falar "
                   "de inclusão e de direitos.\n\nA Lei Complementar 142/2013 garante à pessoa com deficiência "
                   "segurada do INSS uma aposentadoria com regras próprias:\n\n1. Por tempo de contribuição: "
                   "com deficiência grave, 25 anos (homem) e 20 anos (mulher); moderada, 29 e 24 anos; leve, "
                   "33 e 28 anos.\n2. Por idade: 60 anos (homem) e 55 anos (mulher), com 15 anos de "
                   "contribuição e deficiência comprovada durante igual período, em qualquer grau.\n3. "
                   "Avaliação: o grau da deficiência é atestado por perícia própria do INSS, médica e "
                   "funcional.\n\nEssas regras continuam valendo depois da Reforma da Previdência (EC "
                   "103/2019, art. 22).\n\nSalve este vídeo e compartilhe com quem pode ter esse direito.",
        "hashtags": ["#pessoacomdeficiencia", "#aposentadoria", "#inss", "#direitoprevidenciario",
                     "#inclusao"] + TAGS_FIXAS,
        "fontes": [f"LC 142/2013, arts. 2º a 5º ({CONFERIDO})", f"EC 103/2019, art. 22 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------ 08/12 Dia da Justiça
    {
        "id": "2026-12-08_dia-da-justica-cartorio",
        "data_publicacao": "2026-12-08", "formato": "carrossel", "area": "Direito Imobiliário",
        "data_comemorativa": {"dia": "08", "mes": "Dezembro", "nome": "Dia da Justiça"},
        "titulo": "Nem tudo precisa de *processo*: resolva no cartório",
        "subtitulo": "Caminhos extrajudiciais para regularizar o seu imóvel.",
        "foto": "assets/fotos/escolhidas/pexels-8112197.jpg",
        "slides": [
            {"titulo": "Usucapião",
             "texto": "Pode ser pedida diretamente no Cartório de Registro de Imóveis da cidade do imóvel, sem "
                      "processo judicial (Lei 6.015/1973, art. 216-A)."},
            {"titulo": "Adjudicação compulsória",
             "texto": "Quem comprou por promessa de compra e venda e não recebeu a escritura definitiva pode "
                      "pedir a transferência no Registro de Imóveis (Lei 6.015/1973, art. 216-B)."},
            {"titulo": "Inventário e partilha",
             "texto": "Se todos os herdeiros forem capazes e estiverem de acordo, o inventário pode ser feito "
                      "por escritura pública, em cartório (CPC, art. 610, § 1º)."},
            {"titulo": "Sempre com advogado",
             "texto": "Nos três caminhos, a lei exige advogado. No inventário, as partes também podem ser "
                      "assistidas por defensor público (CPC, art. 610, § 2º)."},
        ],
        "chamada_final": "Você sabia que esses caminhos existiam?",
        "legenda": "Hoje, 8 de dezembro, é o Dia da Justiça. E justiça também é ter acesso a caminhos mais "
                   "simples para resolver o que é seu.\n\nVárias situações do seu imóvel podem ser resolvidas "
                   "em cartório, sem processo judicial:\n\n1. Usucapião extrajudicial, no Registro de Imóveis "
                   "da cidade do imóvel.\n2. Adjudicação compulsória, para quem comprou por promessa de compra "
                   "e venda e não recebeu a escritura definitiva.\n3. Inventário e partilha por escritura "
                   "pública, quando todos os herdeiros são capazes e estão de acordo.\n\nEm todos esses "
                   "caminhos, a lei exige a participação de advogado. Cada caso precisa de análise dos "
                   "documentos para saber se a via extrajudicial é possível.\n\nSalve este post e envie para "
                   "quem precisa regularizar um imóvel.",
        "hashtags": ["#diadajustica", "#cartorio", "#usucapiaoextrajudicial", "#adjudicacaocompulsoria",
                     "#inventarioextrajudicial"] + TAGS_IMOB[:2] + TAGS_FIXAS,
        "fontes": [f"Lei 6.015/1973, arts. 216-A e 216-B ({CONFERIDO})",
                   f"CPC, art. 610, §§ 1º e 2º ({CONFERIDO})", "Lei 1.408/1951 (Dia da Justiça)"],
    },
    # ------------------------------------------------------------ 21/12 Começa o verão
    {
        "id": "2026-12-21_reel-verao-temporada",
        "data_publicacao": "2026-12-21", "formato": "reel", "area": "Direito Imobiliário",
        "data_comemorativa": {"dia": "21", "mes": "Dezembro", "nome": "Começa o verão"},
        "titulo": "Imóvel na temporada: 3 regras da *lei*",
        "subtitulo": "Para quem aluga no verão",
        "video_capa": "assets/videos/pexels-39576501.mp4", "video_final": "assets/videos/pexels-35879035.mp4",
        "trilha": "assets/audio/pixabay-595943-upbeat-corporate.mp3",
        "slides": [
            {"titulo": "Até 90 dias",
             "texto": "A locação para temporada é contratada por até 90 dias, para lazer, cursos, tratamento "
                      "de saúde ou obras, com ou sem mobília.",
             "video": "assets/videos/pexels-9536490.mp4"},
            {"titulo": "Pagamento antecipado",
             "texto": "O locador pode receber de uma só vez e antecipadamente os aluguéis e encargos, além de "
                      "exigir uma garantia.",
             "video": "assets/videos/pexels-8814707.mp4"},
            {"titulo": "Atenção ao prazo",
             "texto": "Se o inquilino ficar mais de 30 dias após o fim do contrato, sem oposição, a locação "
                      "passa a ser por prazo indeterminado.",
             "video": "assets/videos/pexels-31921650.mp4"},
        ],
        "chamada_final": "Vai alugar neste verão? Salve para conferir.",
        "legenda": "O verão começou hoje, e com ele a procura por imóveis para alugar na temporada. Seja você "
                   "proprietário ou inquilino, vale conhecer as regras da Lei do Inquilinato:\n\n1. Prazo: a "
                   "locação para temporada é contratada por até 90 dias, para lazer, cursos, tratamento de "
                   "saúde, obras no próprio imóvel e situações semelhantes, esteja ou não mobiliado.\n2. "
                   "Pagamento: o locador pode receber de uma só vez e antecipadamente os aluguéis e encargos, "
                   "além de exigir uma das garantias previstas na lei.\n3. Prazo encerrado: se o inquilino "
                   "permanecer no imóvel por mais de 30 dias após o fim do contrato, sem oposição do locador, "
                   "a locação passa a ser por prazo indeterminado, e o pagamento antecipado deixa de ser "
                   "exigível.\n\nContrato por escrito, com prazo e regras claras, evita surpresas.\n\nSalve "
                   "este vídeo e compartilhe com quem vai alugar neste verão.",
        "hashtags": ["#aluguel", "#temporada", "#leidoinquilinato", "#verao", "#direitoimobiliario"]
                    + TAGS_FIXAS,
        "fontes": [f"Lei 8.245/1991, arts. 48, 49 e 50 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------ 25/12 Natal
    {
        "id": "2026-12-25_natal-doacao-imovel",
        "data_publicacao": "2026-12-25", "formato": "carrossel", "area": "Direito Imobiliário",
        "data_comemorativa": {"dia": "25", "mes": "Dezembro", "nome": "Natal"},
        "titulo": "Vai dar um imóvel de *presente*?",
        "subtitulo": "Veja antes o que a lei exige na doação de imóveis.",
        "foto": "assets/fotos/escolhidas/pexels-6087540.jpg",
        "slides": [
            {"titulo": "Doação exige escritura",
             "texto": "Em regra, a doação de imóvel de valor superior a 30 salários mínimos exige escritura "
                      "pública (Código Civil, art. 108)."},
            {"titulo": "E precisa de registro",
             "texto": "A propriedade só passa para o nome de quem recebe com o registro da escritura no "
                      "Registro de Imóveis (art. 1.245)."},
            {"titulo": "Adiantamento de herança",
             "texto": "A doação de pais para filhos, ou de um cônjuge ao outro, importa adiantamento do que "
                      "lhes cabe por herança (art. 544)."},
            {"titulo": "Há imposto",
             "texto": "A doação está sujeita ao ITCMD, imposto estadual. Em São Paulo, ele é regulado pela "
                      "Lei 10.705/2000."},
            {"titulo": "Doar e continuar morando",
             "texto": "É possível doar e reservar o usufruto: quem doa mantém o direito de usar o imóvel ou de "
                      "receber o aluguel enquanto viver (arts. 1.394 e 1.410)."},
        ],
        "chamada_final": "Feliz Natal! Que o seu lar esteja sempre protegido.",
        "legenda": "Feliz Natal! Que esta data seja de paz, união e muito carinho em todos os lares.\n\nE, "
                   "falando em lar: muitas famílias pensam em doar um imóvel aos filhos. Antes de fazer esse "
                   "presente, vale conhecer as regras:\n\n1. Em regra, a doação de imóvel de valor superior a "
                   "30 salários mínimos exige escritura pública.\n2. A propriedade só passa para o nome de quem "
                   "recebe com o registro no Registro de Imóveis.\n3. A doação de pais para filhos importa "
                   "adiantamento de herança.\n4. Incide o ITCMD, imposto estadual; em São Paulo, regulado pela "
                   "Lei 10.705/2000.\n5. É possível reservar o usufruto e continuar usando o imóvel ou "
                   "recebendo o aluguel enquanto viver.\n\nCada família tem uma realidade, e a doação merece "
                   "planejamento.\n\nSalve este post e compartilhe com quem está pensando nisso.",
        "hashtags": ["#doacao", "#usufruto", "#itcmd", "#planejamentosucessorio", "#natal"] + TAGS_IMOB[:2]
                    + TAGS_FIXAS,
        "fontes": [f"Código Civil, arts. 108, 544, 1.245, 1.394 e 1.410, I ({CONFERIDO})",
                   "Lei estadual SP 10.705/2000 (ITCMD)"],
    },
    # ------------------------------------------------------------ 01/01 Ano-Novo
    {
        "id": "2027-01-01_reel-ano-novo-resolucoes",
        "data_publicacao": "2027-01-01", "formato": "reel", "area": "Direito Imobiliário",
        "data_comemorativa": {"dia": "01", "mes": "Janeiro", "nome": "Ano-Novo"},
        "titulo": "3 resoluções para o seu *imóvel* em 2027",
        "subtitulo": "Comece o ano com tudo em ordem",
        "video_capa": "assets/videos/pexels-38457587.mp4", "video_final": "assets/videos/pexels-7646544.mp4",
        "trilha": "assets/audio/pixabay-583436-trailer-energetic.mp3",
        "slides": [
            {"titulo": "Registre a escritura",
             "texto": "Sem o registro no Cartório de Registro de Imóveis, o imóvel continua no nome do "
                      "vendedor (Código Civil, art. 1.245).",
             "video": "assets/videos/pexels-8814706.mp4"},
            {"titulo": "Averbe a construção",
             "texto": "Construiu ou ampliou? A obra precisa ser averbada na matrícula para existir "
                      "oficialmente.",
             "video": "assets/videos/pexels-7817202.mp4"},
            {"titulo": "Confira a matrícula",
             "texto": "A certidão mostra quem é o dono e se há penhora ou hipoteca. Qualquer pessoa pode "
                      "pedi-la no cartório.",
             "video": "assets/videos/pexels-8731516.mp4"},
        ],
        "chamada_final": "Feliz 2027! Qual será a sua primeira resolução?",
        "legenda": "Feliz Ano-Novo! Que 2027 seja um ano de conquistas, e de conquistas bem documentadas.\n\n"
                   "Três resoluções para o seu imóvel:\n\n1. Registre a escritura: sem o registro no Cartório "
                   "de Registro de Imóveis, a propriedade continua no nome do vendedor (Código Civil, art. "
                   "1.245).\n2. Averbe a construção: a obra só existe oficialmente quando é averbada na "
                   "matrícula (Lei 6.015/1973, art. 167, II, 4).\n3. Confira a matrícula: a certidão mostra "
                   "quem é o dono e se há penhora, hipoteca ou outra restrição. Qualquer pessoa pode pedi-la, "
                   "sem precisar explicar o motivo (Lei 6.015/1973, art. 17).\n\nSalve este vídeo e "
                   "compartilhe com quem quer começar o ano com tudo em ordem.",
        "hashtags": ["#anonovo", "#matricula", "#escritura", "#averbacao"] + TAGS_IMOB + TAGS_FIXAS,
        "fontes": [f"Código Civil, art. 1.245 ({CONFERIDO})",
                   f"Lei 6.015/1973, arts. 17 e 167, II, 4 ({CONFERIDO})"],
    },
]


def gravar():
    PASTA_FILA.mkdir(parents=True, exist_ok=True)
    for p in POSTS:
        arq = PASTA_FILA / f"{p['id']}.json"
        if arq.exists():  # preserva o que já foi produzido (imagens, vídeo, testes)
            antigo = json.loads(arq.read_text(encoding="utf-8"))
            p = {**{k: antigo[k] for k in ("imagens", "video", "musica", "testes_video", "alertas_oab")
                    if k in antigo}, **p}
        arq.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(POSTS)


if __name__ == "__main__":
    print(gravar())
