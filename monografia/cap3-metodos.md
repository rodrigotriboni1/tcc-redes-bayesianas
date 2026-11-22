# 3 MATERIAIS E MÉTODOS

<!-- Entradas do.bib marcadas "% VERIFICAR" ou "A CONFERIR" só podem ser citadas depois de conferidas no original (PLANO.md §9). -->

Este capítulo descreve a base de dados, o protocolo de divisão e validação, os modelos de risco, as métricas, a camada de decisão por utilidade esperada, a análise de sensibilidade, o estudo secundário de seleção e os cuidados de reprodutibilidade. O plano principal de análise foi estabelecido antes da observação dos resultados do teste; duas decisões complementares de leitura foram registradas em 18/11/2026, após sua abertura, conforme a Seção 3.6; uma análise exploratória posterior foi decidida em 22/11/2026 (Seção 4.7).

## 3.1 Base de dados

Utiliza-se a base South German Credit \cite{gromping2019}, versão corrigida da German Credit Data \cite{hofmann1994}, disponibilizada no repositório da UCI \cite{uci573}. A base contém 1000 registros, 20 variáveis preditoras e a variável-alvo risco do crédito, com 300 casos classificados como ruins e 700 como bons. A codificação do alvo é invertida em relação ao usual: o valor 0 indica crédito ruim e o valor 1, crédito bom; a classe positiva adotada em todo o trabalho é a classe ruim, e toda probabilidade reportada refere-se à probabilidade de o caso ser ruim.

Das 20 variáveis preditoras, três são contínuas (duração do crédito, valor do crédito e idade) e as 17 restantes já são categóricas. No texto e nas tabelas de resultados, adotam-se os nomes traduzidos para o português; os nomes originais em alemão são mantidos apenas no código-fonte e na Tabela 1 para referência à base original. O identificador `record_id` é removido antes de qualquer etapa de modelagem.

