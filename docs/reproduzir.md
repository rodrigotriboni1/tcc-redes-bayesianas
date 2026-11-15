# Como reproduzir

Passo a passo para gerar de novo todos os arquivos de `resultados/`. Vira o apêndice "Como reproduzir" da monografia.

Tudo roda a partir da raiz do repositório, sem interação, com Python 3.12 e as dependências travadas pelo `uv`.

**Situação em 15/11/2026.** Só `codigo/preparar_sgc.py` existe. Os demais scripts nascem das issues em `docs/issues/`, e cada seção abaixo vale só depois do merge da issue correspondente. A coluna "Issue" diz qual.

## 1. Ambiente

```bash
uv sync --frozen
```

`--frozen` instala exatamente o que está no `uv.lock`, incluindo `pgmpy` 1.1.2. Não atualize: a API do `pgmpy` mudou entre 1.0 e 1.1.2.

## 2. Ordem de execução

Cada script grava só em `resultados/` (o `preparar_sgc.py` grava em `dados/processados/`). Rodar duas vezes gera arquivos CSV e JSON idênticos byte a byte; toda aleatoriedade usa a semente 2026.

| # | Passo | Comando | Grava | Issue |
|---|---|---|---|---|
| 1 | Divisão dev/teste | `uv run python codigo/preparar_sgc.py` | `dados/processados/sgc.csv`, `dev.csv`, `teste.csv`, `SHA256SUMS` | já existe |
| 3 | Predições no dev | `uv run python codigo/modelos.py` | `predicoes_dev.csv`, `cortes.json` | 01 |
| 4 | Métricas e calibração | `uv run python codigo/avaliar.py` | `metricas_dev.csv`, `calibracao_dev.png` | 02 |
| 5 | Evidência incompleta | `uv run python codigo/modelos.py --ocultar` e depois `uv run python codigo/avaliar.py --ocultar` | `predicoes_dev_oculta.csv`, `evidencia_incompleta.csv` | 03 |
| 6 | Camada de decisão | `uv run python codigo/decisao.py` | `politicas_dev.csv`, `resumo_politicas_dev.csv` | 04 |
| 7 | Sensibilidade | `uv run python codigo/sensibilidade.py` | `sensibilidade.csv`, `sensibilidade.png` | 05 |
| 8 | Demonstração | `uv run python codigo/demo.py <record_id> [--modelo nb\|tan\|logreg]` | nada, imprime no terminal | 06 |

O passo 4 lê `predicoes_dev.csv` e o 6 também; por isso a ordem acima. Os passos 2, 9 e 10 do plano não aparecem aqui: o 2 é um teste de fumaça que abre o `modelos.py`, o 9 (hill climbing) é opcional, e o 10 está na seção 5.

O passo 1 só precisa ser repetido se `dados/brutos/` mudar. Como a divisão é determinística, rodá-lo de novo deve reproduzir os mesmos hashes de `dados/processados/SHA256SUMS`.

## 3. Autotestes

Cada script tem um modo `--verificar` que confere contas com resposta conhecida e não grava nada:

```bash
uv run python codigo/modelos.py --verificar
uv run python codigo/avaliar.py --verificar
uv run python codigo/decisao.py --verificar
uv run python codigo/sensibilidade.py --verificar
uv run python codigo/test_decisao.py
```

O `test_decisao.py` usa só `assert` e inclui o exemplo da apresentação: com p = 0,20, +100 e −400, UE(aprovar) = 0; com perda de 600, UE(aprovar) = −40.

## 4. Conferir que reproduziu

Os arquivos gerados são commitados junto com o código. Depois de rodar tudo, o Git diz se algo mudou:

```bash
git status --short resultados/
git diff --exit-code -- 'resultados/*.csv' 'resultados/*.json'
```

Saída vazia e código 0 significam que os CSV e JSON são idênticos aos commitados. Os PNG **não** são comparados byte a byte: nunca se verificou se saem idênticos entre execuções.

Para tudo de uma vez, na ordem do gate da factory (hashes dos dados, buscas por uso proibido, autotestes, scripts do zero, comparação com `resultados/`):

```bash
bash factory/checks.sh
```

Estimativa de cerca de 1 minuto. Não foi medido.

## 5. Teste final

Este passo **não** é para agentes nem para reproduzir à toa. É feito pelo autor, à mão, uma única vez, depois do commit de congelamento.

1. Reler todo o código e escolher, antes do congelamento, o modelo da tabela 2×2 e se a calibração entra (ver [decisoes.md](decisoes.md), seção 6).
2. Fazer o commit de congelamento e anotar o hash.
3. Rodar, nesta ordem:

```bash
uv run python codigo/modelos.py --final <arquivo do teste>
uv run python codigo/avaliar.py --final
uv run python codigo/decisao.py --final
```

O caminho do arquivo é argumento obrigatório de `modelos.py --final`; nenhum nome de arquivo de teste está no código. Se `resultados/predicoes_teste.csv` já existir, o script recusa e não sobrescreve.

Saídas: `predicoes_teste.csv`, `metricas_teste.csv`, `calibracao_teste.png`, `politicas_teste.csv`, `resumo_politicas_teste.csv`. Os intervalos usam bootstrap com 2000 reamostras e semente 2026.

## 6. O que a reprodução não cobre

- O teste e os dados brutos: a divisão sai de `dados/brutos/` com a semente, mas nenhum agente os lê.
- Valores de métrica: reproduzir confere que os arquivos são idênticos, não que o modelo é bom. Resultado ruim é resultado e vai para a monografia como saiu.
- Tempo de `uv sync` num ambiente novo e tempo total do modo `--ocultar`: não medidos.
