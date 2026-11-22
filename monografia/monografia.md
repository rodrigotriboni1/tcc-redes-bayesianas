## CAPA

**UNIVERSIDADE FEDERAL DE UBERLÂNDIA (UFU)** 

[Faculdade e curso conforme o modelo do Colegiado — a preencher pelo autor]

Curso: Engenharia de Controle e Automação

**RODRIGO MIALICHI TRIBONI**

**REDES BAYESIANAS E UTILIDADE ESPERADA APLICADAS À SELEÇÃO DE *NEXT BEST ACTION* EM SISTEMAS AUTOMATIZADOS DE DECISÃO** 

[Local — a preencher pelo autor]

[Ano — a preencher pelo autor]

<!-- quebra de página -->

## FOLHA DE ROSTO

**RODRIGO MIALICHI TRIBONI**

**REDES BAYESIANAS E UTILIDADE ESPERADA APLICADAS À SELEÇÃO DE *NEXT BEST ACTION* EM SISTEMAS AUTOMATIZADOS DE DECISÃO**

[Natureza do trabalho e objetivo (por exemplo, trabalho de conclusão de curso, grau pretendido), instituição e curso, conforme o modelo do Colegiado — a preencher pelo autor]

Curso: Engenharia de Controle e Automação

Orientador: Fabio Vincenzi

[Titulação do orientador — a preencher pelo autor]

[Local — a preencher pelo autor]

[Ano — a preencher pelo autor]

# RESUMO

A concessão de crédito costuma decidir comparando um escore de risco com um ponto de corte, o que mistura a estimativa do risco com a escolha da ação. Pergunta-se se uma política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) produz (1) limiares explícitos, reproduzíveis a partir da matriz de utilidade e da probabilidade estimada, e (2) qual efeito medido exerce sobre as ações e a utilidade média, diante de um limiar fixo de 0,5. Usa-se a base South German Credit, dividida de forma estratificada em 800 casos de desenvolvimento e 200 de teste, com validação cruzada estratificada em 5 partições no desenvolvimento. O risco de o crédito ser ruim é estimado por duas redes bayesianas, *Naive Bayes* e TAN (*Naive Bayes* aumentado por árvore), implementadas com a biblioteca pgmpy, e por uma regressão logística de referência. Os modelos são avaliados pela área sob a curva ROC (ROC-AUC), pela área sob a curva de precisão e sensibilidade (PR-AUC), pelo escore de Brier, pelo *log loss* e pelo erro de calibração esperado (ECE); a calibração é medida, sem correção. Uma camada de utilidade esperada escolhe, para cada caso, entre três ações: aprovar, rejeitar ou encaminhar para análise manual. A matriz de utilidade é demonstrativa, não calibrada com dados reais, e supõe que o analista da análise manual sempre acerta o estado do cliente. Mede-se a distribuição das ações, a utilidade média e o número de casos que mudam de ação em relação ao limiar fixo. Mede-se também a sensibilidade das fronteiras aos custos e o comportamento com evidência incompleta. Um estudo de seleção secundário de estrutura e *prior*, por validação cruzada aninhada, com a grade definida depois de ver as métricas de desenvolvimento, é relatado à parte. Como a base não registra o resultado das ações não tomadas, a camada de decisão é uma simulação metodológica, e não a validação de uma política real. Os resultados de desenvolvimento são relatados sem intervalo de confiança. O conjunto de teste, aberto uma única vez, tem 200 casos e 60 ruins. Nele, as diferenças de ROC-AUC entre os três modelos ficaram abaixo de 0,03 e são tratadas como ruído, e o escore de Brier do TAN (0,215) não foi melhor que prever a taxa base (0,210). Na comparação principal, com o TAN, a utilidade média foi 17,5 na política de três ações e −5,0 no corte 0,5. O critério de leitura é a diferença pareada entre as duas: 22,5, com intervalo de 95% de 9,2 a 37,2, que exclui zero; 60 casos mudaram de ação. A política de três ações ganha por construção, pois só ela tem a análise manual com analista infalível, e o resultado vale para a simulação. Os resultados de desenvolvimento e de teste são distintos e relatados separadamente.

**Palavras-chave:** redes bayesianas; risco de crédito; utilidade esperada; calibração; teoria da decisão.

# ABSTRACT

Credit granting usually decides by comparing a risk score with a threshold, which mixes risk estimation with the choice of action. This work asks whether a policy that separates risk estimation (Bayesian network, with measured calibration) from the choice of action (expected utility) has (1) explicit thresholds that anyone can reproduce from the utility matrix and the estimated probability and (2) what measured effect it has on the actions and the average utility, compared with a fixed threshold of 0.5. The South German Credit dataset is used, split in a stratified way into 800 development cases and 200 test cases, with stratified five-fold cross-validation on the development set. The probability of bad credit is estimated by two Bayesian networks, Naive Bayes and Tree-Augmented Naive Bayes (TAN), implemented with the pgmpy library, and by a reference logistic regression. The models are evaluated by the area under the ROC curve (ROC-AUC), the area under the precision-recall curve (PR-AUC), the Brier score, log loss and expected calibration error (ECE); calibration is measured but not corrected. An expected-utility layer chooses, for each case, among three actions: approve, reject or refer to manual review. The utility matrix is illustrative, not calibrated with real data, and assumes that the manual-review analyst always identifies the client's true state. The distribution of actions, the average utility and the number of cases that change action relative to the fixed threshold are measured. The sensitivity of the boundaries to costs and the behavior under incomplete evidence are also measured. A secondary structure and prior selection study, by nested cross-validation, with the grid defined after seeing the development metrics, is reported separately. Because the dataset does not record the outcome of actions not taken, the decision layer is a methodological simulation, not the validation of a real policy. The development results are reported as a baseline, without confidence intervals. The test set, opened only once, has 200 cases, 60 of them bad credit. On it, the ROC-AUC differences among the three models were below 0.03 and are treated as noise, and the Brier score of TAN (0.215) was not better than predicting the base rate (0.210). In the main comparison, with TAN, the average utility was 17.5 for the three-action policy and −5.0 for the 0.5 threshold. The reading criterion is the paired difference between them: 22.5, with a 95% interval from 9.2 to 37.2, which excludes zero; 60 cases changed action. The three-action policy wins by construction, since only it has manual review with an infallible analyst, and the result holds for the simulation. The development and test results are distinct and reported separately.

**Keywords:** Bayesian networks; credit risk; expected utility; calibration; decision theory.

## LISTA DE FIGURAS

Figura 4.1 – Diagramas de confiabilidade no desenvolvimento........ p. __

Figura 4.2 – Diagramas de confiabilidade no conjunto de teste (n = 200; 60 ruins)........ p. __

Figura 4.3 – Limiares da política em função da perda e do custo da análise manual........ p. __

## LISTA DE TABELAS

Tabela 3.1 – Dicionário das variáveis........ p. __

Tabela 3.2 – Descrição do conjunto de desenvolvimento (n = 800), calculada a partir de `dados/processados/dev.csv`........ p. __

Tabela 4.1 – Métricas por modelo no desenvolvimento, média (desvio) entre 5 partições........ p. __


Tabela 4.2 – Métricas por modelo no conjunto de teste (n = 200; 60 ruins), valor [intervalo de 95%]........ p. __

Tabela 4.3 – Variação de métricas ao esconder uma variável, seleção de linhas........ p. __

Tabela 4.4 – Política de três ações por utilidade esperada contra corte 0,5 de duas ações, desenvolvimento........ p. __

Tabela 4.5 – Política de três ações contra corte 0,5 de duas ações, conjunto de teste (n = 200; 60 ruins)........ p. __

Tabela 4.6 – Diferença pareada de utilidade média (`ue` − `limiar`), conjunto de teste (n = 200; 60 ruins)........ p. __

Tabela 4.7 – Limiares da política por perda e custo da análise manual, seleção de linhas........ p. __

Tabela 4.8 – Saída de `codigo/demo.py` para o caso sgc-0000........ p. __

Tabela 4.9 – Métricas das 8 configurações e da seleção aninhada, média (desvio) entre 5 partições externas........ p. __

Tabela 4.10 – *Log loss* interno por partição externa, seleção de colunas........ p. __

## LISTA DE QUADROS

Quadro 3.1 – Matriz de utilidade demonstrativa........ p. __

Quadro A.1 – Comandos, em ordem, e arquivos gravados........ p. __

## LISTA DE SIGLAS E ABREVIATURAS

BDeu – *Bayesian Dirichlet equivalent uniform* (prior usado no aprendizado de parâmetros, seção 2.3)

CSV – 

ECE – Erro esperado de calibração (seção 2.5)

NB – 

PR-AUC – 

ROC-AUC – Área sob a curva ROC (seção 2.5)

TAN – *Tree-Augmented Naive Bayes*, Naive Bayes aumentado por árvore (seções 2.2 e 3.5)

UCI – 

FEELT – 

UFU – 

## SUMÁRIO

RESUMO........ p. __

ABSTRACT........ p. __

LISTA DE FIGURAS........ p. __

LISTA DE TABELAS........ p. __

LISTA DE QUADROS........ p. __

LISTA DE SIGLAS E ABREVIATURAS........ p. __

**1 INTRODUÇÃO**........ p. __

- 1.1 Contexto........ p. __
- 1.2 Pergunta de pesquisa........ p. __
- 1.3 Objetivos........ p. __
- 1.4 O que o trabalho não faz........ p. __
- 1.5 Mudanças em relação à proposta........ p. __
- 1.6 Organização do texto........ p. __
**2 FUNDAMENTAÇÃO**........ p. __

- 2.1 Redes bayesianas........ p. __
- 2.2 *Naive Bayes* e TAN........ p. __
- 2.3 Aprendizado de parâmetros e *prior* BDeu........ p. __
- 2.4 Inferência exata........ p. __
- 2.5 Calibração........ p. __
- 2.6 Utilidade esperada........ p. __
- 2.7 Limiares derivados dos custos........ p. __
- 2.8 Opção de rejeição........ p. __
- 2.9 Escore de crédito e *next best action*........ p. __
**3 MATERIAIS E MÉTODOS**........ p. __

- 3.1 Base de dados........ p. __
 - 3.2 Divisão em desenvolvimento e teste........ p. __
- 3.3 Validação cruzada........ p. __
- 3.4 Discretização........ p. __
- 3.5 Modelos de risco........ p. __
 - 3.5.1 Evidência incompleta........ p. __
- 3.6 Métricas........ p. __
- 3.7 Camada de decisão por utilidade esperada........ p. __
 - 3.7.1 Comparação de políticas........ p. __
- 3.8 Análise de sensibilidade........ p. __
- 3.9 Demonstração........ p. __
- 3.10 Estudo de seleção aninhado (secundário)........ p. __
- 3.11 Ambiente e reprodutibilidade........ p. __
**4 RESULTADOS**........ p. __

- 4.1 Desempenho preditivo........ p. __
- 4.2 Evidência incompleta........ p. __
- 4.3 Política de decisão........ p. __
- 4.4 Sensibilidade........ p. __
- 4.5 Demonstração........ p. __
- 4.6 Estudo de seleção (secundário)........ p. __
**5 DISCUSSÃO E LIMITAÇÕES**........ p. __

- 5.1 Leitura do desenvolvimento........ p. __
- 5.2 Leitura do teste final........ p. __
- 5.3 Estudo de seleção........ p. __
- 5.4 Simulação, não política real........ p. __
- 5.5 Matriz demonstrativa e analista infalível........ p. __
- 5.6 Tamanho do teste........ p. __
- 5.7 Modelo e representação variam juntos........ p. __
- 5.8 O que o intervalo não cobre........ p. __
- 5.9 Calibração só medida........ p. __
- 5.10 Direções futuras........ p. __
**6 CONCLUSÃO**........ p. __

- 6.1 Limiares explícitos e reprodutíveis........ p. __
- 6.2 Efeito medido nas ações e na utilidade média........ p. __
- 6.3 Limitações essenciais........ p. __

**REFERÊNCIAS**........ p. __

**APÊNDICES**........ p. __

- APÊNDICE A – Como reproduzir os resultados........ p. __
- APÊNDICE B – Resultados dos três modelos........ p. __
- APÊNDICE C – Plano de análise........ p. __

<!-- INÍCIO DO TEXTO -->

# 1 INTRODUÇÃO

## 1.1 Contexto

Na concessão de crédito, decisões automatizadas costumam apoiar-se em modelos de escore que atribuem pesos a variáveis do solicitante, em geral por regressão logística, e a decisão de aprovar ou rejeitar resulta da comparação desse escore com um ponto de corte \cite{thomas2000,siddiqi2012}. A interpretabilidade e a facilidade de auditoria explicam a adoção dessa prática pela indústria \cite{thomas2000,siddiqi2012}. 

Nesse arranjo, duas tarefas de natureza distinta ficam fundidas em uma única regra. A primeira é estimar o risco do caso, isto é, a probabilidade de um desfecho desfavorável dada a evidência observada. A segunda é escolher uma ação diante dessa estimativa, o que depende dos custos e benefícios de cada combinação de ação e desfecho. Quando o ponto de corte é fixado sem referência explícita a esses custos, o critério que de fato governa a recomendação permanece implícito, e a sensibilidade da decisão a mudanças nos critérios de negócio não pode ser examinada.

