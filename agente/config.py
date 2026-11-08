"""Carrega o perfil (config/perfil.yaml), a skill e os caminhos do projeto."""
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml

# Horário de Brasília (UTC-3; sem horário de verão desde 2019)
FUSO = timezone(timedelta(hours=-3))


def hoje() -> date:
    """Data de hoje no horário de Brasília (o GitHub roda no horário UTC)."""
    return datetime.now(FUSO).date()


def agora() -> datetime:
    """Data e hora atuais no horário de Brasília."""
    return datetime.now(FUSO)

RAIZ = Path(__file__).resolve().parent.parent
PASTA_CONFIG = RAIZ / "config"
PASTA_PROMPTS = RAIZ / "prompts"
PASTA_FILA = RAIZ / "posts" / "fila"
PASTA_PUBLICADOS = RAIZ / "posts" / "publicados"
PASTA_IMAGENS = RAIZ / "posts" / "imagens"
PASTA_FOTOS = RAIZ / "assets" / "fotos"
PASTA_SKILLS = RAIZ / "skills"


def carregar_perfil() -> dict:
    with open(PASTA_CONFIG / "perfil.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _sem_frontmatter(texto: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n", "", texto, flags=re.S)


def carregar_skill(nome: str = "marketing-juridico") -> str:
    """SKILL.md + todas as referências da skill, em um único texto."""
    pasta = PASTA_SKILLS / nome
    partes = [_sem_frontmatter((pasta / "SKILL.md").read_text(encoding="utf-8"))]
    for ref in sorted((pasta / "references").glob("*.md")):
        partes.append(f"<!-- {ref.name} -->\n" + ref.read_text(encoding="utf-8"))
    return "\n\n---\n\n".join(partes)


def carregar_prompt_sistema() -> str:
    base = (PASTA_PROMPTS / "sistema.md").read_text(encoding="utf-8")
    return base + "\n\n---\n\n" + carregar_skill()
