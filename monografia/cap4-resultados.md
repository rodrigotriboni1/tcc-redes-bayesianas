# 4 RESULTADOS

Este capítulo relata os resultados. Os números de desenvolvimento (Tabelas 4.1, 4.3, 4.4, 4.7, 4.9, 4.10) são resultados pré-estudo, obtidos só com os 800 casos de desenvolvimento (validação cruzada estratificada em 5 partições, Capítulo 3, Seções 3.2 e 3.3); os blocos do conjunto de teste (Tabelas 4.2, 4.5, 4.6, 4.11, 4.12 e Figura 4.2) são identificados na legenda pelo rótulo "conjunto de teste (n = 200; 60 ruins)". As Tabelas 4.13 a 4.15 também usam só o desenvolvimento, mas são posteriores ao plano (Seções 4.8 a 4.10). O conjunto de teste final foi aberto uma única vez, após o *commit* de congelamento 49d77ff. Cada seção remete à seção correspondente do Capítulo 3. A leitura dos resultados segue as regras originais do plano de análise (`docs/plano-de-analise.md`), com as complementações posteriores explicitadas na Seção 3.6, e a interpretação fica para o Capítulo 5.

Nas tabelas de métricas (4.1, 4.9 e 4.15), os valores são médias e desvios entre as 5 partições. Cada número traz a indicação do arquivo e da coluna de origem. A Tabela 4.2 traz o valor no conjunto de teste com intervalo de 95% por *bootstrap*. Os valores são arredondados a três casas, salvo indicação.

## 4.1 Desempenho preditivo

As métricas (Seção 3.6) dos três modelos e da referência de taxa base estão na Tabela 4.1.

**Tabela 4.1** – Métricas por modelo no desenvolvimento, média (desvio) entre 5 partições

| Modelo | ROC-AUC (desvio) | PR-AUC (desvio) | Brier (desvio) | *log loss* (desvio) | ECE (desvio) |
|---|---|---|---|---|---|
| NB | 0,789 (0,024) | 0,616 (0,049) | 0,171 (0,013) | 0,523 (0,035) | 0,093 (0,014) |
| TAN | 0,742 (0,049) | 0,549 (0,076) | 0,200 (0,030) | 0,704 (0,136) | 0,152 (0,050) |
| Regressão logística | 0,788 (0,021) | 0,649 (0,042) | 0,165 (0,012) | 0,504 (0,026) | 0,095 (0,031) |
| Taxa base | 0,500 (0,000) | 0,300 (0,000) | 0,210 (0,000) | 0,611 (0,000) | 0,000 (0,000) |

Aplicando as regras da §4 do plano de análise:

- **ROC-AUC, nb contra logreg.** A diferença é 0,001 (0,7890 contra 0,7880), menor que 0,03. Pela regra do plano de análise, fica abaixo do limite descritivo de 0,03 adotado no plano, sem que isso constitua, por si só, teste estatístico de equivalência entre modelos.
- **ROC-AUC, nb e logreg contra tan.** As diferenças são 0,047 (nb − tan) e 0,046 (logreg − tan). Ambas passam de 0,03, de modo que a regra de ruído não se aplica a esses pares. O plano não prevê outra regra para esse caso; registra-se ao lado que o desvio do tan entre partições é 0,049. O TAN teve desempenho pior que o NB nas cinco métricas no desenvolvimento (ROC-AUC e PR-AUC menores; Brier, *log loss* e ECE maiores).
- **Brier contra taxa base.** O Brier médio dos três modelos (nb 0,171; tan 0,200; logreg 0,165) é menor que o da taxa base, 0,210. A condição "igual ou maior que 0,21" não ocorre; a frase "não melhor que prever a taxa base" não é acionada para nenhum modelo.
- **Calibração.** O ECE do tan, 0,152, é o maior dos três (nb 0,093; logreg 0,095). Conforme o plano de análise e a decisão P1, a calibração é apenas medida e relatada; não há correção. Os diagramas de confiabilidade dos três modelos estão em `resultados/calibracao_dev.png`.

**Figura 4.1** – Diagramas de confiabilidade no desenvolvimento (`resultados/calibracao_dev.png`)

**Arestas do TAN.** O plano determina que as arestas aprendidas pelo TAN em cada partição sejam relatadas nesta seção. Em todas as 5 partições há 39 arestas, 20 das quais saem da classe risco do crédito.

Fora a classe, a variável da qual sai o maior número de arestas, em todas as partições, é finalidade do crédito (7 a 9 por partição; 1 ou 2 chegam a ela). Registra-se, como **hipótese não testada**, que o fato de finalidade do crédito ser pai de muitas variáveis poderia produzir tabelas de probabilidade condicional esparsas e excesso de confiança, o que seria coerente com o *log loss* e o erro de calibração maiores do tan. Nenhuma análise deste trabalho testou essa hipótese: a contagem de arestas e as métricas apenas coexistem, e a observação não autoriza alterar modelo, faixa ou parâmetro.

**Conjunto de teste (n = 200; 60 ruins).** Os intervalos são de 95% por *bootstrap*. A Tabela 4.2 traz as métricas; a linha `sel` é a análise secundária da Seção 4.6.

