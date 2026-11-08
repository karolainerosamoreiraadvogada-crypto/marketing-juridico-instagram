"""Verificação automática de termos vedados (Provimento 205/2021 e Código de Ética da OAB).

É um filtro AUXILIAR: pega os deslizes mais comuns, mas não substitui a revisão
da advogada responsável antes de aprovar o post. Também sinaliza travessões,
proibidos pelo padrão de redação do perfil.
"""
import re
import unicodedata

# (padrão regex aplicado ao texto sem acentos e em minúsculas, motivo)
REGRAS = [
    (r"\bgarantid[oa]s?\b|\bgarantimos\b|\b100\s?%", "promessa de resultado"),
    (r"\bganhe\b|\bvenca\b|\bcausa ganha\b|\bsucesso garantido\b|\bresolvemos\b",
     "promessa de resultado"),
    (r"\bconsulta (gratis|gratuita)\b|\bsem custo\b|\bgratis\b", "oferta de gratuidade"),
    # valores em R$ só são alerta quando ligados a serviço (honorários, consulta etc.);
    # limites e valores da lei (ex.: "R$ 440 mil", teto do MEI) são conteúdo informativo
    (r"(honorarios?|consultas?|atendimentos?|servicos?|pacotes?)[^.\n]{0,40}r\$\s?\d"
     r"|r\$\s?\d[^.\n]{0,40}(honorarios?|consultas?|atendimentos?|pacotes?)"
     r"|\bhonorarios?\b|\bpreco\b|\bdescontos?\s+(em|nos?|promocional|especial)\b|\bparcelamos\b", "menção a valores/honorários"),
    (r"\bcontrate\b|\bligue (ja|agora)\b|\bwhats\s?app\b|\bzap\b|\bchame no direct\b"
     r"|\bme chame\b|\bagende (ja|agora|sua)\b|\bentre em contato\b", "captação de clientela"),
    (r"\b[Cc]omenta [A-Z]{3,}\b", "captação por palavra-chave nos comentários"),
    (r"\bo melhor\b|\ba melhor\b|\bnumero 1\b|\bn[oº]\s?1\b|\bo mais experiente\b"
     r"|\bimbativel\b|\breferencia (na|em)\b", "autopromoção comparativa"),
    (r"\bespecialista\b", "uso de 'especialista' (só com título comprovado)"),
    (r"\burgente\b|\bultima chance\b|\bso hoje\b|\bimperdivel\b|\baproveite\b"
     r"|\bultimas vagas\b|\bo prazo esta acabando\b", "urgência/tom mercantil"),
    # "faturamento" sozinho é termo técnico (ex.: limite do MEI); o alerta é para apelo comercial
    (r"\bfature mais\b|\baumente (seu|o seu) faturamento\b|\baumente (seus|o seu) lucro", "tom mercantil"),
    (r"\bganhei\b|\bmeu cliente\b|\bminha cliente\b|\bcaso real\b", "exposição de caso/cliente"),
]


def _normalizar(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()


def verificar(texto: str) -> list[str]:
    """Retorna a lista de alertas encontrados (vazia se estiver tudo ok)."""
    base = _normalizar(texto)
    alertas = []
    for padrao, motivo in REGRAS:
        # padrões com letras maiúsculas diferenciam caixa (ex.: "Comenta IMPUGNAR")
        flags = 0 if re.search(r"\[A-Z\]", padrao) else re.I
        achado = re.search(padrao, base, flags)
        if achado:
            alertas.append(f'{motivo}: "{achado.group(0)}"')
    if "—" in texto:
        alertas.append("travessão (—) no texto")
    return alertas


def verificar_post(post: dict) -> list[str]:
    partes = [post.get(k, "") for k in ("titulo", "subtitulo", "chamada_final", "legenda")]
    for slide in post.get("slides", []):
        partes += [slide.get("titulo", ""), slide.get("texto", "")]
    return verificar("\n".join(partes))
