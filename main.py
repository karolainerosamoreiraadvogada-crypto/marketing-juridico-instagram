"""Agente de Marketing Jurídico - linha de comando.

  python main.py gerar [--quantidade 3] [--tema "usucapião"] [--area "Direito Imobiliário"]
  python main.py gerar-mes [--mes 2026-11]   (programação do mês para aprovação)
  python main.py kpi-coletar                 (métricas do Instagram)
  python main.py kpi-relatorio [--dias 30]
  python main.py listar
  python main.py publicar [--simular] [--max 1]
  python main.py demo                 (gera imagens de exemplo, sem usar API)
  python main.py verificar-token
  python main.py renovar-token
"""
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from agente import fila
from agente.config import RAIZ, carregar_perfil


def carregar_env(arquivo: Path = RAIZ / ".env") -> None:
    """Lê chaves do arquivo .env local (nunca enviado ao GitHub)."""
    if not arquivo.exists():
        return
    for linha in arquivo.read_text(encoding="utf-8-sig").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#") and "=" in linha:
            nome, valor = linha.split("=", 1)
            valor = valor.strip().strip('"').strip("'")
            if valor:
                os.environ.setdefault(nome.strip(), valor)


carregar_env()


def url_base_imagens() -> str:
    """URL pública onde o Instagram vai buscar as imagens."""
    if os.environ.get("URL_IMAGENS"):
        return os.environ["URL_IMAGENS"].rstrip("/") + "/"
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        sys.exit("Defina URL_IMAGENS ou rode dentro do GitHub Actions.")
    ref = os.environ.get("GITHUB_REF_NAME", "main")
    return f"https://raw.githubusercontent.com/{repo}/{ref}/"


def cmd_gerar(args):
    from agente.gerador import gerar_lote, resumo_markdown

    from agente.revisor import resumo

    posts = gerar_lote(args.quantidade, args.tema, args.area)
    for p in posts:
        print(f"[novo] {p['data_publicacao']}  {p['area']}  {p['formato']}  {p['titulo']}")
        print(f"       {resumo(p)}")
    if args.resumo_pr:
        base = os.environ.get("URL_IMAGENS_PR", "")
        Path(args.resumo_pr).write_text(resumo_markdown(posts, base), encoding="utf-8")


def cmd_gerar_mes(args):
    from datetime import date
    from agente.gerador import gerar_mes, resumo_markdown
    from agente.revisor import resumo

    if args.mes:
        ano, mes = (int(x) for x in args.mes.split("-"))
    else:
        from agente.config import hoje
        dia = hoje()
        ano, mes = dia.year, dia.month
    posts = gerar_mes(ano, mes)
    print(f"Programação de {mes:02d}/{ano}: {len(posts)} posts")
    for p in posts:
        print(f"[novo] {p['data_publicacao']}  {p['area']}  {p['formato']}  {p['titulo']}")
        print(f"       {resumo(p)}")
    if args.resumo_pr:
        base = os.environ.get("URL_IMAGENS_PR", "")
        Path(args.resumo_pr).write_text(resumo_markdown(posts, base), encoding="utf-8")


def cmd_kpi_coletar(_args):
    from agente.kpi import coletar
    foto = coletar()
    print(f"Métricas coletadas: {foto['seguidores']} seguidores, {len(foto['posts'])} posts.")


def cmd_kpi_relatorio(args):
    from agente.kpi import relatorio
    texto = relatorio(args.dias)
    if args.saida:
        Path(args.saida).parent.mkdir(parents=True, exist_ok=True)
        Path(args.saida).write_text(texto, encoding="utf-8")
    print(texto)


def cmd_listar(_args):
    posts = fila.na_fila()
    if not posts:
        print("Fila vazia.")
    for p in posts:
        print(f"{p['data_publicacao']}  {p['formato']:9}  {p.get('titulo', p['id'])}")


def hashtags_finais(post: dict, maximo: int = 5) -> list[str]:
    """As mais específicas do tema + hashtags regionais do escritório (máximo 5)."""
    fixas = carregar_perfil().get("hashtags_fixas", ["#advocacia", "#cornelioprocopio", "#parana"])
    temas = [h for h in post.get("hashtags", []) if h not in fixas]
    regional = "#cornelioprocopio"
    return list(dict.fromkeys(temas[: maximo - 1] + [regional]))[:maximo]