**Tabela 4.2** – Métricas por modelo no conjunto de teste (n = 200; 60 ruins), valor [intervalo de 95%]

| Modelo | ROC-AUC [IC 95%] | PR-AUC [IC 95%] | Brier [IC 95%] | *log loss* | ECE |
|---|---|---|---|---|---|
| NB | 0,728 [0,648; 0,802] | 0,490 [0,378; 0,630] | 0,199 [0,161; 0,239] | 0,627 | 0,115 |
| TAN | 0,706 [0,623; 0,789] | 0,480 [0,372; 0,617] | 0,215 [0,173; 0,261] | 0,780 | 0,157 |
| Regressão logística | 0,729 [0,651; 0,800] | 0,500 [0,383; 0,636] | 0,191 [0,157; 0,228] | 0,578 | 0,078 |
| Taxa base | 0,500 [0,500; 0,500] | 0,300 [0,235; 0,365] | 0,210 [0,184; 0,236] | 0,611 | 0,000 |
| sel (secundária) | 0,720 [0,641; 0,795] | 0,477 [0,365; 0,620] | 0,202 [0,164; 0,242] | 0,623 | 0,120 |

Aplicando as regras da §4 do plano de análise ao conjunto de teste:

- **ROC-AUC.** As diferenças entre os três modelos primários são 0,001 (logreg − nb: 0,7287 contra 0,7277), 0,021 (nb − tan: 0,7277 contra 0,7063) e 0,022 (logreg − tan: 0,7287 contra 0,7063). As três são menores que 0,03 e, pela regra do plano de análise, consideradas pequenas segundo a regra descritiva de 0,03; essa classificação não demonstra equivalência estatística.
- **PR-AUC.** Os valores são 0,490 (nb), 0,480 (tan) e 0,500 (logreg), contra 0,300 da taxa base. O limite de 0,03 vale só para ROC-AUC; por decisão do autor registrada em docs/decisoes.md (plano de análise, §8), nenhuma regra é aplicada a essas diferenças e elas são apenas descritas, sem conclusão de ruído.
- **Brier contra taxa base.** O Brier do tan no teste é 0,215, maior que o da taxa base, 0,210. Pela regra do plano de análise, o tan apresentou escore de Brier pontual maior que o do preditor de taxa base no conjunto de teste; não foi realizada inferência específica sobre a diferença. O nb (0,199) e o logreg (0,191) ficam abaixo de 0,21, e a regra não é acionada para eles.
- **Calibração.** O ECE é 0,115 (nb), 0,157 (tan) e 0,078 (logreg). Conforme a decisão P1, a calibração é apenas relatada; não há correção. O *log loss* do tan, 0,780, do nb, 0,627, e do sel (secundária), 0,623, são maiores que o da taxa base, 0,611. O plano não tem regra para *log loss* contra a taxa base, e o fato é apenas descrito.
- **Desenvolvimento e teste.** ROC-AUC e PR-AUC do teste são menores que as do desenvolvimento nos três modelos: ROC-AUC 0,728 contra 0,789 (nb), 0,706 contra 0,742 (tan) e 0,729 contra 0,788 (logreg); PR-AUC 0,490 contra 0,616 (nb), 0,480 contra 0,549 (tan) e 0,500 contra 0,649 (logreg). Brier e *log loss* do teste são maiores que os do desenvolvimento nos três modelos; a ECE é maior no teste para nb (0,115 contra 0,093) e tan (0,157 contra 0,152) e menor para logreg (0,078 contra 0,095). O plano não tem regra para essa comparação; o fato é descrito sem conclusão.

**Figura 4.2** – Diagramas de confiabilidade no conjunto de teste (n = 200; 60 ruins) (`resultados/calibracao_teste.png`)

## 4.2 Evidência incompleta

O efeito de esconder uma variável por vez (Seção 3.5.1) está em `resultados/evidencia_incompleta.csv`, com 60 linhas (3 modelos × 20 variáveis). A Tabela 4.3 traz, para cada modelo, as variáveis cuja ocultação produziu as maiores variações absolutas de ROC-AUC. A ressalva da decisão P9 acompanha toda a seção: as redes bayesianas marginalizam a variável ausente, enquanto a regressão logística a imputa; as duas operações não são equivalentes.

**Tabela 4.3** – Variação de métricas ao esconder uma variável, seleção de linhas

| Modelo | Variável oculta | ROC-AUC | Brier | Δ ROC-AUC | Δ Brier |
|---|---|---|---|---|---|
| NB | situação da conta corrente | 0,741 | 0,183 | −0,048 | 0,012 |
| NB | histórico de crédito | 0,777 | 0,175 | −0,012 | 0,004 |
| NB | poupança | 0,783 | 0,174 | −0,006 | 0,003 |
| TAN | situação da conta corrente | 0,692 | 0,216 | −0,050 | 0,016 |
| TAN | finalidade do crédito | 0,768 | 0,183 | 0,025 | −0,018 |
| TAN | duração do crédito | 0,733 | 0,205 | −0,010 | 0,005 |
| Regressão logística | situação da conta corrente | 0,742 | 0,198 | −0,046 | 0,033 |
| Regressão logística | histórico de crédito | 0,769 | 0,174 | −0,019 | 0,009 |
| Regressão logística | valor do crédito | 0,773 | 0,168 | −0,015 | 0,003 |

