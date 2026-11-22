# Auditoria dos números (cap. 4, 5, 6 e resumo)

Data: 18/11/2026. Escopo: `monografia/cap4-resultados.md`, `cap5-discussao.md`, `cap6-conclusao.md` e `resumo.md` (PT e abstract), contra `resultados/*.csv`, `config/utilidade.json` e `docs/plano-de-analise.md`. Nenhum arquivo de `dados/` foi lido; nenhum script de `codigo/` foi rodado; `resultados/` não foi alterado. Todos os números foram recalculados com pandas a partir dos arquivos e comparados com o texto (arredondamento a três casas, ou uma casa nas utilidades, vírgula decimal, sinal −).

## Divergências encontradas

| Localização | O que o texto dizia | O que o arquivo/estrutura diz | Ação |
|---|---|---|---|
| cap4, preâmbulo (linha 4) | "Os números das seções 4.1 a 4.7 são o baseline de desenvolvimento" | O capítulo 4 termina na seção 4.6; não existe seção 4.7 (a Tabela 4.6 é do teste, mas seção 4.7 não existe) | Corrigido para "4.1 a 4.6" |

Nenhuma outra divergência numérica foi encontrada.

## Verificações sem divergência

| Item | Resultado |
|---|---|
| Tabela 4.1 (metricas_dev.csv, 4 linhas x 10 colunas) e diferenças ROC-AUC 0,001 / 0,047 / 0,046, desvio 0,049, Brier 0,171/0,200/0,165 vs 0,210, ECE 0,152/0,093/0,095 | Iguais |
| Tabela  (tan_arestas.csv: 39 arestas por fold; 20 saem de kredit; verw como origem 9/8/8/7/8; destino verw 1/1/1/2/1; "7 a 9") | Igual |
| Tabela 4.2 (metricas_teste.csv, 5 linhas, incluindo ICs; ex.: logreg roc_auc_ic_inf 0,6515 = 0,651; sel pr_auc_ic_sup 0,61950 = 0,620) e diferenças de ROC-AUC (0,001 / 0,021 / 0,022; 0,7287, 0,7277, 0,7063), PR-AUC, Brier, ECE, log loss (tan 0,780, nb 0,627, sel 0,623 > 0,611) | Iguais |
| Comparação dev x teste (ROC-AUC, PR-AUC, Brier, log loss, ECE; ECE maior no teste para nb e tan, menor para logreg) | Iguais e sentidos corretos |
| Contagem do teste: 60 kredit=0 e 140 kredit=1 (predicoes_teste.csv, 200 linhas) | Igual |
| Tabela 4.3 (9 linhas selecionadas; 60 linhas no arquivo; os 3 maiores |delta_roc_auc| por modelo; 88% das variações < 0,01; nenhuma linha com os dois deltas zero; menor variação do nb em `hoehe`, 0,0001) | Iguais |
| Tabela 4.4 e diferenças 28,125 / 25,4 / 27,25; análise manual 355/262/415; n_mudam = n_analise_manual | Iguais |
| Tabelas 4.5 e 4.6 (utilidades, ICs, contagens, diferenças pareadas; ex.: logreg dif_ic_inf 20,195 exibido como 20,2) | Iguais; todos os ICs da diferença excluem 0 (inclui sel) |
| Tabela 4.7 e texto (84 linhas = 4 perdas x 21 custos; limiares; faixa some a partir de custo 70 para perda 200 e a partir de 80 para perda 400; 800/50 = 0,0625 exibido 0,063) | Iguais |
| Tabela 4.8 (demo): P(ruim) 0,834/0,734/0,696 e kredit=1 conferem com predicoes_dev.csv, linha sgc-0000, fold 4. UE aprovar −267,18 = 100 − 500p; UE manual −13,44 = 60 − 100p; fronteiras 0,10 e 0,60, derivadas de `config/utilidade.json` | Conferem (a saída de terminal em si não foi rodada, conforme a instrução) |
| Tabela 4.9 (9 linhas x 10 números em selecao_dev.csv) e Tabela 4.10 (selecao_escolha.csv; ex.: fold 3 nb_ess5 0,5385 = 0,539); nb_ess50 escolhida nas 5 partições e em `dev`; aninhado = nb_ess50; diferenças 0,001 (ROC-AUC) e 0,011 (log loss, 0,0105); TAN 0,825 a 0,583; nenhuma escolha de TAN | Iguais |
| Teste `sel`: ROC-AUC 0,720 [0,641; 0,795]; diferenças 0,008 (nb − sel), 0,014 (sel − tan); log loss 0,623 vs 0,627 (0,005); Brier 0,202; PR-AUC 0,477; ECE 0,120; dif. pareada 34,4 [16,4; 52,5] | Iguais |
| Cap. 5 (5.1, 5.1b, 5.2, 5.4, 5.5): todos os números citados; matriz +100, −400, c = 40 (config/utilidade.json: aprovar 100/−400, manual 60/−40 = 100 − 40 e −40); faixa 0,10 a 0,60 | Iguais |
| Cap. 6 (22,5 [9,2; 37,2]; ações 92/48/60 vs 145/55; diferenças de ROC-AUC 0,001 a 0,022; Brier 0,215 vs 0,210; PR-AUC; ECE 0,115/0,157/0,078; fronteiras c/400 e 1 − c/100) | Iguais |
| Resumo PT e abstract EN (200 casos, 60 ruins; Brier 0,215 vs 0,210 / 0.215 vs 0.210; 22,5, 9,2 a 37,2; 60 casos; 17,5 (−1,4 a 35,3); −5,0 (−29,5 a 19,5)) | Iguais; PT e EN coerentes entre si |
| Consistência cruzada cap. 4 / 5 / 6 / resumo (mesmos números para ROC-AUC, Brier, ECE, PR-AUC, 22,5 [9,2; 37,2], 60 casos, 34,4 etc.) | Sem inconsistência |
| Formato: vírgula decimal e sinal "−" (U+2212) nos textos e tabelas; nenhum ponto decimal ou hífen como sinal | Sem ocorrência fora do padrão |
| Frases interpretativas ("ruído" para diferenças < 0,03; TAN não melhor que a taxa base no teste; intervalo exclui zero; TAN abaixo do NB nas 5 métricas no dev; diferença de log loss menor que os desvios 0,033 e 0,035) | Sustentadas pelos números |