**Tabela 3.1** – Dicionário das variáveis. Categorias: número de valores inteiros distintos observados no conjunto de desenvolvimento (n = 800), calculado a partir de `dados/processados/dev.csv`; os códigos e seus significados seguem o codetable.txt da UCI (South German Credit, https://archive.ics.uci.edu/dataset/573/south+german+credit+update), traduzidos para o português.

| Variável | Tradução | Tipo | Categorias |
|---|---|---|---|
| `kredit` | Risco do crédito (alvo) | Binária | 2: 0 = ruim; 1 = bom |
| `laufzeit` | Duração do crédito (meses) | Contínua, 3 faixas por tercis | — |
| `hoehe` | Valor do crédito | Contínua, 3 faixas por tercis | — |
| `alter` | Idade | Contínua, 3 faixas por tercis | — |
| `laufkont` | Situação da conta corrente | Categórica | 4 |
| `verw` | Finalidade do crédito | Categórica | 10 observados (a fonte define 0 a 10) |
| `bishkred` | Número de créditos neste banco, incluindo o atual | Categórica | 4 |
| `telef` | Telefone fixo no nome do cliente | Categórica | 2 |
| `moral` | Histórico de crédito | Categórica | 5 |
| `sparkont` | Poupança | Categórica | 5 |
| `beszeit` | Tempo no emprego atual | Categórica | 5 |
| `rate` | Parcela em relação à renda disponível | Categórica | 4 |
| `famges` | Estado civil e sexo (`personal_status_sex`) | Categórica | 4 |
| `buerge` | Outros devedores ou fiadores | Categórica | 3 |
| `wohnzeit` | Tempo na residência atual | Categórica | 4 |
| `verm` | Bem mais valioso | Categórica | 4 |
| `weitkred` | Outros planos de parcelamento | Categórica | 3 |
| `wohn` | Tipo de moradia | Categórica | 3 |
| `beruf` | Qualificação da ocupação | Categórica | 4 |
| `pers` | Pessoas dependentes (`people_liable`) | Categórica | 2 |
| `gastarb` | Trabalhador estrangeiro | Categórica | 2 |

Traduções e códigos conferidos, variável a variável, no codetable.txt do conjunto South German Credit, UCI, https://archive.ics.uci.edu/dataset/573/south+german+credit+update. Na fonte, finalidade do crédito tem 11 códigos (0 a 10); 10 aparecem no conjunto de desenvolvimento.

A base apresenta categorias raras, por exemplo número de créditos no banco = 4 e finalidade do crédito = 8. Essa característica motiva o uso de *prior* bayesiano na estimação dos parâmetros (Seção 3.5).

No conjunto de desenvolvimento (n = 800), número de créditos no banco = 4 tem 5 casos e finalidade do crédito = 8 tem 7 casos; as demais categorias pequenas têm de 9 a 35 casos.

A análise exploratória relatada limita-se à tabela descritiva apresentada a seguir (contagens e as três variáveis contínuas), elaborada a partir do conjunto de desenvolvimento, sem *script* dedicado.

**Tabela 3.2** – Descrição do conjunto de desenvolvimento (n = 800), calculada a partir de `dados/processados/dev.csv`.

| Item | Valor |
|---|---|
| Linhas | 800 |
| Casos ruins (risco do crédito = 0) | 240 (30,0%) |
| duração do crédito (meses) | mínimo 4; cortes dos tercis 12 e 24; máximo 72 |
| valor do crédito | mínimo 250; cortes dos tercis 1553 e 3384; máximo 18424 |
| idade (anos) | mínimo 19; cortes dos tercis 28 e 38; máximo 75 |

Os tercis acima são calculados sobre todo o conjunto de desenvolvimento, apenas para descrição; no experimento os cortes são aprendidos só no treino de cada partição.

## 3.2 Divisão em desenvolvimento e teste

A base é dividida de forma estratificada, com semente 2026, em um conjunto de desenvolvimento, com 800 casos (240 ruins), e um conjunto de teste, com 200 casos (60 ruins). Uma divisão anterior, com semente 42, foi descartada porque seu conjunto de teste já havia sido usado para avaliar a regressão logística em trabalho anterior.

O conjunto de teste permanece fechado durante todo o desenvolvimento. Todos os modelos, inclusive o de referência, são avaliados nele uma única vez, após um *commit* de congelamento do código. O teste foi executado uma única vez, em 17/11/2026, sobre o *commit* de congelamento 49d77ff0eec74de98d7ce7ec83a9d0d2907bb207, com os três comandos do caminho `--final`. Os *scripts* de modelagem leem exclusivamente o conjunto de desenvolvimento. Em 22/11/2026, depois de conhecido o resultado, o comando `decisao.py --final` foi executado de novo sobre as predições já gravadas, sem reabrir o arquivo do teste, para a análise exploratória da Seção 4.7; os seis arquivos anteriores não mudaram.

## 3.3 Validação cruzada

No conjunto de desenvolvimento, adota-se validação cruzada estratificada em 5 partições, com semente 2026. Cada partição é usada uma vez como validação enquanto as outras quatro compõem o treino, de modo que cada caso recebe uma predição de um modelo que não o viu. As métricas de desenvolvimento são reportadas como média e desvio entre as 5 partições.

Todas as constantes (partições, faixas, tamanho equivalente e grade da sensibilidade) foram fixadas por convenção, e não por desempenho.

## 3.4 Discretização

As implementações de redes bayesianas discretas adotadas neste trabalho exigem variáveis discretas. As três variáveis contínuas são discretizadas em 3 faixas por tercis, com cortes aprendidos apenas no treino de cada partição, para evitar vazamento de informação da partição de validação \cite{kaufman2012}. Para o teste final, os cortes são aprendidos no conjunto de desenvolvimento inteiro e gravados em `resultados/cortes.json`.

O número de faixas segue essa convenção (ver Seção 3.3), não foi otimizado, e a discretização descarta informação das três variáveis contínuas.

## 3.5 Modelos de risco

São comparados três modelos que estimam a probabilidade de um crédito ser ruim:

1. **Naive Bayes**, rede em que a variável-alvo é pai de cada preditora, tratadas como condicionalmente independentes dado o alvo \cite{friedman1997}; 
2. **TAN** (*Naive Bayes* aumentado por árvore), que acrescenta ao *Naive Bayes* uma árvore de dependências entre as preditoras \cite{friedman1997,chowliu1968}. A árvore é a de máximo peso no grafo completo das preditoras, em que o peso de cada aresta é a informação mútua entre as duas preditoras condicional à classe, $I(X_i; X_j \mid C)$; a árvore é então orientada a partir de uma raiz, e a classe é acrescentada como pai de todas as preditoras \cite{friedman1997,chowliu1968}; 
3. **Regressão logística**, como modelo de referência \cite{pedregosa2011}.

A busca por *hill climbing*, prevista como opcional, não foi rodada.

As redes são implementadas com a biblioteca `pgmpy`, na versão fixa 1.1.2 \cite{ankan2024}. O *Naive Bayes* é montado como rede em estrela, pois a classe específica da biblioteca falha no cálculo de probabilidades nessa versão. A raiz da árvore do TAN não é indicada na chamada `TreeSearch(treino).estimate(estimator_type="tan", class_node="kredit")`; nesse caso, o `pgmpy` 1.1.2 toma como raiz a variável com a maior soma de informação mútua (não condicional) com as demais colunas. A estrutura do TAN é aprendida em cada partição, e as arestas resultantes são registradas em `resultados/tan_arestas.csv` para descrever a estabilidade da estrutura entre partições.

Os parâmetros das redes são estimados por estimação bayesiana com *prior* BDeu de tamanho equivalente 5 \cite{heckerman1995}, para evitar probabilidade zero em combinações raras. O *prior* BDeu é uma distribuição de Dirichlet uniforme sobre cada tabela de probabilidade condicional: o tamanho equivalente $N'$ é repartido igualmente entre as células, de modo que cada combinação de valor $x_i$ do nó e configuração $\mathrm{pa}_i$ dos pais recebe a pseudocontagem $N'/(r_i q_i)$, em que $r_i$ é o número de estados do nó e $q_i$ o número de configurações dos pais \cite{heckerman1995}. O espaço de estados de cada variável é fixado com todos os valores que aparecem no conjunto de desenvolvimento inteiro, para que uma categoria rara ausente do treino de uma partição não interrompa a inferência. Essa escolha não usa o rótulo, mas constitui um vazamento brando de informação, aqui declarado.

O tamanho equivalente segue essa convenção (ver Seção 3.3); outros valores só aparecem no estudo de seleção secundário.

A inferência é exata, por eliminação de variáveis, viável porque as redes são pequenas (`predict_probability` do `pgmpy`, conferida contra `VariableElimination` no modo `--verificar`) \cite{koller2009}.

A regressão logística é configurada como `LogisticRegression(max_iter=1000)`, herdada da avaliação anterior, e recebe as três variáveis contínuas em sua forma original, sem discretização. Em consequência, a diferença entre as redes e a regressão logística mistura modelo e representação das variáveis, e não é interpretada como efeito do modelo isoladamente.

A calibração das probabilidades é apenas medida, sem aplicação de método de correção.

### 3.5.1 Evidência incompleta

Para avaliar o comportamento com evidência incompleta, cada variável é ocultada, uma por vez, no momento da predição, medindo-se a variação de ROC-AUC e de Brier. As redes marginalizam a variável ocultada; na regressão logística, ela é preenchida com a mediana do treino (para as 3 contínuas) ou com a moda do treino (para as 17 categóricas). Por isso, as quedas não são comparáveis entre as duas famílias de modelos.

## 3.6 Métricas

O desempenho dos modelos de risco é medido pela área sob a curva ROC (ROC-AUC), pela área sob a curva de precisão e sensibilidade (PR-AUC), pelo escore de Brier \cite{brier1950}, pelo *log loss* e pelo ECE \cite{naeini2015}, acompanhados de diagrama de calibração. A PR-AUC é incluída porque a classe positiva corresponde a 30% dos casos. Como referência, reporta-se também um preditor que atribui a todo caso a taxa base de ruins.

O ECE é calculado com 10 faixas de mesma largura sobre P(ruim), comparando a probabilidade média prevista com a taxa observada de ruins em cada faixa. Essa definição difere da versão *top-label* usada na avaliação anterior; os dois valores não são comparáveis, e apenas a definição atual é usada.

Para $n$ casos com rótulo $y_k \in \{0, 1\}$ (1 = ruim) e probabilidade prevista $p_k$ de ruim, as duas métricas são

$$\text{log loss} = -\frac{1}{n}\sum_{k=1}^{n}\left[y_k \ln p_k + (1-y_k)\ln(1-p_k)\right],$$

$$\text{ECE} = \sum_{b=1}^{10}\frac{|B_b|}{n}\left|\bar{y}_b - \bar{p}_b\right|,$$

em que $B_b$ é o conjunto de casos cuja $p_k$ cai na faixa $b$, e $\bar{y}_b$ e $\bar{p}_b$ são a taxa observada de ruins e a probabilidade média prevista nessa faixa \cite{naeini2015}.

No conjunto de teste, ROC-AUC, PR-AUC, Brier e utilidade média recebem intervalo por *bootstrap* com 2000 reamostras, semente 2026 e percentis 2,5 e 97,5 \cite{efron1993}. O intervalo não cobre a variação devida ao treino.

As regras principais de leitura foram fixadas em 15/11/2026, antes dos resultados; houve complementações documentadas em 18/11/2026, após a abertura do teste (Apêndice B), e uma análise exploratória decidida em 22/11/2026, descrita na Seção 4.7. Diferença de ROC-AUC menor que 0,03 entre dois modelos é tratada como ruído, sem apontar vencedor (convenção descritiva do plano, que não constitui teste de equivalência nem permite concluir que os modelos são iguais); Brier igual ou maior que o da taxa base é relatado como "não melhor que prever a taxa base", comparação pontual, sem inferência estatística.

O limite de 0,03 vale só para ROC-AUC: a PR-AUC é descrita sem conclusão de ruído, e a diferença pareada de utilidade é lida pelo intervalo de 95%, por decisão do autor registrada em docs/decisoes.md.

## 3.7 Camada de decisão por utilidade esperada

A escolha da ação é separada da estimação do risco. Dado o risco estimado *p* de o caso ser ruim, a utilidade esperada de uma ação *a* é

$$UE(a) = (1 - p)\,U(a, \text{bom}) + p\,U(a, \text{ruim}),$$

e escolhe-se a ação de maior utilidade esperada \cite{russell2010,howard2005}. São consideradas três ações: aprovar, rejeitar e encaminhar para análise manual. O custo esperado corresponde ao negativo da utilidade esperada.

A matriz de utilidade é demonstrativa e lida de `config/utilidade.json` (Quadro 3.1).

**Quadro 3.1 – Matriz de utilidade demonstrativa**

| Ação | Caso bom | Caso ruim |
|---|---|---|
| Aprovar | +100 | −400 |
| Rejeitar | 0 | 0 |
| Análise manual | 100 − *c* | −*c* |

Fonte: `config/utilidade.json`, com *c* = 40.

A matriz de utilidade, aprovada pelo orientador para fins demonstrativos, contém valores não calibrados com dados reais e pressupõe que o analista identifique corretamente o estado de cada cliente.

Como a utilidade esperada de cada ação é linear em *p*, a política resultante equivale a uma regra de limiares sobre *p* \cite{elkan2001}. Com a matriz acima, a análise manual é escolhida quando *c*/400 ≤ *p* ≤ 1 − *c*/100; com *c* = 40, a faixa vai de 0,10 a 0,60, e com *c* > 80 a análise manual nunca é escolhida. Empates são resolvidos, com tolerância de 1e-9, pela prioridade análise manual, rejeitar, aprovar. O que se implementa é a aplicação explícita dos limiares derivados dos custos, acompanhada da medição da calibração das probabilidades. A exigência de probabilidade calibrada é tomada da literatura, não demonstrada pelo experimento.

Estimativas de probabilidade bem calibradas são necessárias quando a decisão leva em conta custos \cite{zadrozny2001}.

### 3.7.1 Comparação de políticas

A política é calculada para os três modelos e comparada com um limiar fixo de 0,5 de duas ações. A comparação principal, fixada antes de qualquer métrica, usa o TAN; *Naive Bayes* e regressão logística são reportados em apêndice na mesma estrutura. A comparação de duas regras é descrita como "política de três ações por utilidade esperada contra corte 0,5 de duas ações", sem linguagem causal, pois a diferença mistura modelo, representação e conjunto de ações. A inclusão da análise manual aumenta ou mantém a utilidade esperada máxima prevista pelo modelo, mas não garante superioridade em utilidade realizada para todo conjunto de observações; o corte de 0,5 também não é o limiar ótimo de duas ações para essa matriz, o que é declarado junto da tabela. Com a matriz demonstrativa, o limiar de duas ações é 0,2 (Seção 2.7), e não 0,5: o corte de 0,5 é a regra de referência convencional, fixada no plano, e não foi otimizado. Assim, a diferença entre as duas políticas reúne o efeito da ação adicional, o do corte de referência e o do uso da utilidade esperada, e não isola o método decisório. A Seção 4.7 mede, de forma exploratória e posterior ao teste, a política de duas ações com limiar 0,2.

São medidas a utilidade média, a distribuição das ações e o número de casos que mudam de ação entre as políticas. No teste, reporta-se também a diferença pareada de utilidade média entre a regra de utilidade e o limiar fixo, com intervalo por *bootstrap*. Para a regra de utilidade, registram-se ainda a segunda melhor ação e a diferença de utilidade esperada em relação a ela.

## 3.8 Análise de sensibilidade

A sensibilidade da política aos custos é avaliada calculando-se as fronteiras de decisão em uma grade de perda por inadimplência em {200, 400, 600, 800} e custo da análise manual em {0, 5, …, 100}. A análise mostra a ação recomendada em função do risco, da perda e do custo da análise manual.

Os valores da grade seguem essa convenção (ver Seção 3.3).

A sensibilidade à calibração é avaliada sem recalibrar. Às probabilidades já gravadas (desenvolvimento e teste) soma-se à log-odds um viés *delta*, de modo que a camada de decisão recebe *p*′ = expit(logit(*p*) + *delta*), com *delta* em {−1; −0,5; −0,25; 0; +0,25; +0,5; +1}; valores positivos fazem o modelo parecer mais pessimista. Nenhum modelo é treinado de novo, nenhum método de correção é aplicado e o rótulo observado não é alterado: a utilidade é medida contra ele, como na análise principal. Deslocar *p* dessa forma equivale a deslocar as fronteiras de decisão sobre a probabilidade original, e as fronteiras equivalentes são gravadas junto com os resultados. A grade foi fixada antes de rodar a análise e não é escolhida a partir de nenhum resultado. No teste, a análise é exploratória e posterior à abertura, e não altera a análise primária (Seção 5.9).

## 3.9 Demonstração

Um *script* de terminal recebe o identificador de um caso, treina novamente o modelo nas 4 partições que não contêm o caso e mostra o risco estimado, a utilidade esperada de cada ação, as fronteiras e a ação recomendada; o modelo padrão é o TAN. A demonstração mostra a conta, não uma justificativa textual da recomendação.

## 3.10 Estudo de seleção aninhado (secundário)

Como análise secundária, planejada antes do teste final e depois das métricas de desenvolvimento (declaração de viés abaixo), realiza-se um estudo de seleção de configuração. A análise primária, incluindo a comparação de duas regras com NB e TAN de BDeu 5, não muda.

A grade é fechada, com 8 configurações: {*Naive Bayes*, TAN} × tamanho equivalente BDeu {1, 5, 10, 50}. Ficam fora da grade K2, outras faixas, seleção de variáveis, *hill climbing*, métodos de calibração e reponderação.

Usa-se validação cruzada aninhada. As partições externas são as 5 já descritas; em cada uma, as 640 linhas de treino são divididas em 5 partições internas estratificadas, com semente 2026, nas quais cada configuração é treinada e avaliada. Escolhe-se a configuração de menor *log loss* médio nas partições internas, com empate (diferença menor que 1e-9) resolvido pela ordem da grade; a configuração escolhida prevê as 160 linhas da partição externa, gerando a linha "aninhado". A escolha é também recalculada no conjunto de desenvolvimento inteiro, só para relato; essa configuração é a usada como modelo secundário no teste final.

Relatam-se obrigatoriamente as 8 configurações, o número de comparações (8) e a linha "aninhado", qualquer que seja o resultado. O texto não se refere a um "melhor modelo": informa qual configuração a regra escolheu e quanto ela difere da configuração de base.

**Declaração de viés.** A grade de 8 configurações foi definida depois da observação das métricas de desenvolvimento (`metricas_dev.csv`) e motivada por elas: o TAN saiu pior que o NB e surgiu a hipótese sobre a finalidade do crédito (Seção 4.1). O aninhamento corrige o viés de escolher entre as 8 configurações, mas não o de ter desenhado a grade com base no mesmo conjunto de desenvolvimento.

## 3.11 Ambiente e reprodutibilidade

O experimento é composto por sete *scripts* Python que leem CSV e gravam tabelas e figuras, sem modelo salvo em arquivo. O projeto exige Python 3.12 ou superior. A execução local usou Python 3.12.13 (saída de `uv run python --version`); `uv.lock` e `pyproject.toml` fixam apenas `requires-python = ">=3.12"`, e não há `.python-version`. As bibliotecas são `pgmpy` 1.1.2, `scikit-learn` \cite{pedregosa2011}, `pandas` e `matplotlib`, com dependências fixadas pelo gerenciador `uv`. Toda fonte de aleatoriedade usa a semente 2026, e duas execuções do mesmo comando na mesma máquina geram arquivos CSV e JSON idênticos byte a byte. Os arquivos de resultado são versionados com o código, e a reprodução é conferida pela comparação com a versão registrada no *commit*. As figuras PNG não são comparadas byte a byte. O passo a passo completo está no Apêndice A.

Conferências realizadas. Além dos modos `--verificar` e do teste da camada de decisão, as saídas foram conferidas em uma reimplementação independente em NumPy (sem uso do `pgmpy`, do `scikit-learn` nem do `pandas`), versionada em `codigo/auditoria_independente.py`. Sobre as predições já gravadas do desenvolvimento e do conjunto de teste (sem abrir o arquivo com as linhas do teste), foram recalculados: escore de Brier, *log loss*, ECE de dez faixas, ROC-AUC e PR-AUC, ações escolhidas e utilidade média das políticas (três ações, duas ações com limiar 0,20 e corte 0,50). Também foram conferidos, no desenvolvimento, a divisão estratificada em cinco partições, a árvore do TAN em cada partição (informação mútua condicional à classe e árvore geradora máxima) e a estimação dos parâmetros com prior BDeu ($N' = 5$) seguida de inferência exata para *Naive Bayes* e TAN. Os valores coincidiram com os arquivos gravados (diferenças numéricas abaixo de $10^{-12}$, ações e utilidades idênticas, cinco partições com 160 casos e 48 ruins e 19 arestas entre variáveis em cada partição, todas coincidentes com `tan_arestas.csv`). As probabilidades do teste, que dependem do arquivo com as linhas do teste, não foram recalculadas por outro código: só as métricas e as políticas sobre elas. A reprodução completa do ambiente travado e dos arquivos de resultado foi executada também em ambiente Linux limpo via integração contínua (GitHub Actions, em 22/11/2026). Os arquivos de desenvolvimento gerados coincidiram com os versionados: os demais CSV e JSON ficaram idênticos byte a byte, e os cinco que dependem da regressão logística (predições, métricas, políticas, evidência incompleta e predições com variável oculta) diferiram só nos últimos dígitos, em até $4{,}3 \times 10^{-8}$ nas probabilidades e $4{,}8 \times 10^{-6}$ em colunas em unidades de utilidade, com as mesmas ações e contagens. A regressão logística não reproduz bit a bit entre plataformas, e a comparação byte a byte vale na máquina do autor. Embora essas conferências eliminem a dependência exclusiva das bibliotecas do experimento e do ambiente local do autor, trata-se de verificação automatizada do próprio autor e não substitui uma revisão de código por terceiros.