Nos três modelos, a ocultação de situação da conta corrente é a que mais reduz a ROC-AUC: −0,048 (nb), −0,050 (tan) e −0,046 (logreg). No tan, esconder a finalidade do crédito eleva a ROC-AUC em 0,025 e reduz o Brier em 0,018; o resultado é relatado como saiu, sem interpretação causal e sem que se proponha retirar a variável do modelo. A maior parte das demais variações tem valor absoluto inferior a 0,01. Nenhuma linha tem `delta_roc_auc` e `delta_brier` simultaneamente iguais a zero, de modo que a regra "esconder uma variável não muda nenhuma predição" da §4 não é acionada; a menor variação observada no nb é a do valor do crédito (delta_roc_auc 0,0001). Essas diferenças não têm intervalo.

## 4.3 Política de decisão

A Tabela 4.4 compara a política de três ações por utilidade esperada (`ue`) contra o corte 0,5 de duas ações (`limiar`) (Seções 3.7 e 3.7.1, decisão P8), com os valores de utilidade de `config/utilidade.json`. As contagens referem-se aos 800 casos do desenvolvimento.

**Tabela 4.4** – Política de três ações por utilidade esperada contra corte 0,5 de duas ações, desenvolvimento

| Modelo | Regra | Utilidade média | aprovar (n) | rejeitar (n) | análise manual (n) | mudam de ação (n) |
|---|---|---|---|---|---|---|
| NB | três ações (ue) | 32,625 | 274 | 171 | 355 | 355 |
| NB | corte 0,5 | 4,5 | 581 | 219 | 0 | 355 |
| TAN | três ações (ue) | 22,275 | 361 | 177 | 262 | 262 |
| TAN | corte 0,5 | −3,125 | 590 | 210 | 0 | 262 |
| Regressão logística | três ações (ue) | 30,875 | 243 | 142 | 415 | 415 |
| Regressão logística | corte 0,5 | 3,625 | 599 | 201 | 0 | 415 |

A utilidade média da política de três ações (`ue`) é maior que a do corte 0,5 de duas ações (`limiar`) nos três modelos, com diferenças de 28,125 (nb), 25,4 (tan) e 27,25 (logreg). Trata-se de diferença descritiva no desenvolvimento, sem intervalo: pelo plano, a comparação pareada com intervalo só é feita no teste final, e a diferença mistura modelo, representação e conjunto de ações, razão pela qual não é chamada de efeito da regra. Na política de três ações (`ue`), a análise manual recebe 355 (nb), 262 (tan) e 415 (logreg) dos 800 casos; o corte 0,5 de duas ações (`limiar`) não tem análise manual, por ter só duas ações. As três ações aparecem na política de três ações (`ue`) em todos os modelos, de modo que a regra "alguma ação não aparece numa política" não se aplica. O número de casos cuja ação muda entre as regras coincide, em cada modelo, com o número de casos em análise manual da política de três ações (`ue`). A ação de cada caso está em `resultados/politicas_dev.csv`.

**Conjunto de teste (n = 200; 60 ruins).** A Tabela 4.5 traz as duas regras no teste, e a Tabela 4.6, a diferença pareada de utilidade média (`ue` − `limiar`) com intervalo de 95% por *bootstrap* (Seção 3.7.1). Pela §3 do plano (decisão P5), a comparação principal é a do TAN; NB e regressão logística aparecem nas tabelas, sem destaque na leitura principal, e `sel` é análise secundária (Seção 4.6).

**Tabela 4.5** – Política de três ações contra corte 0,5 de duas ações, conjunto de teste (n = 200; 60 ruins)

| Modelo | Regra | Utilidade média [IC 95%] | aprovar (n) | rejeitar (n) | análise manual (n) | mudam de ação (n) |
|---|---|---|---|---|---|---|
| NB | três ações (ue) | 24,0 [7,6; 38,7] | 74 | 41 | 85 | 85 |
| NB | corte 0,5 | −5,5 [−30,5; 19,5] | 149 | 51 | 0 | 85 |
| TAN | três ações (ue) | 17,5 [−1,4; 35,3] | 92 | 48 | 60 | 60 |
| TAN | corte 0,5 | −5,0 [−29,5; 19,5] | 145 | 55 | 0 | 60 |
| Regressão logística | três ações (ue) | 25,3 [10,2; 39,1] | 62 | 27 | 111 | 111 |
| Regressão logística | corte 0,5 | −13,0 [−38,5; 12,0] | 154 | 46 | 0 | 111 |
| sel (secundária) | três ações (ue) | 27,9 [13,4; 40,8] | 69 | 38 | 93 | 93 |
| sel (secundária) | corte 0,5 | −6,5 [−31,5; 17,5] | 152 | 48 | 0 | 93 |

O intervalo de cada regra isolada não é o critério de leitura; o critério é a diferença pareada (Tabela 4.6).

**Tabela 4.6** – Diferença pareada de utilidade média (`ue` − `limiar`), conjunto de teste (n = 200; 60 ruins)

