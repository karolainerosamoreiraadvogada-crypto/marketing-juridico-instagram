# Agente de Marketing Jurídico para Instagram

Gera e publica posts informativos no Instagram de forma automática, **100% gratuita**,
respeitando o **Provimento 205/2021 da OAB**.

## Como funciona

```
Todo domingo                              Você revisa                Seg/qua/sex às 21h
┌───────────────────────────┐   PR   ┌────────────────────┐ merge ┌──────────────────────┐
│ 1. Gemini escreve         │ ─────▶ │ Pull Request com   │ ────▶ │ Publica no Instagram │
│ 2. Revisor: 10 etapas     │        │ imagens, legendas, │       │ o post do dia        │
│ 3. Filtro de termos OAB   │        │ fontes e relatório │       └──────────────────────┘
│ 4. Python gera as lâminas │        └────────────────────┘
└───────────────────────────┘
```

Nada é publicado sem a sua aprovação: **fazer o merge do Pull Request = aprovar os posts.**

| Peça | Ferramenta | Custo |
|---|---|---|
| Texto e revisão dos posts | Google Gemini API (plano gratuito) | R$ 0 |
| Fotos de fundo | Pexels API (gratuita) ou fotos próprias | R$ 0 |
| Lâminas (capa, conteúdo, encerramento) | Python + Pillow + Google Fonts | R$ 0 |
| Publicação | API oficial do Instagram | R$ 0 |
| Agendamento e hospedagem das imagens | GitHub Actions + repositório público | R$ 0 |

## Áreas (skill `marketing-juridico`)

| Área | Proporção |
|---|---|
| Direito Imobiliário: todas as formas de regularização (principal) | 50% |
| Direito Previdenciário: todos os benefícios | 20% |
| Direito Tributário: isenções, prescrição, decadência | 15% |
| Direito Empresarial | 15% |

Cada área tem sua tabela de lei, normativas e jurisprudência em
`skills/marketing-juridico/references/`. O agente só cita o que está nessas tabelas.
Mantenha-as atualizadas quando a legislação mudar.

## Estrutura

```
config/perfil.yaml        seus dados, cores, calendário e peso de cada área
prompts/sistema.md        papel do agente
skills/marketing-juridico skill: ética OAB, áreas, fontes, design, engajamento, 10 etapas
assets/fonts/             Bodoni Moda e Montserrat (licença livre OFL)
assets/fotos/             (opcional) suas fotos; subpastas por área, ex.: direito-imobiliario/
agente/                   código Python (gerador, revisor, imagem, fotos, instagram)
posts/fila/               posts aprovados aguardando a data
posts/publicados/         histórico do que já foi ao ar
posts/imagens/            imagens JPEG dos posts
.github/workflows/        automações (gerar e publicar)
```

## Configuração (uma única vez)

### 1. Chave gratuita do Gemini
1. Acesse https://aistudio.google.com/apikey e clique em **Create API key**.
2. Guarde a chave.

### 1.1 Chave gratuita do Pexels (fotos de fundo)
1. Crie uma conta em https://www.pexels.com/api/ e copie a chave.
2. Sem ela, as capas saem com fundo vinho liso (também elegante).

### 2. Instagram
1. No app do Instagram: **Configurações > Tipo de conta > Mudar para conta profissional**
   (Criador de conteúdo ou Empresa).
2. Em https://developers.facebook.com crie um app do tipo **Empresa** e adicione o
   produto **Instagram** > **API setup with Instagram login**.
3. Adicione sua conta, gere o token e copie:
   - o **ID da conta do Instagram** (número),
   - o **token de acesso** (vale 60 dias).
4. Permissões necessárias: `instagram_business_basic`, `instagram_business_content_publish`
   e `instagram_business_manage_insights` (para os KPIs).

> Enquanto o app estiver em modo de desenvolvimento, ele publica normalmente na sua
> própria conta. Não é preciso enviar o app para revisão da Meta.

