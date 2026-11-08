"""Análise automática de trilhas: acha o trecho de impacto e o andamento (BPM).

O Reels começa exatamente na "entrada forte" da música (o ponto em que a energia
salta), e os cortes de cena são calculados em múltiplos da batida.
"""
import subprocess
from pathlib import Path

import numpy as np

SR = 22050
HOP = 256


def _carregar(arquivo: Path) -> np.ndarray:
    import imageio_ffmpeg
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(arquivo), "-ac", "1",
                          "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def analisar(arquivo: Path, duracao: float) -> dict:
    """Retorna {"inicio": s, "bpm": x, "salto": razão de energia} para um vídeo de `duracao` s."""
    x = _carregar(arquivo)
    n = len(x) // HOP
    fps = SR / HOP
    rms = np.sqrt((x[:n * HOP].reshape(n, HOP) ** 2).mean(1))
    total = n / fps
    janela = int(2 * fps)
    media = np.convolve(rms, np.ones(janela) / janela, "same")

    # candidato: instante em que a energia dos 2 s seguintes mais supera a dos 2 s anteriores,
    # deixando música suficiente depois para o vídeo inteiro
    melhor, melhor_val = int(1 * fps), -1.0
    limite = int((total - duracao - 0.5) * fps)
    for i in range(janela, max(janela + 1, limite), 4):
        depois = media[min(n - 1, i + janela // 2)]
        antes = media[max(0, i - janela // 2)]
        sustentado = rms[i:i + int(duracao * fps)].mean()  # energia ao longo do vídeo
        val = (depois / (antes + 1e-4)) * sustentado
        if val > melhor_val:
            melhor, melhor_val = i, val
    # ajuste fino: o pico de ataque (onset) mais forte em ±0,5 s
    onset = np.maximum(0, np.diff(rms, prepend=rms[0]))
    a, b = max(0, melhor - int(0.5 * fps)), min(n, melhor + int(0.5 * fps))
    inicio_i = a + int(np.argmax(onset[a:b]))

    # andamento: autocorrelação do onset no trecho usado
    seg = onset[inicio_i:inicio_i + int(min(duracao, 25) * fps)]
    o = seg - seg.mean()
    ac = np.correlate(o, o, "full")[len(o) - 1:]
    lags = np.arange(len(ac)) / fps
    m = (lags > 0.40) & (lags < 0.95)  # 63 a 150 BPM
    periodo = lags[m][int(np.argmax(ac[m]))]
    antes = rms[max(0, inicio_i - int(fps)):inicio_i].mean()
    depois = rms[inicio_i:inicio_i + int(fps)].mean()
    return {"inicio": round(float(inicio_i / fps), 3), "bpm": round(float(60 / periodo), 2),
            "salto": round(float(depois / (antes + 1e-4)), 1)}
