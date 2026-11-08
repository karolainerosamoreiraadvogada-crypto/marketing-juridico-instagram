"""Publicação pela API oficial do Instagram (gratuita).

Usa a "Instagram API with Instagram Login" (conta Profissional: Criador ou
Empresa; não exige Página do Facebook).

Variáveis de ambiente:
  IG_USER_ID       ID numérico da conta do Instagram
  IG_ACCESS_TOKEN  token de longa duração (válido por 60 dias; renove com
                   `python main.py renovar-token`)
  IG_GRAPH_URL     opcional. Padrão: https://graph.instagram.com/v23.0
                   (para contas ligadas a Página do Facebook use
                   https://graph.facebook.com/v23.0)

Importante: a API só aceita imagens JPEG em URL pública. Por isso as imagens
ficam no próprio repositório (público) e são servidas pelo raw.githubusercontent.com.
"""
import os
import time

import requests

URL_PADRAO = "https://graph.facebook.com/v21.0"


class ErroInstagram(RuntimeError):
    pass


class Instagram:
    def __init__(self):
        self.user_id = os.environ.get("IG_USER_ID")
        self.token = os.environ.get("IG_ACCESS_TOKEN")
        # "or": no GitHub a variável pode existir mas vir vazia
        self.base = (os.environ.get("IG_GRAPH_URL") or URL_PADRAO).rstrip("/")
        if not (self.user_id and self.token):
            raise ErroInstagram("Defina IG_USER_ID e IG_ACCESS_TOKEN.")

    def _req(self, metodo: str, caminho: str, **params) -> dict:
        params["access_token"] = self.token
        resp = requests.request(metodo, f"{self.base}/{caminho}", params=params, timeout=60)
        dados = resp.json()
        if not resp.ok or "error" in dados:
            raise ErroInstagram(f"{caminho}: {dados.get('error', dados)}")
        return dados

    def _aguardar(self, container_id: str, limite_s: int = 300):
        """Espera o Instagram terminar de processar a mídia."""
        inicio = time.time()
        while time.time() - inicio < limite_s:
            status = self._req("GET", container_id, fields="status_code").get("status_code")
            if status == "FINISHED":
                return
            if status in ("ERROR", "EXPIRED"):
                raise ErroInstagram(f"Falha ao processar mídia {container_id}: {status}")
            time.sleep(5)
        raise ErroInstagram(f"Tempo esgotado processando {container_id}")

    def _publicar_container(self, container: str) -> str:
        """media_publish com novas tentativas: às vezes o Instagram informa FINISHED, mas
        ainda responde "media is not ready" (código 9007, subcódigo 2207027). Nesse erro
        nada foi publicado, então repetir é seguro e não duplica o post."""
        for tentativa in range(12):
            try:
                return self._req("POST", f"{self.user_id}/media_publish", creation_id=container)["id"]
            except ErroInstagram as erro:
                if "2207027" not in str(erro) or tentativa == 11:
                    raise
                time.sleep(20)

    def publicar(self, urls_imagens: list[str], legenda: str, local: str | None = None) -> str:
        """Publica imagem única ou carrossel (2 a 10 imagens). Retorna o ID do post.
        local: ID de localização (ex.: São Bernardo do Campo), exibido acima do post."""
        extra = {"location_id": local} if local else {}
        if len(urls_imagens) == 1:
            container = self._req("POST", f"{self.user_id}/media",
                                  image_url=urls_imagens[0], caption=legenda, **extra)["id"]
        else:
            filhos = []
            for url in urls_imagens[:10]:
                filho = self._req("POST", f"{self.user_id}/media",
                                  image_url=url, is_carousel_item="true")["id"]
                filhos.append(filho)
            for filho in filhos:
                self._aguardar(filho)
            container = self._req("POST", f"{self.user_id}/media", media_type="CAROUSEL",
                                  children=",".join(filhos), caption=legenda, **extra)["id"]

        self._aguardar(container)
        return self._publicar_container(container)

    def publicar_reel(self, url_video: str, legenda: str, url_capa: str | None = None,
                      local: str | None = None) -> str:
        """Publica um Reels (MP4 H.264 em URL pública). Retorna o ID do post."""
        params = {"media_type": "REELS", "video_url": url_video, "caption": legenda,
                  "share_to_feed": "true"}
        if local:
            params["location_id"] = local
        if url_capa:
            params["cover_url"] = url_capa
        container = self._req("POST", f"{self.user_id}/media", **params)["id"]
        self._aguardar(container, limite_s=900)  # vídeo leva mais tempo para processar
        return self._publicar_container(container)

    def publicar_story(self, url_imagem: str) -> str:
        """Publica uma tela de Stories (imagem JPEG em URL pública). Retorna o ID."""
        container = self._req("POST", f"{self.user_id}/media", media_type="STORIES",
                              image_url=url_imagem)["id"]
        self._aguardar(container)
        return self._publicar_container(container)

    def perfil(self) -> dict:
        alvo = self.user_id if "graph.facebook.com" in self.base else "me"
        campos = "id,username,followers_count,media_count,name" if alvo != "me" else "user_id,username,followers_count,media_count"
        return self._req("GET", alvo, fields=campos)

    def renovar_token(self) -> dict:
        """Gera um novo token de 60 dias (o atual precisa ter mais de 24h e estar válido)."""
        resp = requests.get("https://graph.instagram.com/refresh_access_token",
                            params={"grant_type": "ig_refresh_token",
                                    "access_token": self.token}, timeout=60)
        dados = resp.json()
        if not resp.ok or "error" in dados:
            raise ErroInstagram(f"Falha ao renovar token: {dados}")
        return dados