As redes bayesianas são modelos gráficos probabilísticos que representam dependências condicionais entre variáveis e permitem inferência sob incerteza \cite{pearl1988}. São, portanto, adequadas à primeira tarefa. Uma probabilidade estimada, contudo, não é por si só uma ação recomendada: a passagem do risco à ação exige uma camada de decisão separada, fundamentada na utilidade esperada. Este trabalho investiga essa separação em um estudo de caso de crédito, organizando o sistema em uma camada probabilística, que estima a probabilidade de um crédito ser ruim, e uma camada de decisão, que escolhe a ação de maior utilidade esperada. Os conceitos envolvidos são apresentados no Capítulo 2.

## 1.2 Pergunta de pesquisa

A pergunta que orienta o trabalho é a seguinte:

> Uma política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) produz (1) limiares explícitos, reproduzíveis a partir da matriz de utilidade e de `p`, e (2) qual efeito medido exerce sobre as ações e a utilidade média, em comparação com um limiar fixo de 0,5?

As duas partes têm naturezas distintas. A parte 1 é uma propriedade da política: vale para qualquer escore e não depende de resultado experimental. A parte 2 é o que o experimento mede. A pergunta e o modo de ler cada desfecho da análise primária foram fixados antes de existir qualquer resultado. Existe também um estudo de seleção secundário, desenhado depois de ver as métricas do desenvolvimento, cujo viés é declarado.

## 1.3 Objetivos

O objetivo geral é construir e avaliar uma política de decisão que separa a estimativa do risco de crédito, feita por uma rede bayesiana, da escolha da ação, feita pela maximização da utilidade esperada, e comparar essa política com uma regra de limiar fixo.

Os objetivos específicos são:

1. estimar a probabilidade de um crédito ser ruim com redes bayesianas de duas estruturas, *Naive Bayes* e TAN (*Naive Bayes* aumentado por árvore), na base South German Credit;
2. comparar a qualidade preditiva dessas redes com a de uma regressão logística de referência, medindo discriminação e erro de calibração;
3. definir um conjunto ilustrativo de ações admissíveis e uma matriz de utilidade documentada, e escolher para cada caso a ação de maior utilidade esperada;
4. explicitar os limiares de decisão que decorrem da matriz de utilidade;
5. medir o efeito da política sobre as ações escolhidas e a utilidade média, em comparação com o limiar fixo de 0,5;
6. analisar a sensibilidade da política aos valores de custo adotados;
7. demonstrar o fluxo completo para um caso, do risco estimado à utilidade de cada ação, em um *script* de terminal.

A avaliação do modelo de risco é feita separadamente da avaliação da política de decisão, como previsto na proposta. Como a base não registra o resultado das ações não tomadas, a camada de decisão é avaliada como simulação metodológica, e não como validação de uma política real de concessão. O protocolo experimental é descrito no Capítulo 3.

## 1.4 O que o trabalho não faz

O trabalho é um experimento composto por *scripts* que leem arquivos de dados e gravam tabelas e figuras. Não entrega produto, painel web, servidor, banco de dados nem modelo de linguagem. A matriz de utilidade é demonstrativa: não representa a política de nenhuma instituição, e o trabalho não usa dados nem sistemas proprietários.

O trabalho também não propõe uma regra de tipo distinto do limiar: como a utilidade esperada de cada ação é uma reta em `p`, a política equivale a uma regra de limiares sobre `p`, e a contribuição é derivar esses limiares dos custos de forma explícita. A parte 1 da pergunta vale para qualquer escore e não distingue a rede da regressão logística. Os resultados não se generalizam a outras bases nem validam uma política real de concessão.

Convém separar o que o trabalho toma da teoria, o que implementa e o que observa. A equivalência entre maximizar a utilidade esperada e aplicar limiares sobre a probabilidade, e a ação intermediária análoga à opção de rejeição, são resultados conhecidos \cite{elkan2001,chow1970}, e o trabalho não os apresenta como novidade. A parte própria é a implementação: três modelos de risco treinados em um protocolo fixado antes das métricas, fronteiras calculadas a partir de `config/utilidade.json`, a política de três ações aplicada aos casos, a comparação com o corte 0,5 por *bootstrap* e a análise de sensibilidade dos limiares. O que se observou empiricamente vale só para o conjunto de teste de 200 casos: diferenças de ROC-AUC dentro do ruído, calibração pior no TAN e diferença pareada de utilidade a favor da política de três ações, lida com a ressalva da Seção 5.5.

## 1.5 Mudanças em relação à proposta

Dez pontos mudaram em relação à proposta submetida. Cada um é listado com o motivo registrado na documentação do projeto.

**Base de dados.** A proposta previa a German Credit Data; o trabalho usa a South German Credit, que é a versão corrigida da base citada na proposta \cite{gromping2019}. O protocolo de validação, que a proposta deixava em aberto, ficou fixado no Capítulo 3.

**Protótipo.** O protótipo previsto na proposta, que mostraria evidência, risco estimado, ação recomendada e justificativa, passou a ser uma demonstração em terminal, que recebe um caso e mostra o risco estimado e a utilidade de cada ação. A justificativa textual da recomendação ficou de fora: a demonstração mostra a conta (risco, utilidade de cada ação e fronteiras), e não uma explicação em texto. Uma interface de uma tela foi deixada para depois do experimento pronto.

**Calibração.** A proposta previa calibrar as probabilidades; o trabalho apenas mede o erro de calibração, sem aplicar correção. Essa opção decorre do fato de que corrigir exigiria escolher o método depois de ver as métricas do desenvolvimento, o que fere a pré-especificação da análise. A exigência de probabilidade calibrada para a decisão por custos vem da literatura, e não do experimento; ela é discutida no Capítulo 2.

**Pergunta de pesquisa.** A proposta perguntava se a política baseada em probabilidades calibradas e utilidade esperada produz decisões mais consistentes e transparentes que a política por escore e limiar; "consistentes" aparece na etapa A e "transparentes", no Resumo. A pergunta foi reformulada nas duas partes da Seção 1.2. A reformulação ocorreu porque "consistentes" e "transparentes" não correspondiam a grandezas medidas. Uma redação intermediária, "mais auditáveis", foi descartada porque contradizia a proposta, que chama regras e escores de auditáveis, valia por construção para qualquer escore e deixava a rede sem papel. A forma em duas partes separa a propriedade da política do efeito medido, e a troca de "calibrada" por "com calibração medida" acompanha a mudança anterior.

**Análise exploratória.** A análise exploratória prevista na proposta limita-se a uma tabela de descrição da base, apresentada no Capítulo 3, porque o plano fixa sete *scripts* e uma análise em código seria exceção.

**Conjunto de ações.** A proposta citava quatro ações (aprovar, pedir informação ou garantia, encaminhar para análise manual e rejeitar); o trabalho usa três: aprovar, rejeitar e análise manual. 

**Estrutura da rede.** A proposta previa comparar uma estrutura guiada por conhecimento do domínio com outra aprendida dos dados por BIC (critério de informação bayesiano) ou BDeu (*Bayesian Dirichlet equivalent uniform*); o trabalho usa *Naive Bayes* e TAN, sem estrutura de domínio, e a busca por *hill climbing*, prevista como opcional, não foi rodada. As duas estruturas foram escolhidas porque o *Naive Bayes* é a referência simples e o TAN permite dependência entre variáveis. 

**Linha de base.** A proposta previa a regressão logística com probabilidades calibradas; no trabalho ela não é calibrada, e só se mede o seu erro de calibração. 

**Diagramas de influência e explicação da evidência.** A revisão sobre diagramas de influência e, na etapa F, o uso de Streamlit e a apresentação da evidência mais relevante e da mudança em relação à probabilidade a priori não entram no trabalho. 

**Estudo de seleção.** Foi acrescentado um estudo secundário de seleção aninhada de estrutura e de *prior*, que não estava na proposta; a análise primária não muda. O acréscimo buscou preservar a comparação pré-definida e ainda testar a hipótese levantada no desenvolvimento.

## 1.6 Organização do texto

O Capítulo 2 apresenta a fundamentação: redes bayesianas, calibração, utilidade esperada, limiares derivados de custos e escore de crédito. O Capítulo 3 descreve a base de dados, o protocolo de validação, os modelos, as métricas e a política de decisão. O Capítulo 4 relata os resultados preditivos, os da política de decisão e os da análise de sensibilidade. O Capítulo 5 discute os resultados e as limitações do trabalho. O Capítulo 6 conclui, respondendo às duas partes da pergunta de pesquisa. Também são tratados a opção de rejeição (Seção 2.8), a evidência incompleta (Seção 4.2), a demonstração de um caso (Seções 3.9 e 4.5) e o estudo de seleção secundário (Seções 3.10 e 4.6).

# 2 FUNDAMENTAÇÃO

## 2.1 Redes bayesianas

Raciocinar sob incerteza exige representar crenças sobre muitas variáveis ao mesmo tempo e atualizá-las quando algumas delas são observadas. A teoria das probabilidades oferece o arcabouço para isso, mas a especificação direta de uma distribuição conjunta sobre dezenas de variáveis é inviável tanto em armazenamento quanto em estimação; as redes bayesianas foram propostas como forma de explorar a estrutura de independências do problema para tornar essa representação compacta \cite{pearl1988, russell2010}. 

Uma rede bayesiana é um modelo probabilístico composto por duas partes: um grafo acíclico dirigido, cujos nós são variáveis aleatórias, e um conjunto de distribuições de probabilidade condicional, uma para cada nó, dada a configuração de seus pais no grafo \cite{pearl1988, koller2009}. Quando as variáveis são discretas, cada distribuição condicional é representada por uma tabela de probabilidade condicional, com uma linha para cada combinação de valores dos pais \cite{russell2010}. 

A propriedade central do modelo é que a distribuição conjunta de todas as variáveis se escreve como o produto das distribuições locais. Para variáveis $X_1, \dots, X_n$, sendo $\mathrm{Pa}(X_i)$ o conjunto de pais de $X_i$ no grafo,

$$P(X_1, \dots, X_n) = \prod_{i=1}^{n} P\big(X_i \mid \mathrm{Pa}(X_i)\big).$$

Essa fatoração permite especificar a conjunta com muito menos parâmetros do que uma tabela completa, cujo tamanho cresce exponencialmente com o número de variáveis \cite{koller2009, russell2010}. Com $n$ variáveis binárias, a tabela conjunta completa tem $2^n - 1$ parâmetros livres, ao passo que, em uma rede na qual cada nó tem no máximo $k$ pais, o número de parâmetros cresce apenas linearmente em $n$, da ordem de $n \cdot 2^k$ \cite{russell2010}. 

O grafo também codifica relações de independência condicional. Em particular, cada variável é condicionalmente independente de seus não descendentes, dados os seus pais \cite{koller2009}; o critério de separação dirigida (*d-separation*) permite ler do grafo outras independências implicadas pela estrutura \cite{pearl1988, koller2009}. É essa leitura que torna o modelo interpretável: as arestas indicam quais variáveis entram diretamente no cálculo da probabilidade de cada outra.

Construir uma rede envolve duas tarefas distintas: definir a estrutura do grafo e estimar os parâmetros das tabelas. A estrutura pode vir do conhecimento de especialistas, ser aprendida dos dados ou ser fixada por uma família de modelos, como acontece nos classificadores da Seção 2.2 \cite{koller2009}. Uma vez definida a rede, ela responde a consultas sobre qualquer variável dada qualquer subconjunto das demais, o que a distingue de modelos que apenas mapeiam um vetor fixo de entradas em uma saída \cite{russell2010, jensen2007}. 

## 2.2 *Naive Bayes* e TAN

Em classificação, uma rede bayesiana pode ser usada para estimar a probabilidade a posteriori de uma variável de classe $C$ dados os atributos $A_1, \dots, A_n$. O classificador *Naive Bayes* é a rede mais simples com esse fim: a classe é o único pai de todos os atributos, e os atributos são supostos condicionalmente independentes entre si dada a classe \cite{friedman1997}. Pela regra de Bayes, a posteriori fica

$$P(C \mid A_1, \dots, A_n) \propto P(C) \prod_{i=1}^{n} P(A_i \mid C).$$

A suposição de independência raramente vale em dados reais, mas o classificador costuma ter desempenho competitivo, e a estrutura fixa dispensa o aprendizado do grafo \cite{friedman1997}. 

O classificador TAN (*Tree-Augmented Naive Bayes*) relaxa essa suposição: além da aresta que parte da classe, cada atributo pode ter no máximo um outro atributo como pai, de modo que as arestas entre atributos formam uma árvore \cite{friedman1997}. A árvore é escolhida por uma adaptação do método de Chow e Liu \cite{chowliu1968}, que aproxima uma distribuição conjunta pela árvore de dependência de máxima verossimilhança, obtida como a árvore geradora de peso máximo cujos pesos são as informações mútuas entre pares de variáveis. No TAN, o peso de cada par de atributos é a informação mútua condicional à classe \cite{friedman1997}: 

$$I(A_i; A_j \mid C) = \sum_{a_i, a_j, c} P(a_i, a_j, c) \log \frac{P(a_i, a_j \mid c)}{P(a_i \mid c)\, P(a_j \mid c)}.$$

Escolhida uma raiz, as arestas da árvore são orientadas a partir dela, e a classe é acrescentada como pai de todos os atributos \cite{friedman1997}. O TAN mantém, portanto, a estrutura do *Naive Bayes* e acrescenta uma única dependência por atributo, o que limita o número de parâmetros de cada tabela.

