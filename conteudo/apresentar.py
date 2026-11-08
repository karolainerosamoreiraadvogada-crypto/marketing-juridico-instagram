"""Monta a pasta de aprovação no Windows (Imagens > Programação AAAA-MM) com uma
subpasta por publicação e uma página "Programação.html" com o calendário completo.

  python -m conteudo.apresentar 2026-10
  python -m conteudo.apresentar datas 2026-11 2026-12 2027-01   (só datas comemorativas e estações,
                                                                 com o calendário anual)
"""
import html
import json
import shutil
import sys
from datetime import date
from pathlib import Path

from agente.config import PASTA_FILA, RAIZ

DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
MESES = ["", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
         "outubro", "novembro", "dezembro"]
FORMATO = {"carrossel": "Carrossel", "reel": "Reels animado", "stories": "Stories", "card": "Card"}


def _pasta_imagens() -> Path:
    import ctypes.wintypes
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, 39, None, 0, buf)  # CSIDL_MYPICTURES
    return Path(buf.value)


def _calendario_anual(ano: int) -> str:
    from conteudo.calendario import datas
    linhas = "".join(
        f"<tr><td>{d['data'].strftime('%d/%m')}</td><td>{DIAS[d['data'].weekday()]}</td>"
        f"<td>{html.escape(d['nome'])}</td><td>{FORMATO[d['formato']]}</td><td>{html.escape(d['area'])}</td>"
        f"<td>{html.escape(d['ideia'])}</td></tr>" for d in datas(ano))
    return (f"<h2>Calendário anual de {ano}: estações e datas comemorativas</h2>"
            "<table><tr><th>Data</th><th>Dia</th><th>Ocasião</th><th>Formato</th><th>Área</th><th>Ideia</th></tr>"
            f"{linhas}</table>")


def montar(mes: str, meses: list[str] | None = None) -> Path:
    """mes = "AAAA-MM" (programação do mês) ou "datas" (só datas comemorativas dos meses indicados)."""
    so_datas = mes == "datas"
    if so_datas:
        ano, m = (int(x) for x in meses[-1].split("-"))
        destino = _pasta_imagens() / "Datas Comemorativas e Estações"
        arquivos = [a for mm in meses for a in sorted(PASTA_FILA.glob(f"{mm}-*.json"))]
    else:
        ano, m = (int(x) for x in mes.split("-"))
        destino = _pasta_imagens() / f"Programação {MESES[m].capitalize()} {ano}"
        arquivos = sorted(PASTA_FILA.glob(f"{mes}-*.json"))
    destino.mkdir(parents=True, exist_ok=True)
    posts = [json.loads(a.read_text(encoding="utf-8")) for a in arquivos]
    if so_datas:
        posts = [p for p in posts if p.get("data_comemorativa")]
    blocos, linhas_tabela = [], []
    for p in posts:
        d = date.fromisoformat(p["data_publicacao"])
        hora = p.get("horario") or ("14h" if p["formato"] == "stories" else "21h")
        titulo = (p.get("titulo") or p["quadros"][0]["titulo"]).replace("*", "")
        ocasiao = p.get("data_comemorativa", {}).get("nome")
        nome = f"{d.strftime('%d-%m')} {DIAS[d.weekday()]} - {FORMATO[p['formato']]}"
        if ocasiao:
            nome = f"{d.strftime('%Y-%m-%d')} {ocasiao} - {FORMATO[p['formato']]}"
        pasta = destino / nome
        pasta.mkdir(exist_ok=True)
        midias = []
        if p["formato"] == "reel":
            shutil.copy2(RAIZ / p["video"], pasta / "Reels.mp4")
            midias.append(("video", "Reels.mp4"))
        for i, img in enumerate(p.get("imagens", []), start=1):
            if p["formato"] == "reel":
                break
            nome_img = f"{'Tela' if p['formato'] == 'stories' else 'Lamina'} {i:02d}.jpg"
            shutil.copy2(RAIZ / img, pasta / nome_img)
            midias.append(("img", nome_img))
        legenda = (p.get("legenda", "") + "\n\n" + " ".join(p.get("hashtags", []))).strip()
        if legenda:
            (pasta / "Legenda.txt").write_text(legenda, encoding="utf-8-sig")

        testes = p.get("testes_video", {}).get("resultado")
        selo = f"Testes do vídeo: {testes}" if testes else "Revisão em 10 etapas ✔"
        linhas_tabela.append(
            f"<tr><td>{d.strftime('%d/%m/%Y')}</td><td>{DIAS[d.weekday()]}</td><td>{hora}</td>"
            f"<td>{FORMATO[p['formato']]}</td><td>{html.escape(ocasiao or p['area'])}</td>"
            f"<td>{html.escape(titulo)}</td></tr>")
        galeria = "".join(
            f'<video src="{html.escape(nome)}/{f}" controls preload="metadata"></video>' if t == "video"
            else f'<img src="{html.escape(nome)}/{html.escape(f)}" loading="lazy">' for t, f in midias)
        fontes = "".join(f"<li>{html.escape(f)}</li>" for f in p.get("fontes", []))
        blocos.append(
            f'<section><h2>{d.strftime("%d/%m/%Y")} · {DIAS[d.weekday()]} · {hora} · {FORMATO[p["formato"]]}'
            + (f" · {html.escape(ocasiao)}" if ocasiao else "") + '</h2>'
            f'<p class="area">{html.escape(p["area"])} · <b>{html.escape(titulo)}</b> · <span class="ok">{selo}</span></p>'
            f'<div class="galeria {p["formato"]}">{galeria}</div>'
            + (f'<details><summary>Legenda</summary><pre>{html.escape(legenda)}</pre></details>' if legenda else "")
            + f'<details><summary>Fontes conferidas</summary><ul>{fontes}</ul></details></section>')

    if so_datas:
        titulo_pag = "Datas comemorativas e estações do ano"
        sub = ("O post comemorativo sai no próprio dia da data, às 21h. Em segunda, quarta ou sexta, "
               "ocupa o post do dia; nos outros dias, é um post extra.")
        extra = _calendario_anual(ano)
    else:
        titulo_pag = f"Programação de {MESES[m]} de {ano}"
        sub = "Feed: segunda, quarta e sexta, às 21h · Stories: sábado, às 14h"
        extra = ""
    pagina = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{titulo_pag}</title>
