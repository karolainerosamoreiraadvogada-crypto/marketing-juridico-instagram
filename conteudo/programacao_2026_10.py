"""Programação de outubro/2026 (escrita pelo Claude com a skill marketing-juridico).

Todas as fontes citadas foram conferidas em 30/09/2026 nos sites oficiais:
planalto.gov.br (Leis 6.015/1973, 8.212/1991, 8.213/1991, 7.713/1988, 8.742/1993,
13.465/2017, 13.105/2015, 10.406/2002 e CTN com a LC 236/2026) e al.sp.gov.br (Lei 10.705/2000).

Execute com:  python -m conteudo.programacao_2026_10
Gera os JSON em posts/fila/ (ainda NÃO aprovados: nada vai ao GitHub sem aprovação).
"""
import json

from agente.config import PASTA_FILA

CONFERIDO = "conferido em 30/09/2026"
TAGS_IMOB = ["#regularizacaodeimoveis", "#direitoimobiliario", "#registrodeimoveis"]
TAGS_FIXAS = ["#abcpaulista", "#advocacia", "#saobernardodocampo"]

POSTS = [
    # ------------------------------------------------------------------ 02/10
    {
        "id": "2026-10-02_usucapiao-em-cartorio",
        "data_publicacao": "2026-10-02", "formato": "carrossel", "area": "Direito Imobiliário",
        "titulo": "Usucapião em cartório: *sem* processo judicial",
        "subtitulo": "Entenda como funciona a via extrajudicial.",
        "foto": "assets/fotos/escolhidas/pexels-7937684.jpg",
        "slides": [
            {"titulo": "O que é usucapião",
             "texto": "É o reconhecimento da propriedade de quem mantém a posse de um imóvel por tempo "
                      "prolongado, sem interrupção nem oposição, conforme os prazos e requisitos da lei."},
            {"titulo": "Pode ser feita no cartório",
             "texto": "A lei permite pedir o reconhecimento diretamente no Cartório de Registro de Imóveis "
                      "da cidade do imóvel, sem processo judicial (Lei 6.015/1973, art. 216-A)."},
            {"titulo": "Sempre com advogado",
             "texto": "O pedido é feito pelo interessado representado por advogado. Essa exigência está na "
                      "própria lei."},
            {"titulo": "Documentos principais",
             "texto": "Ata notarial sobre o tempo de posse, planta e memorial descritivo assinados por "
                      "profissional habilitado, certidões negativas e documentos que comprovem a posse, como "
                      "o pagamento de impostos."},
            {"titulo": "O resultado",
             "texto": "Com tudo em ordem, o oficial do Registro de Imóveis registra a aquisição do imóvel em "
                      "nome de quem fez o pedido."},
        ],
        "chamada_final": "Você sabia que a usucapião podia ser feita em cartório?",
        "legenda": "Muita gente acredita que a usucapião só pode ser reconhecida em um processo judicial "
                   "demorado. Não é bem assim.\n\nA Lei de Registros Públicos permite que o pedido seja feito "
                   "diretamente no Cartório de Registro de Imóveis da cidade onde o imóvel está, sempre com a "
                   "representação de um advogado.\n\nO pedido é instruído com ata notarial sobre o tempo de "
                   "posse, planta e memorial descritivo assinados por profissional habilitado, certidões "
                   "negativas e documentos que demonstrem a posse, como comprovantes de impostos. Estando tudo "
                   "em ordem, o próprio cartório registra o imóvel em nome de quem pediu.\n\nCada caso exige "
                   "análise dos documentos e do tempo de posse, porque os prazos variam conforme a modalidade "
                   "de usucapião.\n\nSalve este post para consultar depois e compartilhe com quem precisa "
                   "regularizar um imóvel.",
        "hashtags": ["#usucapiao", "#usucapiaoextrajudicial"] + TAGS_IMOB + ["#cartorio"] + TAGS_FIXAS,
        "fontes": [f"Lei 6.015/1973, art. 216-A ({CONFERIDO})",
                   f"Código Civil, art. 1.238 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 05/10
    {
        "id": "2026-10-05_reel-pensao-por-morte",
        "data_publicacao": "2026-10-05", "formato": "reel", "area": "Direito Previdenciário",
        "titulo": "Pensão por morte: 3 pontos *essenciais*",
        "subtitulo": "O que a família precisa saber",
        "video_capa": "assets/videos/pexels-7413807.mp4", "video_final": "assets/videos/pexels-6624500.mp4",
        "trilha": "assets/audio/pixabay-590331-inspiring-emotional.mp3",
        "slides": [
            {"titulo": "Existe prazo para pedir",
             "texto": "Pedida em até 90 dias do óbito, a pensão é paga desde a data do falecimento. Para filhos "
                      "menores de 16 anos, o prazo é de 180 dias.",
             "video": "assets/videos/pexels-7550648.mp4"},
            {"titulo": "Quem tem direito",
             "texto": "Primeiro, cônjuge, companheiro e filhos menores de 21 anos ou com invalidez ou deficiência. "
                      "Na falta deles, os pais e, depois, os irmãos, nos termos da lei.",
             "video": "assets/videos/pexels-8208901.mp4"},
            {"titulo": "Não exige carência",
             "texto": "A pensão não depende de um número mínimo de contribuições. Em regra, basta que o falecido "
                      "mantivesse a qualidade de segurado do INSS.",
             "video": "assets/videos/pexels-7247823.mp4"},
        ],
        "chamada_final": "Informação certa no momento difícil faz diferença.",
        "legenda": "A perda de alguém querido já é difícil o bastante. Conhecer os direitos da família ajuda a "
                   "evitar prejuízos em um momento delicado.\n\n1. Prazo: quando a pensão por morte é pedida em "
                   "até 90 dias do óbito, ela é paga desde a data do falecimento. Para filhos menores de 16 anos, "
                   "o prazo é de 180 dias. Depois disso, o pagamento começa na data do pedido.\n2. Dependentes: "
                   "em primeiro lugar estão o cônjuge, o companheiro e os filhos menores de 21 anos ou com "
                   "invalidez ou deficiência. Na falta deles, os pais e, depois, os irmãos, nos termos da lei.\n"
                   "3. Carência: a pensão não exige um número mínimo de contribuições. Em regra, basta que o "
                   "falecido mantivesse a qualidade de segurado.\n\nSalve este vídeo e compartilhe com quem "
                   "pode precisar dessa informação.",
        "hashtags": ["#pensaopormorte", "#inss", "#direitoprevidenciario", "#previdencia", "#familia"]
                    + TAGS_FIXAS,
        "fontes": [f"Lei 8.213/1991, arts. 15, 16, 26, I, e 74, I e II ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 07/10
    {
        "id": "2026-10-07_averbacao-da-obra",
        "data_publicacao": "2026-10-07", "formato": "carrossel", "area": "Direito Imobiliário",
        "titulo": "Construiu ou ampliou? Averbe a *obra*.",
        "subtitulo": "Por que a construção precisa constar da matrícula.",
        "foto": "assets/fotos/escolhidas/pexels-35120035.jpg",
        "slides": [
            {"titulo": "O que é averbar",
             "texto": "É anotar na matrícula do imóvel uma mudança, como uma construção, uma ampliação ou uma "
                      "demolição (Lei 6.015/1973, art. 167, II, 4)."},
            {"titulo": "Por que isso importa",
             "texto": "Sem a averbação, a matrícula mostra só o terreno ou a área antiga. Isso pode dificultar a "
                      "venda, o financiamento e a partilha em uma herança."},
            {"titulo": "Primeiro, a prefeitura",
             "texto": "Em regra, o primeiro passo é regularizar a obra na prefeitura e obter o Habite-se. As "
                      "exigências variam de acordo com cada município."},
            {"titulo": "A certidão do INSS da obra",
             "texto": "A lei exige, em regra, a certidão negativa de débitos previdenciários da obra para "
                      "averbá-la no Registro de Imóveis (Lei 8.212/1991, art. 47, II)."},
            {"titulo": "Depois, o cartório",
             "texto": "Com os documentos em ordem, o pedido de averbação é apresentado ao Cartório de Registro "
                      "de Imóveis onde o imóvel está matriculado."},
        ],
        "chamada_final": "A sua construção já consta da matrícula?",
        "legenda": "Construir, ampliar ou reformar a casa é uma conquista. Mas, para a lei, a obra só passa a "
                   "existir oficialmente quando é averbada na matrícula do imóvel.\n\nSem essa anotação, a "
                   "matrícula continua mostrando apenas o terreno ou a área antiga. Na hora de vender, financiar "
                   "ou fazer a partilha em uma herança, a diferença costuma aparecer.\n\nEm regra, o caminho "
                   "passa pela regularização da obra na prefeitura, com a emissão do Habite-se, e pela certidão "
                   "negativa de débitos previdenciários da obra, exigida pela Lei 8.212/1991 para a averbação. "
                   "Com os documentos em ordem, o pedido é apresentado ao Cartório de Registro de Imóveis.\n\n"
                   "As exigências municipais mudam de cidade para cidade, por isso cada caso merece análise.\n\n"
                   "Salve para consultar depois e envie para quem está construindo.",
        "hashtags": ["#averbacao", "#habitese", "#construcao"] + TAGS_IMOB + TAGS_FIXAS,
        "fontes": [f"Lei 6.015/1973, art. 167, II, 4 ({CONFERIDO})",
                   f"Lei 8.212/1991, art. 47, II ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 09/10
    {
        "id": "2026-10-09_reel-isencao-ir-doenca-grave",
        "data_publicacao": "2026-10-09", "formato": "reel", "area": "Direito Tributário",
        "titulo": "Aposentado com doença grave: *isenção* de IR",
        "subtitulo": "Entenda quem tem direito",
        "video_capa": "assets/videos/pexels-7516760.mp4", "video_final": "assets/videos/pexels-5798910.mp4",
        "trilha": "assets/audio/pixabay-409347-inspiring-cinematic.mp3",
        "slides": [
            {"titulo": "Para quem vale",
             "texto": "Para aposentadoria, reforma e pensão de quem tem uma das doenças graves listadas na lei. "
                      "Não vale para o salário de quem ainda está trabalhando.",
             "video": "assets/videos/pexels-5798598.mp4"},
            {"titulo": "Quais doenças",
             "texto": "Entre outras: neoplasia maligna, cardiopatia grave, doença de Parkinson, esclerose "
                      "múltipla, nefropatia grave e cegueira (Lei 7.713/1988, art. 6º, XIV).",
             "video": "assets/videos/pexels-4352133.mp4"},
            {"titulo": "Como comprovar",
             "texto": "Com base em conclusão da medicina especializada, ou seja, laudo médico. Vale mesmo que a "
                      "doença tenha surgido depois da aposentadoria.",
             "video": "assets/videos/pexels-7247861.mp4"},
        ],
        "chamada_final": "Conhece alguém nessa situação? Compartilhe.",
        "legenda": "Muitos aposentados e pensionistas com doenças graves continuam pagando Imposto de Renda "
                   "sem saber que a lei prevê isenção.\n\nA Lei 7.713/1988 isenta os proventos de aposentadoria, "
                   "reforma e pensão de quem tem uma das doenças da lista legal, como neoplasia maligna, "
                   "cardiopatia grave, doença de Parkinson, esclerose múltipla, nefropatia grave e cegueira, "
                   "entre outras.\n\nA doença deve ser comprovada com base em conclusão da medicina "
                   "especializada, e a isenção vale mesmo que ela tenha surgido depois da aposentadoria.\n\n"
                   "Atenção: a regra alcança os proventos de aposentadoria, reforma e pensão. O salário de quem "
                   "ainda está trabalhando não entra.\n\nSalve este vídeo e compartilhe com quem pode ter "
                   "direito.",
        "hashtags": ["#impostoderenda", "#isencaodeir", "#aposentados", "#direitotributario", "#doencagrave"]
                    + TAGS_FIXAS,
        "fontes": [f"Lei 7.713/1988, art. 6º, XIV e XXI ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 12/10
    {
        "id": "2026-10-12_contrato-de-gaveta",
        "data_publicacao": "2026-10-12", "formato": "carrossel", "area": "Direito Imobiliário",
        "titulo": "Contrato de gaveta: *riscos* e caminhos",
        "subtitulo": "O que fazer quando a compra nunca foi registrada.",
        "foto": "assets/fotos/escolhidas/pexels-7875831.jpg",
        "slides": [
            {"titulo": "O que é",
             "texto": "É a compra feita apenas por contrato particular, sem escritura registrada no Cartório de "
                      "Registro de Imóveis."},
            {"titulo": "O principal risco",
             "texto": "Enquanto o título não é registrado, a lei continua considerando o vendedor como dono do "
                      "imóvel (Código Civil, art. 1.245, § 1º)."},
            {"titulo": "Outros problemas",
             "texto": "Dívidas do vendedor podem levar à penhora do imóvel, e o falecimento dele pode exigir "
                      "inventário antes da regularização. Vender ou financiar também fica mais difícil."},
            {"titulo": "Caminho 1: adjudicação",
             "texto": "Quem quitou a compra e não recebeu a escritura pode pedir a adjudicação compulsória, "
                      "inclusive diretamente no Registro de Imóveis (Lei 6.015/1973, art. 216-B)."},
            {"titulo": "Caminho 2: usucapião",
             "texto": "Em alguns casos, a posse prolongada permite a usucapião, que também pode ser feita em "
                      "cartório. Cada situação exige análise dos documentos."},
        ],
        "chamada_final": "Você conhece alguém com contrato de gaveta?",
        "legenda": "O chamado contrato de gaveta ainda é muito comum: a pessoa paga pelo imóvel, assina um "
                   "contrato particular e nunca registra a compra.\n\nO risco é grande. Pelo Código Civil, "
                   "enquanto o título não é registrado, o vendedor continua sendo considerado o dono. Dívidas "
                   "dele podem levar à penhora do imóvel, e o falecimento do vendedor pode exigir inventário "
                   "antes de qualquer regularização.\n\nA boa notícia é que existem caminhos. Quem quitou a "
                   "compra e não recebeu a escritura pode pedir a adjudicação compulsória, inclusive em cartório. "
                   "Em algumas situações, a posse prolongada permite a usucapião.\n\nA escolha do caminho "
                   "depende dos documentos e da história de cada imóvel.\n\nSalve este post e compartilhe com "
                   "quem comprou um imóvel assim.",
        "hashtags": ["#contratodegaveta", "#adjudicacaocompulsoria", "#usucapiao"] + TAGS_IMOB + TAGS_FIXAS,
        "fontes": [f"Código Civil, art. 1.245, § 1º ({CONFERIDO})",
                   f"Lei 6.015/1973, arts. 216-A e 216-B ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 14/10
    {
        "id": "2026-10-14_reel-socio-falecido",
        "data_publicacao": "2026-10-14", "formato": "reel", "area": "Direito Empresarial",
        "titulo": "Sócio faleceu: o que acontece com a *empresa*?",
        "subtitulo": "O contrato social faz toda a diferença",
        "video_capa": "assets/videos/pexels-8348913.mp4", "video_final": "assets/videos/pexels-7981954.mp4",
        "trilha": "assets/audio/pixabay-595943-upbeat-corporate.mp3",
        "slides": [
            {"titulo": "A regra do Código Civil",
             "texto": "Se o contrato nada disser, a quota do sócio falecido é, em regra, liquidada: o valor é "
                      "apurado e pago aos herdeiros (Código Civil, art. 1.028).",
             "video": "assets/videos/pexels-8731516.mp4"},
            {"titulo": "As exceções",
             "texto": "A regra muda se o contrato social dispuser de outra forma, se os sócios optarem pela "
                      "dissolução ou se houver acordo com os herdeiros.",
             "video": "assets/videos/pexels-8814513.mp4"},
            {"titulo": "Planejar evita conflitos",
             "texto": "Prever no contrato social o que acontece em caso de falecimento traz segurança para a "
                      "empresa, para os sócios e para a família.",
             "video": "assets/videos/pexels-7735908.mp4"},
        ],
        "chamada_final": "O contrato social da sua empresa prevê essa situação?",
        "legenda": "Poucos sócios pensam nisso ao abrir uma empresa: o que acontece se um deles falecer?\n\n"
                   "Pelo Código Civil, se o contrato social nada disser, a quota do sócio falecido é, em regra, "
                   "liquidada. Ou seja, o valor correspondente é apurado e pago aos herdeiros, o que pode afetar "
                   "o caixa e a continuidade do negócio.\n\nA lei prevê exceções: o contrato pode dispor de "
                   "outra forma, os sócios podem optar pela dissolução ou pode haver acordo com os herdeiros "
                   "para substituir o sócio falecido.\n\nPor isso, um contrato social bem planejado traz "
                   "segurança para a empresa, para os sócios e para as famílias.\n\nSalve este vídeo e "
                   "compartilhe com seu sócio.",
        "hashtags": ["#direitoempresarial", "#contratosocial", "#sociedade", "#empresario",
                     "#planejamentosucessorio"] + TAGS_FIXAS,
        "fontes": [f"Código Civil, art. 1.028 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 16/10
    {
        "id": "2026-10-16_periodo-de-graca-inss",
        "data_publicacao": "2026-10-16", "formato": "carrossel", "area": "Direito Previdenciário",
        "titulo": "Parou de contribuir? Você ainda pode estar *protegido*",
        "subtitulo": "Entenda o período de graça do INSS.",
        "foto": "assets/fotos/escolhidas/pexels-8441787.jpg",
        "slides": [
            {"titulo": "Qualidade de segurado",
             "texto": "É o vínculo com o INSS que garante o acesso aos benefícios. Ele não termina no mesmo dia "
                      "em que as contribuições param."},
            {"titulo": "Regra geral: 12 meses",
             "texto": "Quem deixa de exercer atividade remunerada mantém a qualidade de segurado por até 12 "
                      "meses após parar de contribuir. Para o segurado facultativo, o prazo é de 6 meses."},
            {"titulo": "Pode chegar a 24 meses",
             "texto": "O prazo é prorrogado para até 24 meses para quem já pagou mais de 120 contribuições "
                      "mensais sem perder a qualidade de segurado."},
            {"titulo": "Desempregado: mais 12 meses",
             "texto": "Quem comprova o desemprego no órgão próprio do Ministério do Trabalho ganha mais 12 "
                      "meses nesses prazos."},
            {"titulo": "Por que isso importa",
             "texto": "Durante esse período, o segurado conserva todos os seus direitos perante a Previdência "
                      "Social (Lei 8.213/1991, art. 15, § 3º)."},
        ],
        "chamada_final": "Você conhecia o período de graça?",
        "legenda": "Muita gente acredita que, ao parar de contribuir, perde na hora o direito aos benefícios "
                   "do INSS. Não é bem assim.\n\nA Lei 8.213/1991 garante o chamado período de graça. Quem deixa "
                   "de exercer atividade remunerada mantém a qualidade de segurado por até 12 meses. O prazo "
                   "pode chegar a 24 meses para quem já pagou mais de 120 contribuições sem perder essa "
                   "qualidade, e ganha mais 12 meses para quem comprova o desemprego no órgão do Ministério do "
                   "Trabalho. Para o segurado facultativo, o prazo é de 6 meses.\n\nDurante esse período, o "
                   "segurado conserva todos os seus direitos perante a Previdência Social.\n\nCada histórico "
                   "de contribuições tem particularidades, por isso vale conferir o seu CNIS.\n\nSalve para "
                   "consultar depois e compartilhe com quem parou de contribuir.",
        "hashtags": ["#inss", "#qualidadedesegurado", "#periododegraca", "#direitoprevidenciario",
                     "#previdencia"] + TAGS_FIXAS,
        "fontes": [f"Lei 8.213/1991, art. 15, II e VI, §§ 1º a 3º ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 19/10
    {
        "id": "2026-10-19_reel-inventario-imovel-herdado",
        "data_publicacao": "2026-10-19", "formato": "reel", "area": "Direito Imobiliário",
        "titulo": "Herdou um imóvel? Faça o *inventário* a tempo",
        "subtitulo": "Prazo, cartório e multa",
        "video_capa": "assets/videos/pexels-7546136.mp4", "video_final": "assets/videos/pexels-7492157.mp4",
        "trilha": "assets/audio/pixabay-590331-inspiring-emotional.mp3",
        "slides": [
            {"titulo": "Existe prazo",
             "texto": "O inventário deve ser aberto em até 2 meses do falecimento (Código de Processo Civil, "
                      "art. 611).",
             "video": "assets/videos/pexels-13511897.mp4"},
            {"titulo": "Pode ser em cartório",
             "texto": "Se todos os herdeiros forem maiores, capazes e estiverem de acordo, o inventário pode ser "
                      "feito por escritura pública, com advogado (CPC, art. 610).",
             "video": "assets/videos/pexels-8731252.mp4"},
            {"titulo": "O atraso pode gerar multa",
             "texto": "Em São Paulo, se o inventário não for aberto em 60 dias, o ITCMD tem multa de 10%. Acima "
                      "de 180 dias, a multa sobe para 20%.",
             "video": "assets/videos/pexels-6964001.mp4"},
        ],
        "chamada_final": "Regularizar a herança protege toda a família.",
        "legenda": "Herdar um imóvel e deixar tudo como está parece simples, mas costuma gerar problemas para "
                   "a família no futuro.\n\nO Código de Processo Civil determina que o inventário seja aberto em "
                   "até 2 meses do falecimento. Quando todos os herdeiros são maiores, capazes e estão de "
                   "acordo, ele pode ser feito em cartório, por escritura pública, com a assistência de "
                   "advogado.\n\nEm São Paulo, o atraso tem custo: se o inventário não for aberto em 60 dias, o "
                   "ITCMD é calculado com multa de 10%. Acima de 180 dias, a multa passa a 20% (Lei estadual "
                   "10.705/2000, art. 21).\n\nAlém disso, sem inventário e partilha registrada, o imóvel não pode "
                   "ser vendido ou financiado de forma regular.\n\nSalve este vídeo e compartilhe com a sua "
                   "família.",
        "hashtags": ["#inventario", "#heranca", "#itcmd", "#partilha"] + TAGS_IMOB[:2] + TAGS_FIXAS,
        "fontes": [f"Código de Processo Civil, arts. 610 e 611 ({CONFERIDO})",
                   f"Lei estadual SP 10.705/2000, art. 21, I ({CONFERIDO} em al.sp.gov.br)"],
    },
    # ------------------------------------------------------------------ 21/10
    {
        "id": "2026-10-21_prescricao-e-decadencia-tributaria",
        "data_publicacao": "2026-10-21", "formato": "carrossel", "area": "Direito Tributário",
        "titulo": "Dívida de imposto antiga ainda pode ser *cobrada*?",
        "subtitulo": "Entenda decadência e prescrição tributária.",
        "foto": "assets/fotos/escolhidas/pexels-6927345.jpg",
        "slides": [
            {"titulo": "Dois prazos diferentes",
             "texto": "Decadência é o prazo para o Fisco constituir o crédito, isto é, lançar o tributo. "
                      "Prescrição é o prazo para cobrá-lo depois de constituído."},
            {"titulo": "Decadência: 5 anos",
             "texto": "Em regra, o Fisco tem 5 anos para lançar, contados do primeiro dia do ano seguinte ao que "
                      "poderia ter lançado (CTN, art. 173, I). Há regra própria para tributos pagos "
                      "antecipadamente."},
            {"titulo": "Prescrição: 5 anos",
             "texto": "Depois de constituído o crédito, o Fisco tem 5 anos para cobrá-lo (CTN, art. 174)."},
            {"titulo": "O prazo pode recomeçar",
             "texto": "O despacho que ordena a citação na execução fiscal e o reconhecimento da dívida pelo "
                      "devedor, entre outros atos, interrompem a prescrição, que volta a correr do início."},
            {"titulo": "Novidade de 2026",
             "texto": "A Lei Complementar 236/2026 incluiu o protesto extrajudicial da certidão de dívida ativa "
                      "entre os atos que interrompem a prescrição (CTN, art. 174, § 1º, II)."},
        ],
        "chamada_final": "Ficou alguma dúvida sobre esses prazos? Comente.",
        "legenda": "Será que aquela dívida de imposto antiga ainda pode ser cobrada? A resposta depende de dois "
                   "prazos do Código Tributário Nacional.\n\nA decadência é o prazo para o Fisco lançar o "
                   "tributo. Em regra, são 5 anos contados do primeiro dia do ano seguinte àquele em que o "
                   "lançamento poderia ter sido feito. Já a prescrição é o prazo para cobrar o crédito depois "
                   "de constituído: também 5 anos.\n\nAtenção: alguns atos interrompem a prescrição, que então "
                   "recomeça do zero. A Lei Complementar 236/2026 ampliou essa lista e incluiu, por exemplo, o "
                   "protesto extrajudicial da certidão de dívida ativa.\n\nComo cada tributo e cada cobrança "
                   "têm datas próprias, a análise precisa ser feita caso a caso.\n\nSalve este post para "
                   "consultar depois.",
        "hashtags": ["#direitotributario", "#prescricao", "#decadencia", "#execucaofiscal", "#contribuinte"]
                    + TAGS_FIXAS,
        "fontes": [f"CTN, arts. 150, § 4º, 173 e 174, com a redação da LC 236/2026 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 23/10
    {
        "id": "2026-10-23_reel-adjudicacao-compulsoria",
        "data_publicacao": "2026-10-23", "formato": "reel", "area": "Direito Imobiliário",
        "titulo": "Pagou tudo e não recebeu a *escritura*?",
        "subtitulo": "Conheça a adjudicação compulsória em cartório",
        "video_capa": "assets/videos/pexels-7817162.mp4", "video_final": "assets/videos/pexels-7817246.mp4",
        "trilha": "assets/audio/pixabay-576594-upbeat-corporate.mp3",
        "slides": [
            {"titulo": "O problema",
             "texto": "Você quitou o imóvel prometido à venda, mas o vendedor não assina a escritura definitiva. "
                      "A lei tem uma solução para isso.",
             "video": "assets/videos/pexels-7646289.mp4"},
            {"titulo": "Agora também em cartório",
             "texto": "A adjudicação compulsória pode ser feita diretamente no Registro de Imóveis, com advogado, "
                      "sem processo judicial (Lei 6.015/1973, art. 216-B).",
             "video": "assets/videos/pexels-8061108.mp4"},
            {"titulo": "O que é preciso",
             "texto": "Contrato de promessa, prova do pagamento, ata notarial, certidões, comprovante do ITBI e "
                      "notificação do vendedor, que tem 15 dias para cumprir a obrigação.",
             "video": "assets/videos/pexels-8814706.mp4"},
        ],
        "chamada_final": "Compartilhe com quem está nessa situação.",
        "legenda": "Você pagou todas as parcelas do imóvel, mas o vendedor nunca assinou a escritura definitiva? "
                   "Essa situação é mais comum do que parece.\n\nA solução se chama adjudicação compulsória. Desde "
                   "a Lei 14.382/2022, ela também pode ser feita diretamente no Cartório de Registro de Imóveis, "
                   "com advogado e sem processo judicial.\n\nO pedido reúne o contrato de promessa de compra e "
                   "venda, a prova do pagamento, ata notarial, certidões, o comprovante do ITBI e a notificação "
                   "do vendedor, que tem 15 dias para cumprir a obrigação. Não é necessário que a promessa "
                   "tenha sido registrada antes.\n\nCada caso exige análise da documentação.\n\nSalve este vídeo "
                   "e compartilhe com quem está nessa situação.",
        "hashtags": ["#adjudicacaocompulsoria", "#escritura", "#compraevenda"] + TAGS_IMOB + TAGS_FIXAS,
        "fontes": [f"Lei 6.015/1973, art. 216-B, §§ 1º a 3º, incluído pela Lei 14.382/2022 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 26/10
    {
        "id": "2026-10-26_holding-familiar",
        "data_publicacao": "2026-10-26", "formato": "carrossel", "area": "Direito Empresarial",
        "titulo": "Holding familiar: o que *realmente* é",
        "subtitulo": "Planejamento patrimonial com segurança jurídica.",
        "foto": "assets/fotos/escolhidas/pexels-8729964.jpg",
        "slides": [
            {"titulo": "O que é",
             "texto": "É uma empresa criada para reunir e administrar bens de uma família, como imóveis e "
                      "participações em outras empresas."},
            {"titulo": "Para que serve",
             "texto": "Pode facilitar a administração do patrimônio e o planejamento da sucessão, com regras "
                      "definidas no contrato social e em acordos entre os sócios."},
            {"titulo": "Não é blindagem absoluta",
             "texto": "Em caso de abuso, como confusão patrimonial ou desvio de finalidade, o juiz pode "
                      "desconsiderar a empresa e alcançar os bens dos sócios (Código Civil, art. 50)."},
            {"titulo": "Não serve para todos",
             "texto": "Custos de abertura e manutenção, tributos e a realidade de cada família precisam ser "
                      "analisados antes da decisão."},
            {"titulo": "Planejamento é individual",
             "texto": "Cada patrimônio tem particularidades. Uma holding bem estruturada depende de análise "
                      "jurídica, contábil e tributária."},
        ],
        "chamada_final": "Você já tinha ouvido falar em holding familiar?",
        "legenda": "A holding familiar virou assunto frequente, mas nem sempre é bem explicada.\n\nEla é uma "
                   "empresa criada para reunir e administrar bens de uma família, como imóveis e participações "
                   "societárias. Bem estruturada, pode facilitar a administração do patrimônio e o planejamento "
                   "da sucessão.\n\nPor outro lado, a holding não é uma blindagem absoluta. Pelo artigo 50 do "
                   "Código Civil, em caso de abuso, como confusão patrimonial ou desvio de finalidade, o juiz "
                   "pode desconsiderar a empresa e alcançar os bens dos sócios. Ela também não é indicada para "
                   "todos: custos, tributos e a realidade de cada família precisam ser avaliados.\n\nPor isso, "
                   "a decisão depende de análise jurídica, contábil e tributária individualizada.\n\nSalve este "
                   "post para consultar depois.",
        "hashtags": ["#holdingfamiliar", "#holding", "#planejamentopatrimonial", "#planejamentosucessorio",
                     "#direitoempresarial"] + TAGS_FIXAS,
        "fontes": [f"Código Civil, arts. 50, 981 e 1.052 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 28/10
    {
        "id": "2026-10-28_reel-bpc-loas",
        "data_publicacao": "2026-10-28", "formato": "reel", "area": "Direito Previdenciário",
        "titulo": "BPC/LOAS: quem tem *direito*?",
        "subtitulo": "Um salário mínimo por mês",
        "video_capa": "assets/videos/pexels-5271503.mp4", "video_final": "assets/videos/pexels-7516761.mp4",
        "trilha": "assets/audio/pixabay-590331-inspiring-emotional.mp3",
        "slides": [
            {"titulo": "Para quem é",
             "texto": "Pessoas idosas a partir de 65 anos e pessoas com deficiência que não tenham meios de se "
                      "manter nem de ser mantidas pela família (Lei 8.742/1993, art. 20).",
             "video": "assets/videos/pexels-7496263.mp4"},
            {"titulo": "O critério de renda",
             "texto": "Em regra, renda familiar por pessoa de até 1/4 do salário mínimo. O regulamento pode "
                      "ampliar esse limite para até 1/2 salário mínimo.",
             "video": "assets/videos/pexels-7981920.mp4"},
            {"titulo": "Cadastro Único obrigatório",
             "texto": "A inscrição no CPF e no Cadastro Único é requisito para conceder, manter e revisar o "
                      "benefício (art. 20, § 12).",
             "video": "assets/videos/pexels-7821798.mp4"},
        ],
        "chamada_final": "Compartilhe com quem pode ter direito.",
        "legenda": "O Benefício de Prestação Continuada, conhecido como BPC/LOAS, garante um salário mínimo por "
                   "mês a quem mais precisa. E não exige contribuições ao INSS.\n\nPodem ter direito pessoas "
                   "idosas a partir de 65 anos e pessoas com deficiência que não tenham meios de se manter nem "
                   "de ser mantidas pela família.\n\nEm regra, a renda familiar por pessoa deve ser de até 1/4 do "
                   "salário mínimo, e o regulamento pode ampliar esse limite para até 1/2 salário mínimo. A "
                   "inscrição no CPF e no Cadastro Único é obrigatória para pedir, manter e revisar o benefício.\n\n"
                   "Cada família tem uma realidade, e outros elementos também podem ser considerados na "
                   "análise.\n\nSalve este vídeo e compartilhe com quem pode ter direito.",
        "hashtags": ["#bpc", "#loas", "#inss", "#direitoprevidenciario", "#assistenciasocial"] + TAGS_FIXAS,
        "fontes": [f"Lei 8.742/1993, art. 20, caput, §§ 3º, 11, 11-A e 12 ({CONFERIDO})"],
    },
    # ------------------------------------------------------------------ 30/10
    {
        "id": "2026-10-30_reurb",
        "data_publicacao": "2026-10-30", "formato": "carrossel", "area": "Direito Imobiliário",
        "titulo": "REURB: a regularização de *bairros* inteiros",
        "subtitulo": "Conheça a regularização fundiária urbana.",
        "foto": "assets/fotos/escolhidas/pexels-17853617.jpg",
        "slides": [
            {"titulo": "O que é a REURB",
             "texto": "Um conjunto de medidas jurídicas, urbanísticas, ambientais e sociais para incorporar "
                      "núcleos urbanos informais à cidade e titular seus ocupantes (Lei 13.465/2017, art. 9º)."},
            {"titulo": "Núcleo urbano informal",
             "texto": "É o loteamento clandestino ou irregular, ou aquele em que não foi possível titular os "
                      "moradores, mesmo que tenha seguido a lei da época (art. 11, II)."},
            {"titulo": "REURB-S",
             "texto": "Voltada a núcleos ocupados predominantemente por população de baixa renda, assim "
                      "declarados pelo município. O primeiro registro é isento de custas e emolumentos."},
            {"titulo": "REURB-E",
             "texto": "Aplica-se aos núcleos ocupados por população que não se enquadra na REURB-S "
                      "(art. 13, II)."},
            {"titulo": "Quem pode pedir",
             "texto": "Os próprios moradores, individual ou coletivamente, associações de moradores, o "
                      "município, a Defensoria Pública e o Ministério Público, entre outros (art. 14)."},
        ],
        "chamada_final": "O seu bairro já passou por regularização?",
        "legenda": "Em muitas cidades, inclusive no ABC, há bairros inteiros formados por loteamentos "
                   "irregulares ou clandestinos. Os moradores vivem ali há anos, mas não têm o título de "
                   "propriedade.\n\nA REURB, criada pela Lei 13.465/2017, reúne medidas jurídicas, urbanísticas, "
                   "ambientais e sociais para incorporar esses núcleos à cidade e titular seus ocupantes.\n\nHá "
                   "duas modalidades: a REURB-S, para núcleos ocupados predominantemente por população de baixa "
                   "renda, com isenção de custas e emolumentos no primeiro registro, e a REURB-E, para os "
                   "demais casos.\n\nO pedido pode partir dos próprios moradores, de associações, do município, "
                   "da Defensoria Pública e do Ministério Público, entre outros.\n\nSalve este post e "
                   "compartilhe com seus vizinhos.",
        "hashtags": ["#reurb", "#regularizacaofundiaria", "#loteamento"] + TAGS_IMOB + TAGS_FIXAS,
        "fontes": [f"Lei 13.465/2017, arts. 9º, 11, II, 13 e 14 ({CONFERIDO})"],
    },
]

STORIES = [
    {"id": "2026-10-03_stories-mito-iptu", "data_publicacao": "2026-10-03", "tipo": "mito_verdade",
     "area": "Direito Imobiliário",
     "quadros": [
         {"etiqueta": "MITO OU VERDADE?", "titulo": "Quem paga o IPTU vira dono do imóvel.",
          "rodape": "toque para ver a resposta"},
         {"etiqueta": "RESPOSTA", "destaque": "Mito!", "titulo": "Pagar o IPTU, sozinho, não torna ninguém *dono*.",
          "texto": "O pagamento pode ajudar a comprovar a posse em um pedido de usucapião, mas a propriedade "
                   "depende do registro ou do reconhecimento da usucapião."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "Quem não registra *não é dono*.",
          "texto": "Código Civil, art. 1.245.", "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"Código Civil, art. 1.245; Lei 6.015/1973, art. 216-A, IV ({CONFERIDO})"]},
    {"id": "2026-10-10_stories-juridiques-averbacao", "data_publicacao": "2026-10-10", "tipo": "juridiques",
     "area": "Direito Imobiliário",
     "quadros": [
         {"etiqueta": "JURIDIQUÊS X PORTUGUÊS", "titulo": "*Averbação*",
          "texto": "Você já ouviu essa palavra no cartório?", "rodape": "toque para traduzir"},
         {"etiqueta": "EM PORTUGUÊS", "titulo": "Anotar na matrícula uma *mudança* no imóvel.",
          "texto": "Por exemplo: uma construção, uma demolição ou a troca do nome da rua "
                   "(Lei 6.015/1973, art. 167, II, 4)."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "Construiu? A obra também precisa ser *averbada*.",
          "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"Lei 6.015/1973, art. 167, II, 4 ({CONFERIDO})"]},
    {"id": "2026-10-17_stories-pensao-sem-carencia", "data_publicacao": "2026-10-17", "tipo": "voce_sabia",
     "area": "Direito Previdenciário",
     "quadros": [
         {"etiqueta": "VOCÊ SABIA?",
          "titulo": "A pensão por morte não exige um número *mínimo* de contribuições.",
          "rodape": "toque para entender"},
         {"etiqueta": "EXPLICANDO", "titulo": "Em regra, basta que o falecido fosse *segurado* do INSS.",
          "texto": "A pensão independe de carência (Lei 8.213/1991, art. 26, I)."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "Pedida em até *90 dias*, é paga desde o óbito.",
          "texto": "Para filhos menores de 16 anos, o prazo é de 180 dias.",
          "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"Lei 8.213/1991, arts. 26, I, e 74, I ({CONFERIDO})"]},
    {"id": "2026-10-24_stories-prazo-inventario", "data_publicacao": "2026-10-24", "tipo": "complete",
     "area": "Direito Imobiliário",
     "quadros": [
         {"etiqueta": "COMPLETE A FRASE", "titulo": "O inventário deve ser aberto em até…",
          "rodape": "toque para ver a resposta"},
         {"etiqueta": "RESPOSTA", "destaque": "2 meses!", "titulo": "Contados do *falecimento*.",
          "texto": "É o prazo do Código de Processo Civil (art. 611). Em São Paulo, o atraso pode gerar multa "
                   "no ITCMD."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "Herança em dia protege a *família*.",
          "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"CPC, art. 611; Lei estadual SP 10.705/2000, art. 21, I ({CONFERIDO})"]},
    {"id": "2026-10-31_stories-expectativa-realidade", "data_publicacao": "2026-10-31", "tipo": "expectativa",
     "area": "Direito Imobiliário",
     "quadros": [
         {"etiqueta": "EXPECTATIVA", "titulo": "“Comprei, paguei e assinei. O imóvel é *meu*!”",
          "rodape": "toque para ver a realidade"},
         {"etiqueta": "REALIDADE", "destaque": "Ainda não…",
          "titulo": "A propriedade só passa para o seu nome com o *registro*.",
          "texto": "Enquanto o título não é registrado, a lei considera o vendedor como dono "
                   "(Código Civil, art. 1.245)."},
         {"etiqueta": "SALVE PARA LEMBRAR", "titulo": "Registro em dia, imóvel *seguro*.",
          "rodape": "compartilhe com quem precisa"}],
     "fontes": [f"Código Civil, art. 1.245, caput e § 1º ({CONFERIDO})"]},
]


def gravar():
    PASTA_FILA.mkdir(parents=True, exist_ok=True)
    for p in POSTS + [dict(s, formato="stories") for s in STORIES]:
        (PASTA_FILA / f"{p['id']}.json").write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(POSTS), len(STORIES)


if __name__ == "__main__":
    print(gravar())
