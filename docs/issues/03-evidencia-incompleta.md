# 03: Medir o efeito de esconder uma variável por vez

Onda 3. Depende das issues 01 e 02 já no `main`. Pode rodar em paralelo com a 05 e a 06. Primeira a cortar se o prazo apertar.

## Objetivo

Acrescentar o modo `--ocultar` a `modelos.py` e a `avaliar.py`: prever com uma variável escondida por vez e medir a queda de desempenho. Passo 5 do `PLANO.md`.

## Contexto

- Ler antes: `AGENTS.md`; `PLANO.md`, item 5 (linha "Evidência incompleta").
- Altera: `codigo/modelos.py`, `codigo/avaliar.py`.
- Cria: `resultados/predicoes_dev_oculta.csv`, `resultados/evidencia_incompleta.csv`.
- Tamanho: um PR só.

## Entradas

| Arquivo | Uso |
|---|---|
| `dados/processados/dev.csv` | Como na issue 01 |
| `resultados/predicoes_dev.csv`, `resultados/metricas_dev.csv` | Referência do desempenho completo |

## Saídas

| Arquivo | Conteúdo |
|---|---|
| `resultados/predicoes_dev_oculta.csv` | 48.000 linhas: `record_id,modelo,variavel_oculta,p_ruim` |
| `resultados/evidencia_incompleta.csv` | 60 linhas: `modelo,variavel_oculta,roc_auc,brier,delta_roc_auc,delta_brier` |

## Comportamento

1. `modelos.py --ocultar` usa as mesmas partições e os mesmos modelos treinados com todas as variáveis.
2. Para cada uma das 20 variáveis, prevê a validação sem ela:
   - nas redes, a coluna é retirada e a inferência usa a evidência restante;
   - na regressão logística, a coluna é preenchida com a mediana do treino (3 contínuas) ou a moda do treino (17 categóricas).
3. Grava as predições em formato longo, em ordem fixa.
4. `avaliar.py --ocultar` calcula ROC-AUC e Brier de cada par (modelo, variável), com a mesma agregação da issue 02, e a diferença para o desempenho completo.
5. Imprime o aviso.

## Critérios de aceitação

Os da seção 4, issue 03, de `docs/criterios-de-aceite.md` (itens 1 a 8), sem acréscimo. Valem também G1 a G9.

## Avisos (não são critérios)

- `AVISO: ocultar laufkont não piorou mais que ocultar telef em <modelo>`

## Fora do escopo

Esconder duas ou mais variáveis, valor ausente no treino, outras formas de imputação, gráfico, texto de "importância" de variáveis, opção de esconder na demonstração.

## Decisões já tomadas (não perguntar, não mudar)

- Os comandos sem `--ocultar` continuam gerando arquivos idênticos aos de antes.
- Nunca passar `NaN` às redes: a variável escondida é retirada.
- Esconder uma variável pode melhorar a métrica. Isso é resultado, não erro.

## Hipóteses a confirmar pelo autor

- O tempo total do modo `--ocultar` foi estimado em 15 a 30 s, não medido.

## Descrição do PR deve conter

`## O que este script faz`, `## Como rodar`, `## Avisos impressos`.