<style>
:root{{--vinho:#3E231D;--terracota:#A8553F;--creme:#F3EADB;--areia:#E4D5BF}}
body{{margin:0;background:var(--creme);color:#2E1B16;font:16px/1.5 Georgia,serif}}
header{{background:var(--vinho);color:var(--creme);padding:28px 24px}}
header h1{{margin:0;font-weight:500}} header p{{margin:6px 0 0;opacity:.85}}
main{{max-width:1100px;margin:auto;padding:16px}}
table{{width:100%;border-collapse:collapse;background:#fff;margin:16px 0 32px}}
td,th{{padding:8px 10px;border-bottom:1px solid var(--areia);text-align:left;font-size:14px}}
th{{background:var(--areia)}}
section{{background:#fff;border-radius:10px;padding:16px;margin:18px 0;box-shadow:0 1px 3px #0001}}
h2{{margin:0 0 4px;color:var(--terracota);font-weight:500}}
.area{{margin:0 0 10px}} .ok{{color:#2f6b3a}}
.galeria{{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px}}
.galeria img{{height:300px;border-radius:6px}} .galeria video{{height:420px;border-radius:6px;background:#000}}
.stories img{{height:360px}}
pre{{white-space:pre-wrap;font:14px/1.5 system-ui,sans-serif;background:var(--creme);padding:10px;border-radius:6px}}
summary{{cursor:pointer;color:var(--terracota);margin-top:8px}}
</style></head><body>
<header><h1>{titulo_pag}</h1>
<p>Dirciléia Pacheco · @dircileiaaparecida_adv · {sub}</p></header>
<main><table><tr><th>Data</th><th>Dia</th><th>Hora</th><th>Formato</th><th>{'Ocasião' if so_datas else 'Área'}</th><th>Tema</th></tr>
{''.join(linhas_tabela)}</table>{''.join(blocos)}{extra}</main></body></html>"""
    (destino / "Programação.html").write_text(pagina, encoding="utf-8")
    return destino


if __name__ == "__main__":
    print(montar(sys.argv[1], sys.argv[2:]))
