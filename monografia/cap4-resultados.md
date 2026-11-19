# 4 RESULTADOS

Este capítulo relata os resultados. Os números de desenvolvimento (Tabelas 4.1, 4.3, 4.4, 4.7, 4.9, 4.10) são resultados de desenvolvimento pré-estudo, obtidos só com os 800 casos de desenvolvimento (validação cruzada estratificada em 5 partições, Capítulo 3, Seções 3.2 e 3.3); os blocos do conjunto de teste (Tabelas 4.2, 4.5, 4.6 e Figura 4.2) são identificados na legenda pelo rótulo "conjunto de teste (n = 200; 60 ruins)". O conjunto de teste final foi aberto uma única vez, em 17/11/2026, após o *commit* de congelamento 49d77ff. A numeração das tabelas e figuras é sequencial. Cada seção remete à seção correspondente do Capítulo 3. A leitura de cada resultado segue as regras pré-registradas na §4 do plano de análise (`docs/plano-de-analise.md`), e a interpretação fica para o Capítulo 5.

Nas tabelas de métricas (4.1 e 4.9), os valores são médias e desvios entre as 5 partições. Cada número traz a indicação do arquivo e da coluna de origem, no formato. A Tabela 4.2 traz o valor no conjunto de teste com intervalo de 95% por *bootstrap*. Os valores são arredondados a três casas, salvo indicação.

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

- **ROC-AUC, nb contra logreg.** A diferença é 0,001 (0,7890 contra 0,7880), menor que 0,03. Pela regra pré-registrada, é tratada como ruído e nenhum dos dois modelos se distingue do outro por essa métrica.
- **ROC-AUC, nb e logreg contra tan.** As diferenças são 0,047 (nb − tan) e 0,046 (logreg − tan). Ambas passam de 0,03, de modo que a regra de ruído não se aplica a esses pares. O plano não prevê outra regra para esse caso; registra-se ao lado que o desvio do tan entre partições é 0,049. O TAN teve desempenho pior que o NB nas cinco métricas no desenvolvimento (ROC-AUC e PR-AUC menores; Brier, *log loss* e ECE maiores), e esse resultado é relatado como saiu.
- **Brier contra taxa base.** O Brier médio dos três modelos (nb 0,171; tan 0,200; logreg 0,165) é menor que o da taxa base, 0,210. A condição "igual ou maior que 0,21" não ocorre; a frase "não melhor que prever a taxa base" não é acionada para nenhum modelo.
- **Calibração.** O ECE do tan, 0,152, é o maior dos três (nb 0,093; logreg 0,095). Conforme a regra pré-registrada e a decisão P1, a calibração é apenas medida e relatada; não há correção. Os diagramas de confiabilidade dos três modelos estão em `resultados/calibracao_dev.png`.

**Figura 4.1** – Diagramas de confiabilidade no desenvolvimento (`resultados/calibracao_dev.png`)

**Arestas do TAN.** O plano determina que as arestas aprendidas pelo TAN em cada partição sejam relatadas nesta seção. Em todas as 5 partições há 39 arestas, 20 das quais saem da classe risco do crédito.

Fora a classe, a variável da qual sai o maior número de arestas, em todas as partições, é finalidade do crédito (7 a 9 por partição; 1 ou 2 chegam a ela). Registra-se, como **hipótese não testada**, que o fato de finalidade do crédito ser pai de muitas variáveis poderia produzir tabelas de probabilidade condicional esparsas e excesso de confiança, o que seria coerente com o *log loss* e o erro de calibração maiores do tan. Nenhuma análise deste trabalho testou essa hipótese: a contagem de arestas e as métricas apenas coexistem, e a observação não autoriza alterar modelo, faixa ou parâmetro.

**Conjunto de teste (n = 200; 60 ruins).** O teste final foi executado uma única vez, em 17/11/2026, sobre o *commit* de congelamento 49d77ff. Os intervalos são de 95% por *bootstrap*. A Tabela 4.2 traz as métricas; a linha `sel` é a análise secundária da Seção 4.6.

**Tabela 4.2** – Métricas por modelo no conjunto de teste (n = 200; 60 ruins), valor [intervalo de 95%]

| Modelo | ROC-AUC [IC 95%] | PR-AUC [IC 95%] | Brier [IC 95%] | *log loss* | ECE |
|---|---|---|---|---|---|
| NB | 0,728 [0,648; 0,802] | 0,490 [0,378; 0,630] | 0,199 [0,161; 0,239] | 0,627 | 0,115 |
| TAN | 0,706 [0,623; 0,789] | 0,480 [0,372; 0,617] | 0,215 [0,173; 0,261] | 0,780 | 0,157 |
| Regressão logística | 0,729 [0,651; 0,800] | 0,500 [0,383; 0,636] | 0,191 [0,157; 0,228] | 0,578 | 0,078 |
| Taxa base | 0,500 [0,500; 0,500] | 0,300 [0,235; 0,365] | 0,210 [0,184; 0,236] | 0,611 | 0,000 |
| sel (secundária) | 0,720 [0,641; 0,795] | 0,477 [0,365; 0,620] | 0,202 [0,164; 0,242] | 0,623 | 0,120 |

