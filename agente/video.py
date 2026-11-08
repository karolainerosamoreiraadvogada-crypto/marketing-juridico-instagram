"""Gera Reels profissionais (1080x1920, 9:16, MP4 H.264 + AAC) no estilo do perfil.

- Fundo: vídeos reais (Pexels) com zoom lento e véu vinho para leitura.
- Trilha: música (Pixabay) cortada no trecho de maior energia; cortes de cena
  caem nas batidas; efeitos sonoros (impacto e "whoosh") sintetizados.
- Texto cinético: palavras surgem no compasso, com "pop", deslizamento e fios.
- Barra de progresso no topo e respeito às áreas seguras do Reels.

Roteiro a partir do JSON do post (formato "reel"):
  titulo, subtitulo, slides[{titulo, texto, video}], chamada_final,
  video_capa, video_final, musica {arquivo, inicio, bpm}
Requer: imageio-ffmpeg e numpy (pip install imageio-ffmpeg numpy).
"""
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from .config import RAIZ, carregar_perfil
from .imagem import _hex, desenhar_titulo, fonte, paragrafo_ajustado, texto_espacado, titulo_ajustado

W, H = 1080, 1920
FPS = 30
SR = 48000
M = 90
UTIL = W - M - 150      # margem direita maior: ícones do Reels ficam à direita
TOPO = 150              # abaixo da barra de progresso
BASE = H - 400          # a parte de baixo da tela é coberta pela legenda do Reels


def _ffmpeg() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def _suave(p: float) -> float:
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3


# ------------------------------------------------------------------ elementos

class Elemento:
    """Texto ou forma já desenhado, que entra em cena com um efeito."""

    def __init__(self, img, inicio, efeito="subir", duracao=0.5, cor_texto=None, nome="", texto=""):
        caixa = img.getbbox() or (0, 0, 1, 1)
        self.img = img.crop(caixa)
        # itálico e sombra podem "vazar" para a esquerda: mantém tudo na área segura
        dx = max(0, 64 - caixa[0])
        self.caixa = (caixa[0] + dx, caixa[1], caixa[2] + dx, caixa[3])
        self.inicio, self.efeito, self.duracao = inicio, efeito, duracao
        self.cor_texto, self.nome, self.texto = cor_texto, nome, texto

    def visivel_em(self) -> float:
        return self.inicio + self.duracao

    def aplicar(self, quadro, t):
        p = _suave((t - self.inicio) / self.duracao)
        if p <= 0:
            return
        img, (x, y) = self.img, self.caixa[:2]
        if self.efeito == "subir":
            y += int(60 * (1 - p))
        elif self.efeito == "esquerda":
            x -= int(90 * (1 - p))
        elif self.efeito == "pop":  # entra levemente maior e assenta
            escala = 1 + 0.18 * (1 - p)
            if escala > 1.001:
                nw, nh = int(img.width * escala), int(img.height * escala)
                img = img.resize((nw, nh), Image.BILINEAR)
                x -= (nw - self.img.width) // 2
                y -= (nh - self.img.height) // 2
        elif self.efeito == "crescer":
            img = img.crop((0, 0, max(1, int(img.width * p)), img.height))
            p = 1.0
        if p < 1:
            img = img.copy()
            img.putalpha(img.getchannel("A").point(lambda v: int(v * p)))
        quadro.alpha_composite(img, (max(0, x), max(0, y)))


def _camada():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def _sombra(img, raio=6, opacidade=150):
    """Sombra suave atrás do texto, para leitura sobre vídeo."""
    alfa = img.getchannel("A").filter(ImageFilter.GaussianBlur(raio))
    sombra = Image.new("RGBA", img.size, (20, 10, 8, 0))
    sombra.putalpha(alfa.point(lambda v: min(opacidade, v)))
    return Image.alpha_composite(sombra, img)


# ------------------------------------------------------------------ fundos

