"""Gera as lâminas dos posts (1080x1350, 4:5) no estilo do perfil.

Capa: foto em tela cheia + degradê vinho + título em Bodoni Moda.
Internas: fundo creme, número em terracota, texto em Montserrat.
Encerramento: fundo vinho, pergunta em itálico.

No título, palavras entre *asteriscos* saem em itálico na cor de destaque.
"""
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from .config import RAIZ
from .fotos import obter_foto

LARGURA, ALTURA = 1080, 1350
MARGEM = 90
UTIL = LARGURA - 2 * MARGEM

FONTES = {
    "titulo": ["assets/fonts/titulo.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
               "C:/Windows/Fonts/georgiab.ttf"],
    "italico": ["assets/fonts/titulo_italico.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
                "C:/Windows/Fonts/georgiai.ttf"],
    "texto": ["assets/fonts/texto.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "C:/Windows/Fonts/arial.ttf"],
    "leve": ["assets/fonts/texto_leve.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "C:/Windows/Fonts/arial.ttf"],
    "negrito": ["assets/fonts/texto_negrito.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "C:/Windows/Fonts/arialbd.ttf"],
}
_cache = {}


def fonte(estilo: str, tamanho: int):
    chave = (estilo, tamanho)
    if chave not in _cache:
        for caminho in FONTES[estilo]:
            p = Path(caminho) if Path(caminho).is_absolute() else RAIZ / caminho
            if p.exists():
                _cache[chave] = ImageFont.truetype(str(p), tamanho)
                break
        else:
            _cache[chave] = ImageFont.load_default(size=tamanho)
    return _cache[chave]


def _hex(cor: str, alfa: int = 255) -> tuple:
    cor = cor.lstrip("#")
    return tuple(int(cor[i:i + 2], 16) for i in (0, 2, 4)) + (alfa,)


# ---------- texto ----------

def texto_espacado(draw, xy, texto, f, cor, espaco=0.18, ancora_direita=False):
    """Texto em caixa alta com espaçamento entre letras (assinaturas e etiquetas)."""
    extra = f.size * espaco
    largura = sum(f.getlength(c) + extra for c in texto) - extra
    x, y = xy
    if ancora_direita:
        x -= largura
    for c in texto:
        draw.text((x, y), c, font=f, fill=cor)
        x += f.getlength(c) + extra
    return largura


def _tokens(texto: str):
    """Divide o título em (palavra, destaque?, colada?) respeitando *itálico*.

    "colada" indica que a palavra vem grudada na anterior (ex.: "*seu*?").
    """
    saida = []
    anterior_com_espaco = True
    for i, trecho in enumerate(re.split(r"\*", texto)):
        for j, palavra in enumerate(trecho.split()):
            colada = (j == 0 and bool(saida) and not trecho[:1].isspace()
                      and not anterior_com_espaco)
            saida.append((palavra, i % 2 == 1, colada))
        if trecho:
            anterior_com_espaco = trecho[-1:].isspace()
    return saida


PONTUACAO_RECUADA = "?!:;"
# Pares de letras que precisam de aproximação (kerning manual, em fração do corpo),
# pois o Pillow sem libraqm não aplica o kerning da fonte.
KERNING = {"V": -0.07, "W": -0.06, "T": -0.06, "Y": -0.06, "P": -0.03, "F": -0.04}
MINUSCULAS_AFETADAS = set("aáàâãeéêoóôõuúcçs.,")


def _desenhar_palavra(draw, x, y, palavra, f, cor):
    """Desenha a palavra aproximando ?, !, : e ; (a Bodoni os afasta demais)
    e aplicando kerning manual na primeira letra (ex.: "Você")."""
    corpo = palavra.rstrip(PONTUACAO_RECUADA)
    final = palavra[len(corpo):]
    if len(corpo) > 1 and corpo[0] in KERNING and corpo[1] in MINUSCULAS_AFETADAS:
        draw.text((x, y), corpo[0], font=f, fill=cor)
        x += f.getlength(corpo[0]) + f.size * KERNING[corpo[0]]
        corpo = corpo[1:]
    if corpo:
        draw.text((x, y), corpo, font=f, fill=cor)
        x += f.getlength(corpo)
    if final:
        x -= f.size * 0.08 if corpo else f.size * 0.04
        draw.text((x, y), final, font=f, fill=cor)
        x += f.getlength(final)
    return x


def _linhas_ricas(texto, tam, largura_max):
    f_n, f_i = fonte("titulo", tam), fonte("italico", tam)
    espaco = f_n.getlength(" ")
    linhas, atual, larg = [], [], 0
    for palavra, destaque, colada in _tokens(texto):
        w = (f_i if destaque else f_n).getlength(palavra)
        sep = 0 if colada else espaco
        if atual and not colada and larg + sep + w > largura_max:
            linhas.append(atual)
            atual, larg = [], 0
        larg += (sep if atual else 0) + w
        atual.append((palavra, destaque, colada))
    if atual:
        linhas.append(atual)
    return linhas


def largura_linha(linha, tam) -> float:
    f_n, f_i = fonte("titulo", tam), fonte("italico", tam)
    espaco = f_n.getlength(" ")
    total = 0.0
    for k, (palavra, destaque, colada) in enumerate(linha):
        if k and not colada:
            total += espaco
        total += (f_i if destaque else f_n).getlength(palavra)
    return total


def titulo_ajustado(texto, largura_max, altura_max, tam_max, tam_min, entrelinha=1.08):
    """Maior tamanho em que o título cabe na altura E nenhuma linha passa da largura
    (uma palavra longa, como "regularizado?", não pode estourar a margem)."""
    tam = tam_max
    while True:
        linhas = _linhas_ricas(texto, tam, largura_max)
        altura = len(linhas) * tam * entrelinha
        larga = max(largura_linha(l, tam) for l in linhas) if linhas else 0
        if (altura <= altura_max and larga <= largura_max) or tam <= tam_min:
            return tam, linhas, int(altura)
        tam -= 4


def desenhar_titulo(draw, x, y, tam, linhas, cor, cor_destaque, entrelinha=1.08):
    f_n, f_i = fonte("titulo", tam), fonte("italico", tam)
    espaco = f_n.getlength(" ")
    for linha in linhas:
        cx = x
        for k, (palavra, destaque, colada) in enumerate(linha):
            if k and not colada:
                cx += espaco
            f = f_i if destaque else f_n
            cx = _desenhar_palavra(draw, cx, y, palavra, f, cor_destaque if destaque else cor)
        y += int(tam * entrelinha)
    return y


NBSP = " "
# expressões que não podem ser separadas no fim da linha: "§ 1º", "art. 216-A", "Lei 6.015/1973"
_COLAR = re.compile(r"(§|art\.|arts\.|Lei|LC|Tema|inciso|n\.º|nº)\s+(?=[\dIVXLC])")
# número e unidade também ficam juntos: "5 dias", "4 horas", "R$ 110 mil", "250 m²"
_NUMERO_UNIDADE = re.compile(r"(\d)\s+(?=(dias?|horas?|anos?|meses|mês|mil|milhões|m²)(\W|$))|(R\$)\s+(?=\d)")


def quebrar(texto, f, largura_max):
    linhas = []
    texto = _COLAR.sub(lambda m: m.group(1) + NBSP, texto)
    texto = _NUMERO_UNIDADE.sub(lambda m: (m.group(1) or m.group(4)) + NBSP, texto)
    for paragrafo in texto.split("\n"):
        atual = ""
        for palavra in [p for p in paragrafo.split(" ") if p]:  # split(" "): preserva o espaço fixo
            teste = f"{atual} {palavra}".strip()
            if f.getlength(teste) <= largura_max:
                atual = teste
            else:
                if atual:
                    linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas


def paragrafo_ajustado(texto, estilo, largura_max, altura_max, tam_max, tam_min, entrelinha):
    tam = tam_max
    while True:
        f = fonte(estilo, tam)
        linhas = quebrar(texto, f, largura_max)
        if len(linhas) * tam * entrelinha <= altura_max or tam <= tam_min:
            return f, linhas
        tam -= 2


def seta(draw, x, y, cor, comprimento=46):
    draw.line((x, y, x + comprimento, y), fill=cor, width=3)
    draw.line((x + comprimento - 14, y - 10, x + comprimento, y), fill=cor, width=3)
    draw.line((x + comprimento - 14, y + 10, x + comprimento, y), fill=cor, width=3)


# ---------- lâminas ----------

class Desenhista:
    def __init__(self, perfil: dict):
        v = perfil["visual"]
        self.adv = perfil["advogado"]
        self.escura = v["cor_escura"]
        self.destaque = v["cor_destaque"]
        self.destaque_clara = v["cor_destaque_clara"]
        self.clara = v["cor_clara"]
        self.areia = v["cor_areia"]
        self.texto_escuro = v["cor_texto_escuro"]

    def _fundo_foto(self, foto):
        if foto is None:
            base = Image.new("RGB", (LARGURA, ALTURA), self.escura)
        else:
            base = ImageOps.fit(foto, (LARGURA, ALTURA), method=Image.LANCZOS)
        # degradê vinho: faixa escura no topo (assinatura), leve no meio,
        # quase opaco embaixo (título)
        camada = Image.new("RGBA", (LARGURA, ALTURA))
        d = ImageDraw.Draw(camada)
        r, g, b, _ = _hex(self.escura)
        for y in range(ALTURA):
            t = y / ALTURA
            if t < 0.15:
                opacidade = 0.75 - 2.67 * t         # 0.75 -> 0.35
            elif t < 0.30:
                opacidade = 0.35
            else:
                opacidade = min(0.95, 0.35 + 1.25 * (t - 0.30))
            d.line((0, y, LARGURA, y), fill=(r, g, b, int(255 * opacidade)))
        return Image.alpha_composite(base.convert("RGBA"), camada).convert("RGB")

    def _assinatura(self, draw, cor):
        texto_espacado(draw, (MARGEM, 84), self.adv["assinatura"], fonte("texto", 22), cor, 0.28)

    def capa(self, post: dict, total: int = 1):
        img = self._fundo_foto(obter_foto(post))
        if post.get("data_comemorativa"):
            # sombra vinho suave atrás do selo de data: legível mesmo sobre céu ou parede clara
            sombra = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
            ImageDraw.Draw(sombra).rectangle((LARGURA - 420, 0, LARGURA, 300), fill=_hex(self.escura, 170))
            sombra = sombra.filter(ImageFilter.GaussianBlur(70))
            img = Image.alpha_composite(img.convert("RGBA"), sombra).convert("RGB")
        draw = ImageDraw.Draw(img)
        self._assinatura(draw, self.clara)

        # título ancorado na parte de baixo
        base_y = ALTURA - 190
        sub_f, sub_linhas = None, []
        if post.get("subtitulo"):
            sub_f, sub_linhas = paragrafo_ajustado(post["subtitulo"], "leve", UTIL - 60, 130, 36, 28, 1.4)
            base_y -= int(len(sub_linhas) * sub_f.size * 1.4) + 56

        tam, linhas, altura = titulo_ajustado(post["titulo"], UTIL, 560, 118, 70)
        y_titulo = base_y - altura
        # etiqueta: a data comemorativa (quando houver) ou a área
        data = post.get("data_comemorativa")
        if data:
            self._selo_data(draw, data)
        etiqueta = (data["nome"] if data else post["area"]).upper()
        draw.line((MARGEM, y_titulo - 58, MARGEM + 60, y_titulo - 58), fill=self.destaque_clara, width=3)
        texto_espacado(draw, (MARGEM + 78, y_titulo - 70), etiqueta, fonte("negrito", 22),
                       self.clara, 0.22)
        y = desenhar_titulo(draw, MARGEM, y_titulo, tam, linhas, self.clara, self.destaque_clara)

        if sub_linhas:
            y += 56 - int(tam * 0.08)
            for linha in sub_linhas:
                draw.text((MARGEM, y), linha, font=sub_f, fill=self.clara)
                y += int(sub_f.size * 1.4)

        # rodapé
        draw.line((MARGEM, ALTURA - 128, LARGURA - MARGEM, ALTURA - 128), fill=self.clara, width=1)
        draw.text((MARGEM, ALTURA - 100), self.adv["instagram"], font=fonte("texto", 26), fill=self.clara)
        if total > 1:
            f = fonte("texto", 26)
            larg = f.getlength("arraste")
            draw.text((LARGURA - MARGEM - 60 - larg, ALTURA - 100), "arraste", font=f, fill=self.clara)
            seta(draw, LARGURA - MARGEM - 46, ALTURA - 84, self.destaque_clara)
        return img

    def _selo_data(self, draw, data):
        """Selo de calendário no canto superior direito: dia em Bodoni itálico e mês espaçado."""
        f_dia, f_mes = fonte("italico", 150), fonte("negrito", 22)
        direita = LARGURA - MARGEM
        draw.text((direita, 40), data["dia"], font=f_dia, fill=self.destaque_clara, anchor="ra")
        y_mes = draw.textbbox((direita, 40), data["dia"], font=f_dia, anchor="ra")[3] + 16
        texto_espacado(draw, (direita, y_mes), data["mes"].upper(), f_mes, self.clara, 0.3, ancora_direita=True)

    def conteudo(self, post: dict, numero: int, slide: dict, pagina: int, total: int):
        img = Image.new("RGB", (LARGURA, ALTURA), self.clara)
        draw = ImageDraw.Draw(img)
        # topo: área e paginação
        texto_espacado(draw, (MARGEM, 84), post["area"].upper(), fonte("negrito", 20), self.destaque, 0.24)
        texto_espacado(draw, (LARGURA - MARGEM, 84), f"{pagina:02d} / {total:02d}", fonte("texto", 20),
                       self.destaque, 0.2, ancora_direita=True)

        # bloco (número + título + fio + texto) centralizado na vertical
        tam, linhas, alt_titulo = titulo_ajustado(slide["titulo"], UTIL, 250, 76, 52)
        f, linhas_txt = paragrafo_ajustado(slide["texto"], "texto", UTIL, 560, 42, 28, 1.5)
        alt_num, alt_txt = 190, int(len(linhas_txt) * f.size * 1.5)
        alt_bloco = alt_num + alt_titulo + 26 + 48 + alt_txt
        topo, base = 150, ALTURA - 170
        y = topo + max(0, (base - topo - alt_bloco) // 2)

        draw.text((MARGEM - 6, y - 20), f"{numero:02d}", font=fonte("titulo", 160), fill=self.destaque)
        y = desenhar_titulo(draw, MARGEM, y + alt_num, tam, linhas, self.texto_escuro, self.destaque)
        y += 40  # espaço para as descendentes (g, p, q) não tocarem o fio
        draw.line((MARGEM, y, MARGEM + 120, y), fill=self.destaque, width=3)
        y += 48
        for linha in linhas_txt:
            draw.text((MARGEM, y), linha, font=f, fill=self.texto_escuro)
            y += int(f.size * 1.5)
        self._rodape_claro(draw)
        return img

    def _rodape_claro(self, draw):
        draw.line((MARGEM, ALTURA - 128, LARGURA - MARGEM, ALTURA - 128), fill=self.areia, width=2)
        f = fonte("texto", 24)
        draw.text((MARGEM, ALTURA - 100), f"{self.adv['nome']}  |  {self.adv['oab']}", font=f,
                  fill=self.texto_escuro)

    def encerramento(self, post: dict, total: int):
        img = Image.new("RGB", (LARGURA, ALTURA), self.escura)
        draw = ImageDraw.Draw(img)
        self._assinatura(draw, self.destaque_clara)
        chamada = post.get("chamada_final") or "Ficou com alguma dúvida?"
        tam, linhas, altura = titulo_ajustado(f"*{chamada}*", UTIL, 420, 96, 60, 1.12)
        y = desenhar_titulo(draw, MARGEM, 330, tam, linhas, self.clara, self.clara, 1.12)
        y += 70
        draw.line((MARGEM, y, MARGEM + 120, y), fill=self.destaque_clara, width=3)
        y += 60
        f = fonte("leve", 34)
        for linha in ("Salve para consultar depois.",
                      "Envie para quem precisa saber disso.",
                      "Conte sua experiência nos comentários."):
            draw.text((MARGEM, y), linha, font=f, fill=self.clara)
            y += 60
        draw.line((MARGEM, ALTURA - 128, LARGURA - MARGEM, ALTURA - 128), fill=self.destaque, width=1)
        draw.text((MARGEM, ALTURA - 100), f"Siga {self.adv['instagram']}", font=fonte("negrito", 26),
                  fill=self.clara)
        texto_espacado(draw, (LARGURA - MARGEM, ALTURA - 96), f"{total:02d} / {total:02d}",
                       fonte("texto", 20), self.destaque_clara, 0.2, ancora_direita=True)
        return img


def gerar_imagens(post: dict, perfil: dict, pasta: Path) -> list[Path]:
    """Cria as lâminas do post em JPEG (formato exigido pela API do Instagram)."""
    pasta.mkdir(parents=True, exist_ok=True)
    d = Desenhista(perfil)
    slides = post.get("slides", [])

    if post["formato"] == "card" or not slides:
        imagens = [d.capa(post)]
    else:
        total = len(slides) + 2
        imagens = [d.capa(post, total)]
        for i, s in enumerate(slides, start=1):
            imagens.append(d.conteudo(post, i, s, i + 1, total))
        imagens.append(d.encerramento(post, total))

    caminhos = []
    for i, img in enumerate(imagens, start=1):
        caminho = pasta / f"{post['id']}_{i:02d}.jpg"
        img.save(caminho, "JPEG", quality=94, subsampling=0)
        caminhos.append(caminho)
    return caminhos
