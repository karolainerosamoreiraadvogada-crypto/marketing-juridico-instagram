"""Stories descontraídos (1080x1920) no estilo do perfil.

Cada quadro: etiqueta em "pílula" (ex.: MITO OU VERDADE?), destaque grande opcional
(ex.: MITO!), título em Bodoni, texto em Montserrat e um grande sinal tipográfico
decorativo ao fundo. Fundos alternam creme e vinho. Áreas seguras: nada nos 250 px
de cima (barra do perfil) nem nos 340 px de baixo (campo de resposta).
"""
from pathlib import Path

from PIL import Image, ImageDraw

from .imagem import _hex, desenhar_titulo, fonte, paragrafo_ajustado, texto_espacado, titulo_ajustado

W, H = 1080, 1920
M = 100
UTIL = W - 2 * M
TOPO_SEGURO = 260
BASE_SEGURA = H - 350

SINAL_DECORATIVO = {"mito_verdade": "?", "juridiques": "§", "voce_sabia": "!", "complete": "…",
                    "expectativa": "×"}


def _pilula(d, x, y, texto, f, cor_fundo, cor_texto):
    larg = sum(f.getlength(c) + f.size * 0.2 for c in texto) - f.size * 0.2
    pad_x, pad_y = 34, 20
    d.rounded_rectangle((x, y, x + larg + 2 * pad_x, y + f.size + 2 * pad_y), radius=(f.size + 2 * pad_y) // 2,
                        fill=cor_fundo)
    texto_espacado(d, (x + pad_x, y + pad_y - 2), texto, f, cor_texto, 0.2)
    return y + f.size + 2 * pad_y


def quadro(perfil, post, q, indice, total):
    v, adv = perfil["visual"], perfil["advogado"]
    escuro = indice % 2 == 1
    fundo = v["cor_escura"] if escuro else v["cor_clara"]
    cor_txt = v["cor_clara"] if escuro else v["cor_texto_escuro"]
    acento = v["cor_destaque_clara"] if escuro else v["cor_destaque"]
    img = Image.new("RGB", (W, H), fundo)

    # sinal tipográfico gigante ao fundo, bem suave
    marca = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dm = ImageDraw.Draw(marca)
    sinal = SINAL_DECORATIVO.get(post.get("tipo"), "?")
    dm.text((W + 60, TOPO_SEGURO + 120), sinal, font=fonte("italico", 820), fill=_hex(acento, 22), anchor="rt")
    img = Image.alpha_composite(img.convert("RGBA"), marca)
    d = ImageDraw.Draw(img)

    # topo: assinatura e contagem de telas
    texto_espacado(d, (M, TOPO_SEGURO + 10), adv["assinatura"], fonte("texto", 26), acento, 0.28)
    texto_espacado(d, (W - M, TOPO_SEGURO + 10), f"{indice + 1}/{total}", fonte("negrito", 26), acento, 0.2,
                   ancora_direita=True)

    # bloco central: mede antes de desenhar, para centralizar na área segura
    f_et = fonte("negrito", 34)
    area_ini, area_fim = TOPO_SEGURO + 120, BASE_SEGURA - (170 if q.get("rodape") else 90)
    disponivel = area_fim - area_ini
    # encolhe destaque, título e texto juntos até o bloco caber na área segura
    for escala in (1.0, 0.93, 0.86, 0.8, 0.74, 0.68, 0.62):
        tam_dest = int(230 * escala)
        while q.get("destaque") and fonte("italico", tam_dest).getlength(q["destaque"]) > UTIL and tam_dest > 80:
            tam_dest -= 6  # o destaque também precisa caber na largura
        tam_t, linhas_t, alt_t = titulo_ajustado(q["titulo"], UTIL, int(520 * escala),
                                                 int(104 * escala), int(56 * escala), 1.08)
        f_tx, linhas_tx = (paragrafo_ajustado(q["texto"], "texto", UTIL, int(420 * escala),
                                              int(46 * escala), int(32 * escala), 1.45)
                           if q.get("texto") else (None, []))
        alt_tx = int(len(linhas_tx) * f_tx.size * 1.45) if f_tx else 0
        alt = ((f_et.size + 40) + 60 + (tam_dest + 30 if q.get("destaque") else 0) + alt_t
               + (60 + alt_tx if alt_tx else 0))
        if alt <= disponivel:
            break
    else:
        raise ValueError(f"Texto longo demais para a tela {indice + 1} do story: encurte o texto.")
    y = area_ini + (disponivel - alt) // 2

    y = _pilula(d, M, y, q["etiqueta"], f_et, acento, v["cor_clara"]) + 60
    if q.get("destaque"):
        d.text((M - 6, y - 30), q["destaque"], font=fonte("italico", tam_dest), fill=acento)
        y += tam_dest + 30
    y = desenhar_titulo(d, M, y, tam_t, linhas_t, cor_txt, acento, 1.08)
    if linhas_tx:
        y += 42  # espaço para as letras com perna (g, p, q) não tocarem o traço
        d.line((M, y, M + 140, y), fill=acento, width=5)
        y += 30
        for linha in linhas_tx:
            d.text((M, y), linha, font=f_tx, fill=cor_txt)
            y += int(f_tx.size * 1.45)

    # rodapé (acima do campo de resposta)
    if q.get("rodape"):
        f = fonte("negrito", 30)
        texto_espacado(d, (M, BASE_SEGURA - 120), q["rodape"].upper(), f, acento, 0.16)
    d.line((M, BASE_SEGURA - 50, W - M, BASE_SEGURA - 50), fill=acento, width=2)
    d.text((M, BASE_SEGURA - 30), f"{adv['nome']}  |  {adv['oab']}", font=fonte("texto", 28), fill=cor_txt)
    return img.convert("RGB")


