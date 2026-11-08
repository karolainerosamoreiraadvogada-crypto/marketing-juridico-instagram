"""Fila de posts: cada post é um arquivo JSON em posts/fila/ ou posts/publicados/."""
import json
from datetime import date, timedelta
from pathlib import Path

from .config import PASTA_FILA, PASTA_PUBLICADOS, hoje


def _ler(pasta: Path) -> list[dict]:
    if not pasta.exists():
        return []
    posts = []
    for arq in sorted(pasta.glob("*.json")):
        post = json.loads(arq.read_text(encoding="utf-8"))
        post["_arquivo"] = arq
        posts.append(post)
    return posts


def na_fila() -> list[dict]:
    return sorted(_ler(PASTA_FILA), key=lambda p: p["data_publicacao"])


def publicados() -> list[dict]:
    return _ler(PASTA_PUBLICADOS)


def salvar(post: dict, pasta: Path = PASTA_FILA) -> Path:
    pasta.mkdir(parents=True, exist_ok=True)
    dados = {k: v for k, v in post.items() if not k.startswith("_")}
    caminho = pasta / f"{post['id']}.json"
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    return caminho


def mover_para_publicados(post: dict) -> Path:
    novo = salvar(post, PASTA_PUBLICADOS)
    post["_arquivo"].unlink()
    return novo


def titulos_recentes(limite: int = 40) -> list[str]:
    todos = publicados() + na_fila()
    todos.sort(key=lambda p: p["data_publicacao"], reverse=True)
    return [p["titulo"] for p in todos[:limite] if p.get("titulo")]


def proximas_datas(qtd: int, dias_semana: list[int]) -> list[date]:
    """Próximas datas livres nos dias da semana configurados."""
    ocupadas = {p["data_publicacao"] for p in na_fila()}
    dia = hoje() + timedelta(days=1)
    if ocupadas:
        dia = max(dia, date.fromisoformat(max(ocupadas)) + timedelta(days=1))
    datas = []
    while len(datas) < qtd:
        if dia.weekday() in dias_semana:
            datas.append(dia)
        dia += timedelta(days=1)
    return datas


def datas_do_mes(ano: int, mes: int, dias_semana: list[int], a_partir_de: date) -> list[date]:
    """Todas as datas de publicação do mês (ex.: seg/qua/sex), a partir de uma data."""
    dia = max(date(ano, mes, 1), a_partir_de)
    ocupadas = {p["data_publicacao"] for p in na_fila()}
    datas = []
    while dia.month == mes:
        if dia.weekday() in dias_semana and dia.isoformat() not in ocupadas:
            datas.append(dia)
        dia += timedelta(days=1)
    return datas


TOLERANCIA_ATRASO_DIAS = 2


def vencidos() -> list[dict]:
    """Posts do dia (ou com até 2 dias de atraso, ex.: aprovação tardia)."""
    dia_hoje = hoje()
    limite = (dia_hoje - timedelta(days=TOLERANCIA_ATRASO_DIAS)).isoformat()
    return [p for p in na_fila() if limite <= p["data_publicacao"] <= dia_hoje.isoformat()]


def atrasados() -> list[dict]:
    """Posts que perderam a data (não são publicados sozinhos: precisam de nova data)."""
    limite = (hoje() - timedelta(days=TOLERANCIA_ATRASO_DIAS)).isoformat()
    return [p for p in na_fila() if p["data_publicacao"] < limite]