## Observações apenas listadas (sem alteração)

| Localização | Observação | Ação |
|---|---|---|
| cap4, Tabelas 4.4 e 4.7 | Algumas células aparecem com menos de três casas (ex.: "4,5", "0,2"), enquanto o preâmbulo diz "arredondados a três casas, salvo indicação". É formato, não valor | Só listado |
| cap4, Tabela 4.6 e cap5/6 | Logreg dif_ic_inf é 20,195 no arquivo e aparece como 20,2 (uma casa, como as demais utilidades) | Só listado |
| cap4, Tabela  (fonte) e cap5 | Citam `docs/resultados-dev.md`, que está fora do escopo desta auditoria e não foi lido | Só listado |
| cap4, seção 4.5 | Cita `codigo/demo.py`, que não consta entre os 7 scripts do `PLANO.md` item 7 segundo o `AGENTS.md`; fora do escopo numérico, o autor deve confirmar | Só listado |

## Atualização de 22/11/2026 (Seção 4.7 e conferências)

Escopo adicional: `cap4-resultados.md` §4.7 (Tabelas 4.11 e 4.12), `cap5-discussao.md` §5.2 e §5.5, `cap6-conclusao.md` §6.2 e `cap3-metodos.md` §3.11, contra `resultados/duas_acoes_teste.csv` e `resultados/diferenca_duas_acoes_teste.csv`, gravados por `decisao.py --final` em 22/11/2026 (os seis arquivos anteriores do teste ficaram idênticos, conferidos por MD5). Os números das tabelas novas e do texto da §4.7 foram gerados por script a partir dos CSV, sem digitação.

| Número no texto | Origem |
|---|---|
| TAN: utilidade média 17,5 (três ações), 8,5 (duas ações, limiar 0,2) e −5,0 (corte 0,5) | `duas_acoes_teste.csv`, `utilidade_media`, linhas `tan` com `ue`, `ue2`, `limiar` |
| Duas ações: 112 aprovados e 88 rejeitados; três ações: 92, 48 e 60; corte 0,5: 145 e 55 | `n_aprovar`, `n_rejeitar`, `n_analise_manual` |
| 22,5 [9,2; 37,2] | `diferenca_duas_acoes_teste.csv`, `tan`, `ue - limiar`; coincide com `diferenca_politicas_teste.csv` |
| 9,0 [1,8; 17,4] e 13,5 [0,5; 28,5] | `tan`, `ue - ue2` e `ue2 - limiar` (o limite inferior 0,49 aparece como 0,5) |
| 11,0, 9,3 e 18,4 (três ações − duas ações); 18,5 e 29,0 (duas ações − corte, NB e logística); 16,0 [−0,5; 33,5] (seleção aninhada, inclui zero) | `nb`, `logreg`, `sel` |
| 60, 85 e 111 casos encaminhados à análise manual (TAN, NB, logística) | `resumo_politicas_teste.csv`, `n_analise_manual` |

Conferências independentes das saídas do desenvolvimento (cap3 §3.11): reimplementação em NumPy, em scripts descartáveis fora do repositório, sem versionamento. Brier, *log loss*, ECE de dez faixas, ROC-AUC e PR-AUC por partição coincidem com `metricas_dev.csv` (diferença máxima de 1,1e-16); ações e utilidade média coincidem com `politicas_dev.csv` e `resumo_politicas_dev.csv`; a coluna `fold` coincide com `StratifiedKFold(5, shuffle=True, random_state=2026)` refeito (160 casos e 48 ruins por partição); a árvore do TAN por informação mútua condicional e árvore geradora máxima coincide com `tan_arestas.csv` nas cinco partições (19 arestas entre variáveis, mesmo peso). Não foram reimplementados as tabelas de probabilidade condicional com BDeu nem a inferência, e o teste não foi recalculado.