def turno_atual() -> str:
    """Turno pelo horário de Brasília: 7h-11h manhã (posts com "horario": "10h"),
    12h-16h Stories (14h), 17h-19h tarde (posts com "horario": "18h"), demais horas feed
    das 21h (inclui atrasos do GitHub após a meia-noite)."""
    from agente.config import agora
    hora = agora().hour
    if 7 <= hora < 12:
        return "manha"
    if 12 <= hora < 17:
        return "stories"
    return "tarde" if 17 <= hora < 20 else "feed"


TURNO_DO_HORARIO = {"10h": "manha", "18h": "tarde"}


def do_turno(post: dict, turno: str) -> bool:
    if turno == "todos":
        return True
    if post.get("horario") in TURNO_DO_HORARIO:
        return turno == TURNO_DO_HORARIO[post["horario"]]
    if post.get("formato") == "stories":
        return turno in ("stories", "tarde")  # 18h: segunda chance se o GitHub atrasar muito
    return turno == "feed"


def cmd_publicar(args):
    for p in fila.atrasados():
        print(f"[atrasado, NÃO publicado] {p['data_publicacao']} {p['id']}: "
              "defina nova data no JSON para publicar.")
    # Turno: a execução das 10h publica só posts marcados "horario": "10h"; a das 14h, só
    # Stories; a das 21h, o restante do feed (assim, cada peça sai no seu horário).
    turno = args.turno or turno_atual()
    pendentes = [p for p in fila.vencidos() if do_turno(p, turno)]
    # primeiro o que é deste horário (ex.: post das 18h); Stories atrasados vêm depois
    pendentes.sort(key=lambda p: (TURNO_DO_HORARIO.get(p.get("horario")) != turno, p["data_publicacao"]))
    pendentes = pendentes[: args.max]
    if not pendentes:
        print(f"Nenhum post programado para hoje (turno: {turno}).")
        return

    from agente import facebook
    alcance = carregar_perfil().get("alcance", {})
    local = alcance.get("localizacao_id")
    base = url_base_imagens()
    ig = fb = None
    if not args.simular:
        from agente.instagram import Instagram
        ig = Instagram()
        fb = facebook.Facebook() if facebook.configurado() else None

    for post in pendentes:
        urls = [base + img for img in post["imagens"]]
        tags = hashtags_finais(post, alcance.get("max_hashtags", 5))
        legenda = (post.get("legenda", "") + "\n\n" + " ".join(tags)).strip()
        video = base + post["video"] if post.get("formato") == "reel" else None
        if args.simular:
            destino = "Instagram + Facebook" if facebook.configurado() else "Instagram"
            print(f"[simulação] {post['id']} -> {destino}\n  vídeo: {video}\n  imagens: {urls}\n"
                  f"  local: {local}  hashtags: {tags}\n  story de aviso: {post.get('story_aviso')}\n")
            continue
        if post.get("formato") == "stories":
            ids = [ig.publicar_story(u) for u in urls]  # telas na ordem do roteiro
            media_id = ",".join(ids)
        elif video:
            media_id = ig.publicar_reel(video, legenda, urls[0] if urls else None, local)
        else:
            media_id = ig.publicar(urls, legenda, local)
        post["instagram_id"] = media_id
        post["publicado_em"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        # Story "NOVO POST NO FEED": uma falha aqui não afeta o post já publicado
        if post.get("story_aviso") and alcance.get("story_aviso", True):
            try:
                post["story_aviso_id"] = ig.publicar_story(base + post["story_aviso"])
            except Exception as erro:  # noqa: BLE001
                post["story_aviso_erro"] = str(erro)[:300]
                print(f"[story de aviso] falhou: {erro}")
        # Facebook: uma falha aqui não desfaz nem bloqueia a publicação no Instagram
        if fb:
            try:
                post["facebook_id"] = fb.publicar(post, urls, video, legenda)
            except Exception as erro:  # noqa: BLE001
                post["facebook_erro"] = str(erro)[:500]
                print(f"[facebook] falhou: {erro}")
        fila.mover_para_publicados(post)
        print(f"[publicado] {post['id']} (instagram {media_id}, facebook {post.get('facebook_id', '-')})")


def cmd_demo(_args):
    from agente.imagem import gerar_imagens

    post = {
        "id": "exemplo",
        "formato": "carrossel",
        "area": "Direito Imobiliário",
        "titulo": "Você pagou pelo imóvel. Mas ele é *seu*?",
        "subtitulo": "Entenda a diferença entre contrato, escritura e registro.",
        "foto_busca": "house keys contract",
        "slides": [
            {"titulo": "O contrato não basta",
             "texto": "Contrato particular e recibo comprovam o negócio, mas não "
                      "transferem a propriedade do imóvel."},
            {"titulo": "A escritura formaliza",
             "texto": "A escritura pública, lavrada em tabelionato de notas, dá forma "
                      "oficial à compra e venda. Ainda assim, sozinha, ela não "
                      "transfere a propriedade."},
            {"titulo": "O registro transfere",
             "texto": "A propriedade só passa para o seu nome com o registro do título "
                      "na matrícula, no Cartório de Registro de Imóveis "
                      "(Código Civil, art. 1.245)."},
            {"titulo": "Por que isso importa",
             "texto": "Sem registro, o imóvel continua no nome do vendedor e pode ser "
                      "atingido por dívidas dele, além de dificultar venda, herança e "
                      "financiamento."},
        ],
        "chamada_final": "O seu imóvel já está registrado no seu nome?",
    }
    pasta = RAIZ / "posts" / "exemplo"
    for c in gerar_imagens(post, carregar_perfil(), pasta):
        print(c.relative_to(RAIZ))


def cmd_verificar_token(_args):
    from agente.instagram import Instagram
    print(Instagram().perfil())


def cmd_renovar_token(_args):
    from agente.instagram import Instagram
    if os.environ.get("GITHUB_ACTIONS"):
        sys.exit("Rode este comando no seu computador: o token apareceria no log público.")
    dados = Instagram().renovar_token()
    dias = int(dados.get("expires_in", 0)) // 86400
    print(f"Novo token válido por {dias} dias. Atualize o secret IG_ACCESS_TOKEN com:")
    print(dados["access_token"])


def main():
    p = argparse.ArgumentParser(description="Agente de Marketing Jurídico")
    sub = p.add_subparsers(dest="comando", required=True)

    g = sub.add_parser("gerar", help="cria novos posts na fila")
    g.add_argument("--quantidade", type=int)
    g.add_argument("--tema")
    g.add_argument("--area", help='ex.: "Direito Previdenciário" (padrão: rodízio por peso)')
    g.add_argument("--resumo-pr", help="grava resumo em Markdown (usado no Pull Request)")
    g.set_defaults(func=cmd_gerar)

    gm = sub.add_parser("gerar-mes", help="programação do mês inteiro para aprovação")
    gm.add_argument("--mes", help="AAAA-MM (padrão: mês atual)")
    gm.add_argument("--resumo-pr")
    gm.set_defaults(func=cmd_gerar_mes)

    sub.add_parser("kpi-coletar", help="coleta métricas do Instagram").set_defaults(func=cmd_kpi_coletar)
    kr = sub.add_parser("kpi-relatorio", help="relatório de KPIs")
    kr.add_argument("--dias", type=int, default=7)
    kr.add_argument("--saida")
    kr.set_defaults(func=cmd_kpi_relatorio)

    sub.add_parser("listar", help="mostra a fila").set_defaults(func=cmd_listar)

    pub = sub.add_parser("publicar", help="publica os posts do dia")
    pub.add_argument("--simular", action="store_true")
    pub.add_argument("--max", type=int, default=1)
    pub.add_argument("--turno", choices=["manha", "tarde", "feed", "stories", "todos"], help="padrão: pelo horário")
    pub.set_defaults(func=cmd_publicar)

    sub.add_parser("demo", help="gera imagens de exemplo").set_defaults(func=cmd_demo)
    sub.add_parser("verificar-token").set_defaults(func=cmd_verificar_token)
    sub.add_parser("renovar-token").set_defaults(func=cmd_renovar_token)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
