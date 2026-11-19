# TCC: redes bayesianas e utilidade esperada

Trabalho de conclusão de curso de Rodrigo Mialichi Triboni (Engenharia de Controle e Automação, UFU).

Uma rede bayesiana estima a probabilidade de um crédito ser ruim, e uma camada de utilidade esperada escolhe a ação: aprovar, rejeitar ou encaminhar para análise manual. Os dados são o South German Credit (1000 créditos). O repositório é um conjunto de scripts Python que leem CSV e gravam tabelas e figuras. Não há frontend, servidor nem banco de dados.

## O que o experimento faz

1. Divide a base em desenvolvimento (800 linhas) e teste final (200 linhas), com semente 2026.
2. Treina três modelos: Naive Bayes, TAN (ambos redes bayesianas, via `pgmpy`) e regressão logística como referência.
3. Mede discriminação (ROC-AUC, PR-AUC), erro de probabilidade (Brier) e calibração (ECE).
4. Compara três políticas de decisão por utilidade esperada, com a matriz de `config/utilidade.json`.
5. Roda o teste final uma única vez. Essa execução já foi feita; os resultados estão em `resultados/*_teste*`.

## Requisitos

- Python 3.12 ou mais novo.
- [uv](https://docs.astral.sh/uv/) (gerenciador de ambiente). Instalar: `brew install uv` (macOS) ou `curl -LsSf https://astral.sh/uv/install.sh | sh`.
- Git e Bash. Testado no macOS; deve funcionar em Linux.

Não precisa de GPU, internet depois da instalação, nem de conta em serviço nenhum.

## Como executar

Tudo roda a partir da raiz do repositório.

**1. Clonar e instalar (cerca de 1 a 2 minutos na primeira vez)**

```bash
git clone https://github.com/rodrigotriboni1/tcc-redes-bayesianas.git
cd tcc-redes-bayesianas
uv sync --frozen
```

`--frozen` instala exatamente as versões do `uv.lock` (inclui `pgmpy` 1.1.2). Não atualize: a API do `pgmpy` mudou entre as versões 1.0 e 1.1.2.

**2. Conferir que o ambiente funciona (cerca de 1 minuto)**

```bash
uv run python codigo/modelos.py --verificar
uv run python codigo/avaliar.py --verificar
uv run python codigo/sensibilidade.py --verificar
uv run python codigo/test_decisao.py
```

Esperado: três linhas `verificar: ok` e `test_decisao: todos os testes passaram`. Nada é gravado. Um `FutureWarning` do `pgmpy` pode aparecer; é só aviso da biblioteca, ignore.

**3. Gerar os resultados de desenvolvimento, na ordem**

```bash
uv run python codigo/modelos.py                 # predições P(ruim) de cada modelo
uv run python codigo/avaliar.py                 # métricas e figura de calibração
uv run python codigo/modelos.py --ocultar       # evidência incompleta
uv run python codigo/avaliar.py --ocultar
uv run python codigo/decisao.py                 # políticas de decisão
uv run python codigo/sensibilidade.py           # variação da matriz de utilidade
uv run python codigo/modelos.py --selecao       # estudo secundário de seleção
uv run python codigo/avaliar.py --selecao
```

Os arquivos saem em `resultados/`. A ordem importa: `avaliar.py` e `decisao.py` leem o que `modelos.py` gravou.

**4. Conferir que reproduziu**

```bash
git status --short resultados/
git diff --exit-code -- 'resultados/*.csv' 'resultados/*.json'
```

Saída vazia e código 0: os CSV e JSON são idênticos aos commitados (a execução é determinística). As figuras PNG não são comparadas byte a byte.

**5. Tudo de uma vez**

```bash
bash factory/checks.sh
```

Confere os hashes dos dados, roda os autotestes, refaz os scripts do zero e compara com `resultados/`. Termina com "tudo certo" e código 0.

## Ver uma decisão de crédito

```bash
uv run python codigo/demo.py sgc-0000 --modelo tan
```

Imprime no terminal as variáveis do caso, P(ruim) de cada modelo, a utilidade esperada de cada ação e a ação recomendada. O `record_id` (`sgc-0000` a `sgc-0999`, só os do desenvolvimento) vem da primeira coluna de `dados/processados/dev.csv`; `--modelo` aceita `nb`, `tan` ou `logreg`. Nada é gravado.

## Teste final

Já foi executado uma única vez, em 17/11/2026, depois do congelamento do código (commit `49d77ff`). **Não rode de novo.** O `modelos.py --final` recusa sobrescrever `resultados/predicoes_teste.csv`, e os números da monografia vêm dessa execução.

## Onde está cada coisa

| Pasta | Conteúdo |
|---|---|
| `codigo/` | os scripts do experimento |
| `config/` | matriz de utilidade (`utilidade.json`) |
| `dados/` | base South German Credit e a divisão em dev e teste |
| `resultados/` | tabelas e figuras geradas, commitadas junto com o código |
| `monografia/` | texto da monografia, referências e slides da defesa |
| `frontend/` | painel web só de leitura para a defesa; mostra os resultados já gerados, sem alterar o experimento (`cd frontend && npm install && npm run build && npm run preview`) |
| `docs/` | documentação do projeto |
| `factory/`, `.claude/` | ferramentas de processo (revisão automática de PRs); não fazem parte do experimento |

## Documentos

| Para | Leia |
|---|---|
| Pergunta, algoritmos, pastas e passos | [PLANO.md](PLANO.md) |
| Passo a passo completo de reprodução | [docs/reproduzir.md](docs/reproduzir.md) |
| Como os scripts se encaixam | [docs/arquitetura.md](docs/arquitetura.md) |
| O que foi decidido, por quê e por quem | [docs/decisoes.md](docs/decisoes.md) |
| Como cada resultado será lido (escrito antes dos resultados) | [docs/plano-de-analise.md](docs/plano-de-analise.md) |
| Termos e dicionário das variáveis | [docs/glossario.md](docs/glossario.md) |
| Regras de quem escreve código aqui | [AGENTS.md](AGENTS.md) |

## Problemas comuns

- `uv: command not found`: instale o uv (veja Requisitos) e abra um terminal novo.
- Erro de import do `pgmpy`: o ambiente não está em 1.1.2. Rode `uv sync --frozen` de novo.
- `bash factory/checks.sh` falha por diferença em `resultados/`: algum script foi rodado com outra versão de dependência ou o arquivo foi editado. Rode `git diff resultados/` para ver qual.

Este repositório substitui os repositórios `lazylabel` e `lazylabel-v2`, que ficam como arquivo.