| Modelo | Diferença de utilidade média | IC 95% inferior | IC 95% superior |
|---|---|---|---|
| TAN (principal) | 22,5 | 9,2 | 37,2 |
| NB | 29,5 | 13,1 | 46,3 |
| Regressão logística | 38,3 | 20,2 | 56,4 |
| sel (secundária) | 34,4 | 16,4 | 52,5 |

Aplicando a §4 do plano: na comparação principal (TAN), a diferença é 22,5, com intervalo de 9,2 a 37,2. Observa-se diferença a favor da política de três ações, com intervalo que exclui zero; não se afirma causa. Em NB, regressão logística e na análise secundária, o intervalo também exclui zero a favor da política de três ações (`ue`): nb 29,5 [13,1; 46,3], logreg 38,3 [20,2; 56,4] e sel 34,4 [16,4; 52,5]. A diferença mistura modelo, representação e conjunto de ações e não é chamada de efeito da regra nem do modelo (ressalva obrigatória da Seção 5.5; §6 do plano, itens 3 e 7). Na política de três ações (`ue`), a análise manual recebe 60 (tan), 85 (nb), 111 (logreg) e 93 (sel) dos 200 casos, e o número de casos que mudam de ação entre as regras coincide com esses valores. As três ações aparecem na política de três ações (`ue`) em todos os modelos, de modo que a regra "alguma ação não aparece numa política" não se aplica. A ação de cada caso está em `resultados/politicas_teste.csv`.

## 4.4 Sensibilidade

A Tabela 4.7 mostra, para alguns pares de perda e custo da análise manual, os limiares de risco que delimitam a faixa de análise manual (Seção 3.8). O arquivo completo tem 84 linhas: perda em {200, 400, 600, 800} e custo de 0 a 100, de 5 em 5. Esses limiares decorrem só da matriz de utilidade e não dependem de nenhum modelo.

**Tabela 4.7** – Limiares da política por perda e custo da análise manual, seleção de linhas

| Perda | Custo da análise | Limiar inferior | Limiar superior |
|---|---|---|---|
| 200 | 50 | 0,25 | 0,5 |
| 200 | 70 | 0,333 | 0,333 |
| 400 | 0 | 0,000 | 1,000 |
| 400 | 50 | 0,125 | 0,5 |
| 400 | 100 | 0,2 | 0,2 |
| 800 | 50 | 0,063 | 0,5 |

Com custo zero, a faixa de análise manual cobre todo o intervalo de 0 a 1 (linha 400, 0). Quando os dois limiares coincidem, a faixa desaparece e a política se reduz a duas ações; isso ocorre, por exemplo, para perda 200 com custo a partir de 70 e para perda 400 com custo a partir de 80. A Figura 4.3 mostra a tabela inteira. Não há regra da §4 para esta análise, e este texto não escolhe valor de custo nem de perda. Essa sensibilidade é à matriz: ela não mede o efeito de um erro de calibração das probabilidades, que a Seção 4.8 mede no desenvolvimento e a Seção 5.9 discute.

**Figura 4.3** – Limiares da política em função da perda e do custo da análise manual (`resultados/sensibilidade.png`)

## 4.5 Demonstração

O *script* `codigo/demo.py` (Seção 3.9) lê apenas o conjunto de desenvolvimento, `resultados/predicoes_dev.csv` e `config/utilidade.json`, e não grava arquivos. Para um caso, ele treina os três modelos nas 4 partições que não contêm o caso e imprime as variáveis do caso, a probabilidade de ruim de cada modelo, a utilidade esperada de cada ação para o modelo indicado (padrão: tan), as fronteiras de risco da matriz e a ação recomendada. O comando `uv run python codigo/demo.py sgc-0000` produziu, para o primeiro caso de `predicoes_dev.csv` (partição 4), a saída resumida na Tabela 4.8.

**Tabela 4.8** – Saída de `codigo/demo.py` para o caso sgc-0000

| Item | Valor |
|---|---|
| P(ruim), NB | 0,834 |
| P(ruim), TAN | 0,734 |
| P(ruim), Regressão logística | 0,696 |
| UE aprovar (TAN) | −267,18 |
| UE rejeitar (TAN) | 0,00 |
| UE análise manual (TAN) | −13,44 |
| fronteira aprovar / análise manual | p = 0,10 |
| fronteira análise manual / rejeitar | p = 0,60 |
| ação recomendada (TAN) | rejeitar |

As probabilidades coincidem com as de `predicoes_dev.csv`, o que é esperado, pois o *script* treina nas mesmas partições. Como a probabilidade de ruim do tan (0,734) está acima da fronteira de 0,60, a ação de maior utilidade esperada é rejeitar. O rótulo verdadeiro desse caso é bom (risco do crédito = 1); o caso foi escolhido por ser o primeiro do arquivo, não por ser representativo.

## 4.6 Estudo de seleção (secundário)

Esta seção relata o estudo secundário da §9 (desenhado depois das métricas de desenvolvimento e antes do teste) do plano de análise (Seção 3.10). Ele não altera a análise primária: as Seções 4.1 a 4.4 continuam com NB e TAN de tamanho equivalente BDeu 5.

**Declaração de viés.** Vale a declaração de viés da Seção 3.10.