### 3. GitHub
1. Crie um repositório **público** (necessário para o Instagram acessar as imagens e
   para o GitHub Actions ser ilimitado) e envie estes arquivos.
2. Em **Settings > Secrets and variables > Actions > Secrets**, crie:
   - `GEMINI_API_KEY`
   - `PEXELS_API_KEY` (opcional)
   - `IG_USER_ID`
   - `IG_ACCESS_TOKEN`
3. Em **Settings > Actions > General**, marque:
   - *Workflow permissions*: **Read and write permissions**
   - **Allow GitHub Actions to create and approve pull requests**

### 4. Personalize
Edite `config/perfil.yaml` com seu nome, OAB, @, cores e dias de publicação.

## Rotina automática

| Quando | O que acontece | Você faz |
|---|---|---|
| Dia 1º de cada mês, 8h | O agente gera **a programação do mês inteiro** (seg, qua e sex) e abre um Pull Request com o calendário, as imagens, as legendas, as fontes e a revisão de cada post | Revisa e faz o merge (= aprova) |
| Segunda, quarta e sexta, 21h | Publica o post do dia (carrossel ou Reels animado), **somente se aprovado** | Nada |
| Sábado, 14h | Publica os **Stories descontraídos** da semana, **somente se aprovados** | Nada |
| Todo dia, 19h | Coleta seguidores, alcance, curtidas, comentários, salvamentos e compartilhamentos | Nada |
| Domingo à noite | **Relatório semanal de KPIs** (abre uma Issue no GitHub, que chega por e-mail) | Lê e decide |
| Último dia do mês | **Relatório mensal de KPIs** com recomendações | Lê e decide |

Post aprovado tarde (até 2 dias após a data) ainda é publicado; depois disso ele
fica parado e precisa de nova data, para não "despejar" posts atrasados de uma vez.

Os aprendizados do relatório (melhores posts, melhor formato) entram
automaticamente na próxima programação.

### KPIs acompanhados

Seguidores e novos seguidores, posts publicados x planejados, alcance médio, taxa de
engajamento (interações ÷ alcance), curtidas, comentários, salvamentos e
compartilhamentos por post, desempenho por área e por formato. As metas ficam em
`config/perfil.yaml` (seção `kpis`) e devem ser revistas após o primeiro mês.

Para a coleta funcionar, o token do Instagram precisa também da permissão
`instagram_business_manage_insights`.

## Uso no dia a dia

- **Gerar posts agora:** aba *Actions* > *Gerar posts* > *Run workflow*
  (pode informar um tema específico).
- **Aprovar:** abra o Pull Request, revise imagens e legendas, edite o que quiser
  e clique em **Merge**.
- **Publicação:** automática, segunda, quarta e sexta às 21h, só nas datas aprovadas.
- **Testar sem publicar:** *Actions* > *Publicar no Instagram* > marque *simular*.

### Renovar o token (a cada ~50 dias)
No seu computador:
```bash
pip install -r requirements.txt
set IG_USER_ID=...
set IG_ACCESS_TOKEN=...
python main.py renovar-token
```
Copie o novo token para o secret `IG_ACCESS_TOKEN`.

## Comandos locais

```bash
python main.py demo                         # gera imagens de exemplo em posts/exemplo
python main.py gerar --quantidade 2         # precisa de GEMINI_API_KEY
python main.py listar                       # mostra a fila
python main.py publicar --simular           # mostra o que seria publicado
```

## Aviso ético

A revisão em 10 etapas e o filtro de termos (`agente/revisor.py` e
`agente/compliance.py`) reduzem muito o risco de erro, mas são **auxiliares**:
a inteligência artificial pode errar. A responsabilidade pelo conteúdo publicado é
da advogada. Revise todo post antes de aprovar, especialmente leis, prazos e valores.
Posts marcados "⚠️ REQUER ATENÇÃO" no Pull Request precisam de ajuste antes do merge.
