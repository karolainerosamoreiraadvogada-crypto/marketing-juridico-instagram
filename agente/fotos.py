"""Fotos de fundo das capas.

Ordem de busca:
  1. assets/fotos/<area>/*.jpg (fotos próprias; ex.: assets/fotos/direito-imobiliario/)
  2. assets/fotos/*.jpg
  3. Pexels (gratuito, licença comercial). Chave em https://www.pexels.com/api/
     Variável de ambiente: PEXELS_API_KEY
Sem nenhuma dessas opções, a capa usa fundo liso na cor da paleta.
"""
import io
import os
import random
import re
import unicodedata

import requests
from PIL import Image

from .config import PASTA_FOTOS, RAIZ


def _slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def _locais(area: str) -> list:
    extensoes = ("*.jpg", "*.jpeg", "*.png")
    for pasta in (PASTA_FOTOS / _slug(area), PASTA_FOTOS):
        if pasta.exists():
            arquivos = [a for ext in extensoes for a in pasta.glob(ext)]
            if arquivos:
                return sorted(arquivos)
    return []


def _pexels(busca: str, semente: str):
    chave = os.environ.get("PEXELS_API_KEY")
    if not (chave and busca):
        return None
    try:
        resp = requests.get("https://api.pexels.com/v1/search",
                            headers={"Authorization": chave},
                            params={"query": busca, "orientation": "portrait", "per_page": 15},
                            timeout=30)
        fotos = resp.json().get("photos", []) if resp.ok else []
        if not fotos:
            return None
        foto = random.Random(semente).choice(fotos)
        img = requests.get(foto["src"]["large2x"], timeout=60)
        img.raise_for_status()
        return Image.open(io.BytesIO(img.content)).convert("RGB")
    except (requests.RequestException, OSError, ValueError, KeyError):
        return None


def obter_foto(post: dict):
    """Retorna uma PIL.Image para o fundo da capa, ou None.

    Se o post tiver o campo "foto" (caminho no repositório), ela tem prioridade.
    """
    if post.get("foto"):
        caminho = RAIZ / post["foto"]
        if caminho.exists():
            return Image.open(caminho).convert("RGB")
    locais = _locais(post.get("area", ""))
    if locais:
        return Image.open(random.Random(post["id"]).choice(locais)).convert("RGB")
    return _pexels(post.get("foto_busca", ""), post["id"])