Foram feitas **8 comparações** (as 8 configurações da grade). A Tabela 4.9 traz as 8 linhas e a linha `aninhado`, que avalia, em cada partição externa, a configuração escolhida pela regra nas partições internas.

**Tabela 4.9** – Métricas das 8 configurações e da seleção aninhada, média (desvio) entre 5 partições externas

| Modelo | ROC-AUC (desvio) | PR-AUC (desvio) | Brier (desvio) | *log loss* (desvio) | ECE (desvio) |
|---|---|---|---|---|---|
| nb_ess1 | 0,788 (0,026) | 0,616 (0,051) | 0,171 (0,013) | 0,527 (0,037) | 0,098 (0,016) |
| nb_ess5 | 0,789 (0,024) | 0,616 (0,049) | 0,171 (0,013) | 0,523 (0,035) | 0,093 (0,014) |
| nb_ess10 | 0,790 (0,024) | 0,618 (0,050) | 0,170 (0,013) | 0,520 (0,035) | 0,093 (0,017) |
| nb_ess50 | 0,788 (0,028) | 0,613 (0,049) | 0,169 (0,012) | 0,512 (0,033) | 0,093 (0,012) |
| tan_ess1 | 0,726 (0,055) | 0,531 (0,080) | 0,207 (0,031) | 0,825 (0,203) | 0,165 (0,065) |
| tan_ess5 | 0,742 (0,049) | 0,549 (0,076) | 0,200 (0,030) | 0,704 (0,136) | 0,152 (0,050) |
| tan_ess10 | 0,749 (0,046) | 0,557 (0,078) | 0,196 (0,028) | 0,660 (0,110) | 0,145 (0,050) |
| tan_ess50 | 0,763 (0,036) | 0,569 (0,081) | 0,186 (0,023) | 0,583 (0,066) | 0,115 (0,040) |
| aninhado | 0,788 (0,028) | 0,613 (0,049) | 0,169 (0,012) | 0,512 (0,033) | 0,093 (0,012) |

**Escolha por partição.** Pela regra da §9 (menor *log loss* médio nas partições internas), `nb_ess50` foi escolhida nas cinco partições externas e também no desenvolvimento inteiro. A Tabela 4.10 traz o *log loss* interno da configuração escolhida e das duas configurações de referência.

**Tabela 4.10** – *Log loss* interno por partição externa, seleção de colunas

| Partição externa | Escolhida | *log loss* interno (escolhida) | nb_ess5 | tan_ess5 |
|---|---|---|---|---|
| 0 | nb_ess50 | 0,539 | 0,558 | 0,855 |
| 1 | nb_ess50 | 0,535 | 0,554 | 0,733 |
| 2 | nb_ess50 | 0,524 | 0,541 | 0,777 |
| 3 | nb_ess50 | 0,527 | 0,539 | 0,786 |
| 4 | nb_ess50 | 0,508 | 0,515 | 0,738 |
| dev | nb_ess50 | 0,512 | 0,523 | 0,704 |

Como a mesma configuração foi escolhida em todas as partições externas, a linha `aninhado` reproduz os valores de `nb_ess50`. A diferença de ROC-AUC entre `aninhado` (0,788) e a configuração de referência `nb_ess5` (0,789) é 0,001, menor que 0,03 e, portanto, tratada como ruído pela regra da §4. A diferença de *log loss* entre as duas é 0,011 (0,512 contra 0,523). Entre as configurações do TAN, o *log loss* médio diminui à medida que o tamanho equivalente aumenta, de 0,825 (`tan_ess1`) a 0,583 (`tan_ess50`); em nenhuma partição uma configuração do TAN foi escolhida.

**Conjunto de teste (n = 200; 60 ruins), análise secundária.** As predições `p_sel` no teste estão em `resultados/predicoes_teste.csv` (coluna `p_sel`), e suas métricas, na linha `sel` da Tabela 4.2. Como define a §9, a diferença principal da escolha é contra a configuração de referência `nb` (NB, BDeu 5): a ROC-AUC de `sel` é 0,720 [0,641; 0,795], contra 0,728 do `nb`; a diferença, 0,008 (nb − sel), é menor que 0,03 e, pela regra da §9, tratada como ruído. De forma apenas descritiva, a diferença contra o `tan` (TAN, BDeu 5, ROC-AUC 0,706) é 0,014 (sel − tan). O *log loss* de `sel` é 0,623, contra 0,627 do `nb` (diferença de 0,005, calculada sobre os valores não arredondados: 0,6273 − 0,6226); o plano não tem regra de leitura para essa diferença, e ela é apenas descrita. O Brier de `sel`, 0,202, é menor que o da taxa base, 0,210. Na política de decisão, a diferença pareada de `sel` é 34,4 [16,4; 52,5] (Tabela 4.6). Esses números relatam quanto a configuração escolhida pela regra difere da configuração de referência no teste; não indicam qual modelo adotar.

## 4.7 Análise exploratória posterior ao teste: política de duas ações

