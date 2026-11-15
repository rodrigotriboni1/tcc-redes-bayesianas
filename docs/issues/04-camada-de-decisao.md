# 04: Escolher a ação por utilidade esperada

Onda 2. Depende da issue 01 já no `main`. Pode rodar em paralelo com a 02.

## Objetivo

Criar a camada de decisão: a matriz de utilidade em arquivo, a conta da utilidade esperada, a regra de limiar fixo e a comparação das políticas no dev. Passo 6 do `PLANO.md`.

## Contexto

- Ler antes: `AGENTS.md`; `PLANO.md`, item 5 (fórmula, matriz proposta, regra de desempate, "o que o trabalho afirma").
- Cria: `codigo/decisao.py`, `codigo/test_decisao.py`, `config/utilidade.json`, `resultados/politicas_dev.csv`, `resultados/resumo_politicas_dev.csv`.
- Tamanho: um PR só.

## Entradas

| Arquivo | Uso |
|---|---|
| `resultados/predicoes_dev.csv` | `record_id`, `kredit`, `p_nb`, `p_tan`, `p_logreg` |
| `config/utilidade.json` | Utilidade de cada ação em caso bom e em caso ruim |

## Saídas

| Arquivo | Conteúdo |
|---|---|
| `config/utilidade.json` | `aprovar` 100 / −400; `rejeitar` 0 / 0; `analise_manual` 60 / −40; campo `hipoteses` |
| `resultados/politicas_dev.csv` | 800 linhas: `record_id,kredit` e 6 colunas `acao_<nb|tan|logreg>_<ue|limiar>` |
| `resultados/resumo_politicas_dev.csv` | 6 linhas: `modelo,regra,utilidade_media,n_aprovar,n_rejeitar,n_analise_manual,n_mudam_vs_outra_regra` |

## Comportamento

1. `decisao.py` lê a matriz do JSON; nenhum valor de utilidade fica no código.
2. Para uma probabilidade de ruim `p`, calcula `UE(a) = (1 − p)·U(a, bom) + p·U(a, ruim)` de cada ação e escolhe a maior; em empate, análise manual, depois rejeitar, depois aprovar.
3. A regra de limiar fixo aprova se `p < 0,5` e rejeita caso contrário.
4. Aplica as duas regras às probabilidades dos três modelos e grava a ação de cada caso.
5. Grava o resumo: utilidade média obtida (usando o `kredit` real e a matriz), contagem de cada ação e quantos casos mudam de ação entre as duas regras.
6. `test_decisao.py` confere a conta com `assert`, sem ler dados.
7. Imprime o aviso.

## Critérios de aceitação

Os da seção 4, issue 04, de `docs/criterios-de-aceite.md` (itens 1 a 16), sem acréscimo. Valem também G1 a G9.

## Avisos (não são critérios)

- `AVISO: a ação <x> não aparece em <modelo>/<regra>`

## Fora do escopo

Escolher modelo ou "melhor política", mudar os valores da matriz, sensibilidade, gráficos, quarta ação, analista que erra, conjunto de teste, calibrar probabilidades.

## Decisões já tomadas (não perguntar, não mudar)

- Os valores da matriz são demonstrativos e estão pendentes de aprovação do orientador. O código tem de funcionar com outra matriz sem alteração.
- As políticas são calculadas para os três modelos. Qual rede vai para o texto é escolha do autor.
- Depois do merge, `config/utilidade.json` e `codigo/test_decisao.py` passam a ser arquivos protegidos.

## Hipóteses a confirmar pelo autor

- Nomes das ações no arquivo: `aprovar`, `rejeitar`, `analise_manual`.
- `n_mudam_vs_outra_regra` conta os casos em que a ação difere entre `ue` e `limiar` para o mesmo modelo.

## Descrição do PR deve conter

`## O que este script faz`, `## Como rodar`, `## Avisos impressos`.