Aplicando as regras da §4 do plano de análise ao conjunto de teste:

- **ROC-AUC.** As diferenças entre os três modelos primários são 0,001 (logreg − nb: 0,7287 contra 0,7277), 0,021 (nb − tan: 0,7277 contra 0,7063) e 0,022 (logreg − tan: 0,7287 contra 0,7063). As três são menores que 0,03 e, pela regra pré-registrada, tratadas como ruído: nenhum modelo se distingue dos outros por essa métrica no teste.
- **PR-AUC.** Os valores são 0,490 (nb), 0,480 (tan) e 0,500 (logreg), contra 0,300 da taxa base. O limite de 0,03 vale só para ROC-AUC; por decisão do autor registrada em docs/decisoes.md (plano de análise, §8), nenhuma regra é aplicada a essas diferenças e elas são apenas descritas, sem conclusão de ruído.
- **Brier contra taxa base.** O Brier do tan no teste é 0,215, maior que o da taxa base, 0,210. Pela regra pré-registrada, o tan é **não melhor que prever a taxa base** no conjunto de teste. O nb (0,199) e o logreg (0,191) ficam abaixo de 0,21, e a regra não é acionada para eles.
- **Calibração.** O ECE é 0,115 (nb), 0,157 (tan) e 0,078 (logreg).

Conforme a decisão P1, é apenas relatado; não há correção. O *log loss* do tan, 0,780, do nb, 0,627, e do sel (secundária), 0,623, são maiores que o da taxa base, 0,611. O plano não tem regra para *log loss* contra a taxa base, e o fato é apenas descrito.
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

A utilidade média da política de três ações (`ue`) é maior que a do corte 0,5 de duas ações (`limiar`) nos três modelos, com diferenças de 28,125 (nb), 25,4 (tan) e 27,25 (logreg). Trata-se de diferença descritiva no desenvolvimento, sem intervalo: pelo plano, a comparação pareada com intervalo só é feita no teste final, e a diferença mistura modelo, representação e conjunto de ações, razão pela qual não é chamada de efeito da regra. Na política de três ações (`ue`), a análise manual recebe 355 (nb), 262 (tan) e 415 (logreg) dos 800 casos; o corte 0,5 de duas ações (`limiar`) tem zero casos nessa ação por definição, por ter só duas ações. As três ações aparecem na política de três ações (`ue`) em todos os modelos, de modo que a regra "alguma ação não aparece numa política" não se aplica. O número de casos cuja ação muda entre as regras coincide, em cada modelo, com o número de casos em análise manual da política de três ações (`ue`). A ação de cada caso está em `resultados/politicas_dev.csv`.

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

Com custo zero, a faixa de análise manual cobre todo o intervalo de 0 a 1 (linha 400, 0). Quando os dois limiares coincidem, a faixa desaparece e a política se reduz a duas ações; isso ocorre, por exemplo, para perda 200 com custo a partir de 70 e para perda 400 com custo a partir de 80. A Figura 4.3 mostra a tabela inteira. Não há regra da §4 para esta análise, e este texto não escolhe valor de custo nem de perda.

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

Esta seção relata o estudo secundário e pré-registrado da §9 do plano de análise (Seção 3.10). Ele não altera a análise primária: as Seções 4.1 a 4.4 continuam com NB e TAN de tamanho equivalente BDeu 5.

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

**Escolha por partição.** Pela regra pré-registrada (menor *log loss* médio nas partições internas), `nb_ess50` foi escolhida nas cinco partições externas e também no desenvolvimento inteiro. A Tabela 4.10 traz o *log loss* interno da configuração escolhida e das duas configurações de referência.

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

**Conjunto de teste (n = 200; 60 ruins), análise secundária.** As predições `p_sel` no teste estão em `resultados/predicoes_teste.csv` (coluna `p_sel`), e suas métricas, na linha `sel` da Tabela 4.2. Como define a §9, a diferença principal da escolha é contra a configuração de referência `nb` (NB, BDeu 5): a ROC-AUC de `sel` é 0,720 [0,641; 0,795], contra 0,728 do `nb`; a diferença, 0,008 (nb − sel), é menor que 0,03 e, pela regra da §9, tratada como ruído. De forma apenas descritiva, a diferença contra o `tan` (TAN, BDeu 5, ROC-AUC 0,706) é 0,014 (sel − tan). O *log loss* de `sel` é 0,623, contra 0,627 do `nb` (diferença de 0,005, calculada sobre os valores não arredondados: 0,6273 − 0,6226); o plano não tem regra de leitura para essa diferença, e ela é apenas descrita. O Brier de `sel`, 0,202, é menor que o da taxa base, 0,210. Na política de decisão, a diferença pareada de `sel` é 34,4 [16,4; 52,5] (Tabela 4.6). Esses números relatam quanto a configuração escolhida pela regra difere da configuração de referência no teste; não indicam qual modelo adotar, e a análise primária continua com NB e TAN de BDeu 5.