Esta seção relata uma análise exploratória feita depois da abertura do teste e de conhecido o resultado da comparação principal, e não substitui essa comparação. Ela foi decidida e registrada antes de rodar (`docs/decisoes.md`; Apêndice B.5). A política de duas ações (`ue2`) escolhe entre aprovar e rejeitar pela utilidade esperada da matriz; seu limiar, *p* = *G*/(*G* + *L*) = 100/500 = 0,2 (Seção 2.7), vem da matriz. A comparação separa duas fontes da diferença de 22,5: a ação análise manual (política de três ações contra `ue2`) e o corte de referência 0,5, que não é o limiar de duas ações da matriz (`ue2` contra o corte 0,5).

A leitura foi definida antes de rodar, para cada diferença: se o intervalo de 95% exclui zero, descreve-se diferença observada a favor de uma das políticas, sem afirmar causa; se inclui zero, não há evidência de diferença com 200 casos e 60 ruins, sem concluir que as políticas são iguais.

**Tabela 4.11** – Utilidade média por regra, análise exploratória posterior ao teste (n = 200; 60 ruins), valor [intervalo de 95%]

| Modelo | Três ações (`ue`) | Duas ações, limiar 0,2 (`ue2`) | Corte 0,5 (`limiar`) |
|---|---|---|---|
| TAN (principal) | 17,5 [−1,4; 35,3] | 8,5 [−12,5; 27,5] | −5,0 [−29,5; 19,5] |
| NB | 24,0 [7,6; 38,7] | 13,0 [−5,5; 30,0] | −5,5 [−30,5; 19,5] |
| Regressão logística | 25,3 [10,2; 39,1] | 16,0 [−2,0; 32,0] | −13,0 [−38,5; 12,0] |
| sel (secundária) | 27,9 [13,4; 40,8] | 9,5 [−9,5; 27,0] | −6,5 [−31,5; 17,5] |

Com o TAN, a utilidade média foi 17,5 na política de três ações, 8,5 na de duas ações com limiar 0,2 e −5,0 no corte 0,5. A política de duas ações aprovou 112 e rejeitou 88 casos; a de três ações aprovou 92, rejeitou 48 e encaminhou 60, e o corte 0,5 aprovou 145 e rejeitou 55.

**Tabela 4.12** – Diferenças pareadas de utilidade média, análise exploratória posterior ao teste (n = 200; 60 ruins), valor [intervalo de 95%]

| Modelo | Três ações − corte 0,5 | Três ações − duas ações | Duas ações − corte 0,5 |
|---|---|---|---|
| TAN (principal) | 22,5 [9,2; 37,2] | 9,0 [1,8; 17,4] | 13,5 [0,5; 28,5] |
| NB | 29,5 [13,1; 46,3] | 11,0 [2,5; 20,9] | 18,5 [2,0; 36,0] |
| Regressão logística | 38,3 [20,2; 56,4] | 9,3 [0,6; 19,0] | 29,0 [10,0; 48,5] |
| sel (secundária) | 34,4 [16,4; 52,5] | 18,4 [7,5; 30,0] | 16,0 [−0,5; 33,5] |

Com o TAN, a diferença de 22,5 entre a política de três ações e o corte 0,5 se decompõe, de forma descritiva, em 9,0 (intervalo de 95%: 1,8 a 17,4) entre a política de três ações e a de duas ações com limiar 0,2, e 13,5 (0,5 a 28,5) entre esta e o corte 0,5. Os dois intervalos excluem zero, o segundo por pouco. Pela regra acima, observa-se diferença a favor da política de três ações sobre a de duas ações, e diferença a favor da política de duas ações sobre o corte 0,5, sem afirmar causa. A parcela atribuída ao corte de referência é maior que a atribuída à ação adicional, mas os intervalos se sobrepõem e a decomposição não é um teste.

No *Naive Bayes*, na regressão logística e na seleção aninhada, a diferença entre a política de três ações e a de duas ações também exclui zero (11,0, 9,3 e 18,4). A diferença entre a política de duas ações e o corte 0,5 exclui zero no *Naive Bayes* (18,5) e na regressão logística (29,0) e inclui zero na seleção aninhada (16,0; −0,5 a 33,5), caso em que não há evidência de diferença.

Esses números herdam as ressalvas das Seções 5.4 e 5.5 (matriz demonstrativa, analista infalível, simulação sobre o rótulo observado) e as de um teste com 200 casos. A política de duas ações não é adotada nem recomendada por causa deste resultado, e a comparação principal e a matriz não mudam. Foram lidos 12 intervalos (4 modelos e 3 comparações) sem correção para comparações múltiplas; os que excluem zero por pouco, como o do TAN entre a política de duas ações e o corte 0,5 (limite inferior de 0,5), são os mais frágeis a essa leitura.

## 4.8 Sensibilidade das ações ao erro de calibração: análise posterior ao plano

A análise a seguir foi feita no desenvolvimento, depois do plano, em resposta à observação de que a calibração foi medida e não corrigida (Seção 5.9). Ela não treina nem recalibra modelo, não usa o teste e não altera a análise primária. Para cada modelo, a probabilidade de ruim *p* de cada um dos 800 casos é trocada por *p* − ECE, *p* e *p* + ECE, em que o ECE é o erro esperado de calibração médio do modelo no desenvolvimento (0,093 no NB, 0,152 no TAN e 0,095 na regressão logística; Tabela 4.1), e a ação de maior utilidade esperada é refeita com a matriz demonstrativa. O deslocamento não é cortado em [0, 1], porque a ação só depende de *p* frente às fronteiras 0,10 e 0,60. A utilidade média é a realizada: a ação deslocada aplicada ao estado verdadeiro de cada caso. O comando é `uv run python codigo/decisao.py --calibracao`, e o resultado está em `resultados/sensibilidade_calibracao_dev.csv`.

