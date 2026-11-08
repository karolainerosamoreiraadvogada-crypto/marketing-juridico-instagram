"""Bateria de 10 testes automáticos de qualidade para Reels.

O vídeo só é entregue para aprovação com os 10 testes aprovados. Se algum
falhar, o problema é corrigido e a bateria inteira é executada de novo.

 1. Formato técnico exigido pelo Instagram (H.264, yuv420p, 1080x1920, 30 fps, AAC 48 kHz)
 2. Duração (15 a 90 s) e coerência com o roteiro
 3. Áudio presente e audível
 4. Áudio sem distorção (pico abaixo de -0,5 dBFS)
 5. Sem silêncio inesperado no meio do vídeo
 6. Sem quadros pretos ou imagem congelada
 7. Textos: idênticos ao roteiro, ética da OAB, sem travessão nem espaço duplo
 8. Legibilidade: contraste mínimo de 4,5:1 entre texto e fundo (WCAG)
 9. Áreas seguras do Reels (nada sob os botões ou sob a legenda)
10. Tempo de leitura suficiente em cada cena
"""
import re
import subprocess
from pathlib import Path

import numpy as np

from . import compliance
from .imagem import _hex
from .video import BASE, FPS, H, SR, W, _ffmpeg

LEITURA = 3.0  # palavras por segundo


def _analise_ffmpeg(arquivo: Path) -> str:
    cmd = [_ffmpeg(), "-hide_banner", "-i", str(arquivo),
           "-af", "volumedetect,silencedetect=noise=-50dB:d=0.7",
           "-vf", "blackdetect=d=0.2:pix_th=0.08,freezedetect=n=0.002:d=1.2",
           "-f", "null", "-"]
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore").stderr


def _lum(rgb) -> float:
    def c(v):
        v = v / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)


