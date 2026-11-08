"""Revisão em 10 etapas (skills/marketing-juridico/references/checklist_10_etapas.md).

Um segundo agente, só com papel de revisor, relê o post etapa por etapa, corrige o
que encontrar e, se houve correção, a revisão recomeça da etapa 1. Ao final, o
filtro de termos vedados (compliance.py) roda mais uma vez.
"""
import json

from . import compliance, llm
from .config import carregar_skill

ETAPAS = [
    "Ética OAB: vedações",
    "Ética OAB: tom",
    "Exatidão jurídica",
    "Fontes",
    "Prazos, valores e requisitos",
    "Ortografia",
    "Gramática e norma culta",
    "Clareza",
    "Coerência entre peças",
    "Acabamento (tamanho dos textos)",
]

CAMPOS = ("titulo", "subtitulo", "slides", "chamada_final", "legenda", "hashtags", "fontes")

PROMPT_REVISOR = """Você é revisor(a) jurídico(a) e de língua portuguesa, rigoroso(a) ao extremo.
Não cria conteúdo novo: revisa e corrige o post recebido seguindo a skill abaixo,
em especial "Revisão em 10 etapas" e "Ética da OAB".

Regras:
- Execute as 10 etapas, uma a uma, relendo o post inteiro em cada uma.
- Qualquer afirmação jurídica que não esteja amparada nas tabelas de base legal e
  jurisprudência da skill deve ser removida ou reescrita sem número de lei/julgado.
- Na dúvida sobre um dado, retire o dado.
- Limites de tamanho: título até 8 palavras; título de slide até 6; texto de slide
  até 45 palavras; legenda de 80 a 180 palavras.
- Nunca use travessões (—).

Responda SOMENTE com JSON:
{
  "etapas": [{"n": 1, "ok": true, "obs": "o que foi verificado ou corrigido"}, ... 10 itens],
  "houve_correcao": true | false,
  "post": { ...o post completo, já corrigido, com os mesmos campos recebidos... }
}
"""


def _extrair(post: dict) -> dict:
    return {k: post[k] for k in CAMPOS if k in post} | {"area": post.get("area"),
                                                        "formato": post.get("formato")}


def revisar(post: dict, max_rodadas: int = 3) -> dict:
    """Revisa e corrige o post. Retorna o post atualizado com o campo "revisao"."""
    sistema = PROMPT_REVISOR + "\n\n---\n\n" + carregar_skill()
    historico = []
    atual = _extrair(post)

    alertas = compliance.verificar_post(atual)
    for rodada in range(1, max_rodadas + 1):
        pedido = "Revise este post:\n" + json.dumps(atual, ensure_ascii=False)
        if alertas:
            pedido += ("\n\nO filtro automático da OAB encontrou estes problemas, que "
                       "DEVEM ser eliminados: " + "; ".join(alertas))
        resp = llm.gerar_json(sistema, pedido)
        etapas = resp.get("etapas", [])
        atual = {**atual, **{k: v for k, v in resp.get("post", {}).items() if k in CAMPOS}}
        todas_ok = len(etapas) == 10 and all(e.get("ok") for e in etapas)
        historico.append({"rodada": rodada, "etapas": etapas})
        alertas = compliance.verificar_post(atual)
        # Se corrigiu algo (ou o filtro ainda acusa problema), recomeça do zero
        if todas_ok and not resp.get("houve_correcao") and not alertas:
            break

    post.update({k: v for k, v in atual.items() if k in CAMPOS})
    alertas = compliance.verificar_post(post)
    ultima = historico[-1]["etapas"] if historico else []
    aprovado = (len(ultima) == 10 and all(e.get("ok") for e in ultima) and not alertas)
    post["revisao"] = {
        "aprovado_pelo_revisor": aprovado,
        "rodadas": len(historico),
        "etapas": [
            {"etapa": ETAPAS[i], "ok": bool(e.get("ok")), "obs": e.get("obs", "")}
            for i, e in enumerate(ultima[:10])
        ],
        "alertas_oab": alertas,
    }
    return post


def resumo(post: dict) -> str:
    r = post.get("revisao", {})
    marcas = " ".join(f"{i + 1}{'✅' if e['ok'] else '❌'}" for i, e in enumerate(r.get("etapas", [])))
    status = "APROVADO pelo revisor" if r.get("aprovado_pelo_revisor") else "⚠️ REQUER ATENÇÃO"
    return f"Revisão 10 etapas ({r.get('rodadas', 0)} rodada(s)): {marcas} | {status}"
