"""Monitoramento de engajamento e KPIs do perfil.

- coletar():   fotografia diária (seguidores + métricas de cada post) pela API
               oficial do Instagram. Precisa da permissão
               instagram_business_manage_insights no token.
- relatorio(): relatório em Markdown (semanal ou mensal) com KPIs, metas,
               ranking de posts, desempenho por área e formato, e recomendações.
- aprendizados_para_prompt(): resumo do que funcionou, enviado ao gerador de posts.

As fotografias ficam em dados/metricas/AAAA-MM-DD.json (histórico no repositório).
"""
import json
from datetime import date, datetime, timedelta

from . import fila
from .config import FUSO, RAIZ, carregar_perfil, hoje

PASTA_METRICAS = RAIZ / "dados" / "metricas"
ARQ_APRENDIZADOS = RAIZ / "dados" / "aprendizados.json"
METRICAS_POST = ["reach", "saved", "shares", "total_interactions", "views"]


# ---------------------------------------------------------------- coleta


def _data_brasilia(timestamp: str) -> str:
    """"2026-10-13T00:08:04+0000" -> "2026-10-12" (data do post no horário de Brasília)."""
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z").astimezone(FUSO).date().isoformat()

def _insights_post(ig, media_id: str) -> dict:
    """Busca as métricas do post; se o lote falhar, tenta uma a uma."""
    from .instagram import ErroInstagram
    try:
        dados = ig._req("GET", f"{media_id}/insights", metric=",".join(METRICAS_POST))
        return {m["name"]: m["values"][0]["value"] for m in dados.get("data", [])}
    except ErroInstagram:
        saida = {}
        for metrica in METRICAS_POST:
            try:
                d = ig._req("GET", f"{media_id}/insights", metric=metrica)
                saida[metrica] = d["data"][0]["values"][0]["value"]
            except (ErroInstagram, KeyError, IndexError):
                pass
        return saida


def coletar(dias: int = 90) -> dict:
    from .instagram import Instagram
    ig = Instagram()
    conta = ig._req("GET", "me", fields="username,followers_count,follows_count,media_count")
    midias = ig._req("GET", f"{ig.user_id}/media", limit=50,
                     fields="id,caption,media_type,media_product_type,timestamp,permalink,"
                            "like_count,comments_count").get("data", [])
    limite = (datetime.now() - timedelta(days=dias)).isoformat()
    posts = []
    for m in midias:
        if m["timestamp"] < limite:
            continue
        registro = {
            "id": m["id"],
            "data": _data_brasilia(m["timestamp"]),  # 21h de Brasília já é o dia seguinte em UTC
            "permalink": m.get("permalink", ""),
            "tipo": m.get("media_type", ""),
            "legenda": (m.get("caption") or "")[:90].replace("\n", " "),
            "curtidas": m.get("like_count", 0),
            "comentarios": m.get("comments_count", 0),
        }
        ins = _insights_post(ig, m["id"])
        registro.update({
            "alcance": ins.get("reach"),
            "salvamentos": ins.get("saved"),
            "compartilhamentos": ins.get("shares"),
            "interacoes": ins.get("total_interactions"),
            "visualizacoes": ins.get("views"),
        })
        posts.append(registro)

    foto = {"data": hoje().isoformat(), "seguidores": conta.get("followers_count"),
            "seguindo": conta.get("follows_count"), "total_posts": conta.get("media_count"),
            "posts": posts}
    PASTA_METRICAS.mkdir(parents=True, exist_ok=True)
    (PASTA_METRICAS / f"{foto['data']}.json").write_text(
        json.dumps(foto, ensure_ascii=False, indent=2), encoding="utf-8")
    return foto


# ---------------------------------------------------------------- análise

def _fotos() -> list[dict]:
    if not PASTA_METRICAS.exists():
        return []
    return [json.loads(a.read_text(encoding="utf-8"))
            for a in sorted(PASTA_METRICAS.glob("????-??-??.json"))]


def _foto_em(fotos: list, dia: date):
    """Fotografia mais próxima (anterior ou igual) de uma data."""
    candidatas = [f for f in fotos if f["data"] <= dia.isoformat()]
    return candidatas[-1] if candidatas else (fotos[0] if fotos else None)


def _nossos_posts() -> dict:
    """Mapa permalink/shortcode -> post do agente (área, formato, título)."""
    mapa = {}
    for p in fila.publicados():
        for chave in (p.get("instagram_id"), p.get("shortcode"), p.get("permalink")):
            if chave:
                mapa[chave] = p
    return mapa


def _enriquecer(post: dict, nossos: dict) -> dict:
    shortcode = post["permalink"].rstrip("/").split("/")[-1] if post.get("permalink") else ""
    nosso = nossos.get(post["id"]) or nossos.get(shortcode) or {}
    interacoes = post.get("interacoes")
    if interacoes is None:
        interacoes = sum(post.get(k) or 0 for k in
                         ("curtidas", "comentarios", "salvamentos", "compartilhamentos"))
    alcance = post.get("alcance") or 0
    return {**post,
            "titulo": (nosso.get("titulo") or post.get("legenda", "")[:60]).replace("*", ""),
            "area": nosso.get("area", "Anterior ao agente"),
            "formato": nosso.get("formato", "carrossel" if post.get("tipo") == "CAROUSEL_ALBUM"
                                 else post.get("tipo", "").lower()),
            "interacoes": interacoes,
            "engajamento": (interacoes / alcance) if alcance else None}


