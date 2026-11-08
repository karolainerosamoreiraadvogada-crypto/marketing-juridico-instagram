"""Calendário anual de estações do ano e datas comemorativas (pedido da Dra. Dirciléia, 02/10/2026).

Regras de publicação:
  - O post comemorativo sai NO PRÓPRIO DIA da data, às 21h (feed). Se a data cair em
    segunda, quarta ou sexta, ele ocupa o post do dia; nos outros dias, é um post extra.
  - Datas marcadas com formato "stories" saem no sábado da semana, às 14h.
  - Na capa entra o selo de calendário (dia e mês) e o nome da data no lugar da área.
  - Ética da OAB (Provimento 205/2021): a data é gancho para conteúdo informativo.
    Nada de promoções, descontos ou "presentes" em serviços, nem Black Friday.
  - A base legal indicada é o ponto de partida: na programação do mês, o Claude confere
    tudo de novo nos sites oficiais, porque as leis mudam.

Uso:  python -m conteudo.calendario 2027        (lista as datas do ano)
"""
import sys
from datetime import date, timedelta


def _domingo(ano: int, mes: int, ordem: int) -> date:
    """N-ésimo domingo do mês (Dia das Mães: 2º domingo de maio; dos Pais: 2º de agosto)."""
    d = date(ano, mes, 1)
    d += timedelta(days=(6 - d.weekday()) % 7)
    return d + timedelta(weeks=ordem - 1)


def _sabado_da_semana(d: date) -> date:
    return d + timedelta(days=(5 - d.weekday()) % 7)


# Início das estações no Hemisfério Sul (horário de Brasília)
ESTACOES = {
    2026: {"outono": date(2026, 3, 20), "inverno": date(2026, 6, 21), "primavera": date(2026, 9, 22),
           "verao": date(2026, 12, 21)},
    2027: {"outono": date(2027, 3, 20), "inverno": date(2027, 6, 21), "primavera": date(2027, 9, 23),
           "verao": date(2027, 12, 21)},
}