Os dois classificadores ocupam pontos diferentes de um mesmo compromisso. O *Naive Bayes* tem menos parâmetros, e por isso suas tabelas são estimadas com mais exemplos por célula, ao custo de ignorar correlações entre atributos; o TAN capta parte dessas correlações, mas cada tabela passa a ter uma configuração de pais a mais e, portanto, menos exemplos por célula \cite{friedman1997}. Em ambos os casos a estrutura é restrita o bastante para ser lida diretamente: cada atributo depende da classe e, no TAN, de no máximo um outro atributo.

## 2.3 Aprendizado de parâmetros e *prior* BDeu

Sob as hipóteses usuais de que os exemplos de treino são independentes e identicamente distribuídos, de que não há valores ausentes e de que os parâmetros de tabelas diferentes são independentes a priori, a verossimilhança de uma rede bayesiana se decompõe em um termo por nó e por configuração dos pais, e cada tabela pode ser estimada separadamente \cite{koller2009, heckerman1995}. 

Dada a estrutura, os parâmetros de uma rede bayesiana discreta são as entradas das tabelas de probabilidade condicional. Seja $\theta_{ijk} = P(X_i = k \mid \mathrm{Pa}(X_i) = j)$ e $N_{ijk}$ o número de exemplos de treino em que $X_i = k$ e os pais assumem a configuração $j$, com $N_{ij} = \sum_k N_{ijk}$. A estimativa de máxima verossimilhança é a frequência relativa $N_{ijk}/N_{ij}$ \cite{koller2009}. Quando uma configuração dos pais aparece poucas vezes, ou nenhuma, essa estimativa é instável ou indefinida e pode atribuir probabilidade zero a eventos possíveis \cite{koller2009}. 

A estimação bayesiana trata esse problema com uma distribuição a priori sobre os parâmetros. Para variáveis multinomiais, a escolha usual é a distribuição de Dirichlet, que é conjugada: com hiperparâmetros $\alpha_{ijk}$ e $\alpha_{ij} = \sum_k \alpha_{ijk}$, a posteriori também é Dirichlet, e sua média é

$$\hat{\theta}_{ijk} = \frac{N_{ijk} + \alpha_{ijk}}{N_{ij} + \alpha_{ij}}$$

\cite{koller2009, heckerman1995}. Os hiperparâmetros funcionam como contagens imaginárias somadas às observadas, e seu total mede quanto peso a priori recebe diante dos dados \cite{koller2009}. 

O *prior* BDeu (*Bayesian Dirichlet equivalent uniform*) fixa um único número, o tamanho amostral equivalente $N'$, e o distribui de modo uniforme: $\alpha_{ijk} = N' / (r_i q_i)$, em que $r_i$ é o número de valores de $X_i$ e $q_i$ o número de configurações de seus pais \cite{heckerman1995}. Com isso, a força total do *prior* é a mesma em todos os nós, e as tabelas com muitas configurações de pais recebem pseudocontagens menores por célula \cite{heckerman1995, koller2009}. Outro caso particular do *prior* de Dirichlet, distinto do BDeu, é o estimador de Laplace, que soma uma unidade a cada célula, isto é, $\alpha_{ijk} = 1$; ele faz a força total do *prior* crescer com o tamanho da tabela \cite{koller2009}. O efeito prático do BDeu é suavizar as estimativas em direção à distribuição uniforme, sobretudo nas células de contagem pequena. Quanto maior $N'$, mais forte essa suavização; quando as contagens crescem, o peso relativo do *prior* diminui e a estimativa se aproxima da frequência relativa \cite{koller2009}. O nome "equivalente" vem da propriedade de atribuir o mesmo escore a estruturas que representam as mesmas independências, o que motivou sua proposta no contexto do aprendizado de estrutura \cite{heckerman1995}. 

## 2.4 Inferência exata

Inferência, em uma rede bayesiana, é o cálculo da distribuição de uma ou mais variáveis de consulta dada a evidência observada em outras, como $P(C \mid \mathbf{e})$. Em princípio, basta somar a distribuição conjunta sobre as variáveis que não são nem consulta nem evidência e normalizar o resultado \cite{russell2010, koller2009}. Essa soma direta tem custo exponencial no número de variáveis, e a fatoração da Seção 2.1 é o que permite fazê-la de forma mais eficiente.

O algoritmo de eliminação de variáveis explora essa fatoração: as somas são empurradas para dentro do produto, de modo que cada variável é eliminada somando apenas os fatores que a mencionam, e o resultado intermediário é guardado como um novo fator \cite{koller2009}. O custo depende da ordem de eliminação e do tamanho dos maiores fatores criados; para grafos de largura de árvore pequena, como os do *Naive Bayes* (uma estrela) e do TAN (uma árvore sobre os atributos, com a classe como pai de todos), esses fatores ficam pequenos \cite{koller2009}. Para estruturas gerais, a inferência exata é NP-difícil \cite{koller2009}; métodos como a propagação em árvore de junção organizam o mesmo cálculo para responder a muitas consultas \cite{jensen2007}. 

No caso de classificação com evidência completa, o cálculo é particularmente simples. No *Naive Bayes*, a posteriori da classe é obtida multiplicando a priori da classe pelas probabilidades condicionais dos valores observados e normalizando, como na fórmula da Seção 2.2; no TAN, o produto inclui, para cada atributo, a probabilidade condicional dado a classe e o atributo pai \cite{friedman1997}. Em ambos os casos não há variáveis a eliminar além da própria normalização.

Uma consequência útil é que a evidência pode ser parcial. Uma variável não observada é tratada como as demais variáveis não observadas, isto é, somada na marginalização, sem necessidade de imputar um valor \cite{koller2009, jensen2007}. A posteriori resultante continua sendo uma distribuição de probabilidade coerente com o modelo, condicionada apenas ao que foi observado. Isso difere de modelos discriminativos que exigem um valor para cada entrada e, diante de uma entrada ausente, dependem de uma regra externa de preenchimento \cite{koller2009}. Além disso, a inferência é exata: dado o modelo, a probabilidade calculada é a que ele de fato implica, sem erro de aproximação numérica além do arredondamento.

## 2.5 Calibração

Um classificador probabilístico é dito calibrado quando, entre os casos aos quais atribui probabilidade $p$ a um evento, a frequência observada desse evento é aproximadamente $p$ \cite{guo2017, naeini2015}. Boa ordenação dos casos não garante calibração: um modelo pode separar bem as classes e, ainda assim, superestimar ou subestimar as probabilidades \cite{guo2017, niculescu2005}. A calibração importa quando a probabilidade é usada como número, por exemplo para calcular uma utilidade esperada, e não apenas para ordenar. Medidas de discriminação, como a área sob a curva ROC (ROC-AUC), dependem só da ordem das previsões e não mudam quando as probabilidades sofrem uma transformação estritamente crescente; por isso não detectam erros de calibração, que precisam de medidas próprias \cite{guo2017, naeini2015}. 

O escore de Brier mede o erro quadrático médio entre a probabilidade prevista $p_i$ e o desfecho observado $y_i \in \{0, 1\}$ \cite{brier1950}:

$$\mathrm{BS} = \frac{1}{N} \sum_{i=1}^{N} (p_i - y_i)^2.$$

Valores menores são melhores \cite{brier1950}. O erro esperado de calibração (ECE) mede só a calibração: as previsões são agrupadas em $M$ faixas de probabilidade $B_1, \dots, B_M$, e compara-se, em cada faixa, a frequência observada do evento $\mathrm{freq}(B_m)$ com a probabilidade média prevista para ele $\mathrm{conf}(B_m)$, ponderando pelo número de casos \cite{naeini2015, guo2017}:

$$\mathrm{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{N} \, \big| \mathrm{freq}(B_m) - \mathrm{conf}(B_m) \big|.$$

 Há variantes: na forma usada por Guo et al. \cite{guo2017}, $p$ é a confiança da classe predita, e o evento é o acerto da previsão; em problemas binários também se usa a probabilidade de uma classe fixa e a frequência dessa classe \cite{naeini2015, guo2017}. A variante e o número de faixas usados neste trabalho estão definidos no Capítulo 3. A mesma comparação aparece no diagrama de confiabilidade, que plota a frequência observada contra a probabilidade média de cada faixa; nele, um modelo perfeitamente calibrado fica sobre a diagonal \cite{guo2017}. 

A literatura propõe métodos para recalibrar as probabilidades de um modelo já treinado, usando dados não vistos no treino. O escalonamento de Platt ajusta uma função sigmoide sobre a saída do modelo, isto é, uma regressão logística com uma única entrada \cite{platt1999}. A regressão isotônica ajusta uma função monótona não decrescente, por partes constantes, sem supor forma paramétrica, e por isso tende a exigir mais dados para não sobreajustar \cite{zadrozny2002, niculescu2005}. O Capítulo 3 diz o que este trabalho faz com a calibração. Ambos os métodos exigem um conjunto de dados separado do treino para ajustar a função de recalibração, sob pena de reproduzir o viés do próprio ajuste \cite{platt1999, zadrozny2002}. Para classificadores *Naive Bayes*, a literatura relata probabilidades frequentemente empurradas para os extremos, efeito atribuído à suposição de independência entre atributos \cite{zadrozny2001, niculescu2005}. 

<!-- refs usadas: pearl1988, koller2009, russell2010, friedman1997, chowliu1968, heckerman1995, jensen2007, zadrozny2001, brier1950, naeini2015, guo2017, platt1999, zadrozny2002, niculescu2005 -->

## 2.6 Utilidade esperada

A teoria da decisão separa duas perguntas que um classificador costuma misturar: o que se acredita sobre o estado do mundo e o que se deve fazer diante dessa crença. A crença é representada por uma distribuição de probabilidade sobre os estados possíveis $y$; as preferências do decisor, por uma função de utilidade $U(a,y)$, que atribui um valor numérico à consequência de tomar a ação $a$ quando o estado verdadeiro é $y$ \cite{russell2010}. Combinadas, as duas definem a utilidade esperada de cada ação,

$$UE(a) = \sum_{y} P(y)\,U(a,y),$$

e o princípio da máxima utilidade esperada recomenda a ação $a^{*} = \arg\max_a UE(a)$ \cite{russell2010,koller2009}. A justificativa clássica do princípio é axiomática: um decisor cujas preferências entre loterias satisfazem os axiomas da utilidade (ordenabilidade, transitividade, continuidade, substitutibilidade, monotonicidade e decomponibilidade) comporta-se como se maximizasse a utilidade esperada de alguma função $U$ \cite{russell2010}. 

Quando os estados e as ações são finitos, a função de utilidade pode ser escrita como uma matriz, com uma linha por ação e uma coluna por estado. No problema de crédito considerado neste trabalho, o estado é a qualidade do cliente (bom ou ruim) e cada célula da matriz registra o ganho ou a perda associada a uma combinação de ação e estado. A matriz é a parte do modelo que expressa o negócio; a distribuição $P(y)$ é a parte que expressa o conhecimento estatístico. Trocar a matriz muda a decisão sem exigir novo treino do modelo de risco, e melhorar o modelo de risco muda a decisão sem exigir nova discussão sobre os valores \cite{koller2009}. Uma utilidade expressa como custo leva às mesmas escolhas, bastando trocar a maximização da utilidade pela minimização do custo esperado.

O diagrama de influência estende a rede bayesiana para representar esse tipo de problema em um único grafo \cite{howard2005}. Além dos nós de chance, que são variáveis aleatórias como na rede bayesiana, o diagrama contém nós de decisão, cujos valores são escolhidos pelo decisor, e nós de utilidade, que dependem de nós de chance e de decisão e atribuem valor às consequências \cite{howard2005,jensen2007}. Os arcos que entram em um nó de decisão indicam a informação disponível no momento de decidir. Resolver o diagrama significa encontrar, para cada configuração dessa informação, a ação que maximiza a utilidade esperada, o que pode ser feito por algoritmos de inferência semelhantes aos usados em redes bayesianas \cite{jensen2007,koller2009}. No caso de uma única decisão tomada após observar todas as evidências, a solução reduz-se a calcular $P(y \mid \text{evidência})$ pela rede e aplicar o princípio da máxima utilidade esperada a esse resultado.

## 2.7 Limiares derivados dos custos

Em um problema com dois estados, a utilidade esperada de cada ação é uma função linear da probabilidade $p = P(\text{ruim} \mid x)$, pois $UE(a) = (1-p)\,U(a,\text{bom}) + p\,U(a,\text{ruim})$. A comparação entre duas ações reduz-se, portanto, à comparação de duas retas, que se cruzam em um único ponto. Disso decorre que a decisão de máxima utilidade esperada equivale a uma regra de limiar sobre $p$, e que o limiar é determinado pela matriz de custos, não escolhido livremente \cite{elkan2001}. Para custos $C(a,y)$ de duas ações, aprovar e rejeitar, a ação rejeitar é ótima quando $p \geq p^{*}$, com

$$p^{*} = \frac{C(\text{rejeitar},\text{bom}) - C(\text{aprovar},\text{bom})}{\big[C(\text{rejeitar},\text{bom}) - C(\text{aprovar},\text{bom})\big] + \big[C(\text{aprovar},\text{ruim}) - C(\text{rejeitar},\text{ruim})\big]}$$

em que os dois termos entre colchetes são positivos quando cada erro custa mais que o acerto correspondente \cite{elkan2001}. Como exemplo genérico, seja $G > 0$ o ganho de aprovar um cliente bom, $L > 0$ a perda de aprovar um cliente ruim e utilidade nula para rejeitar. Em custos, $C(\text{aprovar},\text{bom}) = -G$, $C(\text{aprovar},\text{ruim}) = L$ e $C(\text{rejeitar},\cdot) = 0$, e a fórmula dá $p^{*} = G/(G+L)$. O limiar habitual de 0,5 corresponde apenas ao caso particular $G = L$.

Com três ações, as retas de utilidade esperada podem formar uma envoltória superior com dois cruzamentos relevantes, e a regra passa a ter dois pontos de corte, $0 \leq t_1 \leq t_2 \leq 1$: aprovar se $p < t_1$, encaminhar à ação intermediária se $t_1 \leq p \leq t_2$ e rejeitar se $p > t_2$. Retomando o exemplo, suponha-se uma terceira ação, a análise manual, que custa $c > 0$ e após a qual o caso é corretamente aprovado ou rejeitado. Sua utilidade esperada é $UE(\text{manual}) = (1-p)G - c$. A análise manual supera a aprovação quando $pL \geq c$, isto é, $p \geq c/L$, e supera a rejeição quando $p \leq 1 - c/G$. Os pontos de corte são, assim, $t_1 = c/L$ e $t_2 = 1 - c/G$, e a faixa intermediária só existe quando $c/L \leq 1 - c/G$, ou seja, quando $c \leq GL/(G+L)$; para custos maiores, a regra volta a ter um único limiar. Os valores adotados no experimento e os pontos de corte resultantes são apresentados na Seção 3.7.

A equivalência entre utilidade esperada e limiar supõe que $p$ seja a probabilidade verdadeira do estado dado o caso, ou ao menos uma estimativa calibrada dela \cite{elkan2001,zadrozny2001}. Se o modelo produz escores que ordenam bem os casos, mas não correspondem a frequências, o limiar derivado da matriz é aplicado na escala errada, e a decisão deixa de ser a de máxima utilidade esperada, ainda que a ordenação seja boa \cite{zadrozny2001,niculescu2005}. Essa exigência de calibração vem da literatura e é adotada aqui como premissa: o trabalho mede a calibração das probabilidades (Seção 2.5), mas não a demonstra experimentalmente como condição da regra. Com escores não calibrados, a alternativa usual é escolher o limiar empiricamente, o que reintroduz o ajuste que a derivação a partir dos custos pretende evitar.

## 2.8 Opção de rejeição

A ideia de admitir uma ação além das classes do problema remonta à opção de rejeição de Chow \cite{chow1970}. Na formulação original, um classificador pode recusar-se a decidir quando o caso é ambíguo, e o erro de classificação passa a ser trocado por uma taxa de rejeição. A regra ótima rejeita o caso quando a maior probabilidade a posteriori entre as classes fica abaixo de um limiar, e esse limiar é determinado pela razão entre o custo de rejeitar e o custo de errar \cite{chow1970}. Aumentar o limiar reduz o erro entre os casos aceitos, ao custo de mais rejeições, o que define uma curva de compromisso entre erro e rejeição \cite{chow1970}.

No contexto do crédito, a rejeição de Chow corresponde a encaminhar o caso a um analista, e não a recusar o crédito: a ação intermediária da Seção 2.7 é análoga a uma opção de rejeição com custo. A analogia não é exata: em Chow, o custo de rejeitar é fixo, enquanto $UE(\text{manual}) = (1-p)G - c$ depende de $p$, porque o analista revela o estado verdadeiro e o caso bom ainda rende $G$. Em dois estados, a condição $\max\{p, 1-p\} < \tau$ define uma faixa em torno de $p = 0{,}5$, simétrica quando os erros têm o mesmo custo; com custos de erro diferentes, como no exemplo com $G \neq L$, a faixa desloca-se e torna-se assimétrica, com os pontos de corte $t_1$ e $t_2$ dados pela matriz. Em ambos os casos, a faixa intermediária reúne os casos em que nenhuma das ações automáticas tem utilidade esperada suficiente para compensar o custo do exame.

A regra tem duas consequências. Primeiro, como na Seção 2.7, a regra ótima de rejeição depende das probabilidades a posteriori, de modo que sua otimalidade também supõe probabilidades corretas \cite{chow1970}. Segundo, a vantagem de incluir a rejeição depende do que acontece depois dela: no exemplo da Seção 2.7, supôs-se que o analista sempre acerta o estado, e essa hipótese torna a política com três ações, em utilidade esperada, pelo menos tão boa quanto a de duas ações para qualquer $p$, já que a terceira ação só é escolhida quando sua utilidade esperada é maior. Um analista que erra reduziria $UE(\text{manual})$ e estreitaria a faixa intermediária.

## 2.9 Escore de crédito e *next best action*

O escore de crédito é a prática consolidada de estimar, a partir de dados do solicitante e de seu histórico, a probabilidade de inadimplência ou de mau comportamento, e de usar essa estimativa para decidir sobre a concessão \cite{thomas2000,hand1997}. As revisões da área registram o uso de diversos métodos estatísticos e de aprendizado, como análise discriminante, regressão logística, árvores de classificação, vizinhos mais próximos e redes neurais, sem que um deles domine os demais de modo uniforme \cite{hand1997,thomas2000}. 

Na indústria, a regressão logística ocupa posição de referência. O *scorecard* tradicional é, em geral, uma regressão logística sobre variáveis agrupadas em faixas, cujos coeficientes são convertidos em pontos aditivos por atributo, de modo que o escore final é uma soma legível e auditável \cite{siddiqi2012}. A preferência deve-se menos ao desempenho preditivo do que à interpretabilidade, à estabilidade e à facilidade de explicação a reguladores e a clientes \cite{siddiqi2012,thomas2000}. O papel dela no experimento é descrito no Capítulo 3.

No *scorecard*, a decisão é tomada por limiares sobre o escore, escolhidos a partir de considerações de negócio como taxa de aprovação, perda esperada e lucratividade \cite{siddiqi2012}. É comum haver uma faixa intermediária de escores encaminhada à análise humana, o que corresponde, na linguagem da Seção 2.8, a uma opção de rejeição \cite{siddiqi2012}. A diferença em relação à Seção 2.7 está na origem dos cortes: na prática descrita, eles são definidos sobre a escala do escore e ajustados ao negócio; na abordagem por utilidade esperada, são derivados da matriz de utilidade e aplicados sobre uma probabilidade, o que exige que essa probabilidade seja calibrada.

Neste trabalho, entende-se por *next best action* (próxima melhor ação) a ação de maior utilidade esperada, conforme a Seção 2.6, entre as ações aprovar, rejeitar e encaminhar para análise manual. Trata-se de definição própria, sem fonte citada. A formulação não acrescenta teoria ao que foi exposto nas Seções 2.6 a 2.8; ela nomeia a combinação de um modelo de risco que fornece $P(y \mid x)$ com uma camada de decisão que escolhe a ação.

<!-- refs usadas: russell2010, koller2009, howard2005, jensen2007, elkan2001, zadrozny2001, niculescu2005, chow1970, thomas2000, hand1997, siddiqi2012 -->

# 3 MATERIAIS E MÉTODOS

<!-- Entradas do.bib marcadas "% VERIFICAR" ou "A CONFERIR" só podem ser citadas depois de conferidas no original (PLANO.md §9). -->

Este capítulo descreve a base de dados, o protocolo de divisão e validação, os modelos de risco, as métricas, a camada de decisão por utilidade esperada, a análise de sensibilidade, o estudo secundário de seleção e os cuidados de reprodutibilidade. Todas as decisões de análise foram fixadas antes da observação de resultados no conjunto de teste, e a forma de leitura de cada desfecho foi registrada previamente em um plano de análise.

## 3.1 Base de dados

Utiliza-se a base South German Credit \cite{gromping2019}, versão corrigida da German Credit Data \cite{hofmann1994}, disponibilizada no repositório da UCI \cite{uci573}. A base contém 1000 registros, 20 variáveis preditoras e a variável-alvo risco do crédito, com 300 casos classificados como ruins e 700 como bons. A codificação do alvo é invertida em relação ao usual: o valor 0 indica crédito ruim e o valor 1, crédito bom; a classe positiva adotada em todo o trabalho é a classe ruim, e toda probabilidade reportada refere-se à probabilidade de o caso ser ruim.

Das 20 variáveis preditoras, três são contínuas (duração do crédito, valor do crédito e idade) e as 17 restantes já são categóricas. No texto e nas tabelas de resultados, adotam-se os nomes traduzidos para o português; os nomes originais em alemão são mantidos apenas no código-fonte e na Tabela 1 para referência à base original. O identificador `record_id` é removido antes de qualquer etapa de modelagem.

**Tabela 3.1** – Dicionário das variáveis. Categorias: número de valores inteiros distintos observados no conjunto de desenvolvimento (n = 800), calculado a partir de `dados/processados/dev.csv`; os códigos e seus significados seguem o codetable.txt da UCI (South German Credit (UPDATE), https://archive.ics.uci.edu/dataset/573/south+german+credit+update), traduzidos para o português.

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

Traduções e códigos conferidos, variável a variável, no codetable.txt do conjunto South German Credit (UPDATE), UCI, https://archive.ics.uci.edu/dataset/573/south+german+credit+update. Na fonte, finalidade do crédito tem 11 códigos (0 a 10); 10 aparecem no conjunto de desenvolvimento.

A base apresenta categorias raras, por exemplo número de créditos no banco = 4 e finalidade do crédito = 8. Essa característica motiva o uso de *prior* bayesiano na estimação dos parâmetros (Seção 3.5).

No conjunto de desenvolvimento (n = 800), número de créditos no banco = 4 tem 5 casos e finalidade do crédito = 8 tem 7 casos; as demais categorias pequenas têm de 9 a 35 casos.

A única análise exploratória é a tabela de descrição da base abaixo (contagens e as três variáveis contínuas), elaborada a partir do conjunto de desenvolvimento, sem *script* dedicado.

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

O conjunto de teste permanece fechado durante todo o desenvolvimento. Todos os modelos, inclusive o de referência, são avaliados nele uma única vez, após um *commit* de congelamento do código. O teste foi executado uma única vez, em 17/11/2026, sobre o *commit* de congelamento 49d77ff0eec74de98d7ce7ec83a9d0d2907bb207, com os três comandos do caminho `--final`. Os *scripts* de modelagem leem exclusivamente o conjunto de desenvolvimento.

## 3.3 Validação cruzada

No conjunto de desenvolvimento, adota-se validação cruzada estratificada em 5 partições, com semente 2026. Cada partição é usada uma vez como validação enquanto as outras quatro compõem o treino, de modo que cada caso recebe uma predição de um modelo que não o viu. As métricas de desenvolvimento são reportadas como média e desvio entre as 5 partições.

Todas as constantes (partições, faixas, tamanho equivalente e grade da sensibilidade) foram fixadas por convenção, e não por desempenho.

## 3.4 Discretização

As redes bayesianas utilizadas exigem variáveis discretas. As três variáveis contínuas são discretizadas em 3 faixas por tercis, com cortes aprendidos apenas no treino de cada partição, para evitar vazamento de informação da partição de validação \cite{kaufman2012}. Para o teste final, os cortes são aprendidos no conjunto de desenvolvimento inteiro e gravados em `resultados/cortes.json`.

O número de faixas segue essa convenção (ver Seção 3.3).

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

Regras de leitura foram fixadas antes de qualquer resultado. Diferença de ROC-AUC menor que 0,03 entre dois modelos é tratada como ruído, sem apontar vencedor; Brier igual ou maior que o da taxa base é relatado como "não melhor que prever a taxa base".

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

As hipóteses da matriz são: valores demonstrativos, não calibrados com dados reais, e um analista que sempre acerta o estado do cliente. A matriz demonstrativa foi aprovada pelo orientador, com valores não calibrados com dados reais.

Como a utilidade esperada de cada ação é linear em *p*, a política resultante equivale a uma regra de limiares sobre *p* \cite{elkan2001}. Com a matriz acima, a análise manual é escolhida quando *c*/400 ≤ *p* ≤ 1 − *c*/100; com *c* = 40, a faixa vai de 0,10 a 0,60, e com *c* > 80 a análise manual nunca é escolhida. Empates são resolvidos, com tolerância de 1e-9, pela prioridade análise manual, rejeitar, aprovar. A contribuição pretendida é a derivação explícita dos limiares a partir dos custos, acompanhada da medição da calibração das probabilidades. A exigência de probabilidade calibrada é tomada da literatura, não demonstrada pelo experimento.

Estimativas de probabilidade bem calibradas são necessárias quando a decisão leva em conta custos \cite{zadrozny2001}.

### 3.7.1 Comparação de políticas

A política é calculada para os três modelos e comparada com um limiar fixo de 0,5 de duas ações. A comparação principal, fixada antes de qualquer métrica, usa o TAN; *Naive Bayes* e regressão logística são reportados em apêndice na mesma estrutura. A comparação de duas regras é descrita como "política de três ações por utilidade esperada contra corte 0,5 de duas ações", sem linguagem causal, pois a diferença mistura modelo, representação e conjunto de ações. Com analista infalível, a política de três ações supera o corte de duas ações por construção, o que é declarado junto da tabela.

São medidas a utilidade média, a distribuição das ações e o número de casos que mudam de ação entre as políticas. No teste, reporta-se também a diferença pareada de utilidade média entre a regra de utilidade e o limiar fixo, com intervalo por *bootstrap*. Para a regra de utilidade, registram-se ainda a segunda melhor ação e a diferença de utilidade esperada em relação a ela.

## 3.8 Análise de sensibilidade

A sensibilidade da política aos custos é avaliada calculando-se as fronteiras de decisão em uma grade de perda por inadimplência em {200, 400, 600, 800} e custo da análise manual em {0, 5, …, 100}. A análise mostra a ação recomendada em função do risco, da perda e do custo da análise manual.

Os valores da grade seguem essa convenção (ver Seção 3.3).

## 3.9 Demonstração

Um *script* de terminal recebe o identificador de um caso, treina novamente o modelo nas 4 partições que não contêm o caso e mostra o risco estimado, a utilidade esperada de cada ação, as fronteiras e a ação recomendada; o modelo padrão é o TAN. A demonstração mostra a conta, não uma justificativa textual da recomendação.

## 3.10 Estudo de seleção aninhado (secundário)

Como análise secundária, pré-registrada em relação ao teste final, que será revista pelo autor, realiza-se um estudo de seleção de configuração. A análise primária, incluindo a comparação de duas regras com NB e TAN de BDeu 5, não muda.

A grade é fechada, com 8 configurações: {*Naive Bayes*, TAN} × tamanho equivalente BDeu {1, 5, 10, 50}. Ficam fora da grade K2, outras faixas, seleção de variáveis, *hill climbing*, métodos de calibração e reponderação.

Usa-se validação cruzada aninhada. As partições externas são as 5 já descritas; em cada uma, as 640 linhas de treino são divididas em 5 partições internas estratificadas, com semente 2026, nas quais cada configuração é treinada e avaliada. Escolhe-se a configuração de menor *log loss* médio nas partições internas, com empate (diferença menor que 1e-9) resolvido pela ordem da grade; a configuração escolhida prevê as 160 linhas da partição externa, gerando a linha "aninhado". A escolha é também recalculada no conjunto de desenvolvimento inteiro, só para relato; essa configuração é a usada como modelo secundário no teste final.

Relatam-se obrigatoriamente as 8 configurações, o número de comparações (8) e a linha "aninhado", qualquer que seja o resultado. O texto não se refere a um "melhor modelo": informa qual configuração a regra escolheu e quanto ela difere da configuração de base.

**Declaração de viés.** A grade de 8 configurações foi definida depois da observação das métricas de desenvolvimento (`metricas_dev.csv`) e motivada por elas: o TAN saiu pior que o NB e surgiu a hipótese sobre a finalidade do crédito (Seção 4.1). O aninhamento corrige o viés de escolher entre as 8 configurações, mas não o de ter desenhado a grade com base no mesmo conjunto de desenvolvimento.

## 3.11 Ambiente e reprodutibilidade

O experimento é composto por sete *scripts* Python que leem CSV e gravam tabelas e figuras, sem modelo salvo em arquivo. O projeto exige Python 3.12 ou superior. A execução local usou Python 3.12.13 (saída de `uv run python --version`); `uv.lock` e `pyproject.toml` fixam apenas `requires-python = ">=3.12"`, e não há `.python-version`. As bibliotecas são `pgmpy` 1.1.2, `scikit-learn` \cite{pedregosa2011}, `pandas` e `matplotlib`, com dependências fixadas pelo gerenciador `uv`. Toda fonte de aleatoriedade usa a semente 2026, e duas execuções do mesmo comando geram arquivos CSV e JSON idênticos byte a byte. Os arquivos de resultado são versionados com o código, e a reprodução é conferida pela comparação com a versão registrada no *commit*. As figuras PNG não são comparadas byte a byte. O passo a passo completo está no Apêndice A.

# 4 RESULTADOS

Este capítulo relata os resultados. Os números de desenvolvimento (Tabelas 4.1, 4.3, 4.4, 4.7, 4.9, 4.10) são resultados de desenvolvimento pré-estudo, obtidos só com os 800 casos de desenvolvimento (validação cruzada estratificada em 5 partições, Capítulo 3, Seções 3.2 e 3.3); os blocos do conjunto de teste (Tabelas 4.2, 4.5, 4.6 e Figura 4.2) são identificados na legenda pelo rótulo "conjunto de teste (n = 200; 60 ruins)". O conjunto de teste final foi aberto uma única vez, em 17/11/2026, após o *commit* de congelamento 49d77ff. A numeração das tabelas e figuras é sequencial. Os métodos não são repetidos aqui: cada seção remete à seção correspondente do Capítulo 3. A leitura de cada resultado segue as regras pré-registradas na §4 do plano de análise (`docs/plano-de-analise.md`), e a interpretação fica para o Capítulo 5.

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

A utilidade média da política de três ações (`ue`) é maior que a do corte 0,5 de duas ações (`limiar`) nos três modelos, com diferenças de 28,125 (nb), 25,4 (tan) e 27,25 (logreg). Trata-se de diferença descritiva no desenvolvimento, sem intervalo: pelo plano, a comparação pareada com intervalo só é feita no teste final, e a diferença mistura modelo, representação e conjunto de ações, razão pela qual não é chamada de efeito da regra. Na política de três ações (`ue`), a análise manual recebe 355 (nb), 262 (tan) e 415 (logreg) dos 800 casos; o corte 0,5 de duas ações (`limiar`) tem zero casos nessa ação por definição, por ter só duas ações. Essa ressalva acompanha qualquer leitura da diferença. As três ações aparecem na política de três ações (`ue`) em todos os modelos, de modo que a regra "alguma ação não aparece numa política" não se aplica. O número de casos cuja ação muda entre as regras coincide, em cada modelo, com o número de casos em análise manual da política de três ações (`ue`). A ação de cada caso está em `resultados/politicas_dev.csv`.

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

Aplicando a §4 do plano: na comparação principal (TAN), a diferença é 22,5, com intervalo de 9,2 a 37,2. Observa-se diferença a favor da política de três ações, com intervalo que exclui zero; não se afirma causa. Em NB, regressão logística e na análise secundária, o intervalo também exclui zero a favor da política de três ações (`ue`): nb 29,5 [13,1; 46,3], logreg 38,3 [20,2; 56,4] e sel 34,4 [16,4; 52,5]. A tabela é descritiva: a diferença mistura modelo, representação e conjunto de ações e não é chamada de efeito da regra nem do modelo. Aplica-se a ressalva obrigatória da Seção 5.5 (§6 do plano, itens 3 e 7). Na política de três ações (`ue`), a análise manual recebe 60 (tan), 85 (nb), 111 (logreg) e 93 (sel) dos 200 casos, e o número de casos que mudam de ação entre as regras coincide com esses valores. As três ações aparecem na política de três ações (`ue`) em todos os modelos, de modo que a regra "alguma ação não aparece numa política" não se aplica. A ação de cada caso está em `resultados/politicas_teste.csv`.

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

Como a mesma configuração foi escolhida em todas as partições externas, a linha `aninhado` reproduz os valores de `nb_ess50`. A diferença de ROC-AUC entre `aninhado` (0,788) e a configuração de referência `nb_ess5` (0,789) é 0,001, menor que 0,03 e, portanto, tratada como ruído pela regra da §4. A diferença de *log loss* entre as duas é 0,011 (0,512 contra 0,523). Entre as configurações do TAN, o *log loss* médio diminui à medida que o tamanho equivalente aumenta, de 0,825 (`tan_ess1`) a 0,583 (`tan_ess50`); em nenhuma partição uma configuração do TAN foi escolhida. Esses resultados descrevem o que a regra escolheu e quanto a escolha difere da configuração de referência; não indicam qual modelo adotar.

**Conjunto de teste (n = 200; 60 ruins), análise secundária.** As predições `p_sel` no teste estão em `resultados/predicoes_teste.csv` (coluna `p_sel`), e suas métricas, na linha `sel` da Tabela 4.2. Como define a §9, a diferença principal da escolha é contra a configuração de referência `nb` (NB, BDeu 5): a ROC-AUC de `sel` é 0,720 [0,641; 0,795], contra 0,728 do `nb`; a diferença, 0,008 (nb − sel), é menor que 0,03 e, pela regra da §9, tratada como ruído. De forma apenas descritiva, a diferença contra o `tan` (TAN, BDeu 5, ROC-AUC 0,706) é 0,014 (sel − tan). O *log loss* de `sel` é 0,623, contra 0,627 do `nb` (diferença de 0,005, calculada sobre os valores não arredondados: 0,6273 − 0,6226); o plano não tem regra de leitura para essa diferença, e ela é apenas descrita. O Brier de `sel`, 0,202, é menor que o da taxa base, 0,210. Na política de decisão, a diferença pareada de `sel` é 34,4 [16,4; 52,5] (Tabela 4.6). Esses números relatam quanto a configuração escolhida pela regra difere da configuração de referência no teste; não indicam qual modelo adotar, e a análise primária continua com NB e TAN de BDeu 5.

# 5 DISCUSSÃO E LIMITAÇÕES

Este capítulo interpreta os resultados do Capítulo 4 e declara as limitações do experimento. Os métodos estão no Capítulo 3 e as tabelas no Capítulo 4; aqui apenas se remete a eles. Toda leitura de resultado segue as regras pré-registradas da §4 do plano de análise, escritas antes de existir qualquer número. O conjunto de teste final (200 casos, 60 ruins) foi avaliado uma única vez, em 17/11/2026, sobre o *commit* de congelamento 49d77ff; seus números estão nas Tabelas 4.2, 4.5 e 4.6 e na Figura 4.2, e são lidos aqui pelas mesmas regras.

## 5.1 Leitura do desenvolvimento

Os números de desenvolvimento (Tabelas 4.1, 4.3, 4.4, 4.7, 4.9, 4.10) são resultados de desenvolvimento pré-estudo, obtidos só com os 800 casos de desenvolvimento, por validação cruzada em 5 partições; os blocos do conjunto de teste (Tabelas 4.2, 4.5, 4.6 e Figura 4.2) são identificados na legenda. Não têm intervalo de confiança, e os desvios entre partições são da mesma ordem de várias das diferenças entre modelos. Por isso, a leitura a seguir se limita a aplicar as regras da §4 do plano.

**Desempenho preditivo.** A diferença de ROC-AUC entre *Naive Bayes* e regressão logística é 0,001 (0,789 contra 0,788). Pela regra pré-registrada, diferença menor que 0,03 é ruído e nenhum dos dois modelos se distingue do outro. O TAN teve desempenho pior que o NB nas cinco métricas (ROC-AUC e PR-AUC menores; Brier, *log loss* e ECE maiores) (Tabela 4.1), com ROC-AUC de 0,742 e desvio de 0,049 entre partições. As diferenças para o NB (0,047) e para a regressão logística (0,046) passam de 0,03, de modo que a regra de ruído não se aplica; o plano não prevê outra regra para esse caso. O resultado entra no texto como saiu, e não motivou alteração do TAN, de seus parâmetros nem das faixas da análise primária. O fato tem peso para o trabalho, porque o TAN é o modelo da comparação principal, fixado antes de qualquer métrica (decisão P5). A escolha não é revista à luz do resultado: revê-la seria exatamente o ajuste ao resultado que o pré-registro pretende impedir.

**Brier e calibração.** O Brier médio dos três modelos (NB 0,171; TAN 0,200; regressão logística 0,165) é menor que o da taxa base, 0,210; a frase "não melhor que prever a taxa base" não é acionada. O ECE do TAN, 0,152, é o maior dos três (NB 0,093; regressão logística 0,095). Como a política por utilidade esperada usa a probabilidade diretamente, e a literatura indica que decisões sensíveis a custo dependem de probabilidades calibradas \cite{zadrozny2001,elkan2001}, esse erro pode afetar, segundo a literatura, a qualidade das ações que a política escolhe a partir do TAN. O experimento, porém, não mede esse efeito separadamente: a relação vem da literatura, não dos dados (decisão P2).

**Hipótese sobre a finalidade do crédito.** Em todas as partições, a variável finalidade do crédito é a que tem mais arestas saindo dela no TAN, fora a classe (Seção 4.1). Registra-se, apenas como **hipótese não testada**, que isso poderia gerar tabelas de probabilidade condicional esparsas e excesso de confiança, coerente com o *log loss* e o erro de calibração maiores do TAN. A observação de que esconder a finalidade do crédito eleva a ROC-AUC do TAN em 0,025 coexiste com essa hipótese, mas não a testa: nenhuma análise deste trabalho isola a causa, e a observação não autoriza retirar a variável nem mudar o modelo.

**Políticas.** A utilidade média da regra de três ações supera a do corte 0,5 nos três modelos (Tabela 4.4), com diferenças de 28,125 (NB), 25,4 (TAN) e 27,25 (regressão logística). São diferenças descritivas, sem intervalo, que misturam modelo, representação e conjunto de ações, e não são chamadas de efeito da regra. A Seção 5.5 explica por que essa vantagem era esperada antes de qualquer dado. A coincidência, em cada modelo, entre o número de casos que mudam de ação e o número de casos em análise manual decorre da própria matriz: com *c* = 40, a faixa de análise manual vai de 0,10 a 0,60 e contém o corte 0,5, e fora dela as duas regras escolhem a mesma ação. Trata-se de aritmética da faixa 0,10–0,60, não de um achado do experimento.

## 5.2 Leitura do teste final

**Desempenho preditivo.** No teste, a ROC-AUC foi 0,728 (NB), 0,706 (TAN) e 0,729 (regressão logística) (Tabela 4.2). Todas as diferenças entre pares são menores que 0,03 (NB–regressão logística 0,001; NB–TAN 0,021; regressão logística–TAN 0,022), e, pela regra pré-registrada, são ruído. Os intervalos de 95% são largos e se sobrepõem, como o do TAN, de 0,623 a 0,789. A PR-AUC foi 0,490 (NB), 0,480 (TAN) e 0,500 (regressão logística), contra 0,300 da taxa base; como, por decisão do autor registrada em docs/decisoes.md, o limite de 0,03 vale só para ROC-AUC, os valores são apenas descritos, sem conclusão sobre diferenças.

**Queda do desenvolvimento para o teste.** A ROC-AUC caiu de 0,789 para 0,728 no NB, de 0,742 para 0,706 no TAN e de 0,788 para 0,729 na regressão logística; a PR-AUC caiu de 0,616, 0,549 e 0,649 para 0,490, 0,480 e 0,500. A queda é registrada como saiu. Nenhuma análise deste trabalho testa sua causa, e as duas estimativas não são diretamente comparáveis: uma é média de 5 partições sem intervalo, a outra é um único conjunto de 200 casos com intervalo que não cobre a variação do treino (Seção 5.8).

**Brier e calibração.** O Brier do TAN no teste foi 0,215, maior que o da taxa base, 0,210: pela regra pré-registrada, o TAN **não foi melhor que prever a taxa base** no teste. NB (0,199) e logística (0,191) ficaram abaixo da taxa base. O ECE foi 0,115 (NB), 0,157 (TAN) e 0,078 (regressão logística) (Figura 4.2). A calibração foi apenas medida, sem correção (Seção 5.9); essas probabilidades entram como estão na política.

**Implicação para a camada de decisão.** A política supõe que *p* seja uma estimativa calibrada (Seção 2.7), e o TAN, modelo da comparação principal, é o que mais se afasta disso no teste: tem o Brier acima da taxa base e o maior ECE dos três. A camada de decisão não corrige essa falha, apenas a herda: os limiares 0,10 e 0,60 são aplicados a um *p* que, no TAN, errou mais em erro quadrático que a taxa base. A diferença de 22,5 é, portanto, o resultado da política com um estimador fraco, e não com um bom. O sinal da diferença é o mesmo nos três modelos, e o valor cai à medida que o ECE sobe (regressão logística, 38,3 com ECE de 0,078; NB, 29,5 com 0,115; TAN, 22,5 com 0,157). São três pontos, sem teste, com modelo, representação e conjunto de ações variando juntos (Seção 5.7), e a coincidência não é atribuída à calibração. O que o resultado sustenta é que, neste experimento, uma estimativa mal calibrada não impediu a política de três ações de superar o corte 0,5; ele não sustenta que o TAN seja adequado para decidir.

**Políticas.** Na comparação principal, com o TAN (decisão P5), a diferença pareada de utilidade média (`ue` − `limiar`) foi 22,5, com intervalo de 95% de 9,2 a 37,2 (Tabela 4.6). O intervalo exclui zero, de modo que, pela regra pré-registrada (intervalo de 95%, plano de análise §8), o resultado é **a favor da política de três ações**, sem afirmação de causa. NB e regressão logística aparecem nas tabelas, sem destaque na leitura principal; os intervalos do NB (29,5; de 13,1 a 46,3) e da regressão logística (38,3; de 20,2 a 56,4) também excluem zero. A leitura carrega as ressalvas das Seções 5.4 e 5.5 (vantagem por construção, analista infalível, matriz demonstrativa e utilidade simulada sobre o rótulo observado). O resultado não indica qual modelo usar nem que a política seria vantajosa fora deste experimento.

## 5.3 Estudo de seleção

O estudo da §9 do plano é secundário e não altera a análise primária, que continua com NB e TAN de tamanho equivalente BDeu 5.

**Declaração de viés.** Vale a declaração de viés da Seção 3.10. Os números do estudo devem ser lidos com essas duas ressalvas.

**O que a regra escolheu.** Foram feitas 8 comparações (Tabela 4.9). A regra pré-registrada, de menor *log loss* interno, escolheu `nb_ess50` nas cinco partições externas e no desenvolvimento inteiro. A diferença de ROC-AUC entre a linha `aninhado` (0,788) e a configuração de referência `nb_ess5` (0,789) é 0,001, ruído pela regra da §4. A diferença de *log loss* é 0,011 (0,512 contra 0,523), uma diferença sem intervalo e menor que o desvio entre partições de qualquer das duas (0,033 e 0,035). O estudo relata qual configuração a regra escolheu e quanto ela difere da configuração de referência; não indica qual modelo adotar.

**O TAN na grade.** Nas configurações do TAN, o *log loss* médio cai de 0,825 (`tan_ess1`) para 0,583 (`tan_ess50`) à medida que o tamanho equivalente aumenta. A grade varia só o tamanho equivalente, não a estrutura nem as variáveis. A hipótese sobre a finalidade do crédito continua não testada. Nenhuma configuração do TAN foi escolhida em partição alguma.

**`sel` no teste (análise secundária).** No teste, a configuração escolhida pela regra teve ROC-AUC 0,720, PR-AUC 0,477, Brier 0,202 e erro de calibração 0,120; a diferença de ROC-AUC para o NB de BDeu 5 (0,728) é 0,008, ruído pela regra da §4. A diferença pareada de utilidade foi 34,4, com intervalo de 16,4 a 52,5, lida com as mesmas ressalvas da Seção 5.2. Esses números herdam o viés declarado acima: a grade foi desenhada depois de ver o desenvolvimento, e o teste não remove esse viés. A análise primária continua com NB e TAN de BDeu 5 (P5).

## 5.4 Simulação, não política real

A base não traz o resultado das ações que não foram tomadas. A utilidade de cada política é, portanto, calculada aplicando a matriz de utilidade ao rótulo observado, como se cada ação tivesse sido executada. Isso é uma simulação: não há efeito causal da política nem lucro real medido. Os resultados não afirmam que a política seria vantajosa em operação, nem que se generalizam a outras bases ou carteiras.

O trabalho é, por isso, uma demonstração metodológica: mostra como estimar o risco, derivar os limiares e medir a diferença entre duas regras sob uma matriz dada. Não é validação operacional, que exigiria uma matriz levantada com a instituição, o desfecho observado das ações não tomadas e acompanhamento ao longo do tempo.

## 5.5 Matriz demonstrativa e analista infalível

A matriz de utilidade (+100, −400, custo da análise *c* = 40) é demonstrativa, não calibrada com dados reais, e foi aprovada pelo orientador. Ela supõe que o analista da análise manual sempre acerta o estado do cliente: aprova os bons, recusa os ruins e só paga o custo *c*.

Essa hipótese tem uma consequência direta para a comparação de duas regras (Tabelas 4.4 a 4.6): **a política de três ações ganha do corte de duas ações por construção**. A análise manual é uma ação adicional que, com analista infalível, oferece um resultado intermediário quase sem risco; a política de três ações (`ue`) esperada só a escolhe quando, pelo modelo, ela vale mais que aprovar e que rejeitar \cite{chow1970}. O corte 0,5 não tem acesso a essa ação. Uma vantagem da política de três ações (`ue`) na comparação de duas regras é, assim, em grande parte consequência da matriz e do conjunto de ações, não evidência sobre a rede bayesiana nem sobre o critério da utilidade esperada. Por esse motivo a comparação é descrita como "política de três ações por utilidade esperada contra corte 0,5 de duas ações", sem linguagem causal (decisão P8).

Há uma segunda razão para cautela: a comparação com o corte 0,5 não testa "utilidade esperada contra qualquer limiar", pois a utilidade esperada já equivale a uma regra de limiares sobre *p* \cite{elkan2001}. A análise de sensibilidade (Seção 4.4) mostra como esses limiares mudam com a perda e com *c*, sem que este trabalho escolha um valor de custo. O corte fixo de 0,5 não é o limiar de duas ações da matriz demonstrativa (*G*/(*G*+*L*) = 100/500 = 0,2, com *G* = 100 e *L* = 400), de modo que a comparação não o inclui; isso decorre da Seção 2.7, não de uma métrica.

## 5.6 Tamanho do teste

O teste tem 200 casos, dos quais 60 ruins. Com tão poucos casos da classe positiva, diferenças pequenas entre modelos ou políticas são indistinguíveis de ruído. No resultado, os intervalos da diferença pareada (ressalva da Seção 5.2) não incluíram zero em nenhum modelo, mas são largos: no TAN, vão de 9,2 a 37,2. Já as diferenças de ROC-AUC entre modelos no teste ficaram todas abaixo de 0,03 e são tratadas como ruído (Seção 5.2).

## 5.7 Modelo e representação variam juntos

A regressão logística usa as três variáveis contínuas originais, enquanto as redes usam três faixas por tercis (decisão P6). Uma diferença entre o TAN e a regressão logística mistura, assim, a família do modelo e a representação das variáveis, e não é chamada de efeito do modelo. Do mesmo modo, a evidência incompleta não é comparável entre famílias, porque as redes marginalizam a variável ausente e a regressão logística a imputa (decisão P9). Soma-se a isso o espaço de estados fixado no desenvolvimento inteiro, um vazamento brando que não usa rótulo.

## 5.8 O que o intervalo não cobre

O intervalo por *bootstrap* do teste final reamostra os casos de teste com os modelos já treinados \cite{efron1993}; ele não cobre a variação que viria de treinar os modelos em outra amostra (decisão P4). A incerteza total é, portanto, maior que a indicada pelo intervalo.

## 5.9 Calibração só medida

A calibração das probabilidades é medida, mas não corrigida (decisão P1). Métodos de correção, como a sigmoide de Platt e a regressão isotônica \cite{platt1999,zadrozny2002,niculescu2005}, são citados na fundamentação sem aplicação. Como a política consome a probabilidade diretamente, um erro de calibração alto, como o do TAN no desenvolvimento, entra sem correção nas ações escolhidas. Isso é um desvio em relação à proposta, que prometia calibrar.

A sensibilidade das ações a esse erro não foi quantificada: medi-la exigiria recalcular as ações com probabilidades corrigidas, o que está fora do protocolo primário e do plano. Dá para dizer, porém, onde o efeito se concentra. Com *c* = 40, a ação muda nos limiares 0,10 e 0,60, e um caso troca de ação quando o erro de *p* o faz atravessar um deles; são os casos próximos dessas fronteiras que se afetam, e o corte 0,5 de duas ações tem o mesmo problema em torno de 0,5. O ECE mede a diferença média entre a probabilidade estimada e a frequência observada em 10 faixas, e uma diferença média de 0,157, como a do TAN no teste, pode mudar a ação de casos próximos de um limiar. O sinal do efeito sobre a utilidade média não é conhecido, porque o erro desloca *p* para cima em umas faixas e para baixo em outras. Nada disso altera o protocolo primário: os resultados dos Capítulos 4 e 5 usam as probabilidades dos modelos, sem correção.

## 5.10 Direções futuras

As direções a seguir decorrem das limitações acima, não das métricas do desenvolvimento, e não há promessa sobre o resultado de nenhuma delas:

- substituir a matriz demonstrativa por valores levantados com especialistas e modelar o erro do analista na análise manual, o que permitiria examinar a comparação sem a vantagem por construção discutida na Seção 5.5;
- avaliar políticas com dados que registrem o desfecho das ações não tomadas, condição para falar em efeito, e não só em simulação;
- comparar modelos sob a mesma representação das variáveis, separando modelo e representação;
- medir a sensibilidade das ações à calibração, recalibrando em dados separados daqueles em que a política é avaliada e sem alterar a análise primária;
- estimar a incerteza incluindo a variação do treino.

O teste final não acrescenta direções: nenhuma das listadas decorre de suas métricas, e o resultado do teste não motiva mudança de modelo, parâmetro, faixa ou variável.

# 6 CONCLUSÃO

Este trabalho perguntou (1) se uma política que separa a estimativa de risco da escolha da ação tem limiares explícitos e reprodutíveis e (2) que efeito ela produz, em ações e utilidade média, em comparação com um limiar fixo de 0,5. A estimativa de risco é feita por rede bayesiana, com calibração medida, e a escolha da ação, por utilidade esperada.

## 6.1 Limiares explícitos e reprodutíveis

A primeira parte é respondida pela construção da política, e não pelo desempenho dos modelos. Como a utilidade esperada de cada ação é linear na probabilidade estimada *p* de o caso ser ruim, a escolha da ação de maior utilidade equivale a uma regra de limiares sobre *p* (Capítulo 3, Seção 3.7). Com a matriz demonstrativa aprovada pelo orientador, com valores não calibrados com dados reais, a análise manual é escolhida quando *c*/400 ≤ *p* ≤ 1 − *c*/100; com *c* = 40, a faixa vai de 0,10 a 0,60. Dadas a matriz em `config/utilidade.json` e a coluna de probabilidade, qualquer pessoa obtém a ação de cada caso e as fronteiras. A resposta à primeira parte é, portanto, afirmativa, com uma ressalva que o próprio plano registra: essa propriedade vale para qualquer escore de probabilidade e não distingue a rede bayesiana da regressão logística. Ela também é teoria conhecida, e não achado do experimento (Seção 1.4): o trabalho a implementa e a torna reprodutível.

Quanto aos objetivos de sensibilidade e de demonstração (Seção 1.3), os limiares se movem com a perda e o custo da análise (Tabela 4.7) e a demonstração mostra um caso (Tabela 4.8); nenhum valor foi escolhido.

## 6.2 Efeito medido nas ações e na utilidade média

A segunda parte é respondida pelo conjunto de teste, aberto uma única vez em 17/11/2026 sobre o *commit* de congelamento 49d77ff, com 200 casos, dos quais 60 ruins. O critério de leitura é a diferença pareada de utilidade média entre a política de três ações por utilidade esperada e o corte 0,5 de duas ações, com intervalo de 95% por *bootstrap* (Tabela 4.6); o nível de 95% segue a ressalva da Seção 5.2.

Na comparação principal, com o TAN, a diferença foi de 22,5, com intervalo de 9,2 a 37,2. Pela regra pré-registrada, observa-se diferença a favor da política de três ações, com intervalo que exclui zero; não se afirma causa. Nas ações, a política de três ações aprovou 92, rejeitou 48 e encaminhou 60 casos para análise manual, contra 145 aprovações e 55 rejeições do corte 0,5; os 60 casos que mudaram de ação são exatamente os encaminhados para análise manual.

Esse resultado precisa ser lido com a ressalva que o acompanha desde o plano (ressalva da Seção 5.5). A diferença mistura modelo, representação e conjunto de ações, e não é chamada de efeito da regra nem do modelo. Como a base não registra o desfecho das ações não tomadas, trata-se de uma simulação metodológica, e não da validação de uma política real.

Quanto ao risco estimado, o teste mostrou diferenças de ROC-AUC entre os três modelos de 0,001 a 0,022, todas abaixo de 0,03 e, pela regra pré-registrada, tratadas como ruído. O Brier do TAN, 0,215, foi maior que o da taxa base, 0,210: no teste, o TAN não foi melhor que prever a taxa base. As PR-AUC foram 0,490 (*Naive Bayes*), 0,480 (TAN) e 0,500 (regressão logística), contra 0,300 da taxa base; por decisão do autor registrada em docs/decisoes.md, essa métrica não tem regra de ruído e os valores são apenas descritos. O ECE foi 0,115, 0,157 e 0,078, respectivamente, e foi apenas medido. Os resultados de desenvolvimento e os do teste são distintos e não se substituem (Seção 4.1).

## 6.3 Limitações essenciais

As conclusões acima valem dentro de limites discutidos no Capítulo 5: a matriz de utilidade é demonstrativa, aprovada pelo orientador, com valores não calibrados com dados reais, e supõe analista infalível (Seção 5.5); a camada de decisão é simulação, não política real (Seção 5.4); o teste tem 200 casos e 60 ruins, o que deixa intervalos largos (Seção 5.6); modelo e representação das variáveis variam juntos (Seção 5.7); o intervalo não cobre a variação do treino (Seção 5.8); e a calibração é só medida, sem correção (Seção 5.9). Os resultados não autorizam generalizar para outras bases nem recomendar um modelo. As direções gerais de continuação estão na Seção 5.10.

# REFERÊNCIAS

<!-- Formato ABNT NBR 6023 (autor-data). Gerado de referencias.bib; só campos do.bib. -->
<!-- normas ABNT não citadas retiradas da lista: abnt6023, abnt10520, abnt14724 -->

ANKAN, Ankur; TEXTOR, Johannes. pgmpy: A Python Toolkit for Bayesian Networks. **Journal of Machine Learning Research**, v. 25, n. 265, p. 1–8, 2024.
<!-- ankan2024: Fonte: CITATION.cff do pgmpy (preferred-citation). Autor decidiu citar esta em 17/11/2026. Artigo 265 conferido em jmlr.org/papers/v25/23-0487.html. -->

BRIER, Glenn W. Verification of forecasts expressed in terms of probability. **Monthly Weather Review**, v. 78, n. 1, p. 1–3, 1950.
<!-- brier1950 -->

CHOW, C. K. On optimum recognition error and reject tradeoff. **IEEE Transactions on Information Theory**, v. 16, n. 1, p. 41–46, 1970.
<!-- chow1970: VERIFICAR: todos os campos. -->

CHOW, C. K.; LIU, C. N. Approximating discrete probability distributions with dependence trees. **IEEE Transactions on Information Theory**, v. 14, n. 3, p. 462–467, 1968. DOI: 10.1109/TIT.1968.1054142.
<!-- chowliu1968: Metadados conferidos em 17/11/2026 (OpenAlex, DOI 10.1109/TIT.1968.1054142); texto não lido. -->

EFRON, Bradley; TIBSHIRANI, Robert J. **An Introduction to the Bootstrap**. New York: Chapman & Hall, 1993.
<!-- efron1993 -->

ELKAN, Charles. The foundations of cost-sensitive learning. In: INTERNATIONAL JOINT CONFERENCE ON ARTIFICIAL INTELLIGENCE, 17., 2001. **Proceedings** [...]. [S. l.: s. n.], 2001. p. 973–978.
<!-- elkan2001: Entrada do bloco "A CONFERIR NO ORIGINAL ANTES DE CITAR" (título, ano, volume e páginas podem estar errados). -->
<!-- FALTA: local do evento, local de publicação, editora -->

FRIEDMAN, Nir; GEIGER, Dan; GOLDSZMIDT, Moises. Bayesian network classifiers. **Machine Learning**, v. 29, n. 2–3, p. 131–163, 1997. DOI: 10.1023/A:1007465528199.
<!-- friedman1997: Metadados conferidos em 17/11/2026 (OpenAlex, DOI 10.1023/A:1007465528199); texto não lido. -->

GRÖMPING, Ulrike. **South German Credit Data**: Correcting a Widely Used Data Set. Berlin: Beuth University of Applied Sciences Berlin, 2019. (Reports in Mathematics, Physics and Chemistry, 4/2019). Disponível em: https://www1.beuth-hochschule.de/FB_II/reports/Report-2019-004.pdf. Acesso em: 10 nov. 2026.
<!-- gromping2019: VERIFICAR: nome da série do relatório e da instituição (Beuth University of Applied Sciences Berlin, hoje BHT). -->

GUO, Chuan et al. On calibration of modern neural networks. In: INTERNATIONAL CONFERENCE ON MACHINE LEARNING, 34., 2017. **Proceedings** [...]. PMLR, 2017. p. 1321–1330. (Proceedings of Machine Learning Research, v. 70).
<!-- guo2017 -->
<!-- FALTA: local do evento, local de publicação -->

HAND, David J.; HENLEY, William E. Statistical classification methods in consumer credit scoring: a review. **Journal of the Royal Statistical Society: Series A**, v. 160, n. 3, p. 523–541, 1997.
<!-- hand1997: VERIFICAR: todos os campos. -->

HECKERMAN, David; GEIGER, Dan; CHICKERING, David M. Learning Bayesian networks: the combination of knowledge and statistical data. **Machine Learning**, v. 20, n. 3, p. 197–243, 1995. DOI: 10.1007/BF00994016.
<!-- heckerman1995: Metadados conferidos em 17/11/2026 (Microsoft Research, DOI 10.1007/BF00994016); texto não lido. -->

HOFMANN, Hans. **Statlog (German Credit Data)**. 1994. Conjunto de dados. UCI Machine Learning Repository. Disponível em: https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data).
<!-- hofmann1994: Base original, citada na proposta. O trabalho usa a versão corrigida (gromping2019, uci573). Entrada do bloco "referências da proposta" (conferir no exemplar usado). -->
<!-- FALTA: data de acesso (urlaccessdate) -->

HOWARD, Ronald A.; MATHESON, James E. Influence diagrams. **Decision Analysis**, v. 2, n. 3, p. 127–143, 2005.
<!-- howard2005: VERIFICAR: a proposta cita a reimpressão de 2005 do trabalho original de 1984. -->

JENSEN, Finn V.; NIELSEN, Thomas D. **Bayesian Networks and Decision Graphs**. 2. ed. New York: Springer, 2007.
<!-- jensen2007: Bloco "referências da proposta": conferir edição e páginas no exemplar usado. -->

KAUFMAN, Shachar et al. Leakage in data mining: Formulation, detection, and avoidance. **ACM Transactions on Knowledge Discovery from Data**, v. 6, n. 4, p. 1–21, 2012.
<!-- kaufman2012: VERIFICAR: número do artigo (15) e paginação (1–21). -->

KOLLER, Daphne; FRIEDMAN, Nir. **Probabilistic Graphical Models**: Principles and Techniques. Cambridge: MIT Press, 2009.
<!-- koller2009: Bloco "referências da proposta": conferir edição e páginas no exemplar usado. -->

NAEINI, Mahdi Pakdaman; COOPER, Gregory F.; HAUSKRECHT, Milos. Obtaining well calibrated probabilities using Bayesian binning. In: AAAI CONFERENCE ON ARTIFICIAL INTELLIGENCE, 29., 2015. **Proceedings** [...]. AAAI Press, 2015. p. 2901–2907.
<!-- naeini2015 -->
<!-- FALTA: local do evento, local de publicação -->

NICULESCU-MIZIL, Alexandru; CARUANA, Rich. Predicting good probabilities with supervised learning. In: INTERNATIONAL CONFERENCE ON MACHINE LEARNING, 22., 2005. **Proceedings** [...]. [S. l.: s. n.], 2005. p. 625–632.
<!-- niculescu2005: VERIFICAR: todos os campos. -->
<!-- FALTA: local do evento, local de publicação, editora -->

PEARL, Judea. **Probabilistic Reasoning in Intelligent Systems**: networks of plausible inference. San Francisco: Morgan Kaufmann, 1988.
<!-- pearl1988: Bloco "referências da proposta": conferir edição e páginas no exemplar usado. -->

PEDREGOSA, Fabian et al. Scikit-learn: Machine learning in Python. **Journal of Machine Learning Research**, v. 12, p. 2825–2830, 2011.
<!-- pedregosa2011 -->

PLATT, John C. Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In: SMOLA, Alexander J. et al. (ed.). **Advances in Large Margin Classifiers**. Cambridge: MIT Press, 1999. p. 61–74.
<!-- platt1999: VERIFICAR: ano do livro (1999 na capa; algumas bases citam 2000) e páginas 61–74. -->

RUSSELL, Stuart; NORVIG, Peter. **Artificial Intelligence**: a modern approach. 3. ed. Upper Saddle River: Prentice Hall, 2010.
<!-- russell2010: VERIFICAR: trocada em 15/11/2026 da tradução brasileira para o original em inglês (3ª edição); título, editora, cidade e ano escritos de memória; conferir no original. -->

SIDDIQI, Naeem. **Credit Risk Scorecards**: developing and implementing intelligent credit scoring. Hoboken: John Wiley & Sons, 2012.
<!-- siddiqi2012: Bloco "referências da proposta": conferir edição e páginas no exemplar usado. -->

THOMAS, Lyn C. A survey of credit and behavioural scoring: forecasting financial risk of lending to consumers. **International Journal of Forecasting**, v. 16, n. 2, p. 149–172, 2000.
<!-- thomas2000: Bloco "referências da proposta": conferir no original. -->

UCI MACHINE LEARNING REPOSITORY. **South German Credit (UPDATE)**. 2020. Conjunto de dados n. 573. UCI Machine Learning Repository. DOI: 10.24432/C5QG88. Disponível em: https://archive.ics.uci.edu/dataset/573/south+german+credit+update. Acesso em: 10 nov. 2026.
<!-- uci573: Ano 2020 = criação do conjunto na UCI (decidido pelo autor, 17/11/2026). DOI conferido na API da UCI (docs/conferencia-referencias.md). -->

ZADROZNY, Bianca; ELKAN, Charles. Obtaining calibrated probability estimates from decision trees and naive Bayesian classifiers. In: INTERNATIONAL CONFERENCE ON MACHINE LEARNING, 18., 2001. **Proceedings** [...]. [S. l.: s. n.], 2001. p. 609–616.
<!-- zadrozny2001: Anais e páginas conferidos em 17/11/2026 (mlanthology.org, ICML 2001, pp. 609–616); título, autores e resumo no PDF dos autores. -->
<!-- FALTA: local do evento, local de publicação, editora -->

ZADROZNY, Bianca; ELKAN, Charles. Transforming classifier scores into accurate multiclass probability estimates. In: ACM SIGKDD INTERNATIONAL CONFERENCE ON KNOWLEDGE DISCOVERY AND DATA MINING, 8., 2002. **Proceedings** [...]. [S. l.: s. n.], 2002. p. 694–699.
<!-- zadrozny2002: VERIFICAR: todos os campos. -->
<!-- FALTA: local do evento, local de publicação, editora -->

# APÊNDICES

## APÊNDICE A – Como reproduzir os resultados

Todos os arquivos de `resultados/` são gerados por sete scripts Python que leem CSV e gravam tabelas e figuras, sem servidor, banco de dados nem modelo salvo em arquivo. Os comandos abaixo partem da raiz do repositório, rodam sem interação e usam Python 3.12 com as dependências travadas pelo `uv`, inclusive o `pgmpy` 1.1.2.

### A.1 Ambiente

```bash
uv sync --frozen
```

A opção `--frozen` instala exatamente as versões do `uv.lock`. A versão do `pgmpy` não deve ser atualizada, porque a interface da biblioteca mudou entre as versões 1.0 e 1.1.2.

### A.2 Ordem de execução

Cada script grava apenas em `resultados/`; a exceção é `preparar_sgc.py`, que grava em `dados/processados/`. Toda fonte de aleatoriedade usa a semente 2026, e rodar o mesmo comando duas vezes gera arquivos CSV e JSON idênticos byte a byte. As figuras PNG não foram comparadas byte a byte entre execuções.

**Quadro A.1** – Comandos, em ordem, e arquivos gravados

| Passo | Comando | Grava |
|---|---|---|
| Divisão desenvolvimento/teste | `uv run python codigo/preparar_sgc.py` | `dados/processados/sgc.csv`, `dev.csv`, `teste.csv`, `SHA256SUMS` |
| Predições no desenvolvimento | `uv run python codigo/modelos.py` | `predicoes_dev.csv`, `cortes.json`, `tan_arestas.csv` |
| Métricas e calibração | `uv run python codigo/avaliar.py` | `metricas_dev.csv`, `calibracao_dev.png` |
| Evidência incompleta | `uv run python codigo/modelos.py --ocultar`, depois `uv run python codigo/avaliar.py --ocultar` | `predicoes_dev_oculta.csv`, `evidencia_incompleta.csv` |
| Camada de decisão | `uv run python codigo/decisao.py` | `politicas_dev.csv`, `resumo_politicas_dev.csv` |
| Sensibilidade | `uv run python codigo/sensibilidade.py` | `sensibilidade.csv`, `sensibilidade.png` |
| Estudo de seleção (secundário) | `uv run python codigo/modelos.py --selecao`, depois `uv run python codigo/avaliar.py --selecao` | `predicoes_selecao.csv`, `selecao_dev.csv`, `selecao_escolha.csv` |
| Demonstração | `uv run python codigo/demo.py <record_id> [--modelo nb\|tan\|logreg]` | nada; imprime no terminal |

### A.3 Autotestes e conferência

Os scripts `modelos.py`, `avaliar.py` e `sensibilidade.py` têm o modo `--verificar`, que confere contas com resposta conhecida e não grava nada; `test_decisao.py` usa apenas `assert` e inclui o exemplo da apresentação de 15/10/2026 (com p = 0,20, ganho de 100 e perda de 400, a utilidade esperada de aprovar é 0; com perda de 600, é −40).

```bash
uv run python codigo/modelos.py --verificar
uv run python codigo/avaliar.py --verificar
uv run python codigo/sensibilidade.py --verificar
uv run python codigo/test_decisao.py
```

Os arquivos gerados são versionados junto com o código. Depois de rodar tudo, a reprodução é confirmada se o comando abaixo não imprimir nada e terminar com código 0:

```bash
git diff --exit-code -- 'resultados/*.csv' 'resultados/*.json'
```

Esse teste confere que os arquivos são idênticos aos publicados, não que o modelo é bom.

### A.4 Teste final

O conjunto de teste foi usado uma única vez, em 17/11/2026, sobre o commit de congelamento `49d77ff`, e todos os comandos terminaram com código de saída 0. Os comandos, na ordem, foram:

```bash
uv run python codigo/modelos.py --final <arquivo do teste>
uv run python codigo/avaliar.py --final
uv run python codigo/decisao.py --final
```

Eles gravam `predicoes_teste.csv`, `metricas_teste.csv`, `calibracao_teste.png`, `politicas_teste.csv`, `resumo_politicas_teste.csv` e `diferenca_politicas_teste.csv`; os intervalos usam bootstrap com 2000 reamostras e semente 2026. O primeiro comando exige o caminho do arquivo de teste como argumento e recusa sobrescrever `predicoes_teste.csv` se ele já existir.

Quem reproduz sem o arquivo de teste obtém todos os resultados de desenvolvimento, mas não os `*_teste*`: a divisão é determinística (semente 2026) e sai de `dados/brutos/`, que não acompanha a descrição do código.

---

## APÊNDICE B – Resultados dos três modelos

Os três modelos (Naive Bayes, TAN e regressão logística) aparecem lado a lado nas Tabelas 4.1, 4.2, 4.4, 4.5 e 4.6 do capítulo 4; o TAN é o modelo da comparação principal por decisão de 15/11/2026, tomada antes de qualquer métrica. Por isso este apêndice não repete as tabelas. Se o formato do curso exigir os três modelos fora do corpo do texto, as Tabelas 4.2, 4.5 e 4.6 passam para cá, com as linhas `nb` e `logreg` no apêndice e `tan` no capítulo.
<!-- decidir: manter as tabelas completas no capítulo 4 (como está) ou mover as linhas nb/logreg para este apêndice, como previa o PLANO.md §5 -->

## APÊNDICE C – Plano de análise

O plano de análise foi escrito em 15/11/2026, antes de existir qualquer resultado, e fixa o que será reportado e como cada desfecho será lido. Segue a cópia integral do documento do repositório, com os títulos rebaixados um nível; os links relativos remetem a arquivos do repositório.

Escrito em 15/11/2026, **antes de existir qualquer resultado**. Diz o que será reportado e como cada desfecho será lido. O objetivo é que nenhuma decisão de análise dependa do que os números mostrarem.

Fontes: [PLANO.md](../PLANO.md), [decisoes.md](decisoes.md) e [criterios-de-aceite.md](criterios-de-aceite.md). Este arquivo não cria decisão de modelo: só fixa como ler o que o experimento produzir. Itens que dependem de um número e ainda não têm dono estão marcados **a confirmar pelo autor**.

### 1. Pergunta

A política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) tem (1) limiares explícitos, reproduzíveis a partir da matriz de utilidade e de `p`, e (2) que efeito medido sobre as ações e a utilidade média, em comparação com um limiar fixo de 0,5?

