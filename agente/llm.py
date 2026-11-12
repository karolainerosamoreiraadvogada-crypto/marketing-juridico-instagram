"""Cliente do Google Gemini via REST, sem SDK.

Chave gratuita: https://aistudio.google.com/apikey
Variáveis de ambiente:
  GEMINI_API_KEY  (obrigatória)
  GEMINI_MODEL    (opcional, padrão abaixo)
"""
import json
import os
import time

import requests

MODELO_PADRAO = "gemini-3.5-flash"
URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"


class ErroLLM(RuntimeError):
    pass


def gerar_json(prompt_sistema: str, prompt_usuario: str, tentativas: int = 5) -> dict:
    """Envia o prompt e devolve a resposta já convertida de JSON para dict."""
    chave = os.environ.get("GEMINI_API_KEY")
    if not chave:
        raise ErroLLM("Defina a variável de ambiente GEMINI_API_KEY.")
    modelo = os.environ.get("GEMINI_MODEL") or MODELO_PADRAO

    corpo = {
        "systemInstruction": {"parts": [{"text": prompt_sistema}]},
        "contents": [{"role": "user", "parts": [{"text": prompt_usuario}]}],
        "generationConfig": {
            "temperature": 0.7,
            "responseMimeType": "application/json",
        },
    }

    for tentativa in range(1, tentativas + 1):
        try:
            resp = requests.post(
                URL.format(modelo=modelo),
                headers={"x-goog-api-key": chave},
                params={"key": chave},
                json=corpo,
                timeout=60,
            )
        except requests.exceptions.RequestException as e:
            if tentativa == tentativas:
                raise ErroLLM(f"Falha de rede ao conectar com o Gemini: {e}") from e
            time.sleep(3 * tentativa)
            continue

        # 429 = limite do plano gratuito; 5xx = instabilidade. Espera e tenta de novo.
        if resp.status_code in (429, 500, 502, 503) and tentativa < tentativas:
            time.sleep(5 * tentativa)
            continue
        if not resp.ok:
            raise ErroLLM(f"Gemini respondeu {resp.status_code}: {resp.text[:500]}")

        try:
            parts = resp.json()["candidates"][0]["content"]["parts"]
            texto = next(p["text"] for p in parts if "text" in p)
            return json.loads(texto)
        except (KeyError, IndexError, json.JSONDecodeError, StopIteration) as e:
            if tentativa == tentativas:
                raise ErroLLM(f"Resposta inválida do Gemini: {e}") from e

    raise ErroLLM("Não foi possível obter resposta do Gemini.")
