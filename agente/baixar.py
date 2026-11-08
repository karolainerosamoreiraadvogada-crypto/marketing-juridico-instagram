"""Baixa vídeos e fotos gratuitos do Pexels (licença livre para uso comercial).

Os arquivos ficam em assets/videos e assets/fotos (fora do GitHub). A versão
vertical em alta definição é deduzida do nome da prévia que aparece na busca
(ex.: 123-sd_360_640_25fps.mp4 -> 123-hd_1080_1920_25fps.mp4).
"""
import re
from pathlib import Path

import requests

from .config import RAIZ

UA = {"User-Agent": "Mozilla/5.0"}
PASTA_VIDEOS = RAIZ / "assets" / "videos"
PASTA_FOTOS = RAIZ / "assets" / "fotos" / "escolhidas"


def _baixar(url: str, destino: Path) -> bool:
    r = requests.get(url, headers=UA, timeout=180, stream=True)
    if r.status_code != 200:
        return False
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "wb") as f:
        for bloco in r.iter_content(1 << 20):
            f.write(bloco)
    return True


def video(url_previa: str) -> Path:
    """Recebe a URL da prévia SD e baixa a versão 1080x1920 (ou 720x1280)."""
    m = re.search(r"video-files/(\d+)/(\d+)[-_](?:sd_)?360_640_(\d+)fps", url_previa)
    pasta_id, arquivo_id, fps = m.groups()
    destino = PASTA_VIDEOS / f"pexels-{pasta_id}.mp4"
    if destino.exists():
        return destino
    base = f"https://videos.pexels.com/video-files/{pasta_id}/{arquivo_id}"
    for sufixo in (f"-hd_1080_1920_{fps}fps", f"_1080_1920_{fps}fps", f"-hd_720_1280_{fps}fps",
                   f"_720_1280_{fps}fps"):
        if _baixar(base + sufixo + ".mp4", destino):
            return destino
    raise RuntimeError(f"Não encontrei versão HD de {url_previa}")


def foto(pexels_id: str) -> Path:
    destino = PASTA_FOTOS / f"pexels-{pexels_id}.jpg"
    if not destino.exists():
        url = (f"https://images.pexels.com/photos/{pexels_id}/pexels-photo-{pexels_id}.jpeg"
               "?auto=compress&cs=tinysrgb&w=1600")
        if not _baixar(url, destino):
            raise RuntimeError(f"Falha ao baixar a foto {pexels_id}")
    return destino