**Tabela 4.13** – Ações e utilidade média no desenvolvimento com *p* deslocada pelo ECE do modelo (n = 800)

| Modelo | Cenário | Aprovar | Rejeitar | Análise manual | Utilidade média | Casos que mudam de ação |
|---|---|---|---|---|---|---|
| NB | *p* − ECE | 395 | 121 | 284 | 27,3 | 171 |
| NB | *p* (base) | 274 | 171 | 355 | 32,6 | 0 |
| NB | *p* + ECE | 15 | 216 | 569 | 30,8 | 304 |
| TAN | *p* − ECE | 476 | 107 | 217 | 16,4 | 185 |
| TAN | *p* (base) | 361 | 177 | 262 | 22,3 | 0 |
| TAN | *p* + ECE | 0 | 234 | 566 | 28,3 | 418 |
| Regressão logística | *p* − ECE | 391 | 91 | 318 | 28,5 | 199 |
| Regressão logística | *p* (base) | 243 | 142 | 415 | 30,9 | 0 |
| Regressão logística | *p* + ECE | 3 | 200 | 597 | 30,8 | 298 |

Um erro do tamanho do ECE muda a ação de 171 a 418 dos 800 casos (21% a 52%), conforme o modelo e o sentido. No TAN, o deslocamento para cima tira todas as aprovações (361 para 0) e leva 566 casos à análise manual. A utilidade média não segue uma direção única: com *p* − ECE ela cai nos três modelos (27,3, 16,4 e 28,5); com *p* + ECE ela cai no NB (30,8), sobe no TAN (28,3) e fica quase igual na regressão logística (30,8). Uma leitura compatível com a alta do TAN, não testada aqui, é que o deslocamento encaminha mais casos à análise manual, cujo analista a matriz supõe infalível (Seção 5.5).

Os números valem para este cenário simétrico, no desenvolvimento e sem intervalo. O erro real de calibração não é um deslocamento constante: o ECE é uma média de diferenças em módulo, e a probabilidade pode estar alta numas faixas e baixa em outras (Seção 5.9). A Tabela 4.13 dá uma ordem de grandeza da sensibilidade, não o efeito de recalibrar. Ela não é usada para escolher modelo, parâmetro ou matriz, e os resultados dos Capítulos 4 e 5 seguem com as probabilidades sem correção.

## 4.9 Sensibilidade da comparação ao erro do analista: análise posterior ao plano

A análise a seguir foi feita no desenvolvimento, depois do plano, em resposta à observação de que a política de três ações supõe um analista que nunca erra (Seção 5.5). Ela não treina modelo, não usa o teste e não altera a análise primária. Foi decidida e registrada em `docs/decisoes.md` antes de rodar (Apêndice B.5). A política fica como está, com as fronteiras 0,10 e 0,60. Muda só o analista: um caso encaminhado à análise manual é decidido corretamente com probabilidade *q* e de forma errada com probabilidade 1 − *q*, a mesma nos dois estados do cliente. Essa simetria é uma hipótese do autor. O custo da análise, 40, e as utilidades de errar vêm da matriz (Seção 3.7): o analista que erra paga o custo e recebe o resultado da ação errada, −40 ao rejeitar um cliente bom e −440 ao aprovar um ruim. A utilidade média da política é uma reta em *q*, e a Tabela 4.14 mostra, para cada modelo, o valor de *q* em que ela iguala a da política de duas ações (limiar 0,2, Seção 4.7) e a do corte 0,5. Não há grade de valores de *q*: o ponto de equilíbrio é calculado. O comando é `uv run python codigo/decisao.py --analista`, e o resultado está em `resultados/sensibilidade_analista_dev.csv`.

**Tabela 4.14** – Taxa de acerto *q* do analista em que a política de três ações iguala cada referência, no desenvolvimento (n = 800)

| Modelo | *q* contra duas ações | *q* contra o corte 0,5 | Utilidade com *q* = 1 | Utilidade com *q* = 0 |
|---|---|---|---|---|
| NB | 0,863 | 0,680 | 32,6 | −55,3 |
| TAN | 0,846 | 0,629 | 22,3 | −46,1 |
| Regressão logística | 0,894 | 0,719 | 30,9 | −66,0 |

Com um analista que sempre acerta (*q* = 1), a utilidade média da política de três ações é 32,6 no NB, 22,3 no TAN e 30,9 na regressão logística (a mesma da linha *p* (base) da Tabela 4.13), contra 20,6, 11,8 e 20,6 da política de duas ações e 4,5, −3,1 e 3,6 do corte 0,5. Para continuar acima da política de duas ações, o analista precisa acertar mais de 0,863 dos casos encaminhados no NB, 0,846 no TAN e 0,894 na regressão logística. Contra o corte 0,5, os valores são 0,680, 0,629 e 0,719. Nenhum equilíbrio fica abaixo de 0,5, a taxa de acerto de um analista que decide ao acaso. Com *q* = 0, a utilidade média da política de três ações é negativa nos três modelos (−55,3, −46,1 e −66,0).

