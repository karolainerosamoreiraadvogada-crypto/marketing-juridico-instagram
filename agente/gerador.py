"""Cria novos posts: pauta, redação (Gemini), revisão em 10 etapas e imagens."""
import json
import re
import unicodedata

from . import fila, llm, revisor
from .config import PASTA_IMAGENS, RAIZ, carregar_perfil, carregar_prompt_sistema
from .imagem import gerar_imagens

ESQUEMA = """Responda SOMENTE com JSON neste formato:
{
  "posts": [
    {
      "formato": "carrossel" ou "card",
      "area": "exatamente o nome da área pedida",
      "titulo": "gancho da capa, até 8 palavras; destaque UMA palavra com *asteriscos*",
      "subtitulo": "frase curta de apoio na capa, até 12 palavras",
      "foto_busca": "2 a 4 palavras em inglês para buscar foto (ex.: house keys document)",
      "slides": [ {"titulo": "até 6 palavras", "texto": "até 45 palavras"} ],
      "chamada_final": "pergunta que convide a comentar, até 10 palavras",
      "legenda": "80 a 180 palavras, parágrafos curtos, termina com chamada permitida",
      "hashtags": ["#exemplo"],
      "fontes": ["cada fundamento citado, ex.: Código Civil, art. 1.245"]
    }
  ]
}
Regras do formato:
- "carrossel": de 4 a 6 slides de conteúdo (capa e encerramento são automáticos).
- "card": "slides" deve ser lista vazia; título e subtítulo carregam a mensagem.
- De 6 a 10 hashtags específicas, sem repetir as fixas.
- "fontes": só o que consta nas tabelas da skill. Sem fundamento citado, lista vazia."""


def _ciclo(pesos: dict, inicio: int, qtd: int) -> list:
    """Distribui itens proporcionalmente aos pesos, de forma intercalada."""
    total = sum(pesos.values())
    sequencia, acumulado = [], {k: 0.0 for k in pesos}
    for _ in range(total):
        for k in pesos:
            acumulado[k] += pesos[k] / total
        escolhido = max(acumulado, key=acumulado.get)
        acumulado[escolhido] -= 1
        sequencia.append(escolhido)
    return [sequencia[(inicio + i) % len(sequencia)] for i in range(qtd)]


