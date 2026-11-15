# 02: Calcular métricas e diagrama de calibração no dev

Onda 2. Depende da issue 01 já no `main`. Pode rodar em paralelo com a 04.

## Objetivo

Criar `codigo/avaliar.py`, que lê as predições do dev e grava a tabela de métricas e o diagrama de calibração. Passo 4 do `PLANO.md`.

## Contexto

- Ler antes: `AGENTS.md`; `PLANO.md`, item 6 (métricas).
- Cria: `codigo/avaliar.py`, `resultados/metricas_dev.csv`, `resultados/calibracao_dev.png`.
- Não altera `modelos.py`.
- Tamanho: um PR só.

## Entradas

| Arquivo | Uso |
|---|---|
| `resultados/predicoes_dev.csv` | `kredit`, `fold`, `p_nb`, `p_tan`, `p_logreg` |

## Saídas

| Arquivo | Conteúdo |
|---|---|
| `resultados/metricas_dev.csv` | 4 linhas (`nb`, `tan`, `logreg`, `taxa_base`): média e desvio, entre as 5 partições, de ROC-AUC, PR-AUC, Brier, log loss e erro de calibração |
| `resultados/calibracao_dev.png` | Diagrama de calibração dos três modelos |

## Comportamento

1. Lê as predições e confere colunas, vazios e faixa das probabilidades; entrada inválida encerra com mensagem.
2. Para cada modelo e cada partição, calcula ROC-AUC, PR-AUC (`average_precision_score`), Brier, log loss e erro de calibração (10 faixas de mesma largura), com ruim como classe positiva.
3. Acrescenta a linha `taxa_base`: previsão constante igual à proporção de ruins das outras quatro partições.
4. Grava média e desvio amostral das 5 partições.
5. Desenha o diagrama com as 800 predições juntas, diagonal de referência e uma curva por modelo.
6. Imprime os avisos.
7. No modo `--verificar`, confere a conta do erro de calibração em dois casos de resposta conhecida.

## Critérios de aceitação

Os da seção 4, issue 02, de `docs/criterios-de-aceite.md` (itens 1 a 11), sem acréscimo. Valem também G1 a G9.

## Avisos (não são critérios)

- `AVISO: brier de <modelo> >= taxa_base`
- `AVISO: roc_auc de <modelo> < 0,5`

## Fora do escopo

Calibração isotônica ou de Platt, intervalo por bootstrap, apontar "melhor modelo", testes estatísticos, métricas de política, mexer em `modelos.py`.

## Decisões já tomadas (não perguntar, não mudar)

- O script nunca treina: não importa `pgmpy` nem `modelos`.
- O erro de calibração da tabela é a média por partição; o diagrama junta as 800 predições. Os dois não coincidem e isso é esperado.
- Calibrar ou não é decisão do autor, tomada depois de ler esta tabela.

## Hipóteses a confirmar pelo autor

- Estilo do gráfico (cores, tamanho) fica a critério do construtor, desde que os eixos estejam em português.

## Descrição do PR deve conter

`## O que este script faz`, `## Como rodar`, `## Avisos impressos`.