O resultado é desfavorável à robustez da política de três ações. Ela só supera a de duas ações se o analista acertar mais de 0,846 a 0,894 dos casos encaminhados, conforme o modelo, e só supera o corte 0,5 se acertar mais de 0,629 a 0,719. A vantagem observada nos Capítulos 4 e 5 supõe *q* = 1 e, no desenvolvimento, depende de um analista que acerte acima desses valores. Abaixo deles, a política de três ações tem utilidade média menor que a da referência.

Os números valem para este erro simétrico, no desenvolvimento, sem intervalo e sob a matriz demonstrativa. Um analista real pode errar mais em um estado do que no outro. A Tabela 4.14 não escolhe modelo, parâmetro nem matriz, e os resultados dos Capítulos 4 e 5 seguem com o analista idealizado.

## 4.10 Calibração de Platt nas predições do desenvolvimento: análise posterior ao plano

A análise a seguir foi feita no desenvolvimento, depois do plano e depois de o teste ter sido aberto, em complemento à Seção 4.8. Ela foi decidida e registrada em `docs/decisoes.md` antes de rodar. Não usa o teste e não altera a análise primária: os resultados dos Capítulos 4 e 5 seguem com as probabilidades sem correção, e a calibração do resultado principal continua só medida (Seção 5.9). Para cada partição *k* e cada modelo, uma regressão logística de uma única variável, `LogisticRegression(max_iter=1000)` com o parâmetro de regularização padrão, é ajustada sobre o logit da probabilidade de ruim *p* das outras quatro partições, com o estado ruim como alvo, e aplicada à partição *k*. Isso é a correção sigmoide de Platt \cite{platt2000}. Nenhuma constante nova entra: o ajuste usa só predições que os modelos já haviam feito fora da amostra, e nenhum modelo é treinado de novo. Os comandos são `uv run python codigo/modelos.py --calibrar` e `uv run python codigo/avaliar.py --calibrada`, e os resultados estão em `resultados/predicoes_calibradas_dev.csv` e `resultados/metricas_calibradas_dev.csv`.

**Tabela 4.15** – Brier, *log loss* e ECE no desenvolvimento antes e depois da correção de Platt, média (desvio) entre 5 partições

| Modelo | Brier antes | Brier depois | *Log loss* antes | *Log loss* depois | ECE antes | ECE depois |
|---|---|---|---|---|---|---|
| NB | 0,171 (0,013) | 0,164 (0,009) | 0,523 (0,035) | 0,496 (0,021) | 0,093 (0,014) | 0,074 (0,012) |
| TAN | 0,200 (0,030) | 0,181 (0,012) | 0,704 (0,136) | 0,541 (0,032) | 0,152 (0,050) | 0,074 (0,033) |
| Regressão logística | 0,165 (0,012) | 0,163 (0,008) | 0,504 (0,026) | 0,496 (0,018) | 0,095 (0,031) | 0,069 (0,020) |

Os valores de "antes" são os da Tabela 4.1. O ROC-AUC e o PR-AUC não mudam, porque a correção é monótona, e a linha da taxa base também não muda. Nos três modelos os três erros diminuem. A queda do ECE é 0,019 no NB, 0,078 no TAN e 0,026 na regressão logística; a do Brier é 0,006, 0,019 e 0,002; a do *log loss* é 0,027, 0,163 e 0,009. A maior mudança está no TAN, cujo ECE cai de 0,152 para 0,074 e cujo *log loss* cai de 0,704 para 0,541. Na regressão logística a mudança é pequena: a queda do Brier, 0,002, é menor que o desvio entre partições, 0,008 a 0,012. Mesmo corrigido, o Brier do TAN, 0,181, continua acima dos do NB e da regressão logística, 0,164 e 0,163: a correção melhora a probabilidade, não a separação entre bons e ruins.

**Figura 4.4** – Diagramas de confiabilidade no desenvolvimento, após a correção de Platt (`resultados/calibracao_calibrada_dev.png`)

Os números valem para o ajuste cruzado no desenvolvimento, sem intervalo, e têm três limites. Primeiro, as predições das outras quatro partições vieram de modelos treinados com linhas da partição *k*; os rótulos de *k* entram, de forma indireta, no ajuste, e esse efeito não foi medido, de modo que parte da melhora pode ser otimista. Segundo, o ECE com 10 faixas sobre cerca de 160 casos por partição é ruidoso: a queda do TAN, 0,078, é da mesma ordem do desvio do ECE antes da correção, 0,050, e um ECE de zero não é esperado nem com probabilidades bem calibradas. A leitura usa o ECE junto com o Brier e o *log loss*, que apontam a mesma direção. Terceiro, a política de decisão não foi refeita com as probabilidades corrigidas, e por isso não se mede aqui o efeito sobre as ações nem sobre a utilidade; a Seção 4.8 continua sendo a medida dessa sensibilidade. A Tabela 4.15 não escolhe modelo, parâmetro nem matriz, e a versão corrigida não substitui a original nos resultados dos Capítulos 4 e 5.
