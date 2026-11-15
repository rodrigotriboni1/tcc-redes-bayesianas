# 07: Escrever o caminho do teste final, sem executá-lo

Onda 4. Depende das issues 01, 02, 03 e 04 já no `main`. Não roda em paralelo com nenhuma outra. Se a issue 03 for cortada, depende só de 01, 02 e 04.

## Objetivo

Acrescentar o modo `--final` a `modelos.py`, `avaliar.py` e `decisao.py`, para o autor rodar o teste final uma única vez depois do commit de congelamento. A factory escreve e testa esse caminho só com linhas do dev. Passo 10 do `PLANO.md`.

## Contexto

- Ler antes: `AGENTS.md`, regras duras 1 e 2; `PLANO.md`, item 4 (dados) e passo 10.
- Altera: `codigo/modelos.py`, `codigo/avaliar.py`, `codigo/decisao.py`.
- Não cria arquivo em `resultados/`.
- Tamanho: um PR só.

**Você não abre o arquivo de teste e não roda `--final` sobre ele.** Nem para conferir. O autoteste usa um arquivo falso feito de linhas do dev.

## Entradas

| Arquivo | Uso |
|---|---|
| `dados/processados/dev.csv` | Treino, o dev inteiro |
| `resultados/cortes.json` | Cortes das variáveis contínuas |
| Arquivo passado como argumento a `modelos.py --final` | Mesmas colunas do `dev.csv` |
| `config/utilidade.json` | Matriz de utilidade |

## Saídas (geradas só quando o autor executar)

| Arquivo | Conteúdo |
|---|---|
| `resultados/predicoes_teste.csv` | `record_id,kredit,p_nb,p_tan,p_logreg` |
| `resultados/metricas_teste.csv` | Uma linha por modelo e `taxa_base`: métricas com intervalo por bootstrap para ROC-AUC e Brier |
| `resultados/calibracao_teste.png` | Diagrama de calibração |
| `resultados/politicas_teste.csv`, `resultados/resumo_politicas_teste.csv` | Mesmo formato dos arquivos do dev |

## Comportamento

1. `modelos.py --final <arquivo>` treina os três modelos no dev inteiro, com os cortes de `cortes.json`, e prevê cada linha do arquivo recebido. O caminho é argumento obrigatório; o código não traz nome de arquivo de teste.
2. Se `resultados/predicoes_teste.csv` já existe, encerra com mensagem, sem sobrescrever.
3. `avaliar.py --final` calcula as métricas sobre `predicoes_teste.csv`, com intervalo por bootstrap de 2000 reamostras, semente 2026, percentis 2,5 e 97,5.
4. `decisao.py --final` aplica as duas regras de decisão às predições do teste.
5. O autoteste (`--verificar`) cria um arquivo falso com as 160 linhas da partição 0 do dev, em pasta temporária, e exercita o caminho inteiro sem gravar em `resultados/`.

## Critérios de aceitação

Os da seção 4, issue 07, de `docs/criterios-de-aceite.md` (itens 1 a 12), sem acréscimo. Valem também G1 a G9.

## Avisos (não são critérios)

Nenhum nesta issue.

## Fora do escopo

Executar sobre o teste de verdade, escolher modelo, calibrar, evidência incompleta no teste, sensibilidade no teste, qualquer mudança no treino dos modelos.

## Decisões já tomadas (não perguntar, não mudar)

- O teste final é rodado pelo autor, à mão, uma vez, depois do commit de congelamento.
- Nenhum arquivo `*_teste*` entra no PR.
- Os comandos sem `--final` continuam gerando arquivos idênticos aos de antes.

## Hipóteses a confirmar pelo autor

- Bootstrap com 2000 reamostras e intervalo percentil de 95%. Esses valores não estavam no plano; foram definidos nesta issue.
- A linha `taxa_base` usa a proporção de ruins do dev (0,30).
- Intervalo só para ROC-AUC e Brier.

## Descrição do PR deve conter

`## O que este script faz`, `## Como rodar`, `## Avisos impressos`.