def _slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto.replace("*", "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:40]


def _prompt_usuario(perfil: dict, pedidos: list, tema: str | None) -> str:
    areas = {a["nome"]: a for a in perfil["areas"]}
    linhas = []
    for i, (formato, area) in enumerate(pedidos, start=1):
        exemplos = ", ".join(areas[area].get("temas_exemplo", []))
        linhas.append(f"Post {i}: formato {formato}; área {area} (ideias: {exemplos})")
    recentes = "\n".join(f"- {t}" for t in fila.titulos_recentes()) or "(nenhum ainda)"
    pauta = (f"Todos os posts devem tratar deste tema: {tema}" if tema else
             "Escolha temas com dúvidas reais e frequentes do público, variando formatos "
             "de conteúdo (mito x verdade, checklist, passo a passo, erro comum, comparativo).")
    return f"""Crie {len(pedidos)} post(s) para o Instagram {perfil['advogado']['instagram']}
({perfil['advogado']['nome']}, {perfil['advogado']['cidade']}).

{chr(10).join(linhas)}

Tom de voz: {perfil['tom_de_voz']}
Público: {perfil['publico']}

{pauta}

NÃO repita estes títulos já usados:
{recentes}

{ESQUEMA}"""


def gerar_lote(qtd: int | None = None, tema: str | None = None, area: str | None = None,
               datas: list | None = None) -> list:
    """Gera posts para as datas informadas (ou para as próximas datas livres)."""
    perfil = carregar_perfil()
    if datas is None:
        qtd = qtd or perfil["calendario"]["posts_por_lote"]
        datas = fila.proximas_datas(qtd, perfil["calendario"]["dias_semana"])
    qtd = len(datas)
    inicio = len(fila.publicados()) + len(fila.na_fila())
    formatos = _ciclo(perfil.get("formatos", {"carrossel": 1}), inicio, qtd)
    areas = ([area] * qtd if area else
             _ciclo({a["nome"]: a.get("peso", 1) for a in perfil["areas"]}, inicio, qtd))

    pedidos = list(zip(formatos, areas))
    resposta = llm.gerar_json(carregar_prompt_sistema(),
                              _prompt_usuario(perfil, pedidos, tema) + _aprendizados())
    brutos = resposta.get("posts", [])[:qtd]

    criados = []
    for bruto, (formato, area_post), data in zip(brutos, pedidos, datas):
        if formato == "carrossel" and not bruto.get("slides"):
            formato = "card"
        post = {
            "id": f"{data.isoformat()}_{_slug(bruto.get('titulo', 'post'))}",
            "data_publicacao": data.isoformat(),
            "formato": formato,
            "area": area_post,
            "titulo": bruto["titulo"],
            "subtitulo": bruto.get("subtitulo", ""),
            "foto_busca": bruto.get("foto_busca", ""),
            "slides": bruto.get("slides", []) if formato == "carrossel" else [],
            "chamada_final": bruto.get("chamada_final", ""),
            "legenda": bruto["legenda"],
            "hashtags": bruto.get("hashtags", []),
            "fontes": bruto.get("fontes", []),
        }
        post = revisor.revisar(post)
        fixas = [h for h in perfil.get("hashtags_fixas", []) if h not in post["hashtags"]]
        post["hashtags"] = post["hashtags"] + fixas
        imagens = gerar_imagens(post, perfil, PASTA_IMAGENS)
        post["imagens"] = [p.relative_to(RAIZ).as_posix() for p in imagens]
        fila.salvar(post)
        criados.append(post)
    return criados


def _aprendizados() -> str:
    """Resumo do último relatório de KPIs, para o agente repetir o que funciona."""
    from .kpi import aprendizados_para_prompt
    texto = aprendizados_para_prompt()
    return f"\n\nAPRENDIZADOS DOS KPIs (use como orientação):\n{texto}" if texto else ""


def gerar_mes(ano: int, mes: int, lote: int = 3, pausa_s: int = 10) -> list:
    """Programação do mês inteiro (seg/qua/sex), gerada em lotes pequenos para
    respeitar o limite gratuito do Gemini."""
    import time
    from datetime import timedelta
    from .config import hoje

    perfil = carregar_perfil()
    datas = fila.datas_do_mes(ano, mes, perfil["calendario"]["dias_semana"],
                              a_partir_de=hoje() + timedelta(days=1))
    criados = []
    for i in range(0, len(datas), lote):
        criados += gerar_lote(datas=datas[i:i + lote])
        if i + lote < len(datas):
            time.sleep(pausa_s)
    return criados


def calendario_markdown(posts: list) -> str:
    dias = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
    from datetime import date
    linhas = ["| Data | Dia | Área | Formato | Título | Revisão |", "|---|---|---|---|---|---|"]
    for p in sorted(posts, key=lambda x: x["data_publicacao"]):
        d = date.fromisoformat(p["data_publicacao"])
        ok = "✅" if p.get("revisao", {}).get("aprovado_pelo_revisor") else "⚠️"
        linhas.append(f"| {d.strftime('%d/%m')} | {dias[d.weekday()]} | {p['area']} | "
                      f"{p['formato']} | {p['titulo'].replace('*', '')} | {ok} |")
    return "\n".join(linhas)


def resumo_markdown(posts: list, url_base: str = "") -> str:
    """Corpo do Pull Request de aprovação."""
    linhas = ["## Programação para aprovação da Dra. Dirciléia Pacheco", "",
              calendario_markdown(posts), "",
              "Revise cada post. Para ajustar, edite o arquivo JSON em `posts/fila/`.",
              "**Fazer o merge deste Pull Request = aprovar a publicação.** "
              "Para recusar um post, apague o JSON dele antes do merge.", ""]
    for p in posts:
        linhas += [f"### {p['data_publicacao']} · {p['area']} · {p['formato']}",
                   f"**{p['titulo'].replace('*', '')}**", "",
                   revisor.resumo(p), ""]
        r = p.get("revisao", {})
        if r.get("alertas_oab"):
            linhas += ["> ⚠️ **Termos sensíveis (OAB):** " + "; ".join(r["alertas_oab"]), ""]
        for e in r.get("etapas", []):
            if not e["ok"]:
                linhas.append(f"> ❌ {e['etapa']}: {e['obs']}")
        for img in p["imagens"]:
            linhas.append(f'<img src="{url_base}{img}" width="200">')
        linhas += ["", "<details><summary>Legenda e fontes</summary>", "",
                   p["legenda"], "", " ".join(p["hashtags"]), "",
                   "**Fontes citadas:** " + ("; ".join(p.get("fontes", [])) or "nenhuma"),
                   "</details>", ""]
    return "\n".join(linhas)


if __name__ == "__main__":
    print(json.dumps(gerar_lote(), ensure_ascii=False, indent=2))