# (mês, dia) fixo ou função(ano) -> date
DATAS = [
    {"quando": (1, 1), "nome": "Ano-Novo", "area": "Direito Imobiliário", "formato": "reel",
     "ideia": "Resoluções para o imóvel no ano que começa: registrar, averbar, conferir a matrícula.",
     "base": "Código Civil, art. 1.245; Lei 6.015/1973, arts. 17 e 167"},
    {"quando": (1, 24), "nome": "Dia Nacional do Aposentado", "area": "Direito Previdenciário",
     "formato": "carrossel",
     "ideia": "Homenagem e informação: o prazo de 10 anos para pedir a revisão da aposentadoria.",
     "base": "Lei 6.926/1981 (institui a data); Lei 8.213/1991, art. 103"},
    {"quando": (3, 8), "nome": "Dia Internacional da Mulher", "area": "Direito Previdenciário",
     "formato": "reel",
     "ideia": "Direitos previdenciários da mulher: idade mínima, salário-maternidade, dona de casa.",
     "base": "EC 103/2019, art. 19; Lei 8.213/1991, art. 71; Lei 8.212/1991, art. 21, § 2º"},
    {"quando": (3, 15), "nome": "Dia do Consumidor", "area": "Direito Imobiliário", "formato": "carrossel",
     "ideia": "Comprou na planta e quer desistir? O que a lei diz sobre o distrato.",
     "base": "Lei 4.591/1964, art. 67-A (Lei 13.786/2018)"},
    {"quando": "outono", "nome": "Começa o outono", "area": "Direito Tributário", "formato": "carrossel",
     "ideia": "Estação de organizar a papelada: venda de imóvel e as isenções do ganho de capital.",
     "base": "Lei 9.250/1995, art. 23; Lei 11.196/2005, art. 39"},
    {"quando": (4, 21), "nome": "Tiradentes", "area": "Direito Tributário", "formato": "reel",
     "ideia": "Da derrama à Constituição: os limites ao poder de tributar que protegem o contribuinte.",
     "base": "Constituição Federal, art. 150"},
    {"quando": (5, 1), "nome": "Dia do Trabalhador", "area": "Direito Previdenciário", "formato": "carrossel",
     "ideia": "Trabalhou e o vínculo não aparece no INSS? Como corrigir o CNIS.",
     "base": "Lei 8.213/1991, arts. 29-A e 55"},
    {"quando": lambda a: _domingo(a, 5, 2), "nome": "Dia das Mães", "area": "Direito Previdenciário",
     "formato": "reel",
     "ideia": "Salário-maternidade: também na adoção e para quem está sem emprego.",
     "base": "Lei 8.213/1991, arts. 15, 71 e 71-A"},
    {"quando": (5, 25), "nome": "Dia do Contribuinte", "area": "Direito Tributário", "formato": "carrossel",
     "ideia": "Dia Nacional do Respeito ao Contribuinte: prazos que extinguem dívidas fiscais.",
     "base": "Lei 12.325/2010 (institui a data); CTN, arts. 173 e 174"},
    {"quando": (6, 12), "nome": "Dia dos Namorados", "area": "Direito Imobiliário", "formato": "reel",
     "ideia": "Vão comprar um imóvel juntos? Regime de bens, união estável e escritura.",
     "base": "Código Civil, arts. 1.725 e 1.658"},
    {"quando": "inverno", "nome": "Começa o inverno", "area": "Direito Imobiliário", "formato": "carrossel",
     "ideia": "Agasalhe o seu patrimônio: check-up de documentos do imóvel.",
     "base": "Lei 6.015/1973; Código Civil, art. 1.245"},
    {"quando": lambda a: _sabado_da_semana(date(a, 6, 24)), "nome": "Festa Junina", "area": "Direito Imobiliário",
     "formato": "stories",
     "ideia": "Arraiá do juridiquês: quadrilha de termos do cartório traduzidos para o português.",
     "base": "Lei 6.015/1973"},
    {"quando": lambda a: _domingo(a, 8, 2), "nome": "Dia dos Pais", "area": "Direito Imobiliário",
     "formato": "carrossel",
     "ideia": "Planejar é cuidar: doação de imóvel aos filhos com reserva de usufruto.",
     "base": "Código Civil, arts. 108, 544, 1.394 e 1.410"},
    {"quando": (8, 11), "nome": "Dia do Advogado", "area": "Direito Imobiliário", "formato": "reel",
     "ideia": "Quando a própria lei exige advogado: usucapião, adjudicação e inventário em cartório.",
     "base": "Constituição Federal, art. 133; Lei 6.015/1973, arts. 216-A e 216-B; CPC, art. 610"},
    {"quando": (8, 20), "nome": "Aniversário de São Bernardo do Campo", "area": "Direito Imobiliário",
     "formato": "carrossel",
     "ideia": "Homenagem à cidade e regularização de imóveis em São Bernardo do Campo.",
     "base": "Lei 13.465/2017 e legislação municipal (conferir na época)"},
    {"quando": (8, 27), "nome": "Dia do Corretor de Imóveis", "area": "Direito Imobiliário",
     "formato": "carrossel",
     "ideia": "Antes de assinar: as certidões que protegem quem compra.",
     "base": "Lei 13.097/2015, art. 54; Lei 6.015/1973"},
    {"quando": (9, 7), "nome": "Independência", "area": "Direito Previdenciário", "formato": "reel",
     "ideia": "Independência financeira: por que planejar a aposentadoria antes de pedir.",
     "base": "EC 103/2019 (regras de transição)"},
    {"quando": (9, 21), "nome": "Luta da Pessoa com Deficiência", "area": "Direito Tributário",
     "formato": "carrossel",
     "ideia": "Isenções tributárias para pessoas com deficiência (conferir vigência na época).",
     "base": "Lei 11.133/2005 (institui a data); legislação de isenções vigente"},
    {"quando": "primavera", "nome": "Começa a primavera", "area": "Direito Empresarial", "formato": "reel",
     "ideia": "Estação de florescer: MEI, microempresa ou empresa de pequeno porte?",
     "base": "LC 123/2006, arts. 3º e 18-A"},
    {"quando": (10, 1), "nome": "Dia da Pessoa Idosa", "area": "Direito Previdenciário", "formato": "carrossel",
     "ideia": "BPC para a pessoa idosa: requisitos e o que a lei garante.",
     "base": "Lei 10.741/2003; Lei 8.742/1993, art. 20"},
    {"quando": (10, 5), "nome": "Micro e Pequena Empresa", "area": "Direito Empresarial", "formato": "carrossel",
     "ideia": "Dia Nacional da Micro e Pequena Empresa: limites de faturamento e enquadramento.",
     "base": "Lei 9.841/1999 (origem da data); LC 123/2006, art. 3º"},
    {"quando": (10, 12), "nome": "Dia das Crianças", "area": "Direito Imobiliário", "formato": "reel",
     "ideia": "Imóvel herdado por criança: como fica o inventário.",
     "base": "CPC, art. 610; Resolução CNJ 35/2007 (conferir alterações)"},
    {"quando": (10, 28), "nome": "Dia do Servidor Público", "area": "Direito Previdenciário",
     "formato": "carrossel",
     "ideia": "Trabalhou na iniciativa privada antes? A contagem recíproca do tempo de contribuição.",
     "base": "Constituição Federal, art. 201, § 9º; Lei 8.213/1991, art. 94"},
    {"quando": (11, 2), "nome": "Dia de Finados", "area": "Direito Imobiliário", "formato": "carrossel",
     "ideia": "Testamento: um gesto de cuidado com quem fica.",
     "base": "Código Civil, arts. 1.789, 1.845, 1.846, 1.857 a 1.864"},
    {"quando": (11, 20), "nome": "Consciência Negra", "area": "Direito Imobiliário", "formato": "carrossel",
     "ideia": "Terras quilombolas: a propriedade garantida pela Constituição.",
     "base": "Lei 14.759/2023; ADCT, art. 68; Decreto 4.887/2003; STF, ADI 3.239"},
    {"quando": (12, 3), "nome": "Pessoa com Deficiência", "area": "Direito Previdenciário", "formato": "reel",
     "ideia": "Aposentadoria da pessoa com deficiência: regras próprias e mais favoráveis.",
     "base": "LC 142/2013, arts. 3º a 5º; EC 103/2019, art. 22"},
    {"quando": (12, 8), "nome": "Dia da Justiça", "area": "Direito Imobiliário", "formato": "carrossel",
     "ideia": "Nem tudo precisa de processo: caminhos extrajudiciais para o imóvel.",
     "base": "Lei 1.408/1951; Lei 6.015/1973, arts. 216-A e 216-B; CPC, art. 610"},
    {"quando": "verao", "nome": "Começa o verão", "area": "Direito Imobiliário", "formato": "reel",
     "ideia": "Imóvel na temporada: as regras da Lei do Inquilinato.",
     "base": "Lei 8.245/1991, arts. 48 a 50"},
    {"quando": (12, 25), "nome": "Natal", "area": "Direito Imobiliário", "formato": "carrossel",
     "ideia": "Vai dar um imóvel de presente? Escritura, registro, ITCMD e usufruto.",
     "base": "Código Civil, arts. 108, 544, 1.245, 1.394 e 1.410; Lei SP 10.705/2000"},
]


def data_em(item: dict, ano: int) -> date:
    q = item["quando"]
    if isinstance(q, str):
        return ESTACOES[ano][q]
    if callable(q):
        return q(ano)
    return date(ano, *q)


def datas(ano: int, mes: int | None = None) -> list[dict]:
    """Datas comemorativas do ano (ou do mês), em ordem, com a data calculada."""
    saida = [dict(item, data=data_em(item, ano)) for item in DATAS]
    if mes:
        saida = [d for d in saida if d["data"].month == mes]
    return sorted(saida, key=lambda d: d["data"])


if __name__ == "__main__":
    ano = int(sys.argv[1]) if len(sys.argv) > 1 else date.today().year
    dias = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
    for d in datas(ano):
        print(f"{d['data']:%d/%m} {dias[d['data'].weekday()]}  {d['formato']:9} {d['nome']:38} {d['area']}")