- **Parte 1** é uma propriedade da política: vale para qualquer escore e não depende de resultado. Fica demonstrada pelas fronteiras `c/400` e `1 − c/100` (na matriz demonstrativa) e pela tabela de sensibilidade.
- **Parte 2** é o que o experimento mede.

### 2. O que será reportado, qualquer que seja o resultado

| Item | Arquivo | Onde entra |
|---|---|---|
| ROC-AUC, PR-AUC, Brier, log loss e erro de calibração dos três modelos e da taxa base, com média e desvio entre as 5 partições | `metricas_dev.csv` | Capítulo 4.1 |
| Diagrama de calibração | `calibracao_dev.png` | Capítulo 4.1 |
| Queda por variável escondida | `evidencia_incompleta.csv` | Capítulo 4.2 |
| Utilidade média e distribuição das ações por modelo e regra | `resumo_politicas_dev.csv` | Capítulo 4.3 |
| Fronteiras de decisão por perda e custo da análise | `sensibilidade.csv`, `sensibilidade.png` | Capítulo 4.4 |
| Arestas do TAN em cada partição | `tan_arestas.csv` | Capítulo 4.1 |
| No teste final: métricas com intervalo, utilidade média com intervalo e a diferença pareada entre as regras | `metricas_teste.csv`, `resumo_politicas_teste.csv`, `diferenca_politicas_teste.csv` | Capítulos 4.1 e 4.3 |

