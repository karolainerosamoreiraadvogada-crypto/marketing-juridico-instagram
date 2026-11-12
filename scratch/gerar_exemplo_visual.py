import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(".").resolve()))

import requests
from PIL import Image, ImageDraw, ImageFilter, ImageOps

from agente.config import carregar_perfil, PASTA_IMAGENS
from agente.imagem import (
    Desenhista, fonte, titulo_ajustado, paragrafo_ajustado,
    desenhar_titulo, texto_espacado, seta, LARGURA, ALTURA, MARGEM, UTIL
)

perfil = carregar_perfil()
d = Desenhista(perfil)

post_path = Path("posts/fila/2026-11-12_auxilio-doenca-negado-inss-laudo-medico.json")
post = json.loads(post_path.read_text(encoding="utf-8"))

# Banco curado de fotos médicas do Unsplash (100% royalty-free, alta resolução)
FOTOS_MEDICAS = [
    "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=1080&q=80", # Capa: Estetoscópio e prontuário na mesa
    "https://images.unsplash.com/photo-1666214280557-f1b5022eb634?w=1080&q=80", # Slide 1: Médico profissional com estetoscópio
    "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=1080&q=80", # Slide 2: Prontuário, exames e caneta
    "https://images.unsplash.com/photo-1584467735815-f778f274e296?w=1080&q=80", # Slide 3: Médico e paciente em avaliação
    "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=1080&q=80", # Slide 4: Médico analisando documentos
    "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=1080&q=80", # Encerramento: Balança da justiça / livros
]

headers = {"User-Agent": "Mozilla/5.0"}

def baixar_foto(url):
    r = requests.get(url, headers=headers, timeout=10)
    return Image.open(io.BytesIO(r.content)).convert("RGB")

print("1. Baixando fotos...")
fotos_pil = [baixar_foto(u) for u in FOTOS_MEDICAS]
print(f"Baixadas {len(fotos_pil)} fotos com sucesso!")

# Renderizar Slide 1 (Capa com foto)
print("2. Renderizando Capa com foto...")
capa_img = d._fundo_foto(fotos_pil[0])
draw_capa = ImageDraw.Draw(capa_img)
d._assinatura(draw_capa, d.clara)

# Título da capa
base_y = ALTURA - 190
sub_f, sub_linhas = paragrafo_ajustado(post["subtitulo"], "leve", UTIL - 60, 130, 36, 28, 1.4)
base_y -= int(len(sub_linhas) * sub_f.size * 1.4) + 56
tam, linhas, altura = titulo_ajustado(post["titulo"], UTIL, 560, 118, 70)
y_titulo = base_y - altura

draw_capa.line((MARGEM, y_titulo - 58, MARGEM + 60, y_titulo - 58), fill=d.destaque_clara, width=3)
texto_espacado(draw_capa, (MARGEM + 78, y_titulo - 70), post["area"].upper(), fonte("negrito", 22), d.clara, 0.22)
desenhar_titulo(draw_capa, MARGEM, y_titulo, tam, linhas, d.clara, d.destaque_clara)

y_sub = y_titulo + altura + 56 - int(tam * 0.08)
for linha in sub_linhas:
    draw_capa.text((MARGEM, y_sub), linha, font=sub_f, fill=d.clara)
    y_sub += int(sub_f.size * 1.4)

draw_capa.line((MARGEM, ALTURA - 128, LARGURA - MARGEM, ALTURA - 128), fill=d.clara, width=1)
draw_capa.text((MARGEM, ALTURA - 100), d.adv["instagram"], font=fonte("texto", 26), fill=d.clara)
f_arraste = fonte("texto", 26)
larg = f_arraste.getlength("arraste")
draw_capa.text((LARGURA - MARGEM - 60 - larg, ALTURA - 100), "arraste", font=f_arraste, fill=d.clara)
seta(draw_capa, LARGURA - MARGEM - 46, ALTURA - 84, d.destaque_clara)

# Renderizar Slides Internos (2 a 5) com foto elegante
total_slides = 6
slides_internos = []

