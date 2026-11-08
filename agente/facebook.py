"""Publicação na Página do Facebook pela API oficial da Meta (gratuita).

Variáveis de ambiente (opcionais: sem elas, o agente publica só no Instagram):
  FB_PAGE_ID     ID numérico da Página do Facebook
  FB_PAGE_TOKEN  token de acesso da Página (permissões pages_manage_posts,
                 pages_read_engagement e pages_show_list)

Formatos:
  carrossel -> publicação com várias fotos
  card      -> publicação com uma foto
  reel      -> Reels do Facebook (envio do vídeo pela URL pública)
  stories   -> Stories da Página (uma foto por tela)
"""
import os
import time

import requests

GRAPH = "https://graph.facebook.com/v23.0"


class ErroFacebook(RuntimeError):
    pass


def configurado() -> bool:
    return bool(os.environ.get("FB_PAGE_ID") and os.environ.get("FB_PAGE_TOKEN"))


class Facebook:
    def __init__(self):
        self.page = os.environ.get("FB_PAGE_ID")
        self.token = os.environ.get("FB_PAGE_TOKEN")
        if not (self.page and self.token):
            raise ErroFacebook("Defina FB_PAGE_ID e FB_PAGE_TOKEN.")

    def _post(self, caminho: str, **dados) -> dict:
        dados["access_token"] = self.token
        resp = requests.post(f"{GRAPH}/{caminho}", data=dados, timeout=120)
        corpo = resp.json()
        if not resp.ok or "error" in corpo:
            raise ErroFacebook(f"{caminho}: {corpo.get('error', corpo)}")
        return corpo

    def _foto_oculta(self, url: str) -> str:
        """Envia a foto sem publicar (para montar álbum ou story)."""
        return self._post(f"{self.page}/photos", url=url, published="false")["id"]

    def publicar_fotos(self, urls: list[str], texto: str) -> str:
        if len(urls) == 1:
            return self._post(f"{self.page}/photos", url=urls[0], caption=texto)["post_id"]
        ids = [self._foto_oculta(u) for u in urls]
        anexos = {f"attached_media[{i}]": f'{{"media_fbid":"{fid}"}}' for i, fid in enumerate(ids)}
        return self._post(f"{self.page}/feed", message=texto, **anexos)["id"]

    def publicar_reel(self, url_video: str, texto: str) -> str:
        inicio = self._post(f"{self.page}/video_reels", upload_phase="start")
        video_id = inicio["video_id"]
        envio = requests.post(f"https://rupload.facebook.com/video-upload/v23.0/{video_id}",
                              headers={"Authorization": f"OAuth {self.token}", "file_url": url_video},
                              timeout=300)
        if not envio.ok:
            raise ErroFacebook(f"envio do vídeo: {envio.text[:300]}")
        self._post(f"{self.page}/video_reels", upload_phase="finish", video_id=video_id,
                   video_state="PUBLISHED", description=texto)
        # aguarda o processamento para confirmar a publicação
        for _ in range(60):
            st = requests.get(f"{GRAPH}/{video_id}", params={"fields": "status", "access_token": self.token},
                              timeout=60).json().get("status", {})
            if st.get("video_status") in ("ready", "published") or st.get("publishing_phase", {}).get("status") == "complete":
                break
            if st.get("video_status") == "error":
                raise ErroFacebook(f"processamento do Reels: {st}")
            time.sleep(10)
        return video_id

    def publicar_stories(self, urls: list[str]) -> str:
        ids = []
        for u in urls:
            foto = self._foto_oculta(u)
            ids.append(self._post(f"{self.page}/photo_stories", photo_id=foto).get("post_id", foto))
        return ",".join(ids)

    def publicar(self, post: dict, urls: list[str], url_video: str | None, texto: str) -> str:
        if post.get("formato") == "stories":
            return self.publicar_stories(urls)
        if url_video:
            return self.publicar_reel(url_video, texto)
        return self.publicar_fotos(urls, texto)