Todos os três modelos aparecem em todas as tabelas, também os que não vão para o texto principal.

### 3. Comparação principal

Fixada antes de ver métricas (decisão P5):

- **Modelo:** TAN.
- **Regras comparadas:** a política de três ações por utilidade esperada e o corte 0,5 de duas ações.
- **Medida:** diferença pareada de utilidade média, com intervalo por bootstrap (2000 reamostras, semente 2026, percentis 2,5 e 97,5) no teste final.

Naive Bayes e regressão logística vão para o apêndice, na mesma estrutura. A tabela é descritiva: a diferença mistura modelo, representação e conjunto de ações, e não é chamada de "efeito do modelo" nem de "efeito da regra".

### 4. Como cada desfecho será lido

Regras de leitura definidas agora. Nenhuma depende do valor observado.

| Se o resultado for | O texto diz |
|---|---|
| O intervalo da diferença pareada exclui 0 a favor da utilidade esperada | "Diferença observada a favor da política de utilidade, com intervalo que exclui zero." Sem afirmar causa |
| O intervalo inclui 0 | "Sem evidência de diferença com 200 casos e 60 ruins." Não se conclui que as políticas são iguais |
| O intervalo exclui 0 a favor do limiar 0,5 | Reportado como saiu, junto com a ressalva de que a regra fixa só tem duas ações |
| A diferença de ROC-AUC entre dois modelos é menor que 0,03 | Tratada como ruído, como diz o plano (item 6). Nenhum modelo "vence" |
| O Brier de um modelo é igual ou maior que o da taxa base (0,21) | "Não melhor que prever a taxa base." Entra no texto |
| Alguma ação não aparece numa política | Reportado (é o `AVISO:` do script). Não se muda a matriz por isso |
| O erro de calibração de um modelo é alto | Reportado. A calibração só é medida; não há correção (decisão P1) |
| Esconder uma variável não muda nenhuma predição | Reportado como aviso |