def _media(valores):
    valores = [v for v in valores if v is not None]
    return sum(valores) / len(valores) if valores else None


def _fmt(v, pct=False):
    if v is None:
        return "sem dado"
    return f"{v * 100:.1f}%" if pct else (f"{v:.1f}" if isinstance(v, float) else str(v))


def _agrupar(posts: list, campo: str) -> list:
    grupos = {}
    for p in posts:
        grupos.setdefault(p[campo], []).append(p)
    linhas = []
    for nome, itens in grupos.items():
        linhas.append({"nome": nome, "posts": len(itens),
                       "alcance": _media([i.get("alcance") for i in itens]),
                       "engajamento": _media([i.get("engajamento") for i in itens]),
                       "salvamentos": _media([i.get("salvamentos") for i in itens]),
                       "comentarios": _media([i.get("comentarios") for i in itens])})
    return sorted(linhas, key=lambda x: x["engajamento"] or 0, reverse=True)


def analisar(dias: int) -> dict:
    fotos = _fotos()
    if not fotos:
        return {}
    atual = fotos[-1]
    dia_atual = date.fromisoformat(atual["data"])
    inicio = dia_atual - timedelta(days=dias)
    anterior = _foto_em(fotos, inicio)
    nossos = _nossos_posts()
    posts = [_enriquecer(p, nossos) for p in atual["posts"] if p["data"] > inicio.isoformat()]

    seg_atual, seg_ant = atual.get("seguidores"), (anterior or {}).get("seguidores")
    return {
        "periodo": f"{inicio.strftime('%d/%m/%Y')} a {dia_atual.strftime('%d/%m/%Y')}",
        "dias": dias,
        "seguidores": seg_atual,
        "novos_seguidores": (seg_atual - seg_ant) if (seg_atual is not None and seg_ant is not None) else None,
        "posts": sorted(posts, key=lambda p: p["data"]),
        "qtd_posts": len(posts),
        "alcance_medio": _media([p.get("alcance") for p in posts]),
        "engajamento_medio": _media([p.get("engajamento") for p in posts]),
        "curtidas_medias": _media([p.get("curtidas") for p in posts]),
        "comentarios_medios": _media([p.get("comentarios") for p in posts]),
        "salvamentos_medios": _media([p.get("salvamentos") for p in posts]),
        "compartilhamentos_medios": _media([p.get("compartilhamentos") for p in posts]),
        "por_area": _agrupar(posts, "area"),
        "por_formato": _agrupar(posts, "formato"),
    }


def _recomendacoes(a: dict, metas: dict) -> list[str]:
    rec = []
    esperados = round(a["dias"] / 7 * 3)
    if a["qtd_posts"] < esperados:
        rec.append(f"Frequência abaixo do plano ({a['qtd_posts']} de {esperados} posts). "
                   "Constância é o fator que mais pesa no alcance: aprovar a programação no início do mês.")
    areas = [x for x in a["por_area"] if x["engajamento"] is not None and x["nome"] != "Anterior ao agente"]
    if len(areas) >= 2:
        rec.append(f"Área com melhor engajamento: **{areas[0]['nome']}** "
                   f"({_fmt(areas[0]['engajamento'], True)}). Considerar aumentar sua participação.")
        rec.append(f"Área com menor engajamento: **{areas[-1]['nome']}** "
                   f"({_fmt(areas[-1]['engajamento'], True)}). Testar ganchos e formatos diferentes.")
    formatos = [x for x in a["por_formato"] if x["engajamento"] is not None]
    if len(formatos) >= 2:
        rec.append(f"Formato com melhor resultado: **{formatos[0]['nome']}**.")
    if (a["comentarios_medios"] or 0) < metas.get("comentarios_por_post", 1):
        rec.append("Poucos comentários: encerrar posts com perguntas abertas e responder a todos "
                   "os comentários nas primeiras horas (sem dar consultoria individual).")
    if (a["salvamentos_medios"] or 0) < metas.get("salvamentos_por_post", 3):
        rec.append("Poucos salvamentos: produzir mais checklists, passo a passo e comparativos.")
    if a["novos_seguidores"] is not None and a["novos_seguidores"] < metas.get("novos_seguidores_mes", 20) * a["dias"] / 30:
        rec.append("Crescimento de seguidores abaixo da meta: reforçar o toque local (São Bernardo "
                   "do Campo e ABC), colaborações com perfis parceiros e compartilhar os posts nos stories.")
    return rec or ["Indicadores dentro das metas. Manter a estratégia atual."]