def _trecho_mais_movimentado(arquivo: Path, dur_clipe: float, janela: float) -> float:
    """Início (s) da janela do clipe com mais movimento (diferença entre quadros)."""
    if dur_clipe <= janela + 0.2:
        return 0.0
    raw = subprocess.run([_ffmpeg(), "-v", "error", "-i", str(arquivo), "-vf", "fps=5,scale=96:170",
                          "-pix_fmt", "gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    tam = 96 * 170
    quadros = [np.frombuffer(raw[i:i + tam], np.uint8).astype(np.float32) for i in range(0, len(raw) - tam + 1, tam)]
    mov = np.array([np.abs(a - b).mean() for a, b in zip(quadros, quadros[1:])])
    passo = int(janela * 5)
    if len(mov) <= passo:
        return 0.0
    somas = np.convolve(mov, np.ones(passo), "valid")
    # penaliza janelas que tenham um trecho de 1,5 s quase parado
    minimos = np.array([np.convolve(mov[i:i + passo], np.ones(7), "valid").min() for i in range(len(somas))])
    melhor = int(np.argmax(somas + 3 * minimos))
    return melhor / 5.0

class FundoVideo:
    """Lê o clipe em 30 fps, 1080x1920, com zoom lento e véu vinho."""

    def __init__(self, arquivo: Path, duracao: float, cor_veu: str, texto_a_partir_de: float = 0.40):
        """texto_a_partir_de: fração da altura onde começa o texto; dali para baixo o
        véu fica quase opaco (contraste garantido), e acima dele o vídeo aparece."""
        import imageio_ffmpeg
        _, dur_clipe = imageio_ffmpeg.count_frames_and_secs(str(arquivo))
        # clipe mais curto que a cena: câmera lenta suave para não congelar a imagem;
        # clipe mais longo: começa no trecho com mais movimento
        lento = max(1.0, (duracao + 0.3) / max(0.5, dur_clipe))
        inicio = _trecho_mais_movimentado(arquivo, dur_clipe, duracao + 0.3) if lento == 1.0 else 0.0
        filtro = (f"setpts={lento:.4f}*PTS,fps={FPS},"
                  f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}")
        entrada = ["-ss", f"{inicio:.2f}"] if inicio > 0 else []
        self.leitor = imageio_ffmpeg.read_frames(str(arquivo), input_params=entrada,
                                                 output_params=["-vf", filtro])
        next(self.leitor)  # metadados
        self.arquivo, self.duracao, self.ultimo, self.indice = arquivo, duracao, None, -1
        r, g, b, _ = _hex(cor_veu)
        self.veu = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(self.veu)
        fim = texto_a_partir_de
        ini = max(0.17, fim - 0.10)
        for y in range(H):
            t = y / H
            visivel = 0.10                               # vídeo aparece com força
            if t < 0.095:
                op = 0.78                                # faixa do topo: assinatura legível
            elif t < 0.17:
                op = 0.78 - (0.78 - visivel) * (t - 0.095) / 0.075   # transição para o vídeo
            elif t < ini:
                op = visivel
            elif t < fim:
                op = visivel + (0.90 - visivel) * ((t - ini) / (fim - ini))  # degradê
            else:
                op = 0.90                                # área do texto
            d.line((0, y, W, y), fill=(r, g, b, int(255 * op)))

    def fechar(self):
        try:
            self.leitor.close()
        except Exception:
            pass

    def _quadro_bruto(self, i):
        while self.indice < i:
            try:
                self.ultimo = Image.frombytes("RGB", (W, H), next(self.leitor))
            except StopIteration:
                break  # clipe mais curto que a cena: mantém o último quadro
            self.indice += 1
        return self.ultimo

    def __call__(self, t):
        base = self._quadro_bruto(int(t * FPS))
        # movimento de câmera contínuo (zoom + leve subida), para a imagem nunca
        # parecer parada mesmo quando o vídeo original tem pouco movimento
        p = min(1.0, t / max(0.1, self.duracao))
        z = 1.06 + 0.18 * p
        cw, ch = W / z, H / z
        x0 = (W - cw) * (0.30 + 0.40 * p)   # deslocamento lateral suave
        y0 = (H - ch) * (0.70 - 0.40 * p)   # leve subida
        base = base.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
        return Image.alpha_composite(base.convert("RGBA"), self.veu)


class Cena:
    def __init__(self, duracao, fundo, elementos, nome=""):
        self.duracao, self.fundo, self.elementos, self.nome = duracao, fundo, elementos, nome

    def quadro(self, t):
        img = self.fundo(t)
        img = img if img.mode == "RGBA" else img.convert("RGBA")
        for e in self.elementos:
            e.aplicar(img, t)
        return img


# ------------------------------------------------------------------ roteiro

class Roteirista:
    def __init__(self, perfil, batida):
        v = perfil["visual"]
        self.adv = perfil["advogado"]
        self.escura, self.clara = v["cor_escura"], v["cor_clara"]
        self.destaque, self.destaque_clara = v["cor_destaque"], v["cor_destaque_clara"]
        self.b = batida  # duração de uma batida (s)

    def _assinatura(self):
        img, d = _camada()
        texto_espacado(d, (M, TOPO), self.adv["assinatura"], fonte("texto", 28), self.clara, 0.28)
        return Elemento(_sombra(img), 0.0, "subir", 0.4, self.clara, "assinatura", self.adv["assinatura"])

    def _rodape(self, inicio):
        img, d = _camada()
        d.line((M, BASE, M + UTIL, BASE), fill=self.destaque_clara, width=2)
        texto = f"{self.adv['nome']}  |  {self.adv['oab']}"
        d.text((M, BASE + 28), texto, font=fonte("texto", 30), fill=self.clara)
        return Elemento(_sombra(img), inicio, "subir", 0.4, self.clara, "rodape", texto)

    def capa(self, post, duracao, video):
        b, els = self.b, [self._assinatura()]
        img, d = _camada()
        y_tag = 900
        data = post.get("data_comemorativa")
        etiqueta = data["nome"] if data else post["area"]
        d.line((M, y_tag + 16, M + 70, y_tag + 16), fill=self.destaque_clara, width=4)
        texto_espacado(d, (M + 92, y_tag), etiqueta.upper(), fonte("negrito", 30), self.clara, 0.22)
        els.append(Elemento(_sombra(img), 0.0, "esquerda", 0.35, self.clara, "etiqueta", etiqueta))
        if data:
            # selo de calendário acima da etiqueta: dia grande em itálico e mês espaçado
            img, d = _camada()
            f_dia = fonte("italico", 170)
            caixa = d.textbbox((0, 0), data["dia"], font=f_dia)
            y_dia = y_tag - 50 - caixa[3]  # números terminam 50 px acima da etiqueta
            d.text((M - 6, y_dia), data["dia"], font=f_dia, fill=self.clara)
            f_mes = fonte("negrito", 32)
            texto_espacado(d, (M + caixa[2] + 24, y_dia + caixa[3] - f_mes.size - 8), data["mes"].upper(),
                           f_mes, self.clara, 0.3)
            els.append(Elemento(_sombra(img, 8, 170), 0.0, "pop", 0.4, self.clara, "data",
                                f"{data['dia']} {data['mes']}"))

        # título linha a linha, no compasso da música
        tam, linhas, _ = titulo_ajustado(post["titulo"], UTIL, 430, 132, 90, 1.06)
        y = 990
        for i, linha in enumerate(linhas):
            img, d = _camada()
            desenhar_titulo(d, M, y, tam, [linha], self.clara, self.destaque_clara, 1.06)
            texto = "".join((p if (k == 0 or col) else " " + p) for k, (p, _, col) in enumerate(linha))
            els.append(Elemento(_sombra(img, 8, 170), self.b * 0.5 * i, "pop", 0.35, self.clara,
                                f"titulo{i}", texto))
            y += int(tam * 1.06)
        if post.get("subtitulo"):
            img, d = _camada()
            # o espaçamento entre letras (8%) alarga a linha: quebra numa largura menor
            f, ls = paragrafo_ajustado(post["subtitulo"].upper(), "negrito", int(UTIL / 1.12), 140, 36, 28, 1.45)
            y += 50
            for linha in ls:
                texto_espacado(d, (M, y), linha, f, self.clara, 0.08)
                y += int(f.size * 1.45)
            els.append(Elemento(_sombra(img), self.b * 0.5 * len(linhas) + 0.1, "subir", 0.4, self.clara,
                                "subtitulo", post["subtitulo"]))
        # com selo de data, o véu escurece mais cedo para o dia e o mês ficarem legíveis
        return Cena(duracao, FundoVideo(video, duracao, self.escura, 0.34 if data else 0.46), els, "capa")

    def slide(self, post, n, total, slide, duracao, video):
        b, els = self.b, [self._assinatura()]
        img, d = _camada()
        texto_espacado(d, (W - 150, TOPO), f"{n:02d}/{total:02d}", fonte("negrito", 28),
                       self.clara, 0.2, ancora_direita=True)
        els.append(Elemento(_sombra(img), 0.0, "subir", 0.3, self.clara, "contador"))

        tam, linhas, alt_t = titulo_ajustado(slide["titulo"], UTIL, 300, 104, 70, 1.05)
        f, ls = paragrafo_ajustado(slide["texto"], "texto", UTIL, 420, 46, 36, 1.45)
        alt_txt = int(len(ls) * f.size * 1.45)
        y = BASE - 60 - alt_txt - 60 - 40 - alt_t - 250   # bloco ancorado acima do rodapé
        y_bloco = y

        img, d = _camada()
        d.text((M - 8, y), f"{n:02d}", font=fonte("titulo", 230), fill=self.clara)
        els.append(Elemento(_sombra(img, 10, 160), 0.0, "pop", 0.3, self.clara, "numero"))
        y += 250
        img, d = _camada()
        y = desenhar_titulo(d, M, y, tam, linhas, self.clara, self.destaque_clara, 1.05)
        els.append(Elemento(_sombra(img, 8, 170), b * 0.5, "subir", 0.4, self.clara, "titulo", slide["titulo"]))
        y += 40
        img, d = _camada()
        d.line((M, y, M + 160, y), fill=self.destaque_clara, width=5)
        els.append(Elemento(img, b * 0.9, "crescer", 0.4, None, "fio"))
        y += 60
        img, d = _camada()
        for linha in ls:
            d.text((M, y), linha, font=f, fill=self.clara)
            y += int(f.size * 1.45)
        els.append(Elemento(_sombra(img, 6, 190), b * 1.2, "subir", 0.5, self.clara, "texto", slide["texto"]))
        els.append(self._rodape(b * 1.5))
        return Cena(duracao, FundoVideo(video, duracao, self.escura, (y_bloco - 40) / H), els, f"sinal{n}")

    def encerramento(self, post, duracao, video):
        b, els = self.b, [self._assinatura()]
        frase = post.get("chamada_final") or "Ficou com alguma dúvida?"
        tam, linhas, _ = titulo_ajustado(f"*{frase}*", UTIL, 470, 100, 70, 1.1)
        y = 700
        img, d = _camada()
        y = desenhar_titulo(d, M, y, tam, linhas, self.clara, self.clara, 1.1)
        els.append(Elemento(_sombra(img, 8, 180), 0.0, "subir", 0.5, self.clara, "frase", frase))
        y += 60
        img, d = _camada()
        d.line((M, y, M + 160, y), fill=self.destaque_clara, width=5)
        els.append(Elemento(img, b * 0.8, "crescer", 0.4, None, "fio"))
        y += 70
        chamadas = ("SALVE PARA CONSULTAR DEPOIS", "ENVIE PARA QUEM PRECISA",
                    f"SIGA {self.adv['instagram'].upper()}")
        for i, linha in enumerate(chamadas):
            cor = self.clara
            img, d = _camada()
            texto_espacado(d, (M, y), linha, fonte("negrito", 34), cor, 0.12)
            els.append(Elemento(_sombra(img), b * (1.2 + 0.5 * i), "esquerda", 0.35, cor, f"cta{i}", linha))
            y += 70
        els.append(self._rodape(b * 1.2))
        return Cena(duracao, FundoVideo(video, duracao, self.escura, 660 / H), els, "encerramento")


def _resolver(caminho):
    p = Path(caminho)
    return p if p.is_absolute() else RAIZ / p


def montar_roteiro(post, perfil):
    batida = 60.0 / float(post["musica"]["bpm"])
    r = Roteirista(perfil, batida)
    slides = post["slides"]
    capa = {"titulo": post["titulo"], "texto": post.get("subtitulo", "")}
    cenas = [r.capa(post, _duracao_leitura(capa, batida), _resolver(post["video_capa"]))]
    for i, s in enumerate(slides, start=1):
        cenas.append(r.slide(post, i, len(slides), s, _duracao_leitura(s, batida), _resolver(s["video"])))
    chamadas = "salve para consultar depois envie para quem precisa siga " + perfil["advogado"]["instagram"]
    final = {"titulo": post.get("chamada_final", ""), "texto": chamadas}
    cenas.append(r.encerramento(post, _duracao_leitura(final, batida), _resolver(post["video_final"])))
    return cenas, batida


def fechar_roteiro(cenas):
    for c in cenas:
        if hasattr(c.fundo, "fechar"):
            c.fundo.fechar()


LEITURA_PALAVRAS_S = 3.0  # leitura confortável no celular


def _duracao_leitura(slide, batida):
    """Entrada do texto (~1,7 batida) + leitura + 1 s de respiro, arredondado na batida."""
    palavras = len(slide["titulo"].split()) + len(slide["texto"].split())
    necessario = batida * 1.7 + palavras / LEITURA_PALAVRAS_S + 1.0
    return batida * int(np.ceil(necessario / batida))


# ------------------------------------------------------------------ áudio

def _ruido_filtrado(n, rng, suave):
    x = rng.standard_normal(n).astype(np.float32)
    return np.convolve(x, np.ones(suave, np.float32) / suave, "same")


def _impacto(rng):
    n = int(SR * 1.2)
    t = np.arange(n) / SR
    freq = 55 + 70 * np.exp(-t * 18)
    grave = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-t * 3.2)
    estalo = _ruido_filtrado(n, rng, 6) * np.exp(-t * 40) * 0.6
    return (grave * 0.9 + estalo).astype(np.float32)


def _whoosh(rng, dur=0.45):
    n = int(SR * dur)
    t = np.linspace(0, 1, n)
    env = np.sin(np.pi * t) ** 2
    mistura = _ruido_filtrado(n, rng, 40) * (1 - t) + _ruido_filtrado(n, rng, 4) * t
    return (mistura * env * 3.0).astype(np.float32)


def _somar(destino, sinal, inicio_s, ganho):
    i = int(inicio_s * SR)
    trecho = sinal[: max(0, min(len(sinal), len(destino) - i))]
    destino[i:i + len(trecho)] += trecho * ganho


def montar_audio(post, cortes, duracao, destino: Path):
    """Música (trecho de impacto) + impactos nos cortes + whoosh antes dos cortes."""
    musica = post["musica"]
    raw = subprocess.run([_ffmpeg(), "-v", "error", "-ss", str(musica["inicio"]), "-t", str(duracao + 0.5),
                          "-i", str(_resolver(musica["arquivo"])), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    mus = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
    n = int(duracao * SR)
    if len(mus) < n:
        mus = np.vstack([mus, np.zeros((n - len(mus), 2), np.float32)])
    mus = mus[:n]
    fade_in, fade_out = int(0.08 * SR), int(1.8 * SR)
    mus[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    mus[-fade_out:] *= (np.linspace(1, 0, fade_out) ** 1.5)[:, None]

    efeitos = np.zeros(n, np.float32)
    rng = np.random.default_rng(7)
    impacto = _impacto(rng)
    for t in [0.0] + cortes:
        _somar(efeitos, impacto, t, 0.55)
    for t in cortes:
        _somar(efeitos, _whoosh(rng), t - 0.42, 0.25)

    mix = mus * 0.85 + efeitos[:, None]
    pico = float(np.abs(mix).max())
    if pico > 0:
        mix *= 0.89 / pico  # pico em -1 dBFS, sem distorção
    pcm = (np.clip(mix, -1, 1) * 32767).astype("<i2")
    with wave.open(str(destino), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ------------------------------------------------------------------ render

def gerar_video(post: dict, pasta: Path, perfil: dict | None = None):
    """Renderiza o Reels. Retorna (mp4, capa.jpg, cenas); as cenas servem aos testes."""
    perfil = perfil or carregar_perfil()
    pasta.mkdir(parents=True, exist_ok=True)
    saida, capa = pasta / f"{post['id']}.mp4", pasta / f"{post['id']}_capa.jpg"
    audio = pasta / f"{post['id']}_audio.wav"
    cenas, _ = montar_roteiro(post, perfil)
    duracao = sum(c.duracao for c in cenas)
    cortes, t = [], 0.0
    for c in cenas[:-1]:
        t += c.duracao
        cortes.append(t)
    montar_audio(post, cortes, duracao, audio)

    cmd = [_ffmpeg(), "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", str(audio), "-map", "0:v", "-map", "1:a", "-shortest",
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-level", "4.1",
           "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-movflags", "+faststart", str(saida)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    barra = _hex(perfil["visual"]["cor_destaque_clara"])[:3]
    quadros_cena = [int(round(c.duracao * FPS)) for c in cenas]
    total_q, q_global = sum(quadros_cena), 0
    for i, cena in enumerate(cenas):
        for q in range(quadros_cena[i]):
            t = q / FPS
            img = cena.quadro(t)
            if i > 0 and t < 0.25:  # "soco" de zoom e clarão curto em cada corte
                z = 1.05 - 0.05 * _suave(t / 0.25)
                cw, ch = int(W / z), int(H / z)
                x0, y0 = (W - cw) // 2, (H - ch) // 2
                img = img.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
                if t < 0.1:
                    img = Image.alpha_composite(img, Image.new("RGBA", (W, H), (255, 245, 235, int(70 * (1 - t / 0.1)))))
            d = ImageDraw.Draw(img)
            d.rectangle((0, 0, W, 8), fill=(0, 0, 0, 90))
            d.rectangle((0, 0, int(W * (q_global + 1) / total_q), 8), fill=barra)
            rgb = img.convert("RGB")
            if i == 0 and q == int(2.4 * FPS):
                rgb.save(capa, "JPEG", quality=92)
            proc.stdin.write(rgb.tobytes())
            q_global += 1
    proc.stdin.close()
    proc.wait()
    fechar_roteiro(cenas)
    audio.unlink(missing_ok=True)
    if proc.returncode != 0:
        raise RuntimeError("Falha ao gerar o vídeo (ffmpeg).")
    return saida, capa, cenas