### 5. O que não será feito

1. Ajustar modelo, parâmetro, semente, faixa ou variável por causa de uma métrica (`AGENTS.md`, regra 3).
2. Escolher o modelo do texto depois de ver as métricas (o TAN já está fixado).
3. Rodar o teste final mais de uma vez ou antes do commit de congelamento.
4. Abrir `teste.csv`, `sgc.csv` ou `dados/brutos/` fora do `preparar_sgc.py` e do teste final.
5. Remover casos, trocar a divisão ou mudar a matriz de utilidade porque o resultado incomodou.

Tudo acima vale exceto o estudo da §9, que é secundário, pré-registrado e roda só no modo `--selecao`.

### 6. Limitações a declarar

1. A base não traz o resultado das ações que não foram tomadas: não há efeito causal nem lucro real, só simulação.
2. O teste tem 60 casos ruins; diferenças pequenas são ruído.
3. A matriz de utilidade é demonstrativa e "o analista sempre acerta".
4. A regressão logística usa as contínuas originais e as redes usam 3 faixas.
5. O intervalo por bootstrap não cobre a variação do treino (decisão P4).
6. O espaço de estados foi fixado no dev inteiro, um vazamento brando que não usa rótulo.
7. A comparação com o corte 0,5 não é um teste de "utilidade esperada contra qualquer limiar", porque a utilidade esperada já equivale a limiares.