def _contraste(a, b) -> float:
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def testar(arquivo: Path, post: dict, cenas: list) -> list:
    r = []
    info = _analise_ffmpeg(arquivo)
    dur_roteiro = sum(c.duracao for c in cenas)

    # 1. formato técnico
    v = re.search(r"Video: h264 \((\w+)\).*?yuv420p.*?(\d+)x(\d+).*?([\d.]+) fps", info)
    a = re.search(r"Audio: aac.*?(\d+) Hz, (stereo|mono)", info)
    with open(arquivo, "rb") as f:
        inicio = f.read(200_000)
    faststart = inicio.find(b"moov") != -1 and (inicio.find(b"mdat") == -1 or inicio.find(b"moov") < inicio.find(b"mdat"))
    ok = bool(v and a and v.group(1) == "High" and (v.group(2), v.group(3)) == (str(W), str(H))
              and abs(float(v.group(4)) - FPS) < 0.01 and a.group(1) == str(SR) and faststart)
    r.append((1, "Formato técnico (H.264 High, 1080x1920, 30 fps, AAC 48 kHz, faststart)", ok,
              f"vídeo={v.groups() if v else None} áudio={a.groups() if a else None} faststart={faststart}"))

    # 2. duração
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    dur = int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3)) if d else 0
    r.append((2, "Duração entre 15 e 90 s e igual ao roteiro", 15 <= dur <= 90 and abs(dur - dur_roteiro) < 0.25,
              f"{dur:.2f} s (roteiro {dur_roteiro:.2f} s)"))

    # 3 e 4. volume
    media = re.search(r"mean_volume: (-?[\d.]+) dB", info)
    pico = re.search(r"max_volume: (-?[\d.]+) dB", info)
    media = float(media.group(1)) if media else -99
    pico = float(pico.group(1)) if pico else 0
    r.append((3, "Áudio presente e audível (média acima de -30 dB)", media > -30, f"média {media} dB"))
    r.append((4, "Áudio sem distorção (pico até -0,5 dB)", pico <= -0.5, f"pico {pico} dB"))

    # 5. silêncio inesperado (ignora o final, que tem fade-out)
    silencios = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", info)]
    indevidos = [s for s in silencios if s < dur - 2.0]
    r.append((5, "Sem silêncio inesperado no meio do vídeo", not indevidos, f"silêncios em {indevidos or 'nenhum'}"))

    # 6. pretos / congelados
    pretos = re.findall(r"black_start:([\d.]+)", info)
    congelados = re.findall(r"freeze_start: ([\d.]+)", info)
    r.append((6, "Sem quadros pretos nem imagem congelada", not pretos and not congelados,
              f"pretos={pretos or 'nenhum'} congelados={congelados or 'nenhum'}"))

    # 7. textos
    textos_tela = [e.texto for c in cenas for e in c.elementos if e.texto]
    fonte_roteiro = " ".join([post["titulo"].replace("*", ""), post.get("subtitulo", ""), post.get("chamada_final", ""),
                              post["area"]] + [s["titulo"] + " " + s["texto"] for s in post["slides"]])
    if post.get("data_comemorativa"):
        dc = post["data_comemorativa"]
        fonte_roteiro += f" {dc['nome']} {dc['dia']} {dc['mes']}"
    fora_do_roteiro = [t for t in textos_tela
                       if t.replace("*", "") not in fonte_roteiro
                       and not re.search(r"pacheco|salve|envie|siga|@", t, re.I)]
    todos = "\n".join(textos_tela + [post["legenda"]])
    alertas = compliance.verificar(todos)
    duplos = "  " in todos.replace("  |  ", " | ")
    ok = not fora_do_roteiro and not alertas and not duplos and "—" not in todos
    r.append((7, "Textos idênticos ao roteiro, ética OAB, sem travessão/espaço duplo", ok,
              f"fora do roteiro={fora_do_roteiro or 'nenhum'} alertas={alertas or 'nenhum'} espaço duplo={duplos}"))

    # 8 e 9. contraste e área segura (no momento em que cada texto está visível)
    piores, fora = [], []
    for c in cenas:
        amostras = []
        for e in c.elementos:
            x0, y0, x1, y1 = e.caixa
            if not (60 <= x0 and x1 <= W - 120 and y0 >= 100 and y1 <= H - 320):
                fora.append(f"{c.nome}/{e.nome} {e.caixa}")
            if e.cor_texto and e.nome != "fio":
                for frac in (0.0, 0.5, 1.0):
                    t = min(c.duracao - 1 / FPS, e.visivel_em() + frac * max(0, c.duracao - e.visivel_em() - 0.1))
                    amostras.append((t, e))
        menores = {}
        for t, e in sorted(amostras, key=lambda x: x[0]):  # o fundo em vídeo só avança no tempo
            fundo = np.asarray(c.fundo(t).convert("RGB").crop(e.caixa)).reshape(-1, 3)
            claro = np.percentile(fundo, 90, axis=0)  # parte mais clara do fundo atrás do texto
            menores[e.nome] = min(menores.get(e.nome, 99.0), _contraste(_hex(e.cor_texto)[:3], claro))
        for e in c.elementos:
            if e.nome in menores:
                limite = 3.0 if (e.caixa[3] - e.caixa[1]) > 80 else 4.5  # textos grandes: 3:1 (WCAG)
                if menores[e.nome] < limite:
                    piores.append(f"{c.nome}/{e.nome} {menores[e.nome]:.1f}:1 (mín {limite})")
    r.append((8, "Legibilidade: contraste texto x fundo (WCAG)", not piores, f"abaixo do mínimo: {piores or 'nenhum'}"))
    r.append((9, "Textos dentro das áreas seguras do Reels", not fora, f"fora: {fora or 'nenhum'}"))

    # 10. tempo de leitura
    curtos = []
    for c in cenas:
        palavras = sum(len(e.texto.split()) for e in c.elementos
                       if e.texto and e.nome not in ("assinatura", "rodape", "etiqueta", "data"))
        ultimo = max((e.visivel_em() for e in c.elementos), default=0)
        disponivel = c.duracao - ultimo + (ultimo * 0.5)  # lê enquanto o texto entra
        if palavras and disponivel < palavras / LEITURA:
            curtos.append(f"{c.nome}: {disponivel:.1f}s para {palavras} palavras")
    r.append((10, "Tempo de leitura suficiente em cada cena", not curtos, f"curtos: {curtos or 'nenhum'}"))
    return r


def relatorio(resultados: list) -> str:
    linhas = []
    for n, nome, ok, detalhe in resultados:
        linhas.append(f"{'✅' if ok else '❌'} {n:2d}. {nome}\n      {detalhe}")
    total = sum(1 for _, _, ok, _ in resultados if ok)
    linhas.append(f"\nResultado: {total}/10 aprovados")
    return "\n".join(linhas)
