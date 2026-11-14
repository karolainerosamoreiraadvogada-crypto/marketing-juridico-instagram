"""Motor Editorial de Alta Performance para Carrosséis Jurídicos (HTML5 / CSS3 via Chrome Headless).
Padrão visual aprovado pela Dra. Karolaine Rosa Moreira (OAB/PR 125.692).

Arquitetura inspirada em:
- pabadvogados-hub/marketing-pab (Playwright/Chrome Headless render)
- sbroggioadv/marketing-adv-os-marketplace (Tokens e Compliance OAB)
- Design System 'Capa Chamariz' (Focal Shock Metaphor + Display Typography + 1-Line Hook)
"""

import os
import base64
import subprocess
import shutil
from pathlib import Path

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

DRIVE_DIR = Path(r"G:\Meu Drive\Escritório Advocacia\ESCRITÓRIO KAROLAINE ROSA MOREIRA\Posts - Instagram e TikTok")


def get_base64_image(image_path: Path) -> str:
    """Converte imagem local para string base64 para embutir diretamente no HTML."""
    if image_path.exists():
        return base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return ""


def template_capa_chamariz(
    titulo_linha1: str,
    titulo_linha2: str,
    sub_gancho: str,
    selo_texto: str = "NÃO CONCEDIDO",
    pill_texto: str = "DIREITO PREVIDENCIÁRIO",
    foto_b64: str = "",
    adv_nome: str = "Dra. Karolaine Rosa Moreira",
    adv_oab: str = "OAB/PR 125.692",
    chamada_rodape: str = "Entenda como reverter"
) -> str:
    """Gera o HTML da Capa Chamariz (Stop-Scroll Hook) com visual de impacto e zero poluição textual."""
    bg_style = f"background-image: url('data:image/jpeg;base64,{foto_b64}');" if foto_b64 else "background-color: #140307;"

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,800;0,900;1,700&family=Montserrat:wght@500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1080px; height: 1350px;
    background: #0D0204;
    font-family: 'Montserrat', sans-serif;
    color: #FFFFFF;
    position: relative;
    overflow: hidden;
    padding: 70px 80px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .bg-full {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    {bg_style}
    background-size: cover;
    background-position: center;
    filter: brightness(0.4) contrast(1.2);
    z-index: 1;
  }}
  .vignette {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(180deg, rgba(20, 3, 7, 0.7) 0%, rgba(92, 17, 36, 0.5) 40%, rgba(13, 2, 4, 0.98) 85%);
    z-index: 2;
  }}
  .top-bar {{
    position: relative;
    z-index: 3;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .author-box {{
    display: flex;
    align-items: center;
    gap: 14px;
    background: rgba(0, 0, 0, 0.45);
    padding: 10px 22px;
    border-radius: 40px;
    border: 1px solid rgba(200, 169, 110, 0.35);
    backdrop-filter: blur(10px);
  }}
  .author-name {{ font-size: 16px; font-weight: 700; color: #FFFFFF; letter-spacing: 1px; }}
  .author-oab {{ font-size: 13px; color: #C8A96E; }}
  .center-stamp {{
    position: relative;
    z-index: 3;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: auto 0;
  }}
  .stamp {{
    border: 5px solid #E63946;
    color: #FFFFFF;
    background: rgba(180, 20, 35, 0.88);
    padding: 18px 46px;
    font-size: 44px;
    font-weight: 900;
    letter-spacing: 6px;
    text-transform: uppercase;
    border-radius: 12px;
    transform: rotate(-7deg);
    box-shadow: 0 15px 45px rgba(230, 57, 70, 0.55);
    backdrop-filter: blur(8px);
  }}
  .bottom-block {{
    position: relative;
    z-index: 3;
    display: flex;
    flex-direction: column;
    gap: 18px;
  }}
  .pill {{
    display: inline-block;
    align-self: flex-start;
    background: #FFFFFF;
    color: #5C1124;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 8px 20px;
    border-radius: 50px;
  }}
  .title-line-1 {{
    font-family: 'Playfair Display', serif;
    font-size: 96px;
    font-weight: 900;
    line-height: 0.95;
    letter-spacing: -1px;
    text-transform: uppercase;
    color: #FFFFFF;
  }}
  .title-line-2 {{
    font-family: 'Playfair Display', serif;
    font-size: 102px;
    font-weight: 900;
    font-style: italic;
    line-height: 0.95;
    color: #C8A96E;
    text-shadow: 0 4px 30px rgba(200, 169, 110, 0.35);
  }}
  .sub-question {{
    font-size: 24px;
    font-weight: 600;
    color: #F8F5F0;
    line-height: 1.4;
    margin-top: 10px;
  }}
  .sub-question strong {{ color: #C8A96E; }}
  .cta-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(200, 169, 110, 0.3);
    padding-top: 20px;
    margin-top: 10px;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #C8A96E;
    text-transform: uppercase;
  }}
</style>
</head>
<body>
  <div class="bg-full"></div>
  <div class="vignette"></div>
  <div class="top-bar">
    <div class="author-box">
      <span class="author-name">{adv_nome}</span>
      <span class="author-oab">• {adv_oab}</span>
    </div>
  </div>
  <div class="center-stamp">
    <div class="stamp">{selo_texto}</div>
  </div>
  <div class="bottom-block">
    <div class="pill">{pill_texto}</div>
    <div class="title-line-1">{titulo_linha1}</div>
    <div class="title-line-2">{titulo_linha2}</div>
    <div class="sub-question">{sub_gancho}</div>
    <div class="cta-row">
      <span>{chamada_rodape}</span>
      <span>Arraste &rarr;</span>
    </div>
  </div>
</body>
</html>"""


def template_slide_conteudo(
    num: str,
    tag: str,
    titulo: str,
    destaque_box: str,
    itens: list[str],
    pagina: int,
    total: int = 6,
    adv_nome: str = "Karolaine Rosa Moreira",
    adv_oab: str = "OAB/PR 125.692",
    handle: str = "@karolainemoreira.adv"
) -> str:
    """Gera lâmina interna com respiro amplo, numeral dourado e caixa de destaque."""
    itens_html = ""
    for it in itens:
        itens_html += f"""
        <div class="card-item">
          <div class="card-bullet">&bull;</div>
          <div class="card-text">{it}</div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1080px; height: 1350px;
    background: #F8F5F0;
    font-family: 'Montserrat', sans-serif;
    color: #2A1E17;
    position: relative;
    padding: 80px 90px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(200, 169, 110, 0.4);
    padding-bottom: 24px;
  }}
  .brand {{
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #5C1124;
  }}
  .oab {{
    font-size: 13px;
    letter-spacing: 1.5px;
    color: #C8A96E;
    font-weight: 600;
  }}
  .content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .tag {{
    display: inline-block;
    background: #5C1124;
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 8px 18px;
    border-radius: 4px;
    margin-bottom: 25px;
    align-self: flex-start;
  }}
  .num {{
    font-family: 'Playfair Display', serif;
    font-size: 96px;
    font-weight: 900;
    color: #C8A96E;
    line-height: 1;
    margin-bottom: 10px;
  }}
  h1 {{
    font-family: 'Playfair Display', serif;
    font-size: 56px;
    font-weight: 900;
    color: #5C1124;
    line-height: 1.15;
    margin-bottom: 24px;
  }}
  .highlight-card {{
    background: #FFFFFF;
    border-left: 5px solid #C8A96E;
    padding: 24px 30px;
    border-radius: 0 12px 12px 0;
    font-size: 26px;
    font-weight: 600;
    line-height: 1.5;
    color: #5C1124;
    margin-bottom: 30px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04);
  }}
  .card-item {{
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 16px;
    font-size: 24px;
    line-height: 1.5;
    color: #4A3B32;
  }}
  .card-bullet {{
    color: #C8A96E;
    font-size: 32px;
    line-height: 1;
  }}
  .footer {{
    border-top: 1px solid rgba(200, 169, 110, 0.4);
    padding-top: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 15px;
    letter-spacing: 1px;
    color: #8C7A6B;
  }}
  .footer strong {{ color: #5C1124; }}
</style>
</head>
<body>
  <div class="header">
    <div class="brand">{adv_nome}</div>
    <div class="oab">{adv_oab}</div>
  </div>
  <div class="content">
    <div class="tag">{tag}</div>
    <div class="num">{num}</div>
    <h1>{titulo}</h1>
    <div class="highlight-card">{destaque_box}</div>
    {itens_html}
  </div>
  <div class="footer">
    <div><strong>{handle}</strong></div>
    <div>{pagina:02d} / {total:02d}</div>
  </div>
</body>
</html>"""


def template_slide_cta(
    titulo: str,
    titulo_italico: str,
    tag: str = "DIREITO PREVIDENCIÁRIO",
    acoes: list[tuple[str, str]] = None,
    total: int = 6,
    adv_nome: str = "Karolaine Rosa Moreira",
    adv_oab: str = "OAB/PR 125.692",
    handle: str = "@karolainemoreira.adv"
) -> str:
    """Gera lâmina de encerramento em fundo Bordô Nobre com CTA elegante e compliance OAB."""
    if not acoes:
        acoes = [
            ("&#128278;", "Salve para consultar o prazo"),
            ("&#128227;", "Envie para quem precisa saber disso"),
            ("&#128172;", "Conte seu relato nos comentários")
        ]

    acoes_html = ""
    for icone, texto in acoes:
        acoes_html += f'<div class="cta-item"><span class="cta-icon">{icone}</span> {texto}</div>\n'

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Montserrat:wght@500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1080px; height: 1350px;
    background: #5C1124;
    font-family: 'Montserrat', sans-serif;
    color: #FFFFFF;
    position: relative;
    overflow: hidden;
    padding: 80px 90px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .glow {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 900px; height: 900px;
    background: radial-gradient(circle, rgba(200, 169, 110, 0.15) 0%, rgba(92, 17, 36, 0) 70%);
    pointer-events: none;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(200, 169, 110, 0.35);
    padding-bottom: 24px;
    position: relative;
    z-index: 2;
  }}
  .brand {{
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #FFFFFF;
  }}
  .oab {{
    font-size: 13px;
    letter-spacing: 1.5px;
    color: #C8A96E;
    font-weight: 600;
  }}
  .content {{
    position: relative;
    z-index: 2;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .pill {{
    display: inline-block;
    background: #C8A96E;
    color: #2B0E14;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 8px 18px;
    border-radius: 4px;
    margin-bottom: 30px;
    align-self: flex-start;
  }}
  h1 {{
    font-family: 'Playfair Display', serif;
    font-size: 64px;
    font-weight: 900;
    line-height: 1.15;
    margin-bottom: 35px;
    color: #FFFFFF;
  }}
  h1 em {{
    font-style: italic;
    color: #C8A96E;
  }}
  .cta-card {{
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(200, 169, 110, 0.35);
    border-radius: 16px;
    padding: 30px;
    backdrop-filter: blur(10px);
    margin-bottom: 30px;
  }}
  .cta-item {{
    display: flex;
    align-items: center;
    gap: 16px;
    font-size: 22px;
    font-weight: 600;
    color: #F8F5F0;
    margin-bottom: 16px;
  }}
  .cta-item:last-child {{ margin-bottom: 0; }}
  .cta-icon {{
    color: #C8A96E;
    font-size: 26px;
  }}
  .footer {{
    border-top: 1px solid rgba(200, 169, 110, 0.35);
    padding-top: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 16px;
    letter-spacing: 1.5px;
    color: #C8A96E;
    position: relative;
    z-index: 2;
  }}
  .footer strong {{ color: #FFFFFF; }}
</style>
</head>
<body>
  <div class="glow"></div>
  <div class="header">
    <div class="brand">{adv_nome}</div>
    <div class="oab">{adv_oab}</div>
  </div>
  <div class="content">
    <div class="pill">{tag}</div>
    <h1>{titulo} <em>{titulo_italico}</em>?</h1>
    <div class="cta-card">
      {acoes_html}
    </div>
  </div>
  <div class="footer">
    <div>Siga <strong>{handle}</strong></div>
    <div>{total:02d} / {total:02d}</div>
  </div>
</body>
</html>"""


def render_html_to_jpg(html_content: str, output_jpg_path: Path):
    """Executa o Chrome Headless para renderizar e salvar screenshot exato de 1080x1350px."""
    output_jpg_path.parent.mkdir(parents=True, exist_ok=True)
    temp_html = output_jpg_path.with_suffix(".temp.html")
    temp_html.write_text(html_content, encoding="utf-8")

    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--screenshot={str(output_jpg_path.resolve())}",
        "--window-size=1080,1350",
        f"file:///{str(temp_html.resolve()).replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    if temp_html.exists():
        temp_html.unlink()


def gerar_carrossel_chamariz(post: dict, pasta_saida: Path) -> list[Path]:
    """Gera carrossel completo padrão Dra. Karolaine (Capa Chamariz + Slides Internos + CTA)."""
    pasta_saida.mkdir(parents=True, exist_ok=True)
    caminhos = []

    # Carregar foto se houver no scratch ou post
    foto_b64 = ""
    foto_local = Path("scratch/stressed_patient.jpg")
    if foto_local.exists():
        foto_b64 = get_base64_image(foto_local)

    # 1. Capa
    s1 = template_capa_chamariz(
        titulo_linha1=post.get("chamariz_l1", "AUXÍLIO"),
        titulo_linha2=post.get("chamariz_l2", "NEGADO?"),
        sub_gancho=post.get("chamariz_gancho", "O perito do INSS <strong>não é obrigado</strong> a aceitar o seu atestado."),
        selo_texto=post.get("chamariz_selo", "NÃO CONCEDIDO"),
        pill_texto=post.get("chamariz_pill", "SEU MÉDICO DEU LAUDO?"),
        foto_b64=foto_b64
    )
    p1 = pasta_saida / f"{post['id']}_01.jpg"
    render_html_to_jpg(s1, p1)
    caminhos.append(p1)

    # 2. Slides de Conteúdo
    slides = post.get("slides", [])
    total = len(slides) + 2
    for idx, s in enumerate(slides, start=1):
        html_s = template_slide_conteudo(
            num=f"{idx:02d}",
            tag=s.get("tag", "DIREITO PREVIDENCIÁRIO"),
            titulo=s.get("titulo", ""),
            destaque_box=s.get("destaque", ""),
            itens=s.get("itens", []),
            pagina=idx + 1,
            total=total
        )
        p_s = pasta_saida / f"{post['id']}_{idx + 1:02d}.jpg"
        render_html_to_jpg(html_s, p_s)
        caminhos.append(p_s)

    # 3. Slide Final (CTA)
    s_end = template_slide_cta(
        titulo=post.get("cta_titulo", "Teve o seu pedido"),
        titulo_italico=post.get("cta_italico", "indeferido"),
        tag=post.get("area", "DIREITO PREVIDENCIÁRIO"),
        total=total
    )
    p_end = pasta_saida / f"{post['id']}_{total:02d}.jpg"
    render_html_to_jpg(s_end, p_end)
    caminhos.append(p_end)

    # Sincronizar no Google Drive automaticamente
    if DRIVE_DIR.exists():
        for c in caminhos:
            shutil.copy2(c, DRIVE_DIR / c.name)

    return caminhos