### 7. Se algo mudar

Qualquer mudança neste plano depois de existirem resultados vira uma linha em [decisoes.md](decisoes.md), com data e motivo, **antes** de rodar de novo. A mudança também é declarada no texto como desvio do plano de análise.

### 8. Decidido pelo autor em 18/11/2026

- O intervalo de 95% é o critério de leitura da diferença (seção 4), o mesmo nível do bootstrap das métricas. Decidido em 18/11/2026: confirma o que já estava escrito.
- O limite de 0,03 de AUC, que vem do plano, vale só para ROC-AUC. PR-AUC é apenas descrita, sem conclusão de ruído. Decidido em 18/11/2026; registro em `docs/decisoes.md`.

### 9. Estudo de seleção (secundário, pré-registrado)

Status: estudo secundário pré-registrado em 16/11/2026, antes da execução do teste final.

**Grade fechada, 8 configurações** ({NB, TAN} × tamanho equivalente BDeu {1, 5, 10, 50}):

| id | Modelo | Tamanho equivalente |
|---|---|---|
| `nb_ess1` | NB | 1 |
| `nb_ess5` | NB | 5 (baseline) |
| `nb_ess10` | NB | 10 |
| `nb_ess50` | NB | 50 |
| `tan_ess1` | TAN | 1 |
| `tan_ess5` | TAN | 5 (baseline) |
| `tan_ess10` | TAN | 10 |
| `tan_ess50` | TAN | 50 |

A ordem da tabela é a ordem da grade. Fora da grade: K2, outras faixas, seleção de variáveis, hill climbing, Platt/isotônica e reponderação.

**Validação cruzada aninhada.** Partições externas = as 5 atuais. Em cada externa, as 640 linhas de treino são divididas por `StratifiedKFold(5, shuffle=True, random_state=2026)`; cada configuração é treinada e avaliada nas partições internas.

**Regra de escolha.** Menor log loss médio nas partições internas. Empate (diferença < 1e-9) resolvido pela ordem da grade. A configuração escolhida em cada externa prevê as 160 linhas dela; daí saem `p_sel` (as linhas com `fold_interno` = -1 da configuração escolhida) e a linha "aninhado". A escolha também é recalculada no dev inteiro (linha `dev` de `selecao_escolha.csv`), só para relato.

**Relato obrigatório.** As 8 linhas da grade, o número de comparações (8) e a linha "aninhado", qualquer que seja o resultado.

**Declaração obrigatória de viés.** A grade foi definida depois de ver `metricas_dev.csv` e motivada por ele (TAN pior que NB; hipótese finalidade do crédito em [resultados-dev.md](resultados-dev.md)). O aninhamento corrige o viés de escolher entre as 8 configurações, mas não o de ter desenhado a grade olhando o mesmo dev. O texto da monografia declara isso.

**Leitura dos desfechos.** Diferença de ROC-AUC menor que 0,03 é ruído, como na §4. Não se fala em "melhor modelo": relata-se qual configuração a regra escolheu e quanto ela difere do baseline.

**O que não muda.** A tabela 2×2 e a análise primária continuam com NB e TAN de BDeu 5 (P5 intacta). `p_sel` é análise secundária e aparece rotulada como tal.

Saídas:

- `resultados/predicoes_selecao.csv`: `config, record_id, fold_externo, fold_interno, p_ruim`; `fold_interno` = -1 é a predição externa; 32.000 linhas.
- `resultados/selecao_dev.csv`: as 8 configurações e a linha `aninhado` (sem linha `dev`).
- `resultados/selecao_escolha.csv`: `fold_externo` (0 a 4 e `dev`) × 8 configurações, com `log_loss_interno` e `escolhida`; 48 linhas.


