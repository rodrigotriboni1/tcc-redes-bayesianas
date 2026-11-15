# 01: Gerar as predições dos três modelos no dev

Onda 1. Não depende de outra issue.

## Objetivo

Criar `codigo/modelos.py`, que treina Naive Bayes, TAN e regressão logística com validação cruzada em 5 partições sobre o dev e grava a probabilidade de crédito ruim de cada caso. Passos 2 e 3 do `PLANO.md`.

## Contexto

- Ler antes: `AGENTS.md`; `PLANO.md`, itens 3 (nomes do `pgmpy` 1.1.2), 4 (dados) e 5 (algoritmos).
- Cria: `codigo/modelos.py`, `resultados/predicoes_dev.csv`, `resultados/cortes.json`, `resultados/tan_arestas.csv`.
- Apaga: `codigo/baseline_logreg.py`, depois de levar a função `build()` para `modelos.py` sem alteração.
- Tamanho: um PR só. Não dividir e não ampliar.

## Entradas

| Arquivo | Uso |
|---|---|
| `dados/processados/dev.csv` | 800 linhas; `record_id`, 20 variáveis, `kredit` (0 = ruim) |

## Saídas

| Arquivo | Conteúdo |
|---|---|
| `resultados/predicoes_dev.csv` | 800 linhas: `record_id,kredit,fold,p_nb,p_tan,p_logreg`; cada `p_*` é a probabilidade de ruim |
| `resultados/cortes.json` | Cortes de `laufzeit`, `hoehe` e `alter` aprendidos no dev inteiro |
| `resultados/tan_arestas.csv` | Arestas do TAN aprendido em cada partição: `fold,origem,destino` |

## Comportamento

1. Lê o dev e divide em 5 partições estratificadas com semente 2026, uma única vez; as mesmas partições servem aos três modelos.
2. Para cada partição, usa as outras quatro como treino:
   - aprende os cortes em tercis das 3 variáveis contínuas só no treino e transforma treino e validação em faixas 0, 1, 2;
   - treina o Naive Bayes como rede em estrela e o TAN, ambos com prior BDeu de tamanho equivalente 5 e lista fixa de estados;
   - treina a regressão logística com `build()`;
   - calcula a probabilidade de ruim de cada linha da validação.
3. Grava as predições na ordem do `dev.csv` e, em `tan_arestas.csv`, as arestas do TAN de cada partição.
4. Aprende os cortes no dev inteiro e grava `cortes.json`.
5. Expõe a função `prever(treino, alvo, modelo, ocultar=None)`, usada pelas issues 03, 06 e 07. Nesta issue, `ocultar` fica sem implementação além do valor `None`.
6. No modo `--verificar`, roda os autotestes e não grava nada.

## Critérios de aceitação

Os da seção 4, issue 01, de `docs/criterios-de-aceite.md` (itens 1 a 11), sem acréscimo. Valem também as regras comuns G1 a G9 da seção 3.

## Avisos (não são critérios)

Nenhum nesta issue.

## Fora do escopo

`--ocultar`, `--final`, hill climbing, calibração, métricas, gráficos, salvar modelo em arquivo, busca de hiperparâmetros, seleção ou criação de variáveis, mexer em `preparar_sgc.py`, opções de linha de comando além de `--verificar`.

## Decisões já tomadas (não perguntar, não mudar)

- Constantes congeladas do `AGENTS.md`.
- Naive Bayes é `DiscreteBayesianNetwork` em estrela; a classe `pgmpy.models.NaiveBayes` falha ao prever na 1.1.2.
- A estrutura do TAN é refeita em cada partição e pode diferir entre elas.
- Estados fixos: todos os valores que aparecem no dev inteiro; faixas das contínuas sempre `[0, 1, 2]`.

## Hipóteses a confirmar pelo autor

- Tolerâncias numéricas dos autotestes (1e-12 e 1e-9).
- O tempo limite de 60 s foi estimado, não medido com a regressão logística.

## Descrição do PR deve conter

`## O que este script faz`, `## Como rodar`, `## Avisos impressos`.
