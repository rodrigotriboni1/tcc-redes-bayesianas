# Resultados de dev: baseline pré-estudo

Registro descritivo dos resultados gerados só com `dados/processados/dev.csv`. **Baseline pré-estudo:** resultados gerados pelo commit `808330e` de `main` (`git rev-parse --short origin/main` no momento da escrita). Nada aqui usa o teste final.

Convenções: cada número traz `arquivo` e `coluna` de origem. Frases interpretativas citam a linha da seção 4 de [plano-de-analise.md](plano-de-analise.md) que as autoriza (formato "§4, linha: ..."). Este texto não escolhe modelo nem propõe mudança de modelo, parâmetro, semente, faixa ou variável (`AGENTS.md`, regras 3 e 5). Os valores abaixo são médias e desvios entre as 5 partições; o dev tem 800 casos.

## 1. Métricas por modelo (`resultados/metricas_dev.csv`)

| modelo | roc_auc_media (desvio) | pr_auc_media (desvio) | brier_media (desvio) | log_loss_media (desvio) | ece_media (desvio) |
|---|---|---|---|---|---|
| nb | 0,789 (0,024) | 0,616 (0,049) | 0,171 (0,013) | 0,523 (0,035) | 0,093 (0,014) |
| tan | 0,742 (0,049) | 0,549 (0,076) | 0,200 (0,030) | 0,704 (0,136) | 0,152 (0,050) |
| logreg | 0,788 (0,021) | 0,649 (0,042) | 0,165 (0,012) | 0,504 (0,026) | 0,095 (0,031) |
| taxa_base | 0,500 (0,000) | 0,300 (0,000) | 0,210 (0,000) | 0,611 (0,000) | 0,000 (0,000) |

Colunas: `roc_auc_media`, `roc_auc_desvio`, `pr_auc_media`, `pr_auc_desvio`, `brier_media`, `brier_desvio`, `log_loss_media`, `log_loss_desvio`, `ece_media`, `ece_desvio`.

Leitura:

- A diferença de `roc_auc_media` entre nb (0,7890) e logreg (0,7880) é 0,001, menor que 0,03: tratada como ruído, nenhum dos dois "vence" (§4, linha "A diferença de ROC-AUC entre dois modelos é menor que 0,03").
- A diferença de `roc_auc_media` entre nb (0,7890) e tan (0,7423) é 0,047, e entre logreg (0,7880) e tan (0,7423) é 0,046; as duas passam de 0,03, então a regra de ruído não se aplica a esses pares. O plano não diz mais nada sobre esse caso; o desvio do tan (`roc_auc_desvio` 0,049) fica registrado ao lado.
- O `brier_media` dos três modelos (nb 0,171; tan 0,200; logreg 0,165) é menor que o da taxa base (0,210). A condição "igual ou maior que 0,21" não ocorre, então a frase "Não melhor que prever a taxa base" não é acionada (§4, linha "O Brier de um modelo é igual ou maior que o da taxa base").
- `ece_media` do tan é 0,152, o maior dos três modelos (nb 0,093; logreg 0,095). Reportado como saiu; não há correção de calibração (§4, linha "O erro de calibração de um modelo é alto"; decisão P1).

## 2. Políticas (`resultados/resumo_politicas_dev.csv`)

Regras: `ue` = utilidade esperada, três ações; `limiar` = corte 0,5, duas ações. Contagens sobre os 800 casos do dev.

| modelo | regra | utilidade_media | n_aprovar | n_rejeitar | n_analise_manual | n_mudam_vs_outra_regra |
|---|---|---|---|---|---|---|
| nb | ue | 32,625 | 274 | 171 | 355 | 355 |
| nb | limiar | 4,5 | 581 | 219 | 0 | 355 |
| tan | ue | 22,275 | 361 | 177 | 262 | 262 |
| tan | limiar | -3,125 | 590 | 210 | 0 | 262 |
| logreg | ue | 30,875 | 243 | 142 | 415 | 415 |
| logreg | limiar | 3,625 | 599 | 201 | 0 | 415 |

Leitura:

- A coluna `utilidade_media` da regra `ue` é maior que a da regra `limiar` nos três modelos (diferenças: nb 28,125; tan 25,4; logreg 27,25). Isso é uma diferença descritiva no dev, sem intervalo. Pelo plano, a comparação com intervalo só vale no teste final, e ela mistura modelo, representação e conjunto de ações; não é chamada de "efeito" da regra (seção 3, último parágrafo; seção 6, itens 1, 3 e 7).
- Na regra `ue`, `n_analise_manual` é 355 (nb), 262 (tan) e 415 (logreg), de 800. A regra `limiar` tem `n_analise_manual` igual a 0 porque só tem duas ações. Essa ressalva acompanha qualquer leitura da diferença (§4, linha "O intervalo exclui 0 a favor do limiar 0,5", ressalva sobre a regra fixa de duas ações).
- Nenhuma ação deixa de aparecer: as três colunas `n_*` da regra `ue` são maiores que zero nos três modelos, então o aviso de ação ausente não se aplica (§4, linha "Alguma ação não aparece numa política"). Na regra `limiar`, a ausência de `analise_manual` é a definição da regra.
- Em `n_mudam_vs_outra_regra`, o valor de cada modelo coincide com seu `n_analise_manual` da regra `ue` (355, 262, 415). Fato observado nas tabelas; este texto não interpreta o motivo.

`resultados/politicas_dev.csv` (800 linhas, uma por caso) contém a ação de cada caso por modelo e regra (`acao_*_ue`, `acao_*_limiar`), e as colunas `segunda_*` e `dif_ue_*` (não interpretadas aqui). Os totais de `resumo_politicas_dev.csv` somam 800 em cada linha (por exemplo nb ue: 274 + 171 + 355).

## 3. Sensibilidade dos limiares (`resultados/sensibilidade.csv`)

Colunas: `perda`, `custo_analise`, `limiar_inferior`, `limiar_superior`. A tabela tem 84 linhas (`perda` em 200, 400, 600, 800; `custo_analise` de 0 a 100 de 5 em 5). Exemplos lidos diretamente:

| perda | custo_analise | limiar_inferior | limiar_superior |
|---|---|---|---|
| 200 | 50 | 0,25 | 0,5 |
| 400 | 0 | 0,0 | 1,0 |
| 400 | 50 | 0,125 | 0,5 |
| 400 | 100 | 0,2 | 0,2 |
| 800 | 50 | 0,0625 | 0,5 |

Para `perda` 200 e `custo_analise` a partir de 70, `limiar_inferior` e `limiar_superior` valem ambos 0,3333 (a faixa de análise manual some). Com `custo_analise` 0, a faixa vai de 0 a 1.

Leitura: a tabela descreve as fronteiras da política para cada par de perda e custo; é a Parte 1 da pergunta, que independe de resultado de modelo (plano-de-analise.md, seção 1, "Parte 1"). Não há linha da seção 4 para ela e este texto não escolhe valor de custo (`AGENTS.md`, regra 5).

## 4. Arestas do TAN (`resultados/tan_arestas.csv`)

Colunas: `fold`, `origem`, `destino`. Contagem feita sobre o arquivo (196 linhas = 195 arestas mais o cabeçalho):

| fold | arestas (linhas) | arestas com `origem` = kredit | arestas com `origem` = verw | arestas com `destino` = verw |
|---|---|---|---|---|
| 0 | 39 | 20 | 9 | 1 |
| 1 | 39 | 20 | 8 | 1 |
| 2 | 39 | 20 | 8 | 1 |
| 3 | 39 | 20 | 7 | 2 |
| 4 | 39 | 20 | 8 | 1 |

Em todas as partições `verw` é a variável (fora `kredit`) com mais arestas saindo dela. Nas partições 0 e 1 as seguintes são `beruf` (2); nas partições 2, 3 e 4, `beszeit` (3). O plano diz que as arestas do TAN em cada partição são reportadas no capítulo 4.1 (seção 2, linha "Arestas do TAN"); não há linha da seção 4 que interprete esse número.

**Hipótese não testada:** `verw` ser pai de muitas variáveis no TAN (7 a 9 por partição, na tabela acima) poderia causar esparsidade das tabelas de probabilidade condicional e excesso de confiança, o que seria coerente com o `ece_media` e o `log_loss_media` maiores do tan. Nada neste experimento testou isso: a contagem de arestas e as métricas apenas coexistem. Ela não autoriza mudar o modelo, as faixas ou qualquer parâmetro (`AGENTS.md`, regra 3).

## 5. Limites desta leitura

- Todos os números vêm do dev (800 casos, 5 partições); o teste final não foi aberto.
- Desvios entre partições (por exemplo `roc_auc_desvio` do tan, 0,049) são do mesmo tamanho de várias das diferenças entre modelos; os números acima não têm intervalo.
- `resultados/calibracao_dev.png`, `resultados/evidencia_incompleta.csv` e `resultados/sensibilidade.png` não foram lidos para este texto.