for idx, slide in enumerate(post["slides"]):
    pagina = idx + 2
    numero = idx + 1
    foto = fotos_pil[numero]
    
    img = Image.new("RGB", (LARGURA, ALTURA), d.clara)
    draw = ImageDraw.Draw(img)
    
    # Topo: Área e Paginação
    texto_espacado(draw, (MARGEM, 84), post["area"].upper(), fonte("negrito", 20), d.destaque, 0.24)
    texto_espacado(draw, (LARGURA - MARGEM, 84), f"{pagina:02d} / {total_slides:02d}", fonte("texto", 20), d.destaque, 0.2, ancora_direita=True)
    
    # Foto com cantos arredondados (visual card moderno)
    larg_foto = UTIL
    alt_foto = 440
    y_foto = 140
    raio = 24
    
    foto_fit = ImageOps.fit(foto, (larg_foto, alt_foto), method=Image.LANCZOS)
    mascara = Image.new("L", (larg_foto, alt_foto), 0)
    draw_mask = ImageDraw.Draw(mascara)
    draw_mask.rounded_rectangle((0, 0, larg_foto, alt_foto), radius=raio, fill=255)
    img.paste(foto_fit, (MARGEM, y_foto), mascara)
    
    # Borda sutil dourada/areia
    draw.rounded_rectangle((MARGEM, y_foto, MARGEM + larg_foto, y_foto + alt_foto), radius=raio, outline=d.destaque, width=2)
    
    # Bloco textual
    y_bloco = y_foto + alt_foto + 40
    draw.text((MARGEM, y_bloco), f"{numero:02d}", font=fonte("titulo", 72), fill=d.destaque)
    y_titulo = y_bloco + 75
    
    tam, linhas, alt_titulo = titulo_ajustado(slide["titulo"], UTIL, 160, 64, 46)
    y_fio = desenhar_titulo(draw, MARGEM, y_titulo, tam, linhas, d.texto_escuro, d.destaque) + 20
    draw.line((MARGEM, y_fio, MARGEM + 90, y_fio), fill=d.destaque, width=3)
    
    y_txt = y_fio + 30
    f_txt, linhas_txt = paragrafo_ajustado(slide["texto"], "texto", UTIL, 320, 34, 26, 1.45)
    for linha in linhas_txt:
        draw.text((MARGEM, y_txt), linha, font=f_txt, fill=d.texto_escuro)
        y_txt += int(f_txt.size * 1.45)
        
    # Rodapé institucional
    draw.line((MARGEM, ALTURA - 128, LARGURA - MARGEM, ALTURA - 128), fill=d.areia, width=2)
    draw.text((MARGEM, ALTURA - 100), f"{d.adv['nome']}  |  {d.adv['oab']}", font=fonte("texto", 24), fill=d.texto_escuro)
    
    slides_internos.append(img)

# Slide 6 (Encerramento com foto de fundo e filtro bordô)
foto_enc = fotos_pil[5]
enc_img = d._fundo_foto(foto_enc)
draw_enc = ImageDraw.Draw(enc_img)
d._assinatura(draw_enc, d.destaque_clara)

chamada = post.get("chamada_final") or "Você já passou por perícia médica do INSS?"
tam, linhas, altura = titulo_ajustado(f"*{chamada}*", UTIL, 420, 90, 56, 1.12)
y = desenhar_titulo(draw_enc, MARGEM, 330, tam, linhas, d.clara, d.clara, 1.12) + 70
draw_enc.line((MARGEM, y, MARGEM + 120, y), fill=d.destaque_clara, width=3)
y += 60
f_inst = fonte("leve", 34)
for linha in ("Salve para consultar depois.", "Envie para quem precisa saber disso.", "Conte sua experiência nos comentários."):
    draw_enc.text((MARGEM, y), linha, font=f_inst, fill=d.clara)
    y += 60

draw_enc.line((MARGEM, ALTURA - 128, LARGURA - MARGEM, ALTURA - 128), fill=d.destaque, width=1)
draw_enc.text((MARGEM, ALTURA - 100), f"Siga {d.adv['instagram']}", font=fonte("negrito", 26), fill=d.clara)
texto_espacado(draw_enc, (LARGURA - MARGEM, ALTURA - 96), f"{total_slides:02d} / {total_slides:02d}", fonte("texto", 20), d.destaque_clara, 0.2, ancora_direita=True)

# Salvar todos os 6 slides
todos_slides = [capa_img] + slides_internos + [enc_img]
pasta_out = Path("posts/imagens")
for i, img in enumerate(todos_slides, 1):
    caminho = pasta_out / f"2026-11-12_auxilio-doenca-negado-inss-laudo-medico_{i:02d}.jpg"
    img.save(caminho, "JPEG", quality=95)
    print(f"Salvo: {caminho}")

# Sincronizar com o Google Drive
from agente.imagem import _copiar_para_google_drive
caminhos_finais = [pasta_out / f"2026-11-12_auxilio-doenca-negado-inss-laudo-medico_{i:02d}.jpg" for i in range(1, 7)]
_copiar_para_google_drive(caminhos_finais, post)
print("Todas as 6 imagens com fotos profissionais foram sincronizadas no Google Drive!")