def relatorio(dias: int = 7) -> str:
    perfil = carregar_perfil()
    metas = perfil.get("kpis", {})
    a = analisar(dias)
    if not a:
        return "Ainda não há métricas coletadas. Rode `python main.py kpi-coletar`."

    def meta(valor, alvo, pct=False):
        if valor is None or alvo is None:
            return "sem dado"
        return ("✅" if valor >= alvo else "⚠️") + f" meta {_fmt(alvo, pct)}"

    tipo = "semanal" if dias <= 7 else "mensal"
    L = [f"# Relatório {tipo} de KPIs: @{perfil['advogado']['instagram'].lstrip('@')}",
         f"Período: {a['periodo']}", "",
         "## Indicadores principais", "",
         "| KPI | Resultado | Meta |", "|---|---|---|",
         f"| Seguidores | {_fmt(a['seguidores'])} | |",
         f"| Novos seguidores | {_fmt(a['novos_seguidores'])} | "
         f"{meta(a['novos_seguidores'], round(metas.get('novos_seguidores_mes', 20) * dias / 30))} |",
         f"| Posts publicados | {a['qtd_posts']} | {meta(a['qtd_posts'], round(dias / 7 * 3))} |",
         f"| Alcance médio por post | {_fmt(a['alcance_medio'])} | {meta(a['alcance_medio'], metas.get('alcance_por_post'))} |",
         f"| Taxa de engajamento média | {_fmt(a['engajamento_medio'], True)} | "
         f"{meta(a['engajamento_medio'], metas.get('engajamento_minimo'), True)} |",
         f"| Curtidas por post | {_fmt(a['curtidas_medias'])} | |",
         f"| Comentários por post | {_fmt(a['comentarios_medios'])} | {meta(a['comentarios_medios'], metas.get('comentarios_por_post'))} |",
         f"| Salvamentos por post | {_fmt(a['salvamentos_medios'])} | {meta(a['salvamentos_medios'], metas.get('salvamentos_por_post'))} |",
         f"| Compartilhamentos por post | {_fmt(a['compartilhamentos_medios'])} | |",
         "", "Taxa de engajamento = (curtidas + comentários + salvamentos + compartilhamentos) ÷ alcance.",
         "", "## Posts do período", "",
         "| Data | Título | Área | Alcance | Curt. | Com. | Salv. | Comp. | Engaj. |",
         "|---|---|---|---|---|---|---|---|---|"]
    for p in a["posts"]:
        L.append(f"| {p['data'][8:10]}/{p['data'][5:7]} | [{p['titulo'][:45]}]({p['permalink']}) | {p['area']} | "
                 f"{_fmt(p.get('alcance'))} | {_fmt(p.get('curtidas'))} | {_fmt(p.get('comentarios'))} | "
                 f"{_fmt(p.get('salvamentos'))} | {_fmt(p.get('compartilhamentos'))} | {_fmt(p.get('engajamento'), True)} |")
    for titulo, grupo in (("Desempenho por área", a["por_area"]), ("Desempenho por formato", a["por_formato"])):
        L += ["", f"## {titulo}", "", "| | Posts | Alcance médio | Engajamento | Salvamentos | Comentários |",
              "|---|---|---|---|---|---|"]
        for g in grupo:
            L.append(f"| {g['nome']} | {g['posts']} | {_fmt(g['alcance'])} | {_fmt(g['engajamento'], True)} | "
                     f"{_fmt(g['salvamentos'])} | {_fmt(g['comentarios'])} |")
    ranking = sorted([p for p in a["posts"] if p.get("engajamento") is not None],
                     key=lambda p: p["engajamento"], reverse=True)
    if ranking:
        L += ["", "## Destaques", "", "**Melhores posts:**"]
        L += [f"{i}. {p['titulo']} ({_fmt(p['engajamento'], True)})" for i, p in enumerate(ranking[:3], 1)]
    L += ["", "## Recomendações para decisão", ""]
    L += [f"- {r}" for r in _recomendacoes(a, metas)]

    ARQ_APRENDIZADOS.parent.mkdir(parents=True, exist_ok=True)
    ARQ_APRENDIZADOS.write_text(json.dumps({
        "gerado_em": hoje().isoformat(),
        "melhores_posts": [p["titulo"] for p in ranking[:3]],
        "piores_posts": [p["titulo"] for p in ranking[-2:]] if len(ranking) > 3 else [],
        "melhor_area": a["por_area"][0]["nome"] if a["por_area"] else None,
        "melhor_formato": a["por_formato"][0]["nome"] if a["por_formato"] else None,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return "\n".join(L)


def aprendizados_para_prompt() -> str:
    if not ARQ_APRENDIZADOS.exists():
        return ""
    d = json.loads(ARQ_APRENDIZADOS.read_text(encoding="utf-8"))
    partes = []
    if d.get("melhores_posts"):
        partes.append("Posts com maior engajamento (inspire-se no gancho e no formato, sem repetir o tema): "
                      + "; ".join(d["melhores_posts"]))
    if d.get("piores_posts"):
        partes.append("Posts com menor engajamento (evite abordagens parecidas): " + "; ".join(d["piores_posts"]))
    if d.get("melhor_formato"):
        partes.append(f"Formato com melhor resultado: {d['melhor_formato']}.")
    return "\n".join(partes)