def gerar_stories(post: dict, perfil: dict, pasta: Path) -> list[Path]:
    pasta.mkdir(parents=True, exist_ok=True)
    caminhos = []
    total = len(post["quadros"])
    for i, q in enumerate(post["quadros"]):
        caminho = pasta / f"{post['id']}_{i + 1:02d}.jpg"
        quadro(perfil, post, q, i, total).save(caminho, "JPEG", quality=94, subsampling=0)
        caminhos.append(caminho)
    return caminhos


def aviso_novo_post(post: dict, perfil: dict, capa: Path, pasta: Path) -> Path:
    """Story "NOVO POST": capa do post em moldura, para avisar os seguidores.

    Publicado logo depois do post no feed (a API não permite o adesivo de link,
    por isso o texto convida a abrir o perfil)."""
    from PIL import ImageOps
    v, adv = perfil["visual"], perfil["advogado"]
    img = Image.new("RGB", (W, H), v["cor_escura"])
    d = ImageDraw.Draw(img)
    acento = v["cor_destaque_clara"]
    texto_espacado(d, (M, TOPO_SEGURO + 10), adv["assinatura"], fonte("texto", 26), acento, 0.28)

    y = _pilula(d, M, TOPO_SEGURO + 110, "NOVO POST NO FEED", fonte("negrito", 34), v["cor_destaque"],
                v["cor_clara"]) + 50
    # capa (4:5 no carrossel; 9:16 no Reels, recortada em 4:5) com fio terracota
    f_cham = fonte("italico", 64)
    alt = (BASE_SEGURA - 90) - y - (60 + int(f_cham.size * 1.3))  # cabe entre a etiqueta e a chamada
    larg = int(alt / 1.25)
    x = (W - larg) // 2
    miniatura = ImageOps.fit(Image.open(capa).convert("RGB"), (larg, alt), method=Image.LANCZOS)
    d.rectangle((x - 6, y - 6, x + larg + 5, y + alt + 5), outline=acento, width=3)
    img.paste(miniatura, (x, y))
    y += alt + 60

    chamada = "Toque no perfil e confira." if post.get("formato") != "reel" else "Toque no perfil e assista."
    d.text((W // 2, y), chamada, font=f_cham, fill=v["cor_clara"], anchor="ma")
    d.line((M, BASE_SEGURA - 50, W - M, BASE_SEGURA - 50), fill=acento, width=2)
    d.text((M, BASE_SEGURA - 30), f"{adv['nome']}  |  {adv['oab']}", font=fonte("texto", 28),
           fill=v["cor_clara"])
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = pasta / f"{post['id']}_aviso.jpg"
    img.save(caminho, "JPEG", quality=94, subsampling=0)
    return caminho
