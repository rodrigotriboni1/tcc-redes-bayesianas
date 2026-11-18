# Título provisório: redes bayesianas e utilidade esperada na decisão de crédito

# RESUMO

A concessão de crédito costuma decidir comparando um escore de risco com um ponto de corte, o que mistura a estimativa do risco com a escolha da ação. Este trabalho pergunta se uma política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) tem (1) limiares explícitos, que qualquer pessoa reproduz a partir da matriz de utilidade e da probabilidade estimada, e (2) que efeito medido sobre as ações e a utilidade média, em comparação com um limiar fixo de 0,5 <!-- fonte: PLANO.md §1 (constante da pergunta, não resultado) -->. Usa-se a base South German Credit, dividida de forma estratificada em 800 casos de desenvolvimento e 200 de teste <!-- fonte: monografia/cap3-metodos.md §3.2; PLANO.md §4 -->, com validação cruzada estratificada em 5 partições no desenvolvimento <!-- fonte: monografia/cap3-metodos.md §3.3; PLANO.md §5 -->. O risco de o crédito ser ruim é estimado por duas redes bayesianas, Naive Bayes e TAN (Naive Bayes aumentado por árvore), implementadas com a biblioteca pgmpy, e por uma regressão logística de referência, avaliadas por discriminação (ROC-AUC e PR-AUC), escore de Brier, log loss e erro de calibração esperado (ECE); a calibração é medida, sem correção. Uma camada de utilidade esperada escolhe, para cada caso, entre três ações: aprovar, rejeitar ou encaminhar para análise manual. A matriz de utilidade é demonstrativa, não calibrada com dados reais, e supõe que o analista da análise manual sempre acerta o estado do cliente. Mede-se a distribuição das ações, a utilidade média e o número de casos que mudam de ação em relação ao limiar fixo, além da sensibilidade das fronteiras aos custos e do comportamento com evidência incompleta. Um estudo de seleção secundário de estrutura e prior, por validação cruzada aninhada, com a grade definida depois de ver as métricas de desenvolvimento, é relatado à parte. Como a base não registra o resultado das ações não tomadas, a camada de decisão é uma simulação metodológica, e não a validação de uma política real. Os resultados de desenvolvimento são relatados como linha de base, sem intervalo de confiança. No conjunto de teste, aberto uma única vez, com 200 casos e 60 ruins <!-- fonte: resultados/predicoes_teste.csv, coluna kredit -->, as diferenças de ROC-AUC entre os três modelos ficaram abaixo de 0,03 e são tratadas como ruído, e o Brier do TAN (0,215) não foi melhor que prever a taxa base (0,210) <!-- fonte: resultados/metricas_teste.csv, roc_auc e brier, linhas nb, tan, logreg e taxa_base -->. Na comparação principal, com o TAN, a diferença pareada de utilidade média entre a política de três ações e o corte 0,5 foi de 22,5, com intervalo de 95% de 9,2 a 37,2, que exclui zero <!-- a confirmar: nível de 95% (plano §8) -->, e 60 casos mudaram de ação; a utilidade média de cada política foi 17,5 (−1,4 a 35,3) na de três ações e −5,0 (−29,5 a 19,5) no corte 0,5 <!-- fonte: resultados/resumo_politicas_teste.csv, linhas tan, utilidade_media e IC -->, mas o critério de leitura é a diferença pareada, não o intervalo de cada política isolada <!-- fonte: resultados/diferenca_politicas_teste.csv, linha tan; resultados/resumo_politicas_teste.csv, n_mudam_vs_outra_regra, linha tan -->. A política de três ações ganha por construção, pois só ela tem a análise manual com analista infalível, e o resultado vale para a simulação. Os resultados de desenvolvimento e de teste são distintos e relatados separadamente.

**Palavras-chave:** redes bayesianas; risco de crédito; utilidade esperada; calibração; teoria da decisão.

# ABSTRACT

Credit granting usually decides by comparing a risk score with a cutoff, which mixes risk estimation with the choice of action. For a policy that separates risk estimation (Bayesian network, with measured calibration) from the choice of action (expected utility), this work asks (1) whether such a policy has explicit thresholds that anyone can reproduce from the utility matrix and the estimated probability, and (2) what measured effect it has on the actions and the mean utility, compared with a fixed threshold of 0.5 <!-- fonte: PLANO.md §1 (constante da pergunta, não resultado) -->. The South German Credit dataset is used, split in a stratified way into 800 development cases and 200 test cases <!-- fonte: monografia/cap3-metodos.md §3.2; PLANO.md §4 -->, with stratified 5-fold cross-validation on the development set <!-- fonte: monografia/cap3-metodos.md §3.3; PLANO.md §5 -->. Credit risk (probability of a bad loan) is estimated by two Bayesian networks, Naive Bayes and Tree-Augmented Naive Bayes (TAN), implemented with the pgmpy library, and by a reference logistic regression, evaluated by discrimination (ROC-AUC and PR-AUC), Brier score, log loss and expected calibration error (ECE); calibration is measured but not corrected. An expected-utility layer chooses, for each case, among three actions: approve, reject or refer to manual review. The utility matrix is illustrative, not calibrated with real data, and assumes that the manual-review analyst always identifies the client's true state. The distribution of actions, the mean utility and the number of cases that change action relative to the fixed threshold are measured, as well as the sensitivity of the boundaries to costs and the behavior under incomplete evidence. A secondary structure and prior selection study, by nested cross-validation, with the grid defined after seeing the development metrics, is reported separately. Because the dataset does not record the outcome of actions not taken, the decision layer is a methodological simulation, not the validation of a real policy. The development results are reported as a baseline, without confidence intervals. On the test set, opened only once, with 200 cases and 60 bad ones <!-- fonte: resultados/predicoes_teste.csv, coluna kredit -->, the ROC-AUC differences among the three models were below 0.03 and are treated as noise, and the Brier score of TAN (0.215) was not better than predicting the base rate (0.210) <!-- fonte: resultados/metricas_teste.csv, roc_auc e brier, linhas nb, tan, logreg e taxa_base -->. In the main comparison, with TAN, the paired difference in mean utility between the three-action policy and the 0.5 cutoff was 22.5, with a 95% interval from 9.2 to 37.2, which excludes zero <!-- a confirmar: nível de 95% (plano §8) -->, and 60 cases changed action; the mean utility of each policy was 17.5 (−1.4 to 35.3) for the three-action policy and −5.0 (−29.5 to 19.5) for the 0.5 cutoff <!-- fonte: resultados/resumo_politicas_teste.csv, linhas tan, utilidade_media e IC -->, but the reading criterion is the paired difference, not the interval of each policy alone <!-- fonte: resultados/diferenca_politicas_teste.csv, linha tan; resultados/resumo_politicas_teste.csv, n_mudam_vs_outra_regra, linha tan -->. The three-action policy wins by construction, since only it has manual review with an infallible analyst, and the result holds for the simulation. The development and test results are distinct and reported separately.

**Keywords:** Bayesian networks; credit risk; expected utility; calibration; decision theory.

# SUMÁRIO

- 1 Introdução
  - 1.1 Contexto
  - 1.2 Pergunta de pesquisa
  - 1.3 Objetivos
  - 1.4 O que o trabalho não faz
  - 1.5 Mudanças em relação à proposta
  - 1.6 Organização do texto
- 2 FUNDAMENTAÇÃO
  - 2.1 Redes bayesianas
  - 2.2 Naive Bayes e TAN
  - 2.3 Aprendizado de parâmetros e prior BDeu
  - 2.4 Inferência exata
  - 2.5 Calibração
  - 2.6 Utilidade esperada
  - 2.7 Limiares derivados dos custos
  - 2.8 Opção de rejeição
  - 2.9 Escore de crédito e *next best action*
- 3 MATERIAIS E MÉTODOS
  - 3.1 Base de dados
    - 3.1.1 Análise exploratória
  - 3.2 Divisão em desenvolvimento e teste
  - 3.3 Validação cruzada
  - 3.4 Discretização
  - 3.5 Modelos de risco
    - 3.5.1 Evidência incompleta
  - 3.6 Métricas
  - 3.7 Camada de decisão por utilidade esperada
    - 3.7.1 Comparação de políticas
  - 3.8 Análise de sensibilidade
  - 3.9 Demonstração
  - 3.10 Estudo de seleção aninhado (secundário)
  - 3.11 Ambiente e reprodutibilidade
- 4 RESULTADOS
  - 4.1 Desempenho preditivo
  - 4.2 Evidência incompleta
  - 4.3 Política de decisão
  - 4.4 Sensibilidade
  - 4.5 Demonstração
  - 4.6 Estudo de seleção (secundário)
- 5 DISCUSSÃO E LIMITAÇÕES
  - 5.1 Leitura do desenvolvimento
  - 5.1b Leitura do teste final
  - 5.2 Estudo de seleção
  - 5.3 Simulação, não política real
  - 5.4 Matriz demonstrativa e analista infalível
  - 5.5 Tamanho do teste
  - 5.6 Modelo e representação variam juntos
  - 5.7 O que o intervalo não cobre
  - 5.8 Calibração só medida
  - 5.9 Escopo das entregas
  - 5.10 Direções futuras
- 6 CONCLUSÃO
  - 6.1 Limiares explícitos e reprodutíveis
  - 6.2 Efeito medido nas ações e na utilidade média
  - 6.3 Limitações essenciais
- Referências

# LISTA DE TABELAS

- Tabela 4.1 – Métricas por modelo no desenvolvimento, média (desvio) entre 5 partições
- Tabela 4.2 – Arestas do TAN por partição
- Tabela 4.3 – Métricas por modelo no conjunto de teste (n=200; 60 ruins), valor [intervalo de 95%]
- Tabela 4.4 – Variação de métricas ao esconder uma variável, seleção de linhas
- Tabela 4.5 – Política de três ações por utilidade esperada contra corte 0,5 de duas ações, desenvolvimento
- Tabela 4.6 – Política de três ações contra corte 0,5 de duas ações, conjunto de teste (n=200; 60 ruins)
- Tabela 4.7 – Diferença pareada de utilidade média (`ue` − `limiar`), conjunto de teste (n=200; 60 ruins)
- Tabela 4.8 – Limiares da política por perda e custo da análise manual, seleção de linhas
- Tabela 4.9 – Saída de `codigo/demo.py` para o caso sgc-0000
- Tabela 4.10 – Métricas das 8 configurações e da seleção aninhada, média (desvio) entre 5 partições externas
- Tabela 4.11 – Log loss interno por partição externa, seleção de colunas

# LISTA DE FIGURAS

- Figura 4.1 – Diagramas de confiabilidade no desenvolvimento
- Figura 4.2 – Diagramas de confiabilidade no conjunto de teste (n=200; 60 ruins)
- Figura 4.3 – Limiares da política em função da perda e do custo da análise manual

<!-- INÍCIO DO TEXTO -->

# 1 Introdução

<!-- rascunho; fonte: proposta (docs/proposta/), PLANO.md itens 1 a 4, 11 e 12, docs/plano-de-analise.md §1, docs/decisoes.md -->

## 1.1 Contexto

A automação de decisões é uma aplicação frequente de técnicas estatísticas e de inteligência artificial em sistemas de negócio. A concessão de crédito é o exemplo clássico: modelos de escore atribuem pesos a variáveis do solicitante, em geral por regressão logística, e a decisão de aprovar ou recusar resulta da comparação desse escore com um ponto de corte \cite{thomas2000,siddiqi2012}. A interpretabilidade e a facilidade de auditoria explicam a adoção dessa prática pela indústria \cite{thomas2000,siddiqi2012}. <!-- LACUNA: página em thomas2000/siddiqi2012 -->

Nesse arranjo, duas tarefas de natureza distinta ficam fundidas em uma única regra. A primeira é estimar o risco do caso, isto é, a probabilidade de um desfecho desfavorável dada a evidência observada. A segunda é escolher uma ação diante dessa estimativa, o que depende dos custos e benefícios de cada combinação de ação e desfecho. Quando o ponto de corte é fixado sem referência explícita a esses custos, o critério que de fato governa a recomendação permanece implícito, e a sensibilidade da decisão a mudanças nos critérios de negócio não pode ser examinada [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §1 e §1.1].

As redes bayesianas são modelos gráficos probabilísticos que representam dependências condicionais entre variáveis e permitem inferência sob incerteza \cite{pearl1988}. São, portanto, adequadas à primeira tarefa. Uma probabilidade estimada, contudo, não é por si só uma ação recomendada: a passagem do risco à ação exige uma camada de decisão separada, fundamentada na utilidade esperada [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §1]. Este trabalho investiga essa separação em um estudo de caso de crédito, organizando o sistema em uma camada probabilística, que estima a probabilidade de um crédito ser ruim, e uma camada de decisão, que escolhe a ação de maior utilidade esperada [fonte: PLANO.md §2]. Os conceitos envolvidos são apresentados no Capítulo 2.

<!-- LACUNA: fonte para a afirmação de que a regra de limiar sobre o escore mistura estimativa de risco e escolha de ação sem explicitar a função de utilidade (a proposta afirma isso sem citar; ver se thomas2000 ou siddiqi2012 sustentam no original, com página) -->

## 1.2 Pergunta de pesquisa

A pergunta que orienta o trabalho é a seguinte [fonte: PLANO.md §1; docs/plano-de-analise.md §1]:

> Uma política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) tem (1) limiares explícitos, que qualquer pessoa reproduz a partir da matriz de utilidade e de `p`, e (2) que efeito medido sobre as ações e a utilidade média, em comparação com um limiar fixo de 0,5?

As duas partes têm naturezas distintas. A parte 1 é uma propriedade da política: vale para qualquer escore e não depende de resultado experimental. A parte 2 é o que o experimento mede [fonte: docs/plano-de-analise.md §1]. A pergunta e o modo de ler cada desfecho da análise primária foram fixados antes de existir qualquer resultado [fonte: docs/plano-de-analise.md, abertura e §1 a §8]. Existe também um estudo de seleção secundário, desenhado depois de ver as métricas do desenvolvimento, cujo viés é declarado [fonte: docs/decisoes.md, Estudo de seleção; monografia/cap3-metodos.md §3.10].

## 1.3 Objetivos

O objetivo geral é construir e avaliar uma política de decisão que separa a estimativa do risco de crédito, feita por uma rede bayesiana, da escolha da ação, feita pela maximização da utilidade esperada, e comparar essa política com uma regra de limiar fixo [fonte: PLANO.md §1 e §2].

Os objetivos específicos são [fonte: PLANO.md §2; docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §1.2]:

1. estimar a probabilidade de um crédito ser ruim com redes bayesianas de duas estruturas, Naive Bayes e TAN, na base South German Credit [fonte: PLANO.md §4 e §5];
2. comparar a qualidade preditiva dessas redes com a de uma regressão logística de referência, medindo discriminação e erro de calibração [fonte: PLANO.md §2 e §5];
3. definir um conjunto ilustrativo de ações admissíveis e uma matriz de utilidade documentada, e escolher para cada caso a ação de maior utilidade esperada [fonte: PLANO.md §2 e §5];
4. explicitar os limiares de decisão que decorrem da matriz de utilidade [fonte: docs/plano-de-analise.md §1];
5. medir o efeito da política sobre as ações escolhidas e a utilidade média, em comparação com o limiar fixo de 0,5 [fonte: PLANO.md §1];
6. analisar a sensibilidade da política aos valores de custo adotados [fonte: PLANO.md §2];
7. demonstrar o fluxo completo para um caso, do risco estimado à utilidade de cada ação, em um script de terminal [fonte: PLANO.md §3].

A avaliação do modelo de risco é feita separadamente da avaliação da política de decisão, como previsto na proposta [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §1.2]. Como a base não registra o resultado das ações não tomadas, a camada de decisão é avaliada como simulação metodológica, e não como validação de uma política real de concessão [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §1]. O protocolo experimental é descrito no Capítulo 3.

## 1.4 O que o trabalho não faz

O trabalho é um experimento composto por scripts que leem arquivos de dados e gravam tabelas e figuras [fonte: PLANO.md §3]. Não entrega produto, painel web, servidor, banco de dados nem modelo de linguagem [fonte: PLANO.md §2]. A matriz de utilidade é demonstrativa: não representa a política de nenhuma instituição, e o trabalho não usa dados nem sistemas proprietários [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §1 e §1.1; PLANO.md §5].

O trabalho também não propõe uma regra de outro tipo que o limiar: como a utilidade esperada de cada ação é uma reta em `p`, a política equivale a uma regra de limiares sobre `p`, e a contribuição é derivar esses limiares dos custos de forma explícita [fonte: PLANO.md §5; docs/decisoes.md, P8]. A parte 1 da pergunta vale para qualquer escore e não distingue a rede da regressão logística [fonte: PLANO.md §5]. Os resultados não se generalizam a outras bases nem validam uma política real de concessão [fonte: PLANO.md §5; docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §1].

## 1.5 Mudanças em relação à proposta

Dez pontos mudaram em relação à proposta submetida. Cada um é listado com o motivo registrado na documentação do projeto [fonte: PLANO.md §11.4; docs/decisoes.md].

**Base de dados.** A proposta previa a German Credit Data; o trabalho usa a South German Credit, que é a versão corrigida da base citada na proposta \cite{gromping2019} [fonte: PLANO.md §4 e §11.4]. O protocolo de validação, que a proposta deixava em aberto, ficou fixado no Capítulo 3 [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §3, etapa A; monografia/cap3-metodos.md §3.2].

<!-- LACUNA: motivo da troca de base além de "versão corrigida" não está registrado em docs/decisoes.md; conferir em gromping2019 o que foi corrigido, com página -->

**Protótipo.** O protótipo previsto na proposta, que mostraria evidência, risco estimado, ação recomendada e justificativa, passou a ser uma demonstração em terminal, que recebe um caso e mostra o risco estimado e a utilidade de cada ação [fonte: PLANO.md §3 e §11.4]. A justificativa textual da recomendação ficou de fora: a demonstração mostra a conta (risco, utilidade de cada ação e fronteiras), e não uma explicação em texto [fonte: docs/decisoes.md, P15]. Uma interface de uma tela foi deixada para depois do experimento pronto [fonte: PLANO.md §12; docs/decisoes.md].

<!-- LACUNA: motivo da troca do protótipo por demonstração em terminal não está registrado em docs/decisoes.md -->

**Calibração.** A proposta previa calibrar as probabilidades; o trabalho apenas mede o erro de calibração, sem aplicar correção [fonte: PLANO.md §5; docs/decisoes.md, D4 e P1]. O motivo registrado é que corrigir exigiria escolher o método depois de ver as métricas do desenvolvimento, o que fere a pré-especificação da análise [fonte: docs/decisoes.md, D4 e P1]. A exigência de probabilidade calibrada para a decisão por custos vem da literatura, e não do experimento [fonte: docs/decisoes.md, P2]; ela é discutida no Capítulo 2.

**Pergunta de pesquisa.** A proposta perguntava se a política baseada em probabilidades calibradas e utilidade esperada produz decisões mais consistentes e transparentes que a política por escore e limiar; "consistentes" aparece na etapa A e "transparentes", no Resumo [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx, Resumo e §3, etapa A]. A pergunta foi reformulada nas duas partes da Seção 1.2 [fonte: docs/decisoes.md, P3]. O motivo registrado é que "consistentes" e "transparentes" não eram medidos; uma redação intermediária, "mais auditáveis", foi descartada porque contradizia a proposta, que chama regras e escores de auditáveis, valia por construção para qualquer escore e deixava a rede sem papel [fonte: docs/decisoes.md, P3]. A forma em duas partes separa a propriedade da política do efeito medido, e a troca de "calibrada" por "com calibração medida" acompanha a mudança anterior [fonte: docs/decisoes.md, P1 e P3].

**Análise exploratória.** A análise exploratória prevista na proposta limita-se a uma tabela de descrição da base, apresentada no Capítulo 3, porque o plano fixa sete scripts e uma análise em código seria exceção [fonte: docs/decisoes.md, P12].

**Conjunto de ações.** A proposta citava quatro ações (aprovar, pedir informação ou garantia, encaminhar para análise manual e rejeitar); o trabalho usa três: aprovar, rejeitar e análise manual [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §3, etapa D; docs/decisoes.md §4]. <!-- LACUNA: motivo não registrado -->

**Estrutura da rede.** A proposta previa comparar uma estrutura guiada por conhecimento do domínio com outra aprendida dos dados por BIC ou BDeu; o trabalho usa Naive Bayes e TAN, sem estrutura de domínio, e deixa a busca por *hill climbing* como opcional [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §3, etapa C; PLANO.md §5]. O motivo registrado para as duas estruturas é que o Naive Bayes é a referência simples e o TAN permite dependência entre variáveis [fonte: docs/decisoes.md, escolhas de 14/11/2026]. <!-- LACUNA: motivo não registrado para abandonar a estrutura de domínio -->

**Linha de base.** A proposta previa a regressão logística com probabilidades calibradas; no trabalho ela não é calibrada, e só se mede o seu erro de calibração [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §3, etapa C; PLANO.md §5]. <!-- LACUNA: motivo não registrado para a logística especificamente (D4 e P1 tratam da calibração em geral) -->

**Diagramas de influência e explicação da evidência.** A revisão sobre diagramas de influência e, na etapa F, o uso de Streamlit e a apresentação da evidência mais relevante e da mudança em relação à probabilidade a priori não entram no trabalho [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §1.2 e §3, etapa F; docs/decisoes.md, P15]. <!-- LACUNA: motivo não registrado; o autor deve decidir se a revisão de diagramas de influência entra no Capítulo 2 -->

**Estudo de seleção.** Foi acrescentado um estudo secundário de seleção aninhada de estrutura e de prior, que não estava na proposta; a análise primária não muda [fonte: docs/decisoes.md, Estudo de seleção, Q1]. O motivo registrado é preservar a comparação pré-definida e ainda testar a hipótese levantada no desenvolvimento [fonte: docs/decisoes.md, Estudo de seleção, Q1].

## 1.6 Organização do texto

O Capítulo 2 apresenta a fundamentação: redes bayesianas, calibração, utilidade esperada, limiares derivados de custos e escore de crédito. O Capítulo 3 descreve a base de dados, o protocolo de validação, os modelos, as métricas e a política de decisão. O Capítulo 4 relata os resultados preditivos, os da política de decisão e os da análise de sensibilidade. O Capítulo 5 discute os resultados e as limitações do trabalho. O Capítulo 6 conclui, respondendo às duas partes da pergunta de pesquisa [fonte: monografia/esqueleto.md]. Entre esses temas estão a opção de rejeição (Seção 2.8), a evidência incompleta (Seção 4.2), a demonstração de um caso (Seções 3.9 e 4.5) e o estudo de seleção secundário (Seções 3.10 e 4.6) [fonte: monografia/esqueleto.md; monografia/cap3-metodos.md].

# 2 FUNDAMENTAÇÃO

<!-- rascunho das seções 2.1 a 2.5; a teoria fica aqui, o que foi feito fica no cap. 3 -->

## 2.1 Redes bayesianas

Raciocinar sob incerteza exige representar crenças sobre muitas variáveis ao mesmo tempo e atualizá-las quando algumas delas são observadas. A teoria das probabilidades oferece o arcabouço para isso, mas a especificação direta de uma distribuição conjunta sobre dezenas de variáveis é inviável tanto em armazenamento quanto em estimação; as redes bayesianas foram propostas como forma de explorar a estrutura de independências do problema para tornar essa representação compacta \cite{pearl1988, russell2010}. <!-- confirmar: capítulo introdutório em pearl1988 -->

Uma rede bayesiana é um modelo probabilístico composto por duas partes: um grafo acíclico dirigido, cujos nós são variáveis aleatórias, e um conjunto de distribuições de probabilidade condicional, uma para cada nó, dada a configuração de seus pais no grafo \cite{pearl1988, koller2009}. <!-- confirmar: capítulo de representação em koller2009 --> Quando as variáveis são discretas, cada distribuição condicional é representada por uma tabela de probabilidade condicional, com uma linha para cada combinação de valores dos pais \cite{russell2010}. <!-- confirmar: capítulo de raciocínio probabilístico em russell2010 -->

A propriedade central do modelo é que a distribuição conjunta de todas as variáveis se escreve como o produto das distribuições locais. Para variáveis $X_1, \dots, X_n$, sendo $\mathrm{Pa}(X_i)$ o conjunto de pais de $X_i$ no grafo,

$$P(X_1, \dots, X_n) = \prod_{i=1}^{n} P\big(X_i \mid \mathrm{Pa}(X_i)\big).$$

Essa fatoração permite especificar a conjunta com muito menos parâmetros do que uma tabela completa, cujo tamanho cresce exponencialmente com o número de variáveis \cite{koller2009, russell2010}. <!-- confirmar: página da fatoração em koller2009 --> Com $n$ variáveis binárias, a tabela conjunta completa tem $2^n - 1$ parâmetros livres, ao passo que, em uma rede na qual cada nó tem no máximo $k$ pais, o número de parâmetros cresce apenas linearmente em $n$, da ordem de $n \cdot 2^k$ \cite{russell2010}. <!-- confirmar: página do exemplo de contagem de parâmetros em russell2010 -->

O grafo também codifica relações de independência condicional. Em particular, cada variável é condicionalmente independente de seus não descendentes, dados os seus pais \cite{koller2009}; o critério de separação dirigida (*d-separation*) permite ler do grafo outras independências implicadas pela estrutura \cite{pearl1988, koller2009}. <!-- confirmar: seção de d-separação em koller2009 e capítulo correspondente em pearl1988 --> É essa leitura que torna o modelo interpretável: as arestas indicam quais variáveis entram diretamente no cálculo da probabilidade de cada outra.

Construir uma rede envolve duas tarefas distintas: definir a estrutura do grafo e estimar os parâmetros das tabelas. A estrutura pode vir do conhecimento de especialistas, ser aprendida dos dados ou ser fixada por uma família de modelos, como acontece nos classificadores da seção 2.2 \cite{koller2009}. <!-- confirmar: capítulo de aprendizado de estrutura em koller2009 --> Uma vez definida a rede, ela responde a consultas sobre qualquer variável dada qualquer subconjunto das demais, o que a distingue de modelos que apenas mapeiam um vetor fixo de entradas em uma saída \cite{russell2010, jensen2007}. <!-- confirmar: capítulo de redes bayesianas em jensen2007 -->

## 2.2 Naive Bayes e TAN

Em classificação, uma rede bayesiana pode ser usada para estimar a probabilidade a posteriori de uma variável de classe $C$ dados os atributos $A_1, \dots, A_n$. O classificador Naive Bayes é a rede mais simples com esse fim: a classe é o único pai de todos os atributos, e os atributos são supostos condicionalmente independentes entre si dada a classe \cite{friedman1997}. <!-- LACUNA: referência a conferir no original --> Pela regra de Bayes, a posteriori fica

$$P(C \mid A_1, \dots, A_n) \propto P(C) \prod_{i=1}^{n} P(A_i \mid C).$$

A suposição de independência raramente vale em dados reais, mas o classificador costuma ter desempenho competitivo, e a estrutura fixa dispensa o aprendizado do grafo \cite{friedman1997}. <!-- LACUNA: referência a conferir no original -->

O classificador TAN (*Tree-Augmented Naive Bayes*) relaxa essa suposição: além da aresta que parte da classe, cada atributo pode ter no máximo um outro atributo como pai, de modo que as arestas entre atributos formam uma árvore \cite{friedman1997}. <!-- LACUNA: referência a conferir no original --> A árvore é escolhida por uma adaptação do método de Chow e Liu \cite{chowliu1968}, <!-- LACUNA: referência a conferir no original --> que aproxima uma distribuição conjunta pela árvore de dependência de máxima verossimilhança, obtida como a árvore geradora de peso máximo cujos pesos são as informações mútuas entre pares de variáveis. No TAN, o peso de cada par de atributos é a informação mútua condicional à classe \cite{friedman1997}: <!-- LACUNA: referência a conferir no original -->

$$I(A_i; A_j \mid C) = \sum_{a_i, a_j, c} P(a_i, a_j, c) \log \frac{P(a_i, a_j \mid c)}{P(a_i \mid c)\, P(a_j \mid c)}.$$

Escolhida uma raiz, as arestas da árvore são orientadas a partir dela, e a classe é acrescentada como pai de todos os atributos \cite{friedman1997}. <!-- LACUNA: referência a conferir no original --> O TAN mantém, portanto, a estrutura do Naive Bayes e acrescenta uma única dependência por atributo, o que limita o número de parâmetros de cada tabela.

Os dois classificadores ocupam pontos diferentes de um mesmo compromisso. O Naive Bayes tem menos parâmetros, e por isso suas tabelas são estimadas com mais exemplos por célula, ao custo de ignorar correlações entre atributos; o TAN capta parte dessas correlações, mas cada tabela passa a ter uma configuração de pais a mais e, portanto, menos exemplos por célula \cite{friedman1997}. <!-- LACUNA: referência a conferir no original --> Em ambos os casos a estrutura é restrita o bastante para ser lida diretamente: cada atributo depende da classe e, no TAN, de no máximo um outro atributo.

## 2.3 Aprendizado de parâmetros e prior BDeu

Sob as hipóteses usuais de que os exemplos de treino são independentes e identicamente distribuídos, de que não há valores ausentes e de que os parâmetros de tabelas diferentes são independentes a priori, a verossimilhança de uma rede bayesiana se decompõe em um termo por nó e por configuração dos pais, e cada tabela pode ser estimada separadamente \cite{koller2009, heckerman1995}. <!-- confirmar: página da decomposição da verossimilhança em koller2009 --> <!-- LACUNA: referência a conferir no original (heckerman1995) -->

Dada a estrutura, os parâmetros de uma rede bayesiana discreta são as entradas das tabelas de probabilidade condicional. Seja $\theta_{ijk} = P(X_i = k \mid \mathrm{Pa}(X_i) = j)$ e $N_{ijk}$ o número de exemplos de treino em que $X_i = k$ e os pais assumem a configuração $j$, com $N_{ij} = \sum_k N_{ijk}$. A estimativa de máxima verossimilhança é a frequência relativa $N_{ijk}/N_{ij}$ \cite{koller2009}. <!-- confirmar: capítulo de estimação de parâmetros em koller2009 --> Quando uma configuração dos pais aparece poucas vezes, ou nenhuma, essa estimativa é instável ou indefinida e pode atribuir probabilidade zero a eventos possíveis \cite{koller2009}. <!-- confirmar: página em koller2009 -->

A estimação bayesiana trata esse problema com uma distribuição a priori sobre os parâmetros. Para variáveis multinomiais, a escolha usual é a distribuição de Dirichlet, que é conjugada: com hiperparâmetros $\alpha_{ijk}$ e $\alpha_{ij} = \sum_k \alpha_{ijk}$, a posteriori também é Dirichlet, e sua média é

$$\hat{\theta}_{ijk} = \frac{N_{ijk} + \alpha_{ijk}}{N_{ij} + \alpha_{ij}}$$

\cite{koller2009, heckerman1995}. <!-- confirmar: página da posteriori Dirichlet em koller2009 --> <!-- LACUNA: referência a conferir no original --> Os hiperparâmetros funcionam como contagens imaginárias somadas às observadas, e seu total mede quanto peso a priori recebe diante dos dados \cite{koller2009}. <!-- confirmar: página em koller2009 -->

O prior BDeu (*Bayesian Dirichlet equivalent uniform*) fixa um único número, o tamanho amostral equivalente $N'$, e o distribui de modo uniforme: $\alpha_{ijk} = N' / (r_i q_i)$, em que $r_i$ é o número de valores de $X_i$ e $q_i$ o número de configurações de seus pais \cite{heckerman1995}. <!-- LACUNA: referência a conferir no original --> Com isso, a força total do prior é a mesma em todos os nós, e as tabelas com muitas configurações de pais recebem pseudocontagens menores por célula \cite{heckerman1995, koller2009}. <!-- LACUNA: referência a conferir no original --> <!-- confirmar: página do BDe/BDeu em koller2009 --> Outro caso particular do prior de Dirichlet, distinto do BDeu, é o estimador de Laplace, que soma uma unidade a cada célula, isto é, $\alpha_{ijk} = 1$; ele faz a força total do prior crescer com o tamanho da tabela \cite{koller2009}. <!-- confirmar: página em koller2009 --> O efeito prático do BDeu é suavizar as estimativas em direção à distribuição uniforme, sobretudo nas células de contagem pequena. Quanto maior $N'$, mais forte essa suavização; quando as contagens crescem, o peso relativo do prior diminui e a estimativa se aproxima da frequência relativa \cite{koller2009}. <!-- confirmar: página em koller2009 --> O nome "equivalente" vem da propriedade de atribuir o mesmo escore a estruturas que representam as mesmas independências, o que motivou sua proposta no contexto do aprendizado de estrutura \cite{heckerman1995}. <!-- LACUNA: referência a conferir no original -->

## 2.4 Inferência exata

Inferência, em uma rede bayesiana, é o cálculo da distribuição de uma ou mais variáveis de consulta dada a evidência observada em outras, como $P(C \mid \mathbf{e})$. Em princípio, basta somar a distribuição conjunta sobre as variáveis que não são nem consulta nem evidência e normalizar o resultado \cite{russell2010, koller2009}. <!-- confirmar: capítulo de inferência exata em russell2010 e koller2009 --> Essa soma direta tem custo exponencial no número de variáveis, e a fatoração da seção 2.1 é o que permite fazê-la de forma mais eficiente.

O algoritmo de eliminação de variáveis explora essa fatoração: as somas são empurradas para dentro do produto, de modo que cada variável é eliminada somando apenas os fatores que a mencionam, e o resultado intermediário é guardado como um novo fator \cite{koller2009}. <!-- confirmar: capítulo de eliminação de variáveis em koller2009 --> O custo depende da ordem de eliminação e do tamanho dos maiores fatores criados; para grafos de largura de árvore pequena, como os do Naive Bayes (uma estrela) e do TAN (uma árvore sobre os atributos, com a classe como pai de todos), esses fatores ficam pequenos \cite{koller2009}. <!-- confirmar: página em koller2009 --> Para estruturas gerais, a inferência exata é NP-difícil \cite{koller2009}; <!-- confirmar: página do resultado de complexidade em koller2009 --> métodos como a propagação em árvore de junção organizam o mesmo cálculo para responder a muitas consultas \cite{jensen2007}. <!-- confirmar: capítulo de inferência em jensen2007 -->

No caso de classificação com evidência completa, o cálculo é particularmente simples. No Naive Bayes, a posteriori da classe é obtida multiplicando a priori da classe pelas probabilidades condicionais dos valores observados e normalizando, como na fórmula da seção 2.2; no TAN, o produto inclui, para cada atributo, a probabilidade condicional dado a classe e o atributo pai \cite{friedman1997}. <!-- LACUNA: referência a conferir no original --> Em ambos os casos não há variáveis a eliminar além da própria normalização.

Uma consequência útil é que a evidência pode ser parcial. Uma variável não observada é tratada como as demais variáveis não observadas, isto é, somada na marginalização, sem necessidade de imputar um valor \cite{koller2009, jensen2007}. <!-- confirmar: página em koller2009 e jensen2007 --> A posteriori resultante continua sendo uma distribuição de probabilidade coerente com o modelo, condicionada apenas ao que foi observado. Isso difere de modelos discriminativos que exigem um valor para cada entrada e, diante de uma entrada ausente, dependem de uma regra externa de preenchimento \cite{koller2009}. <!-- confirmar: página em koller2009 --> Além disso, a inferência é exata: dado o modelo, a probabilidade calculada é a que ele de fato implica, sem erro de aproximação numérica além do arredondamento.

## 2.5 Calibração

Um classificador probabilístico é dito calibrado quando, entre os casos aos quais atribui probabilidade $p$ a um evento, a frequência observada desse evento é aproximadamente $p$ \cite{guo2017, naeini2015}. <!-- confirmar: seção de definição em guo2017 --> Boa ordenação dos casos não garante calibração: um modelo pode separar bem as classes e, ainda assim, superestimar ou subestimar as probabilidades \cite{guo2017, niculescu2005}. <!-- LACUNA: referência a conferir no original (niculescu2005) --> A calibração importa quando a probabilidade é usada como número, por exemplo para calcular uma utilidade esperada, e não apenas para ordenar. Medidas de discriminação, como a área sob a curva ROC, dependem só da ordem das previsões e não mudam quando as probabilidades sofrem uma transformação estritamente crescente; por isso não detectam erros de calibração, que precisam de medidas próprias \cite{guo2017, naeini2015}. <!-- confirmar: página em guo2017 e naeini2015 -->

O escore de Brier mede o erro quadrático médio entre a probabilidade prevista $p_i$ e o desfecho observado $y_i \in \{0, 1\}$ \cite{brier1950}:

$$\mathrm{BS} = \frac{1}{N} \sum_{i=1}^{N} (p_i - y_i)^2.$$

Valores menores são melhores \cite{brier1950}. <!-- confirmar: página em brier1950 --> O erro esperado de calibração (ECE) mede só a calibração: as previsões são agrupadas em $M$ faixas de probabilidade $B_1, \dots, B_M$, e compara-se, em cada faixa, a frequência observada do evento $\mathrm{freq}(B_m)$ com a probabilidade média prevista para ele $\mathrm{conf}(B_m)$, ponderando pelo número de casos \cite{naeini2015, guo2017}:

$$\mathrm{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{N} \, \big| \mathrm{freq}(B_m) - \mathrm{conf}(B_m) \big|.$$

<!-- confirmar: forma exata da fórmula em naeini2015 e guo2017 --> Há variantes: na forma usada por Guo et al. \cite{guo2017}, $p$ é a confiança da classe predita, e o evento é o acerto da previsão; em problemas binários também se usa a probabilidade de uma classe fixa e a frequência dessa classe \cite{naeini2015, guo2017}. <!-- confirmar: forma exata da fórmula em naeini2015 e guo2017 --> A variante e o número de faixas usados neste trabalho estão definidos no capítulo 3. A mesma comparação aparece no diagrama de confiabilidade, que plota a frequência observada contra a probabilidade média de cada faixa; nele, um modelo perfeitamente calibrado fica sobre a diagonal \cite{guo2017}. <!-- confirmar: seção do diagrama em guo2017 -->

A literatura propõe métodos para recalibrar as probabilidades de um modelo já treinado, usando dados não vistos no treino. O escalonamento de Platt ajusta uma função sigmoide sobre a saída do modelo, isto é, uma regressão logística com uma única entrada \cite{platt1999}. <!-- confirmar: seção de método e páginas em platt1999 --> A regressão isotônica ajusta uma função monótona não decrescente, por partes constantes, sem supor forma paramétrica, e por isso tende a exigir mais dados para não sobreajustar \cite{zadrozny2002, niculescu2005}. <!-- LACUNA: referência a conferir no original --> O capítulo 3 diz o que este trabalho faz com a calibração. Ambos os métodos exigem um conjunto de dados separado do treino para ajustar a função de recalibração, sob pena de reproduzir o viés do próprio ajuste \cite{platt1999, zadrozny2002}. <!-- confirmar: seção de método em platt1999 --> <!-- LACUNA: referência a conferir no original (zadrozny2002) --> Para classificadores Naive Bayes, a literatura relata probabilidades frequentemente empurradas para os extremos, efeito atribuído à suposição de independência entre atributos \cite{zadrozny2001, niculescu2005}. <!-- confirmar: página em zadrozny2001 --> <!-- LACUNA: referência a conferir no original (niculescu2005) -->

<!-- refs usadas: pearl1988, koller2009, russell2010, friedman1997, chowliu1968, heckerman1995, jensen2007, zadrozny2001, brier1950, naeini2015, guo2017, platt1999, zadrozny2002, niculescu2005 -->

<!-- rascunho: as seções 2.1 a 2.5 estão em outro arquivo. A matriz concreta, o valor de c e as regras de desempate ficam na seção 3.7. -->

## 2.6 Utilidade esperada

A teoria da decisão separa duas perguntas que um classificador costuma misturar: o que se acredita sobre o estado do mundo e o que se deve fazer diante dessa crença. A crença é representada por uma distribuição de probabilidade sobre os estados possíveis $y$; as preferências do decisor, por uma função de utilidade $U(a,y)$, que atribui um valor numérico à consequência de tomar a ação $a$ quando o estado verdadeiro é $y$ \cite{russell2010}. <!-- confirmar: capítulo de decisões simples em russell2010 --> Combinadas, as duas definem a utilidade esperada de cada ação,

$$EU(a) = \sum_{y} P(y)\,U(a,y),$$

e o princípio da máxima utilidade esperada recomenda a ação $a^{*} = \arg\max_a EU(a)$ \cite{russell2010,koller2009}. <!-- confirmar: capítulo de decisão em koller2009 --> A justificativa clássica do princípio é axiomática: um decisor cujas preferências entre loterias satisfazem os axiomas da utilidade (ordenabilidade, transitividade, continuidade, substitutibilidade, monotonicidade e decomponibilidade) comporta-se como se maximizasse a utilidade esperada de alguma função $U$ \cite{russell2010}. <!-- confirmar: seção dos axiomas da utilidade em russell2010 -->

Quando os estados e as ações são finitos, a função de utilidade pode ser escrita como uma matriz, com uma linha por ação e uma coluna por estado. No problema de crédito considerado neste trabalho, o estado é a qualidade do cliente (bom ou ruim) e cada célula da matriz registra o ganho ou a perda associada a uma combinação de ação e estado. A matriz é a parte do modelo que expressa o negócio; a distribuição $P(y)$ é a parte que expressa o conhecimento estatístico. Trocar a matriz muda a decisão sem exigir novo treino do modelo de risco, e melhorar o modelo de risco muda a decisão sem exigir nova discussão sobre os valores \cite{koller2009}. <!-- confirmar: capítulo de decisão em koller2009 --> Uma utilidade expressa como custo leva às mesmas escolhas, bastando trocar a maximização da utilidade pela minimização do custo esperado.

O diagrama de influência estende a rede bayesiana para representar esse tipo de problema em um único grafo \cite{howard2005}. Além dos nós de chance, que são variáveis aleatórias como na rede bayesiana, o diagrama contém nós de decisão, cujos valores são escolhidos pelo decisor, e nós de utilidade, que dependem de nós de chance e de decisão e atribuem valor às consequências \cite{howard2005,jensen2007}. <!-- confirmar: capítulo de diagramas de influência em jensen2007 --> Os arcos que entram em um nó de decisão indicam a informação disponível no momento de decidir. Resolver o diagrama significa encontrar, para cada configuração dessa informação, a ação que maximiza a utilidade esperada, o que pode ser feito por algoritmos de inferência semelhantes aos usados em redes bayesianas \cite{jensen2007,koller2009}. No caso de uma única decisão tomada após observar todas as evidências, a solução reduz-se a calcular $P(y \mid \text{evidência})$ pela rede e aplicar o princípio da máxima utilidade esperada a esse resultado.

## 2.7 Limiares derivados dos custos

Em um problema com dois estados, a utilidade esperada de cada ação é uma função linear da probabilidade $p = P(\text{ruim} \mid x)$, pois $EU(a) = (1-p)\,U(a,\text{bom}) + p\,U(a,\text{ruim})$. A comparação entre duas ações reduz-se, portanto, à comparação de duas retas, que se cruzam em um único ponto. Disso decorre que a decisão de máxima utilidade esperada equivale a uma regra de limiar sobre $p$, e que o limiar é determinado pela matriz de custos, não escolhido livremente \cite{elkan2001}. <!-- confirmar: seção --> Para custos $C(a,y)$ de duas ações, aprovar e rejeitar, a ação rejeitar é ótima quando $p \geq p^{*}$, com

$$p^{*} = \frac{C(\text{rejeitar},\text{bom}) - C(\text{aprovar},\text{bom})}{\big[C(\text{rejeitar},\text{bom}) - C(\text{aprovar},\text{bom})\big] + \big[C(\text{aprovar},\text{ruim}) - C(\text{rejeitar},\text{ruim})\big]}$$

em que os dois termos entre colchetes são positivos quando cada erro custa mais que o acerto correspondente \cite{elkan2001}. Como exemplo genérico, seja $G > 0$ o ganho de aprovar um cliente bom, $L > 0$ a perda de aprovar um cliente ruim e utilidade nula para rejeitar. Em custos, $C(\text{aprovar},\text{bom}) = -G$, $C(\text{aprovar},\text{ruim}) = L$ e $C(\text{rejeitar},\cdot) = 0$, e a fórmula dá $p^{*} = G/(G+L)$. Do mesmo modo, $EU(\text{aprovar}) = (1-p)G - pL$ e $EU(\text{rejeitar}) = 0$, e a rejeição é ótima quando $p \geq G/(G+L)$. O limiar habitual de 0,5 corresponde apenas ao caso particular $G = L$.

Com três ações, as retas de utilidade esperada podem formar uma envoltória superior com dois cruzamentos relevantes, e a regra passa a ter dois pontos de corte, $0 \leq t_1 \leq t_2 \leq 1$: aprovar se $p < t_1$, encaminhar à ação intermediária se $t_1 \leq p \leq t_2$ e rejeitar se $p > t_2$. Retomando o exemplo, suponha-se uma terceira ação, a análise manual, que custa $c > 0$ e após a qual o caso é corretamente aprovado ou rejeitado. Sua utilidade esperada é $EU(\text{manual}) = (1-p)G - c$. A análise manual supera a aprovação quando $pL \geq c$, isto é, $p \geq c/L$, e supera a rejeição quando $p \leq 1 - c/G$. Os pontos de corte são, assim, $t_1 = c/L$ e $t_2 = 1 - c/G$, e a faixa intermediária só existe quando $c/L \leq 1 - c/G$, ou seja, quando $c \leq GL/(G+L)$; para custos maiores, a regra volta a ter um único limiar. Os valores adotados no experimento e os pontos de corte resultantes são apresentados na seção 3.7.

A equivalência entre utilidade esperada e limiar supõe que $p$ seja a probabilidade verdadeira do estado dado o caso, ou ao menos uma estimativa calibrada dela \cite{elkan2001,zadrozny2001}. Se o modelo produz escores que ordenam bem os casos, mas não correspondem a frequências, o limiar derivado da matriz é aplicado na escala errada, e a decisão deixa de ser a de máxima utilidade esperada, ainda que a ordenação seja boa \cite{zadrozny2001,niculescu2005}. <!-- confirmar: seções de motivação em zadrozny2001 e niculescu2005 --> Essa exigência de calibração vem da literatura e é adotada aqui como premissa: o trabalho mede a calibração das probabilidades (seção 2.5), mas não a demonstra experimentalmente como condição da regra. Com escores não calibrados, a alternativa usual é escolher o limiar empiricamente, o que reintroduz o ajuste que a derivação a partir dos custos pretende evitar.

## 2.8 Opção de rejeição

A ideia de admitir uma ação além das classes do problema remonta à opção de rejeição de Chow \cite{chow1970}. <!-- LACUNA: referência a conferir no original --> Na formulação original, um classificador pode recusar-se a decidir quando o caso é ambíguo, e o erro de classificação passa a ser trocado por uma taxa de rejeição. A regra ótima rejeita o caso quando a maior probabilidade a posteriori entre as classes fica abaixo de um limiar, e esse limiar é determinado pela razão entre o custo de rejeitar e o custo de errar \cite{chow1970}. <!-- confirmar: enunciado da regra ótima e forma do limiar em chow1970 --> Aumentar o limiar reduz o erro entre os casos aceitos, ao custo de mais rejeições, o que define uma curva de compromisso entre erro e rejeição \cite{chow1970}.

No contexto do crédito, a rejeição de Chow corresponde a encaminhar o caso a um analista, e não a recusar o crédito: a ação intermediária da seção 2.7 é análoga a uma opção de rejeição com custo. A analogia não é exata: em Chow, o custo de rejeitar é fixo, enquanto $EU(\text{manual}) = (1-p)G - c$ depende de $p$, porque o analista revela o estado verdadeiro e o caso bom ainda rende $G$. Em dois estados, a condição $\max\{p, 1-p\} < \tau$ define uma faixa em torno de $p = 0{,}5$, simétrica quando os erros têm o mesmo custo; com custos de erro diferentes, como no exemplo com $G \neq L$, a faixa desloca-se e torna-se assimétrica, com os pontos de corte $t_1$ e $t_2$ dados pela matriz. Em ambos os casos, a faixa intermediária reúne os casos em que nenhuma das ações automáticas tem utilidade esperada suficiente para compensar o custo do exame.

Duas consequências teóricas merecem registro. Primeiro, como na seção 2.7, a regra ótima de rejeição depende das probabilidades a posteriori, de modo que sua otimalidade também supõe probabilidades corretas \cite{chow1970}. Segundo, a vantagem de incluir a rejeição depende do que acontece depois dela: no exemplo da seção 2.7, supôs-se que o analista sempre acerta o estado, e essa hipótese torna a política com três ações pelo menos tão boa quanto a de duas ações para qualquer $p$, já que a terceira ação só é escolhida quando sua utilidade esperada é maior. Um analista que erra reduziria $EU(\text{manual})$ e estreitaria a faixa intermediária.

## 2.9 Escore de crédito e *next best action*

O escore de crédito é a prática consolidada de estimar, a partir de dados do solicitante e de seu histórico, a probabilidade de inadimplência ou de mau comportamento, e de usar essa estimativa para decidir sobre a concessão \cite{thomas2000,hand1997}. <!-- LACUNA: referência a conferir no original --> As revisões da área registram o uso de diversos métodos estatísticos e de aprendizado, como análise discriminante, regressão logística, árvores de classificação, vizinhos mais próximos e redes neurais, sem que um deles domine os demais de modo uniforme \cite{hand1997,thomas2000}. <!-- confirmar: seções de comparação de métodos em hand1997 e thomas2000 -->

Na indústria, a regressão logística ocupa posição de referência. O *scorecard* tradicional é, em geral, uma regressão logística sobre variáveis agrupadas em faixas, cujos coeficientes são convertidos em pontos aditivos por atributo, de modo que o escore final é uma soma legível e auditável \cite{siddiqi2012}. <!-- confirmar: capítulos de desenvolvimento e de escalonamento do scorecard em siddiqi2012 --> A preferência deve-se menos ao desempenho preditivo do que à interpretabilidade, à estabilidade e à facilidade de explicação a reguladores e a clientes \cite{siddiqi2012,thomas2000}. O papel dela no experimento é descrito no capítulo 3.

No *scorecard*, a decisão é tomada por pontos de corte sobre o escore, escolhidos a partir de considerações de negócio como taxa de aprovação, perda esperada e lucratividade \cite{siddiqi2012}. <!-- confirmar: capítulo de ponto de corte em siddiqi2012 --> É comum haver uma faixa intermediária de escores encaminhada à análise humana, o que corresponde, na linguagem da seção 2.8, a uma opção de rejeição \cite{siddiqi2012}. <!-- confirmar: menção à faixa de revisão manual em siddiqi2012 --> A diferença em relação à seção 2.7 está na origem dos cortes: na prática descrita, eles são definidos sobre a escala do escore e ajustados ao negócio; na abordagem por utilidade esperada, são derivados da matriz de utilidade e aplicados sobre uma probabilidade, o que exige que essa probabilidade seja calibrada.

Neste trabalho, entende-se por *next best action* (próxima melhor ação) a ação de maior utilidade esperada, conforme a seção 2.6, entre as ações aprovar, rejeitar e encaminhar para análise manual. Trata-se de definição própria, sem fonte citada. A formulação não acrescenta teoria ao que foi exposto nas seções 2.6 a 2.8; ela nomeia a combinação de um modelo de risco que fornece $P(y \mid x)$ com uma camada de decisão que escolhe a ação.

<!-- refs usadas: russell2010, koller2009, howard2005, jensen2007, elkan2001, zadrozny2001, niculescu2005, chow1970, thomas2000, hand1997, siddiqi2012 -->

# 3 MATERIAIS E MÉTODOS

<!-- Rascunho gerado por subagente em 17/11/2026, a revisar pelo autor. Não contém resultado de desempenho. -->
<!-- Entradas do .bib marcadas "% VERIFICAR" ou "A CONFERIR" só podem ser citadas depois de conferidas no original (PLANO.md §9). -->

Este capítulo descreve a base de dados, o protocolo de divisão e validação, os modelos de risco, as métricas, a camada de decisão por utilidade esperada, a análise de sensibilidade, o estudo secundário de seleção e os cuidados de reprodutibilidade. Todas as decisões de análise foram fixadas antes da observação de resultados no conjunto de teste, e a forma de leitura de cada desfecho foi registrada previamente em um plano de análise [fonte: docs/plano-de-analise.md §1–§5].

## 3.1 Base de dados

Utiliza-se a base South German Credit \cite{gromping2019}, versão corrigida da German Credit Data \cite{hofmann1994}, disponibilizada no repositório da UCI \cite{uci573}. A base contém 1000 registros, 20 variáveis preditoras e a variável-alvo `kredit`, com 300 casos classificados como ruins e 700 como bons [fonte: PLANO.md §4]. A codificação do alvo é invertida em relação ao usual: o valor 0 indica crédito ruim e o valor 1, crédito bom; a classe positiva adotada em todo o trabalho é a classe ruim, e toda probabilidade reportada refere-se à probabilidade de o caso ser ruim [fonte: PLANO.md §4; AGENTS.md, Convenções].

Das 20 variáveis preditoras, três são contínuas — duração do crédito (`laufzeit`), valor do crédito (`hoehe`) e idade (`alter`) — e as 17 restantes já são categóricas [fonte: PLANO.md §4]. Os nomes originais, em alemão, são mantidos no código; a tradução é usada apenas no texto [fonte: PLANO.md §4]. O identificador `record_id` é removido antes de qualquer etapa de modelagem [fonte: PLANO.md §4].

Tabela 3.1 — Dicionário das variáveis [fonte: docs/glossario.md §1]. Categorias: número de valores inteiros distintos observados no conjunto de desenvolvimento (n=800), calculado a partir de `dados/processados/dev.csv`; os códigos e seus significados seguem o codetable.txt da UCI (South German Credit (UPDATE), https://archive.ics.uci.edu/dataset/573/south+german+credit+update), traduzidos para o português.

| Variável | Tradução | Tipo | Categorias |
|---|---|---|---|
| `kredit` | Risco do crédito (alvo) | Binária | 2: 0 = ruim; 1 = bom |
| `laufzeit` | Duração do crédito (meses) | Contínua, 3 faixas por tercis | — |
| `hoehe` | Valor do crédito | Contínua, 3 faixas por tercis | — |
| `alter` | Idade | Contínua, 3 faixas por tercis | — |
| `laufkont` | Situação da conta corrente | Categórica | 4: 1 = sem conta; 2 = saldo < 0 DM; 3 = 0 a < 200 DM; 4 = >= 200 DM ou salário por pelo menos 1 ano |
| `verw` | Finalidade do crédito | Categórica | 10 observados (a fonte define 0 a 10): 0 = outros; 1 = carro novo; 2 = carro usado; 3 = móveis/equipamentos; 4 = rádio/televisão; 5 = eletrodomésticos; 6 = reformas; 7 = educação; 8 = férias; 9 = requalificação; 10 = negócios |
| `bishkred` | Número de créditos neste banco, incluindo o atual | Categórica | 4: 1 = 1; 2 = 2 a 3; 3 = 4 a 5; 4 = >= 6 |
| `telef` | Telefone fixo no nome do cliente | Categórica | 2: 1 = não; 2 = sim |
| `moral` | Histórico de crédito | Categórica | 5: 0 = atraso no pagamento no passado; 1 = conta crítica/outros créditos em outro lugar; 2 = nenhum crédito tomado/todos pagos em dia; 3 = créditos existentes pagos em dia até agora; 4 = todos os créditos neste banco pagos em dia |
| `sparkont` | Poupança | Categórica | 5: 1 = desconhecida/sem poupança; 2 = < 100 DM; 3 = 100 a < 500 DM; 4 = 500 a < 1000 DM; 5 = >= 1000 DM |
| `beszeit` | Tempo no emprego atual | Categórica | 5: 1 = desempregado; 2 = < 1 ano; 3 = 1 a < 4 anos; 4 = 4 a < 7 anos; 5 = >= 7 anos |
| `rate` | Parcela em relação à renda disponível | Categórica | 4: 1 = >= 35; 2 = 25 a < 35; 3 = 20 a < 25; 4 = < 20 (em %) |
| `famges` | Estado civil e sexo (`personal_status_sex`) | Categórica | 4: 1 = homem divorciado/separado; 2 = mulher não solteira ou homem solteiro; 3 = homem casado/viúvo; 4 = mulher solteira |
| `buerge` | Outros devedores ou fiadores | Categórica | 3: 1 = nenhum; 2 = co-solicitante; 3 = fiador |
| `wohnzeit` | Tempo na residência atual | Categórica | 4: 1 = < 1 ano; 2 = 1 a < 4 anos; 3 = 4 a < 7 anos; 4 = >= 7 anos |
| `verm` | Bem mais valioso | Categórica | 4: 1 = desconhecido/sem bens; 2 = carro ou outro; 3 = poupança habitacional/seguro de vida; 4 = imóvel |
| `weitkred` | Outros planos de parcelamento | Categórica | 3: 1 = banco; 2 = lojas; 3 = nenhum |
| `wohn` | Tipo de moradia | Categórica | 3: 1 = sem pagar; 2 = aluguel; 3 = própria |
| `beruf` | Qualificação da ocupação | Categórica | 4: 1 = desempregado/não qualificado, não residente; 2 = não qualificado, residente; 3 = empregado qualificado/funcionário; 4 = gerente/autônomo/empregado altamente qualificado |
| `pers` | Pessoas dependentes (`people_liable`) | Categórica | 2: 1 = 3 ou mais; 2 = 0 a 2 |
| `gastarb` | Trabalhador estrangeiro | Categórica | 2: 1 = sim; 2 = não |

Traduções e códigos conferidos, variável a variável, no codetable.txt do conjunto South German Credit (UPDATE), UCI, https://archive.ics.uci.edu/dataset/573/south+german+credit+update. Na fonte, `verw` tem 11 códigos (0 a 10); 10 aparecem no conjunto de desenvolvimento.

A base apresenta categorias raras, por exemplo `bishkred` = 4 e `verw` = 8 [fonte: PLANO.md §4]. Essa característica motiva o uso de prior bayesiano na estimação dos parâmetros (Seção 3.5).

No conjunto de desenvolvimento (n=800), `bishkred` = 4 tem 5 casos e `verw` = 8 tem 7 casos; outras categorias pequenas são `verw` = 4 e `verw` = 10 (9 casos cada), `buerge` = 2 (35 casos) e `beruf` = 1 (16 casos). <!-- LACUNA: a contagem na base completa (n=1000) é do autor, a conferir no sgc.csv (docs/decisoes.md §4, P25). -->

### 3.1.1 Análise exploratória

A análise exploratória limita-se a uma tabela de descrição da base (contagens, categorias raras e as três variáveis contínuas), elaborada a partir do conjunto de desenvolvimento e do dicionário, sem script dedicado [fonte: docs/decisoes.md §4, P12].

Tabela 3.2 — Descrição do conjunto de desenvolvimento (n=800), calculada a partir de `dados/processados/dev.csv`.

| Item | Valor |
|---|---|
| Linhas | 800 |
| Casos ruins (`kredit` = 0) | 240 (30,0%) |
| `laufzeit` (meses) | mínimo 4; cortes dos tercis 12 e 24; máximo 72 |
| `hoehe` | mínimo 250; cortes dos tercis 1553 e 3384; máximo 18424 |
| `alter` (anos) | mínimo 19; cortes dos tercis 28 e 38; máximo 75 |

Os tercis acima são calculados sobre todo o conjunto de desenvolvimento, apenas para descrição; no experimento os cortes são aprendidos só no treino de cada partição.

## 3.2 Divisão em desenvolvimento e teste

A base é dividida de forma estratificada, com semente 2026, em um conjunto de desenvolvimento (dev), com 800 casos (240 ruins), e um conjunto de teste, com 200 casos (60 ruins) [fonte: PLANO.md §4; docs/decisoes.md §1]. Uma divisão anterior, com semente 42, foi descartada porque seu conjunto de teste já havia sido usado para avaliar a regressão logística em trabalho anterior [fonte: docs/decisoes.md §1].

O conjunto de teste permanece fechado durante todo o desenvolvimento. Todos os modelos, inclusive o de referência, são avaliados nele uma única vez, pelo autor, após um commit de congelamento do código [fonte: PLANO.md §8, passo 10; docs/decisoes.md §1]. Os scripts de modelagem leem exclusivamente o conjunto de desenvolvimento [fonte: docs/decisoes.md §1, D11].

## 3.3 Validação cruzada

No conjunto de desenvolvimento, adota-se validação cruzada estratificada em 5 partições, com semente 2026 [fonte: PLANO.md §5; docs/decisoes.md §2]. Cada partição é usada uma vez como validação enquanto as outras quatro compõem o treino, de modo que cada caso recebe uma predição de um modelo que não o viu [fonte: docs/glossario.md §2]. As métricas de desenvolvimento são reportadas como média e desvio entre as 5 partições [fonte: docs/plano-de-analise.md §2].

O número de partições (5) foi escolhido por convenção, e não por desempenho [fonte: decisão do autor, 17/11/2026].

## 3.4 Discretização

As redes bayesianas utilizadas exigem variáveis discretas. As três variáveis contínuas são discretizadas em 3 faixas por tercis, com cortes aprendidos apenas no treino de cada partição, para evitar vazamento de informação da partição de validação \cite{kaufman2012} [fonte: PLANO.md §5; docs/decisoes.md §2]. Para o teste final, os cortes são aprendidos no conjunto de desenvolvimento inteiro e gravados em `resultados/cortes.json` [fonte: PLANO.md §7].

O número de faixas (3, por tercis) foi escolhido por convenção, e não por desempenho [fonte: decisão do autor, 17/11/2026].

## 3.5 Modelos de risco

São comparados três modelos que estimam a probabilidade de um crédito ser ruim [fonte: docs/decisoes.md §3]:

1. **Naive Bayes**, rede em que a variável-alvo é pai de cada preditora, tratadas como condicionalmente independentes dado o alvo \cite{friedman1997}; <!-- LACUNA: referência a conferir no original -->
2. **TAN** (Naive Bayes aumentado por árvore), que acrescenta ao Naive Bayes uma árvore de dependências entre as preditoras \cite{friedman1997,chowliu1968}. A árvore é a de máximo peso no grafo completo das preditoras, em que o peso de cada aresta é a informação mútua entre as duas preditoras condicional à classe, $I(X_i; X_j \mid C)$; a árvore é então orientada a partir de uma raiz, e a classe é acrescentada como pai de todas as preditoras \cite{friedman1997,chowliu1968}; <!-- LACUNA: referência a conferir no original -->
3. **Regressão logística**, como modelo de referência \cite{pedregosa2011}.

As redes são implementadas com a biblioteca `pgmpy`, na versão fixa 1.1.2 \cite{ankan2024} [fonte: PLANO.md §3; docs/decisoes.md §3; CITATION.cff do pgmpy]. O Naive Bayes é montado como rede em estrela, pois a classe específica da biblioteca falha no cálculo de probabilidades nessa versão [fonte: docs/decisoes.md §3]. A estrutura do TAN é aprendida em cada partição, e as arestas resultantes são registradas em `resultados/tan_arestas.csv` para descrever a estabilidade da estrutura entre partições [fonte: docs/decisoes.md §4, P16].


Os parâmetros das redes são estimados por estimação bayesiana com prior BDeu de tamanho equivalente 5 \cite{heckerman1995}, para evitar probabilidade zero em combinações raras [fonte: PLANO.md §5; docs/decisoes.md §2]. <!-- LACUNA: referência a conferir no original --> O prior BDeu é uma distribuição de Dirichlet uniforme sobre cada tabela de probabilidade condicional: o tamanho equivalente $N'$ é repartido igualmente entre as células, de modo que cada combinação de valor $x_i$ do nó e configuração $\mathrm{pa}_i$ dos pais recebe a pseudocontagem $N'/(r_i q_i)$, em que $r_i$ é o número de estados do nó e $q_i$ o número de configurações dos pais \cite{heckerman1995}. <!-- LACUNA: referência a conferir no original --> O espaço de estados de cada variável é fixado com todos os valores que aparecem no conjunto de desenvolvimento inteiro, para que uma categoria rara ausente do treino de uma partição não interrompa a inferência. Essa escolha não usa o rótulo, mas constitui um vazamento brando de informação, aqui declarado [fonte: docs/decisoes.md §4, P10; docs/plano-de-analise.md §6, item 6].

O tamanho equivalente 5 foi escolhido por convenção, e não por desempenho; outros valores só aparecem no estudo de seleção secundário [fonte: decisão do autor, 17/11/2026; docs/plano-de-analise.md §9].

A inferência é exata, por eliminação de variáveis, viável porque as redes são pequenas \cite{koller2009} [fonte: PLANO.md §5].

A regressão logística é configurada como `LogisticRegression(max_iter=1000)`, herdada do baseline anterior, e recebe as três variáveis contínuas em sua forma original, sem discretização [fonte: docs/decisoes.md §2; docs/decisoes.md §4, P6]. Em consequência, a diferença entre as redes e a regressão logística mistura modelo e representação das variáveis, e não é interpretada como efeito do modelo isoladamente [fonte: docs/decisoes.md §4, P6].

A calibração das probabilidades é apenas medida, sem aplicação de método de correção [fonte: PLANO.md §5; docs/decisoes.md §4, P1].

### 3.5.1 Evidência incompleta

Para avaliar o comportamento com evidência incompleta, cada variável é ocultada, uma por vez, no momento da predição, medindo-se a variação de ROC-AUC e de Brier [fonte: PLANO.md §5]. As redes marginalizam a variável ocultada; na regressão logística, ela é preenchida com a mediana do treino (para as 3 contínuas) ou com a moda do treino (para as 17 categóricas). Por isso, as quedas não são comparáveis entre as duas famílias de modelos [fonte: docs/decisoes.md §3, D2; docs/decisoes.md §4, P9].

## 3.6 Métricas

O desempenho dos modelos de risco é medido por ROC-AUC, PR-AUC, escore de Brier \cite{brier1950}, log loss e erro esperado de calibração (ECE) \cite{naeini2015}, acompanhados de diagrama de calibração [fonte: PLANO.md §6; docs/decisoes.md §4, P14]. A PR-AUC é incluída porque a classe positiva corresponde a 30% dos casos [fonte: docs/decisoes.md §4, P14]. Como referência, reporta-se também um preditor que atribui a todo caso a taxa base de ruins [fonte: docs/plano-de-analise.md §2].

O ECE é calculado com 10 faixas de mesma largura sobre P(ruim), comparando a probabilidade média prevista com a taxa observada de ruins em cada faixa. Essa definição difere da versão *top-label* usada no baseline anterior; os dois valores não são comparáveis, e apenas a definição atual é usada [fonte: docs/decisoes.md §2; docs/decisoes.md §4, P11].

Para $n$ casos com rótulo $y_k \in \{0, 1\}$ (1 = ruim) e probabilidade prevista $p_k$ de ruim, as duas métricas são

$$\text{log loss} = -\frac{1}{n}\sum_{k=1}^{n}\left[y_k \ln p_k + (1-y_k)\ln(1-p_k)\right],$$

$$\text{ECE} = \sum_{b=1}^{10}\frac{|B_b|}{n}\left|\bar{y}_b - \bar{p}_b\right|,$$

em que $B_b$ é o conjunto de casos cuja $p_k$ cai na faixa $b$, e $\bar{y}_b$ e $\bar{p}_b$ são a taxa observada de ruins e a probabilidade média prevista nessa faixa \cite{naeini2015} [fonte: docs/decisoes.md §2].

No conjunto de teste, ROC-AUC, PR-AUC, Brier e utilidade média recebem intervalo por bootstrap com 2000 reamostras, semente 2026 e percentis 2,5 e 97,5 \cite{efron1993} [fonte: docs/decisoes.md §4, P4; docs/plano-de-analise.md §3]. O intervalo não cobre a variação devida ao treino [fonte: docs/plano-de-analise.md §6, item 5].

Regras de leitura foram fixadas antes de qualquer resultado. Diferença de ROC-AUC menor que 0,03 entre dois modelos é tratada como ruído, sem apontar vencedor; Brier igual ou maior que o da taxa base é relatado como "não melhor que prever a taxa base" [fonte: docs/plano-de-analise.md §4; PLANO.md §6].

<!-- LACUNA: o autor ainda não confirmou se o limite de 0,03 vale também para PR-AUC, nem se 95% é o nível de leitura da diferença (docs/plano-de-analise.md §8). -->

## 3.7 Camada de decisão por utilidade esperada

A escolha da ação é separada da estimação do risco. Dado o risco estimado *p* de o caso ser ruim, a utilidade esperada de uma ação *a* é

$$UE(a) = (1 - p)\,U(a, \text{bom}) + p\,U(a, \text{ruim}),$$

e escolhe-se a ação de maior utilidade esperada \cite{russell2010,howard2005} [fonte: PLANO.md §5]. São consideradas três ações: aprovar, rejeitar e encaminhar para análise manual [fonte: docs/decisoes.md §4]. O custo esperado corresponde ao negativo da utilidade esperada [fonte: docs/decisoes.md §4, P14].

A matriz de utilidade é demonstrativa e lida de `config/utilidade.json` (Quadro 3.1) [fonte: config/utilidade.json; PLANO.md §5].

**Quadro 3.1 – Matriz de utilidade demonstrativa**

| Ação | Caso bom | Caso ruim |
|---|---|---|
| Aprovar | +100 | −400 |
| Rejeitar | 0 | 0 |
| Análise manual | 100 − *c* | −*c* |

Fonte: `config/utilidade.json`, com *c* = 40 [fonte: config/utilidade.json; PLANO.md §5].

As hipóteses da matriz são: valores demonstrativos, não calibrados com dados reais, e um analista que sempre acerta o estado do cliente [fonte: config/utilidade.json]. A matriz está pendente de aprovação do orientador [fonte: docs/decisoes.md §6].

<!-- LACUNA: aprovação da matriz (c = 40) pelo orientador ainda em aberto (PLANO.md §11, item 2). -->

Como a utilidade esperada de cada ação é linear em *p*, a política resultante equivale a uma regra de limiares sobre *p* \cite{elkan2001}. Com a matriz acima, a análise manual é escolhida quando *c*/400 ≤ *p* ≤ 1 − *c*/100; com *c* = 40, a faixa vai de 0,10 a 0,60, e com *c* > 80 a análise manual nunca é escolhida [fonte: PLANO.md §5]. Empates são resolvidos, com tolerância de 1e-9, pela prioridade análise manual, rejeitar, aprovar [fonte: docs/decisoes.md §4, D5]. A contribuição pretendida não é uma regra de tipo distinto do limiar, mas a derivação explícita dos limiares a partir dos custos, acompanhada da medição da calibração das probabilidades. A exigência de probabilidade calibrada é tomada da literatura, não demonstrada pelo experimento [fonte: PLANO.md §5; docs/decisoes.md §4, P2].

Estimativas de probabilidade bem calibradas são necessárias quando a decisão leva em conta custos \cite{zadrozny2001}.

### 3.7.1 Comparação de políticas

A política é calculada para os três modelos e comparada com um limiar fixo de 0,5 de duas ações [fonte: PLANO.md §5]. A comparação principal, fixada antes de qualquer métrica, usa o TAN; Naive Bayes e regressão logística são reportados em apêndice na mesma estrutura [fonte: docs/decisoes.md §4, P5; docs/plano-de-analise.md §3]. A tabela 2×2 é descrita como "política de três ações por utilidade esperada contra corte 0,5 de duas ações", sem linguagem causal, pois a diferença mistura modelo, representação e conjunto de ações [fonte: docs/decisoes.md §4, P8]. Com analista infalível, a política de três ações supera o corte de duas ações por construção, o que é declarado junto da tabela [fonte: docs/decisoes.md §4, P7].

São medidas a utilidade média, a distribuição das ações e o número de casos que mudam de ação entre as políticas [fonte: PLANO.md §6]. No teste, reporta-se também a diferença pareada de utilidade média entre a regra de utilidade e o limiar fixo, com intervalo por bootstrap [fonte: docs/decisoes.md §4; docs/plano-de-analise.md §3]. Para a regra de utilidade, registram-se ainda a segunda melhor ação e a diferença de utilidade esperada em relação a ela [fonte: docs/decisoes.md §4, P13].

## 3.8 Análise de sensibilidade

A sensibilidade da política aos custos é avaliada calculando-se as fronteiras de decisão em uma grade de perda por inadimplência em {200, 400, 600, 800} e custo da análise manual em {0, 5, …, 100} [fonte: PLANO.md §7; docs/decisoes.md §4, D7]. A análise mostra a ação recomendada em função do risco, da perda e do custo da análise manual [fonte: PLANO.md §6].

Os valores da grade da análise de sensibilidade foram escolhidos por convenção, e não por desempenho [fonte: decisão do autor, 17/11/2026; docs/decisoes.md §4, D7].

## 3.9 Demonstração

Um script de terminal recebe o identificador de um caso, treina novamente o modelo nas 4 partições que não contêm o caso e mostra o risco estimado, a utilidade esperada de cada ação, as fronteiras e a ação recomendada; o modelo padrão é o TAN [fonte: PLANO.md §7; docs/decisoes.md §4, D1, D8]. A demonstração mostra a conta, não uma justificativa textual da recomendação [fonte: docs/decisoes.md §4, P15].

## 3.10 Estudo de seleção aninhado (secundário)

Como análise secundária, pré-registrada em relação ao teste final e decidida por delegação, a rever pelo autor, realiza-se um estudo de seleção de configuração [fonte: docs/plano-de-analise.md §9; docs/decisoes.md, Estudo de seleção]. A análise primária, incluindo a tabela 2×2 com NB e TAN de BDeu 5, não muda [fonte: docs/plano-de-analise.md §9].

A grade é fechada, com 8 configurações: {Naive Bayes, TAN} × tamanho equivalente BDeu {1, 5, 10, 50} [fonte: docs/plano-de-analise.md §9]. Ficam fora da grade K2, outras faixas, seleção de variáveis, hill climbing, métodos de calibração e reponderação [fonte: docs/plano-de-analise.md §9].

Usa-se validação cruzada aninhada. As partições externas são as 5 já descritas; em cada uma, as 640 linhas de treino são divididas em 5 partições internas estratificadas, com semente 2026, nas quais cada configuração é treinada e avaliada [fonte: docs/plano-de-analise.md §9]. Escolhe-se a configuração de menor log loss médio nas partições internas, com empate (diferença menor que 1e-9) resolvido pela ordem da grade; a configuração escolhida prevê as 160 linhas da partição externa, gerando a linha "aninhado" [fonte: docs/plano-de-analise.md §9]. A escolha é também recalculada no conjunto de desenvolvimento inteiro, só para relato; essa configuração é a usada como modelo secundário no teste final [fonte: docs/plano-de-analise.md §9; docs/reproduzir.md §5].

Relatam-se obrigatoriamente as 8 configurações, o número de comparações (8) e a linha "aninhado", qualquer que seja o resultado. O texto não se refere a um "melhor modelo": informa qual configuração a regra escolheu e quanto ela difere da configuração de base [fonte: docs/plano-de-analise.md §9].

**Declaração de viés.** A grade foi definida depois da observação das métricas de desenvolvimento e motivada por elas (ver cap. 4). O aninhamento corrige o viés de escolher entre as 8 configurações, mas não o de ter desenhado a grade com base no mesmo conjunto de desenvolvimento [fonte: docs/plano-de-analise.md §9; docs/decisoes.md, Estudo de seleção].

## 3.11 Ambiente e reprodutibilidade

O experimento é composto por sete scripts Python que leem CSV e gravam tabelas e figuras, sem modelo salvo em arquivo [fonte: PLANO.md §3, §7; docs/arquitetura.md §2]. O projeto exige Python 3.12 ou superior [fonte: pyproject.toml, `requires-python`]. A execução local usou Python 3.12.13 (saída de `uv run python --version`); `uv.lock` e `pyproject.toml` fixam apenas `requires-python = ">=3.12"`, e não há `.python-version`. As bibliotecas são `pgmpy` 1.1.2, `scikit-learn` \cite{pedregosa2011}, `pandas` e `matplotlib`, com dependências travadas pelo gerenciador `uv` [fonte: PLANO.md §3]. Toda fonte de aleatoriedade usa a semente 2026, e duas execuções do mesmo comando geram arquivos CSV e JSON idênticos byte a byte [fonte: AGENTS.md, Reprodutibilidade; docs/reproduzir.md §2]. Os arquivos de resultado são versionados com o código, e a reprodução é conferida pela comparação com a versão commitada [fonte: docs/reproduzir.md §4]. As figuras PNG não são comparadas byte a byte [fonte: docs/reproduzir.md §4]. O passo a passo completo está no Apêndice A [fonte: docs/reproduzir.md].

<!-- LACUNA: hash do commit de congelamento, a anotar pelo autor no passo 10 (PLANO.md §8). -->

<!-- mapa de numeração (17/11/2026): Tabela 4.1→4.1; 4.2→4.2; 4.1b→4.3; 4.3→4.4; 4.4→4.5; 4.4b→4.6; 4.4c→4.7; 4.5→4.8; 4.6→4.9; 4.7→4.10; 4.8→4.11. Figura 4.1→4.1; 4.1b→4.2; 4.2→4.3. -->
# 4 RESULTADOS

Este capítulo relata os resultados obtidos até o momento. Os números das seções 4.1 a 4.7 são o baseline de desenvolvimento (validação cruzada estratificada em 5 partições sobre os 800 casos, capítulo 3, seções 3.2 e 3.3), salvo os blocos rotulados "conjunto de teste (n=200; 60 ruins)". O conjunto de teste final foi aberto uma única vez, em 17/11/2026, após o commit de congelamento 49d77ff. A numeração das tabelas e figuras é sequencial; os blocos do conjunto de teste são identificados pelo rótulo "conjunto de teste (n=200; 60 ruins)" na legenda. Os métodos não são repetidos aqui: cada seção remete à seção correspondente do capítulo 3. A leitura de cada resultado segue as regras pré-registradas na §4 do plano de análise (`docs/plano-de-analise.md`), e a interpretação fica para o capítulo 5.

Nas tabelas de métricas (4.1 e 4.10), os valores são médias e desvios entre as 5 partições. Cada número traz a indicação do arquivo e da coluna de origem, no formato [fonte: arquivo, coluna/linha]. A Tabela 4.3 traz o valor no conjunto de teste com intervalo de 95% por bootstrap. Valores arredondados a três casas, salvo indicação.

## 4.1 Desempenho preditivo

As métricas (seção 3.6) dos três modelos e da referência de taxa base estão na Tabela 4.1.

**Tabela 4.1** – Métricas por modelo no desenvolvimento, média (desvio) entre 5 partições [fonte: resultados/metricas_dev.csv, todas as colunas]

| modelo | roc_auc_media (desvio) | pr_auc_media (desvio) | brier_media (desvio) | log_loss_media (desvio) | ece_media (desvio) |
|---|---|---|---|---|---|
| nb | 0,789 (0,024) | 0,616 (0,049) | 0,171 (0,013) | 0,523 (0,035) | 0,093 (0,014) |
| tan | 0,742 (0,049) | 0,549 (0,076) | 0,200 (0,030) | 0,704 (0,136) | 0,152 (0,050) |
| logreg | 0,788 (0,021) | 0,649 (0,042) | 0,165 (0,012) | 0,504 (0,026) | 0,095 (0,031) |
| taxa_base | 0,500 (0,000) | 0,300 (0,000) | 0,210 (0,000) | 0,611 (0,000) | 0,000 (0,000) |

Aplicando as regras da §4 do plano de análise:

- **ROC-AUC, nb contra logreg.** A diferença é 0,001 (0,7890 contra 0,7880) [fonte: resultados/metricas_dev.csv, roc_auc_media, linhas nb e logreg], menor que 0,03. Pela regra pré-registrada, é tratada como ruído e nenhum dos dois modelos se distingue do outro por essa métrica.
- **ROC-AUC, nb e logreg contra tan.** As diferenças são 0,047 (nb − tan) e 0,046 (logreg − tan) [fonte: resultados/metricas_dev.csv, roc_auc_media, linhas nb, tan e logreg]. Ambas passam de 0,03, de modo que a regra de ruído não se aplica a esses pares. O plano não prevê outra regra para esse caso; registra-se ao lado que o desvio do tan entre partições é 0,049 [fonte: resultados/metricas_dev.csv, roc_auc_desvio, linha tan]. O TAN ficou abaixo do NB em todas as cinco métricas no desenvolvimento, e esse resultado é relatado como saiu.
- **Brier contra taxa base.** O Brier médio dos três modelos (nb 0,171; tan 0,200; logreg 0,165) é menor que o da taxa base, 0,210 [fonte: resultados/metricas_dev.csv, brier_media]. A condição "igual ou maior que 0,21" não ocorre; a frase "não melhor que prever a taxa base" não é acionada para nenhum modelo.
- **Calibração.** O erro de calibração esperado do tan, 0,152, é o maior dos três (nb 0,093; logreg 0,095) [fonte: resultados/metricas_dev.csv, ece_media]. Conforme a regra pré-registrada e a decisão P1, a calibração é apenas medida e relatada; não há correção. Os diagramas de confiabilidade dos três modelos estão em `resultados/calibracao_dev.png`.

**Figura 4.1** – Diagramas de confiabilidade no desenvolvimento (`resultados/calibracao_dev.png`).

**Arestas do TAN.** O plano determina que as arestas aprendidas pelo TAN em cada partição sejam relatadas nesta seção. A Tabela 4.2 resume o arquivo de arestas; em cada partição há 39 arestas, 20 das quais saem da classe `kredit`.

**Tabela 4.2** – Arestas do TAN por partição [fonte: resultados/tan_arestas.csv, colunas fold, origem, destino; contagens sobre as linhas, conforme docs/resultados-dev.md, §4]

| fold | arestas | origem = kredit | origem = verw | destino = verw |
|---|---|---|---|---|
| 0 | 39 | 20 | 9 | 1 |
| 1 | 39 | 20 | 8 | 1 |
| 2 | 39 | 20 | 8 | 1 |
| 3 | 39 | 20 | 7 | 2 |
| 4 | 39 | 20 | 8 | 1 |

Em todas as partições, `verw` (finalidade do crédito) é, fora `kredit`, a variável da qual sai o maior número de arestas (7 a 9) [fonte: resultados/tan_arestas.csv, coluna origem]. Registra-se, como **hipótese não testada**, que o fato de `verw` ser pai de muitas variáveis poderia produzir tabelas de probabilidade condicional esparsas e excesso de confiança, o que seria coerente com o log loss e o erro de calibração maiores do tan. Nenhuma análise deste trabalho testou essa hipótese: a contagem de arestas e as métricas apenas coexistem, e a observação não autoriza alterar modelo, faixa ou parâmetro.

**Conjunto de teste (n=200; 60 ruins).** O teste final foi rodado uma única vez, em 17/11/2026, sobre o commit de congelamento 49d77ff [fonte: resultados/predicoes_teste.csv, coluna kredit: 60 linhas com 0 e 140 com 1]. Os intervalos são de 95% por bootstrap. A Tabela 4.3 traz as métricas; a linha `sel` é a análise secundária da seção 4.6.

**Tabela 4.3** – Métricas por modelo no conjunto de teste (n=200; 60 ruins), valor [intervalo de 95%] [fonte: resultados/metricas_teste.csv, todas as colunas]

| modelo | roc_auc [ic_inf; ic_sup] | pr_auc [ic_inf; ic_sup] | brier [ic_inf; ic_sup] | log_loss | ece |
|---|---|---|---|---|---|
| nb | 0,728 [0,648; 0,802] | 0,490 [0,378; 0,630] | 0,199 [0,161; 0,239] | 0,627 | 0,115 |
| tan | 0,706 [0,623; 0,789] | 0,480 [0,372; 0,617] | 0,215 [0,173; 0,261] | 0,780 | 0,157 |
| logreg | 0,729 [0,651; 0,800] | 0,500 [0,383; 0,636] | 0,191 [0,157; 0,228] | 0,578 | 0,078 |
| taxa_base | 0,500 [0,500; 0,500] | 0,300 [0,235; 0,365] | 0,210 [0,184; 0,236] | 0,611 | 0,000 |
| sel (secundária) | 0,720 [0,641; 0,795] | 0,477 [0,365; 0,620] | 0,202 [0,164; 0,242] | 0,623 | 0,120 |

Aplicando as regras da §4 do plano de análise ao conjunto de teste:

- **ROC-AUC.** As diferenças entre os três modelos primários são 0,001 (logreg − nb: 0,7287 contra 0,7277), 0,021 (nb − tan: 0,7277 contra 0,7063) e 0,022 (logreg − tan: 0,7287 contra 0,7063) [fonte: resultados/metricas_teste.csv, roc_auc, linhas nb, tan e logreg]. As três são menores que 0,03 e, pela regra pré-registrada, tratadas como ruído: nenhum modelo se distingue dos outros por essa métrica no teste.
- **PR-AUC.** Os valores são 0,490 (nb), 0,480 (tan) e 0,500 (logreg), contra 0,300 da taxa base [fonte: resultados/metricas_teste.csv, pr_auc]. A §8 do plano deixa em aberto se o limite de 0,03 vale para PR-AUC; por isso, nenhuma regra é aplicada a essas diferenças e elas são apenas descritas.
- **Brier contra taxa base.** O Brier do tan no teste é 0,215, maior que o da taxa base, 0,210 [fonte: resultados/metricas_teste.csv, brier, linhas tan e taxa_base]. Pela regra pré-registrada, o tan é **não melhor que prever a taxa base** no conjunto de teste. O nb (0,199) e o logreg (0,191) ficam abaixo de 0,21, e a regra não é acionada para eles [fonte: resultados/metricas_teste.csv, brier].
- **Calibração.** O erro de calibração esperado é 0,115 (nb), 0,157 (tan) e 0,078 (logreg) [fonte: resultados/metricas_teste.csv, ece]. Conforme a decisão P1, é apenas relatado; não há correção. O log loss do tan, 0,780, do nb, 0,627, e do sel (secundária), 0,623, são maiores que o da taxa base, 0,611 [fonte: resultados/metricas_teste.csv, log_loss, linhas tan, nb, sel e taxa_base]. O plano não tem regra para log loss contra a taxa base, e o fato é apenas descrito.
- **Desenvolvimento e teste.** ROC-AUC e PR-AUC do teste são menores que as do desenvolvimento nos três modelos: ROC-AUC 0,728 contra 0,789 (nb), 0,706 contra 0,742 (tan) e 0,729 contra 0,788 (logreg); PR-AUC 0,490 contra 0,616 (nb), 0,480 contra 0,549 (tan) e 0,500 contra 0,649 (logreg) [fonte: resultados/metricas_teste.csv, roc_auc e pr_auc; resultados/metricas_dev.csv, roc_auc_media e pr_auc_media]. Brier e log loss do teste são maiores que os do desenvolvimento nos três modelos; a ECE é maior no teste para nb (0,115 contra 0,093) e tan (0,157 contra 0,152) e menor para logreg (0,078 contra 0,095) [fonte: resultados/metricas_teste.csv, brier, log_loss, ece; resultados/metricas_dev.csv, brier_media, log_loss_media, ece_media]. O plano não tem regra para essa comparação; o fato é descrito sem conclusão.

**Figura 4.2** – Diagramas de confiabilidade no conjunto de teste (n=200; 60 ruins) (`resultados/calibracao_teste.png`).

## 4.2 Evidência incompleta

O efeito de esconder uma variável por vez (seção 3.5.1) está em `resultados/evidencia_incompleta.csv`, com 60 linhas (3 modelos × 20 variáveis). A Tabela 4.4 traz, para cada modelo, as variáveis cuja ocultação produziu as maiores variações absolutas de ROC-AUC. A ressalva da decisão P9 acompanha toda a seção: as redes bayesianas marginalizam a variável ausente, enquanto a regressão logística a imputa; as duas operações não são equivalentes.

**Tabela 4.4** – Variação de métricas ao esconder uma variável, seleção de linhas [fonte: resultados/evidencia_incompleta.csv, colunas modelo, variavel_oculta, roc_auc, brier, delta_roc_auc, delta_brier]

| modelo | variavel_oculta | roc_auc | brier | delta_roc_auc | delta_brier |
|---|---|---|---|---|---|
| nb | laufkont | 0,741 | 0,183 | −0,048 | 0,012 |
| nb | moral | 0,777 | 0,175 | −0,012 | 0,004 |
| nb | sparkont | 0,783 | 0,174 | −0,006 | 0,003 |
| tan | laufkont | 0,692 | 0,216 | −0,050 | 0,016 |
| tan | verw | 0,768 | 0,183 | 0,025 | −0,018 |
| tan | laufzeit | 0,733 | 0,205 | −0,010 | 0,005 |
| logreg | laufkont | 0,742 | 0,198 | −0,046 | 0,033 |
| logreg | moral | 0,769 | 0,174 | −0,019 | 0,009 |
| logreg | hoehe | 0,773 | 0,168 | −0,015 | 0,003 |

Nos três modelos, a ocultação de `laufkont` (situação da conta corrente) é a que mais reduz a ROC-AUC: −0,048 (nb), −0,050 (tan) e −0,046 (logreg) [fonte: resultados/evidencia_incompleta.csv, delta_roc_auc, linhas laufkont]. No tan, esconder `verw` eleva a ROC-AUC em 0,025 e reduz o Brier em 0,018 [fonte: resultados/evidencia_incompleta.csv, delta_roc_auc e delta_brier, linha tan/verw]; o resultado é relatado como saiu, sem interpretação causal e sem que se proponha retirar a variável do modelo. A maior parte das demais variações tem valor absoluto inferior a 0,01 [fonte: resultados/evidencia_incompleta.csv, delta_roc_auc]. Nenhuma linha tem `delta_roc_auc` e `delta_brier` simultaneamente iguais a zero, de modo que a regra "esconder uma variável não muda nenhuma predição" da §4 não é acionada; a menor variação observada no nb é a de `hoehe` (delta_roc_auc 0,0001) [fonte: resultados/evidencia_incompleta.csv, linha nb/hoehe]. Essas diferenças não têm intervalo.

## 4.3 Política de decisão

A Tabela 4.5 compara a política de três ações por utilidade esperada (`ue`) contra o corte 0,5 de duas ações (`limiar`) (seções 3.7 e 3.7.1, decisão P8), com os valores de utilidade de `config/utilidade.json`. Contagens sobre os 800 casos do desenvolvimento.

**Tabela 4.5** – Política de três ações por utilidade esperada contra corte 0,5 de duas ações, desenvolvimento [fonte: resultados/resumo_politicas_dev.csv, todas as colunas]

| modelo | regra | utilidade_media | n_aprovar | n_rejeitar | n_analise_manual | n_mudam_vs_outra_regra |
|---|---|---|---|---|---|---|
| nb | ue | 32,625 | 274 | 171 | 355 | 355 |
| nb | limiar | 4,5 | 581 | 219 | 0 | 355 |
| tan | ue | 22,275 | 361 | 177 | 262 | 262 |
| tan | limiar | −3,125 | 590 | 210 | 0 | 262 |
| logreg | ue | 30,875 | 243 | 142 | 415 | 415 |
| logreg | limiar | 3,625 | 599 | 201 | 0 | 415 |

A utilidade média da regra `ue` é maior que a da regra `limiar` nos três modelos, com diferenças de 28,125 (nb), 25,4 (tan) e 27,25 (logreg) [fonte: resultados/resumo_politicas_dev.csv, utilidade_media]. Trata-se de diferença descritiva no desenvolvimento, sem intervalo: pelo plano, a comparação pareada com intervalo só é feita no teste final, e a diferença mistura modelo, representação e conjunto de ações, razão pela qual não é chamada de efeito da regra. Na regra `ue`, a análise manual recebe 355 (nb), 262 (tan) e 415 (logreg) dos 800 casos [fonte: resultados/resumo_politicas_dev.csv, n_analise_manual]; a regra `limiar` tem zero casos nessa ação por definição, por ter só duas ações. Essa ressalva acompanha qualquer leitura da diferença. As três ações aparecem na regra `ue` em todos os modelos, de modo que a regra "alguma ação não aparece numa política" não se aplica. O número de casos cuja ação muda entre as regras coincide, em cada modelo, com o número de casos em análise manual da regra `ue` [fonte: resultados/resumo_politicas_dev.csv, n_mudam_vs_outra_regra]. A ação de cada caso está em `resultados/politicas_dev.csv`.

**Conjunto de teste (n=200; 60 ruins).** A Tabela 4.6 traz as duas regras no teste, e a Tabela 4.7, a diferença pareada de utilidade média (`ue` − `limiar`) com intervalo de 95% por bootstrap (seção 3.7.1). Pela §3 do plano (decisão P5), a comparação principal é a do TAN; NB e regressão logística vão para o apêndice na mesma estrutura, e `sel` é análise secundária (seção 4.6).

**Tabela 4.6** – Política de três ações contra corte 0,5 de duas ações, conjunto de teste (n=200; 60 ruins) [fonte: resultados/resumo_politicas_teste.csv, todas as colunas]

| modelo | regra | utilidade_media [ic_inf; ic_sup] | n_aprovar | n_rejeitar | n_analise_manual | n_mudam_vs_outra_regra |
|---|---|---|---|---|---|---|
| nb | ue | 24,0 [7,6; 38,7] | 74 | 41 | 85 | 85 |
| nb | limiar | −5,5 [−30,5; 19,5] | 149 | 51 | 0 | 85 |
| tan | ue | 17,5 [−1,4; 35,3] | 92 | 48 | 60 | 60 |
| tan | limiar | −5,0 [−29,5; 19,5] | 145 | 55 | 0 | 60 |
| logreg | ue | 25,3 [10,2; 39,1] | 62 | 27 | 111 | 111 |
| logreg | limiar | −13,0 [−38,5; 12,0] | 154 | 46 | 0 | 111 |
| sel (secundária) | ue | 27,9 [13,4; 40,8] | 69 | 38 | 93 | 93 |
| sel (secundária) | limiar | −6,5 [−31,5; 17,5] | 152 | 48 | 0 | 93 |

O intervalo de cada regra isolada não é o critério de leitura; o critério é a diferença pareada (Tabela 4.7).

**Tabela 4.7** – Diferença pareada de utilidade média (`ue` − `limiar`), conjunto de teste (n=200; 60 ruins) [fonte: resultados/diferenca_politicas_teste.csv, todas as colunas]

| modelo | dif_utilidade_media | dif_ic_inf | dif_ic_sup |
|---|---|---|---|
| tan (principal) | 22,5 | 9,2 | 37,2 |
| nb | 29,5 | 13,1 | 46,3 |
| logreg | 38,3 | 20,2 | 56,4 |
| sel (secundária) | 34,4 | 16,4 | 52,5 |

Aplicando a §4 do plano: na comparação principal (TAN), a diferença é 22,5, com intervalo de 9,2 a 37,2 [fonte: resultados/diferenca_politicas_teste.csv, linha tan]. Diferença observada a favor da política de utilidade, com intervalo que exclui zero; não se afirma causa. Nos modelos do apêndice e na análise secundária, o intervalo também exclui zero a favor da regra `ue`: nb 29,5 [13,1; 46,3], logreg 38,3 [20,2; 56,4] e sel 34,4 [16,4; 52,5] [fonte: resultados/diferenca_politicas_teste.csv, linhas nb, logreg e sel]. A tabela é descritiva: a diferença mistura modelo, representação e conjunto de ações e não é chamada de efeito da regra nem do modelo. Ressalva obrigatória: a política de três ações ganha por construção, pois tem a ação de análise manual, ausente na regra `limiar`, e a matriz supõe que o analista sempre acerta (capítulo 5, seção 5.4; §6 do plano, itens 3 e 7). Na regra `ue`, a análise manual recebe 60 (tan), 85 (nb), 111 (logreg) e 93 (sel) dos 200 casos, e o número de casos que mudam de ação entre as regras coincide com esses valores [fonte: resultados/resumo_politicas_teste.csv, n_analise_manual e n_mudam_vs_outra_regra]. As três ações aparecem na regra `ue` em todos os modelos, de modo que a regra "alguma ação não aparece numa política" não se aplica [fonte: resultados/resumo_politicas_teste.csv, n_aprovar, n_rejeitar, n_analise_manual]. A ação de cada caso está em `resultados/politicas_teste.csv`.

## 4.4 Sensibilidade

A Tabela 4.8 mostra, para alguns pares de perda e custo da análise manual, os limiares de risco que delimitam a faixa de análise manual (seção 3.8). O arquivo completo tem 84 linhas: perda em {200, 400, 600, 800} e custo de 0 a 100, de 5 em 5 [fonte: resultados/sensibilidade.csv, colunas perda e custo_analise]. Esses limiares decorrem só da matriz de utilidade e não dependem de nenhum modelo.

**Tabela 4.8** – Limiares da política por perda e custo da análise manual, seleção de linhas [fonte: resultados/sensibilidade.csv, colunas perda, custo_analise, limiar_inferior, limiar_superior]

| perda | custo_analise | limiar_inferior | limiar_superior |
|---|---|---|---|
| 200 | 50 | 0,25 | 0,5 |
| 200 | 70 | 0,333 | 0,333 |
| 400 | 0 | 0,000 | 1,000 |
| 400 | 50 | 0,125 | 0,5 |
| 400 | 100 | 0,2 | 0,2 |
| 800 | 50 | 0,063 | 0,5 |

Com custo zero, a faixa de análise manual cobre todo o intervalo de 0 a 1 (linha 400, 0). Quando os dois limiares coincidem, a faixa desaparece e a política se reduz a duas ações; isso ocorre, por exemplo, para perda 200 com custo a partir de 70 e para perda 400 com custo a partir de 80 [fonte: resultados/sensibilidade.csv, linhas 200/70 e 400/80 a 400/100]. A Figura 4.3 mostra a tabela inteira. Não há regra da §4 para esta análise, e este texto não escolhe valor de custo nem de perda.

**Figura 4.3** – Limiares da política em função da perda e do custo da análise manual (`resultados/sensibilidade.png`).

## 4.5 Demonstração

O script `codigo/demo.py` (seção 3.9) lê apenas o conjunto de desenvolvimento, `resultados/predicoes_dev.csv` e `config/utilidade.json`, e não grava arquivos. Para um caso, ele treina os três modelos nas 4 partições que não contêm o caso e imprime as variáveis do caso, a probabilidade de ruim de cada modelo, a utilidade esperada de cada ação para o modelo indicado (padrão: tan), as fronteiras de risco da matriz e a ação recomendada. O comando `uv run python codigo/demo.py sgc-0000` produziu, para o primeiro caso de `predicoes_dev.csv` (partição 4), a saída resumida na Tabela 4.9.

**Tabela 4.9** – Saída de `codigo/demo.py` para o caso sgc-0000 [fonte: saída de terminal de `uv run python codigo/demo.py sgc-0000`]

| item | valor |
|---|---|
| P(ruim), nb | 0,834 |
| P(ruim), tan | 0,734 |
| P(ruim), logreg | 0,696 |
| UE aprovar (tan) | −267,18 |
| UE rejeitar (tan) | 0,00 |
| UE análise manual (tan) | −13,44 |
| fronteira aprovar / análise manual | p = 0,10 |
| fronteira análise manual / rejeitar | p = 0,60 |
| ação recomendada (tan) | rejeitar |

As probabilidades coincidem com as de `predicoes_dev.csv` [fonte: resultados/predicoes_dev.csv, colunas p_nb, p_tan, p_logreg, linha sgc-0000], o que é esperado, pois o script treina nas mesmas partições. Como a probabilidade de ruim do tan (0,734) está acima da fronteira de 0,60, a ação de maior utilidade esperada é rejeitar. O rótulo verdadeiro desse caso é bom (`kredit` = 1) [fonte: resultados/predicoes_dev.csv, coluna kredit, linha sgc-0000]; o caso foi escolhido por ser o primeiro do arquivo, não por ser representativo.

## 4.6 Estudo de seleção (secundário)

Esta seção relata o estudo secundário e pré-registrado da §9 do plano de análise (seção 3.10). Ele não altera a análise primária: as seções 4.1 a 4.4 continuam com NB e TAN de tamanho equivalente BDeu 5.

**Declaração de viés.** A grade de 8 configurações foi definida depois de ver `resultados/metricas_dev.csv` e foi motivada por ele (TAN pior que NB; hipótese `verw` da seção 4.1). A validação cruzada aninhada corrige o viés de escolher entre as 8 configurações, mas não o de ter desenhado a grade olhando o mesmo conjunto de desenvolvimento.

Foram feitas **8 comparações** (as 8 configurações da grade). A Tabela 4.10 traz as 8 linhas e a linha `aninhado`, que avalia, em cada partição externa, a configuração escolhida pela regra nas partições internas.

**Tabela 4.10** – Métricas das 8 configurações e da seleção aninhada, média (desvio) entre 5 partições externas [fonte: resultados/selecao_dev.csv, todas as colunas]

| modelo | roc_auc_media (desvio) | pr_auc_media (desvio) | brier_media (desvio) | log_loss_media (desvio) | ece_media (desvio) |
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

**Escolha por partição.** Pela regra pré-registrada (menor log loss médio nas partições internas), `nb_ess50` foi escolhida nas cinco partições externas e também no desenvolvimento inteiro [fonte: resultados/selecao_escolha.csv, coluna escolhida, linhas fold_externo 0 a 4 e dev]. A Tabela 4.11 traz o log loss interno da configuração escolhida e das duas configurações de baseline.

**Tabela 4.11** – Log loss interno por partição externa, seleção de colunas [fonte: resultados/selecao_escolha.csv, colunas fold_externo, config, log_loss_interno, escolhida]

| fold_externo | escolhida | log_loss_interno (escolhida) | nb_ess5 | tan_ess5 |
|---|---|---|---|---|
| 0 | nb_ess50 | 0,539 | 0,558 | 0,855 |
| 1 | nb_ess50 | 0,535 | 0,554 | 0,733 |
| 2 | nb_ess50 | 0,524 | 0,541 | 0,777 |
| 3 | nb_ess50 | 0,527 | 0,539 | 0,786 |
| 4 | nb_ess50 | 0,508 | 0,515 | 0,738 |
| dev | nb_ess50 | 0,512 | 0,523 | 0,704 |

Como a mesma configuração foi escolhida em todas as partições externas, a linha `aninhado` reproduz os valores de `nb_ess50` [fonte: resultados/selecao_dev.csv, linhas nb_ess50 e aninhado]. A diferença de ROC-AUC entre `aninhado` (0,788) e o baseline `nb_ess5` (0,789) é 0,001 [fonte: resultados/selecao_dev.csv, roc_auc_media], menor que 0,03 e, portanto, tratada como ruído pela regra da §4. A diferença de log loss entre as duas é 0,011 (0,512 contra 0,523) [fonte: resultados/selecao_dev.csv, log_loss_media]. Entre as configurações do TAN, o log loss médio diminui à medida que o tamanho equivalente aumenta, de 0,825 (`tan_ess1`) a 0,583 (`tan_ess50`) [fonte: resultados/selecao_dev.csv, log_loss_media]; em nenhuma partição uma configuração do TAN foi escolhida. Esses resultados descrevem o que a regra escolheu e quanto a escolha difere do baseline; não indicam qual modelo adotar.

**Conjunto de teste (n=200; 60 ruins), análise secundária.** As predições `p_sel` no teste estão em `resultados/predicoes_teste.csv` (coluna `p_sel`), e suas métricas, na linha `sel` da Tabela 4.3. Como define a §9, a diferença principal da escolha é contra o baseline `nb` (NB, BDeu 5): a ROC-AUC de `sel` é 0,720 [0,641; 0,795], contra 0,728 do `nb` [fonte: resultados/metricas_teste.csv, roc_auc, roc_auc_ic_inf, roc_auc_ic_sup, linhas sel e nb]; a diferença, 0,008 (nb − sel), é menor que 0,03 e, pela regra da §9, tratada como ruído. De forma apenas descritiva, a diferença contra o `tan` (TAN, BDeu 5, ROC-AUC 0,706) é 0,014 (sel − tan) [fonte: resultados/metricas_teste.csv, roc_auc, linha tan]. O log loss de `sel` é 0,623, contra 0,627 do `nb` (diferença de 0,005) [fonte: resultados/metricas_teste.csv, log_loss, linhas sel e nb]; o plano não tem regra de leitura para essa diferença, e ela é apenas descrita. O Brier de `sel`, 0,202, é menor que o da taxa base, 0,210 [fonte: resultados/metricas_teste.csv, brier]. Na política de decisão, a diferença pareada de `sel` é 34,4 [16,4; 52,5] (Tabela 4.7). Esses números relatam quanto a configuração escolhida pela regra difere do baseline no teste; não indicam qual modelo adotar, e a análise primária continua com NB e TAN de BDeu 5.

# 5 DISCUSSÃO E LIMITAÇÕES

Este capítulo interpreta os resultados do capítulo 4 e declara as limitações do experimento. Os métodos estão no capítulo 3 e as tabelas no capítulo 4; aqui apenas se remete a eles. Toda leitura de resultado segue as regras pré-registradas da §4 do plano de análise [fonte: docs/plano-de-analise.md §4], escritas antes de existir qualquer número [fonte: docs/plano-de-analise.md, preâmbulo]. O conjunto de teste final (200 casos, 60 ruins) foi avaliado uma única vez, em 17/11/2026, sobre o commit de congelamento 49d77ff; seus números estão nas Tabelas 4.3, 4.6 e 4.7 e na Figura 4.2, e são lidos aqui pelas mesmas regras.

## 5.1 Leitura do desenvolvimento

Os números do capítulo 4 constituem um *baseline* pré-estudo, obtidos só com os 800 casos do desenvolvimento, por validação cruzada em 5 partições [fonte: docs/resultados-dev.md, preâmbulo; monografia/cap4-resultados.md, preâmbulo]. Não têm intervalo de confiança, e os desvios entre partições são da mesma ordem de várias das diferenças entre modelos [fonte: docs/resultados-dev.md §5]. Por isso, a leitura a seguir se limita a aplicar as regras da §4 do plano.

**Desempenho preditivo.** A diferença de ROC-AUC entre Naive Bayes e regressão logística é 0,001 (0,789 contra 0,788) [fonte: resultados/metricas_dev.csv, roc_auc_media, linhas nb e logreg]. Pela regra pré-registrada, diferença menor que 0,03 é ruído e nenhum dos dois modelos se distingue do outro [fonte: docs/plano-de-analise.md §4]. O TAN ficou abaixo do Naive Bayes nas cinco métricas (Tabela 4.1), com ROC-AUC de 0,742 e desvio de 0,049 entre partições [fonte: resultados/metricas_dev.csv, roc_auc_media e roc_auc_desvio, linha tan]. As diferenças para o NB (0,047) e para a logística (0,046) passam de 0,03, de modo que a regra de ruído não se aplica; o plano não prevê outra regra para esse caso [fonte: docs/plano-de-analise.md §4; docs/resultados-dev.md §1]. O resultado entra no texto como saiu, e não motivou alteração do TAN, de seus parâmetros nem das faixas da análise primária [fonte: AGENTS.md, regra 3; docs/plano-de-analise.md §5]. O fato tem peso para o trabalho, porque o TAN é o modelo da comparação principal, fixado antes de qualquer métrica (decisão P5) [fonte: docs/decisoes.md §4, P5; docs/plano-de-analise.md §3]. A escolha não é revista à luz do resultado: revê-la seria exatamente o ajuste ao resultado que o pré-registro pretende impedir.

**Brier e calibração.** O Brier médio dos três modelos (nb 0,171; tan 0,200; logreg 0,165) é menor que o da taxa base, 0,210 [fonte: resultados/metricas_dev.csv, brier_media]; a frase "não melhor que prever a taxa base" não é acionada [fonte: docs/plano-de-analise.md §4]. O erro de calibração do TAN, 0,152, é o maior dos três (nb 0,093; logreg 0,095) [fonte: resultados/metricas_dev.csv, ece_media]. Como a política por utilidade esperada usa a probabilidade diretamente, e a literatura indica que decisões sensíveis a custo dependem de probabilidades calibradas \cite{zadrozny2001,elkan2001}, esse erro pode afetar, segundo a literatura, a qualidade das ações que a política escolhe a partir do TAN. O experimento, porém, não mede esse efeito separadamente: a relação vem da literatura, não dos dados (decisão P2) [fonte: docs/decisoes.md §4, P2].

**Hipótese sobre `verw`.** Em todas as partições, a variável `verw` é a que tem mais arestas saindo dela no TAN, fora a classe (Tabela 4.2) [fonte: resultados/tan_arestas.csv, coluna origem]. Registra-se, apenas como **hipótese não testada**, que isso poderia gerar tabelas de probabilidade condicional esparsas e excesso de confiança, coerente com o log loss e o erro de calibração maiores do TAN [fonte: docs/resultados-dev.md §4]. A observação de que esconder `verw` eleva a ROC-AUC do TAN em 0,025 [fonte: resultados/evidencia_incompleta.csv, delta_roc_auc, linha tan/verw] coexiste com essa hipótese, mas não a testa: nenhuma análise deste trabalho isola a causa, e a observação não autoriza retirar a variável nem mudar o modelo [fonte: docs/resultados-dev.md §4; monografia/cap4-resultados.md §4.2].

**Políticas.** A utilidade média da regra de três ações supera a do corte 0,5 nos três modelos (Tabela 4.5), com diferenças de 28,125 (nb), 25,4 (tan) e 27,25 (logreg) [fonte: resultados/resumo_politicas_dev.csv, utilidade_media]. São diferenças descritivas, sem intervalo, que misturam modelo, representação e conjunto de ações, e não são chamadas de efeito da regra [fonte: docs/plano-de-analise.md §3; docs/decisoes.md §4, P8]. A seção 5.4 explica por que essa vantagem era esperada antes de qualquer dado. A coincidência, em cada modelo, entre o número de casos que mudam de ação e o número de casos em análise manual [fonte: resultados/resumo_politicas_dev.csv, n_mudam_vs_outra_regra e n_analise_manual] decorre da própria matriz: com *c* = 40, a faixa de análise manual vai de 0,10 a 0,60 e contém o corte 0,5, e fora dela as duas regras escolhem a mesma ação [fonte: monografia/cap3-metodos.md §3.7; resultados/sensibilidade.csv, perda 400, custo_analise 40; resultados/resumo_politicas_dev.csv]. Trata-se de aritmética da faixa 0,10–0,60, não de um achado do experimento.

## 5.1b Leitura do teste final

**Desempenho preditivo.** No teste, a ROC-AUC foi 0,728 (nb), 0,706 (tan) e 0,729 (logreg) [fonte: resultados/metricas_teste.csv, coluna roc_auc, linhas nb, tan e logreg] (Tabela 4.3). Todas as diferenças entre pares são menores que 0,03 (nb–logreg 0,001; nb–tan 0,021; logreg–tan 0,022), e pela regra pré-registrada são ruído [fonte: docs/plano-de-analise.md §4]. Os intervalos de 95% são largos e se sobrepõem, como o do TAN, de 0,623 a 0,789 [fonte: resultados/metricas_teste.csv, roc_auc_ic_inf e roc_auc_ic_sup, linha tan]. A PR-AUC foi 0,490 (nb), 0,480 (tan) e 0,500 (logreg), contra 0,300 da taxa base [fonte: resultados/metricas_teste.csv, coluna pr_auc]; como o plano deixa em aberto a regra para a PR-AUC, os valores são apenas descritos, sem conclusão sobre diferenças.

**Queda do desenvolvimento para o teste.** A ROC-AUC caiu de 0,789 para 0,728 no NB, de 0,742 para 0,706 no TAN e de 0,788 para 0,729 na logística [fonte: resultados/metricas_dev.csv, roc_auc_media; resultados/metricas_teste.csv, roc_auc]; a PR-AUC caiu de 0,616, 0,549 e 0,649 para 0,490, 0,480 e 0,500 [fonte: resultados/metricas_dev.csv, pr_auc_media; resultados/metricas_teste.csv, pr_auc]. A queda é registrada como saiu. Nenhuma análise deste trabalho testa sua causa, e as duas estimativas não são diretamente comparáveis: uma é média de 5 partições sem intervalo, a outra é um único conjunto de 200 casos com intervalo que não cobre a variação do treino (seção 5.7).

**Brier e calibração.** O Brier do TAN no teste foi 0,215, maior que o da taxa base, 0,210 [fonte: resultados/metricas_teste.csv, coluna brier, linhas tan e taxa_base]: pela regra pré-registrada, o TAN **não foi melhor que prever a taxa base** no teste [fonte: docs/plano-de-analise.md §4]. NB (0,199) e logística (0,191) ficaram abaixo da taxa base [fonte: resultados/metricas_teste.csv, coluna brier]. O erro de calibração foi 0,115 (nb), 0,157 (tan) e 0,078 (logreg) [fonte: resultados/metricas_teste.csv, coluna ece] (Figura 4.2). A calibração foi apenas medida, sem correção (seção 5.8); essas probabilidades entram como estão na política.

**Políticas.** Na comparação principal, com o TAN (decisão P5), a diferença pareada de utilidade média (`ue` − `limiar`) foi 22,5, com intervalo de 95% de 9,2 a 37,2 [fonte: resultados/diferenca_politicas_teste.csv, linha tan, colunas dif_utilidade_media, dif_ic_inf e dif_ic_sup] (Tabela 4.7). O intervalo exclui zero, de modo que, pela regra pré-registrada (nível de 95% ainda a confirmar pelo autor, plano de análise §8), o resultado é **a favor da política de três ações**, sem afirmação de causa [fonte: docs/plano-de-analise.md §4 e §8]. Como apêndice, os intervalos do NB (29,5; de 13,1 a 46,3) e da logística (38,3; de 20,2 a 56,4) também excluem zero [fonte: resultados/diferenca_politicas_teste.csv, linhas nb e logreg]. A leitura carrega todas as ressalvas das seções 5.3 e 5.4: a política de três ações ganha do corte de duas ações por construção, pois só ela tem a ação de análise manual, e a matriz supõe que o analista sempre acerta; a matriz é demonstrativa; e a utilidade é simulada sobre o rótulo observado, não medida em operação. O resultado não indica qual modelo usar nem que a política seria vantajosa fora deste experimento.

## 5.2 Estudo de seleção

O estudo da §9 do plano é secundário e não altera a análise primária, que continua com NB e TAN de tamanho equivalente BDeu 5 [fonte: docs/plano-de-analise.md §9; docs/decisoes.md, Estudo de seleção, Q1].

**Declaração de viés.** A grade de 8 configurações foi definida depois de ver `metricas_dev.csv` e foi motivada por ele: o TAN saiu pior que o NB e surgiu a hipótese sobre `verw` [fonte: docs/plano-de-analise.md §9]. A validação cruzada aninhada corrige o viés de escolher entre as 8 configurações, mas não corrige o viés de ter desenhado a grade olhando o mesmo conjunto de desenvolvimento [fonte: docs/plano-de-analise.md §9; docs/decisoes.md, Estudo de seleção]. Além disso, o estudo foi decidido por delegação e ainda está a rever pelo autor [fonte: docs/decisoes.md, Estudo de seleção]. Os números do estudo devem ser lidos com essas duas ressalvas.

**O que a regra escolheu.** Foram feitas 8 comparações (Tabela 4.10). A regra pré-registrada, de menor log loss interno, escolheu `nb_ess50` nas cinco partições externas e no desenvolvimento inteiro [fonte: resultados/selecao_escolha.csv, coluna escolhida]. A diferença de ROC-AUC entre a linha `aninhado` (0,788) e o baseline `nb_ess5` (0,789) é 0,001 [fonte: resultados/selecao_dev.csv, roc_auc_media], ruído pela regra da §4 [fonte: docs/plano-de-analise.md §4 e §9]. A diferença de log loss é 0,011 (0,512 contra 0,523) [fonte: resultados/selecao_dev.csv, log_loss_media], uma diferença sem intervalo e menor que o desvio entre partições de qualquer das duas (0,033 e 0,035) [fonte: resultados/selecao_dev.csv, log_loss_desvio]. O estudo relata qual configuração a regra escolheu e quanto ela difere do baseline; não indica qual modelo adotar [fonte: docs/plano-de-analise.md §9].

**O TAN na grade.** Nas configurações do TAN, o log loss médio cai de 0,825 (`tan_ess1`) para 0,583 (`tan_ess50`) à medida que o tamanho equivalente aumenta [fonte: resultados/selecao_dev.csv, log_loss_media]. A grade varia só o tamanho equivalente, não a estrutura nem as variáveis. A hipótese continua não testada. Nenhuma configuração do TAN foi escolhida em partição alguma [fonte: resultados/selecao_escolha.csv, coluna escolhida].

**`sel` no teste (análise secundária).** No teste, a configuração escolhida pela regra teve ROC-AUC 0,720, PR-AUC 0,477, Brier 0,202 e erro de calibração 0,120 [fonte: resultados/metricas_teste.csv, linha sel]; a diferença de ROC-AUC para o NB de BDeu 5 (0,728) é 0,008, ruído pela regra da §4 [fonte: docs/plano-de-analise.md §4]. A diferença pareada de utilidade foi 34,4, com intervalo de 16,4 a 52,5 [fonte: resultados/diferenca_politicas_teste.csv, linha sel], lida com as mesmas ressalvas da seção 5.1b. Esses números herdam o viés declarado acima: a grade foi desenhada depois de ver o desenvolvimento [fonte: docs/plano-de-analise.md §9], e o teste não remove esse viés. A análise primária continua com NB e TAN de BDeu 5 (P5) [fonte: docs/plano-de-analise.md §9].

## 5.3 Simulação, não política real

A base não traz o resultado das ações que não foram tomadas [fonte: docs/plano-de-analise.md §6, item 1]. A utilidade de cada política é, portanto, calculada aplicando a matriz de utilidade ao rótulo observado, como se cada ação tivesse sido executada. Isso é uma simulação: não há efeito causal da política nem lucro real medido [fonte: docs/plano-de-analise.md §6, item 1]. Os resultados não afirmam que a política seria vantajosa em operação, nem que se generalizam a outras bases ou carteiras.

## 5.4 Matriz demonstrativa e analista infalível

A matriz de utilidade (+100, −400, custo da análise *c* = 40) é demonstrativa, não calibrada com dados reais, e aguarda aceite do orientador [fonte: config/utilidade.json, campo hipoteses; docs/decisoes.md §6]. Ela supõe que o analista da análise manual sempre acerta o estado do cliente: aprova os bons, recusa os ruins e só paga o custo *c* [fonte: config/utilidade.json, campo hipoteses; docs/decisoes.md §4, P7].

Essa hipótese tem uma consequência direta para a tabela 2×2 (Tabela 4.5): **a política de três ações ganha do corte de duas ações por construção** [fonte: docs/decisoes.md §4, P7]. A análise manual é uma ação adicional que, com analista infalível, oferece um resultado intermediário quase sem risco; a política de utilidade esperada só a escolhe quando, pelo modelo, ela vale mais que aprovar e que rejeitar \cite{chow1970}. O corte 0,5 não tem acesso a essa ação. Uma vantagem da regra `ue` na tabela 2×2 é, assim, em grande parte consequência da matriz e do conjunto de ações, não evidência sobre a rede bayesiana nem sobre o critério da utilidade esperada [fonte: docs/decisoes.md §4, P7 e P8]. Por esse motivo a tabela é descrita como "política de três ações por utilidade esperada contra corte 0,5 de duas ações", sem linguagem causal (decisão P8) [fonte: docs/decisoes.md §4, P8].

Há uma segunda razão para cautela: a comparação com o corte 0,5 não testa "utilidade esperada contra qualquer limiar", pois a utilidade esperada já equivale a uma regra de limiares sobre *p* \cite{elkan2001} [fonte: docs/plano-de-analise.md §6, item 7; monografia/cap3-metodos.md §3.7]. A análise de sensibilidade (seção 4.4) mostra como esses limiares mudam com a perda e com *c*, sem que este trabalho escolha um valor de custo [fonte: docs/resultados-dev.md §3].

## 5.5 Tamanho do teste

O teste tem 200 casos, dos quais 60 ruins [fonte: monografia/cap3-metodos.md §3.2]. Com tão poucos casos da classe positiva, diferenças pequenas entre modelos ou políticas são indistinguíveis de ruído [fonte: docs/plano-de-analise.md §6, item 2]. No resultado, os intervalos da diferença pareada (nível de 95% ainda a confirmar pelo autor, plano de análise §8) não incluíram zero em nenhum modelo [fonte: resultados/diferenca_politicas_teste.csv, dif_ic_inf], mas são largos: no TAN, vão de 9,2 a 37,2 [fonte: resultados/diferenca_politicas_teste.csv, linha tan]. Já as diferenças de ROC-AUC entre modelos no teste ficaram todas abaixo de 0,03 e são tratadas como ruído (seção 5.1b); com 60 ruins, pela regra, as diferenças são ruído e nenhum modelo se distingue.

## 5.6 Modelo e representação variam juntos

A regressão logística usa as três variáveis contínuas originais, enquanto as redes usam três faixas por tercis (decisão P6) [fonte: docs/decisoes.md §4, P6; monografia/cap3-metodos.md §3.4]. Uma diferença entre o TAN e a logística mistura, assim, a família do modelo e a representação das variáveis, e não é chamada de efeito do modelo [fonte: docs/decisoes.md §4, P6; docs/plano-de-analise.md §6, item 4]. Do mesmo modo, a evidência incompleta não é comparável entre famílias, porque as redes marginalizam a variável ausente e a logística a imputa (decisão P9) [fonte: docs/decisoes.md §4, P9]. Soma-se a isso o espaço de estados fixado no desenvolvimento inteiro, um vazamento brando que não usa rótulo [fonte: docs/plano-de-analise.md §6, item 6; docs/decisoes.md §4, P10].

## 5.7 O que o intervalo não cobre

O intervalo por bootstrap do teste final reamostra os casos de teste com os modelos já treinados \cite{efron1993}; ele não cobre a variação que viria de treinar os modelos em outra amostra (decisão P4) [fonte: docs/decisoes.md §4, P4; docs/plano-de-analise.md §6, item 5]. A incerteza total é, portanto, maior que a indicada pelo intervalo.

## 5.8 Calibração só medida

A calibração das probabilidades é medida, mas não corrigida (decisão P1) [fonte: docs/decisoes.md §4, P1]. Métodos de correção, como a sigmoide de Platt e a regressão isotônica \cite{platt1999,zadrozny2002,niculescu2005}, são citados na fundamentação sem aplicação [fonte: docs/decisoes.md §4, P27]. Como a política consome a probabilidade diretamente, um erro de calibração alto, como o do TAN no desenvolvimento [fonte: resultados/metricas_dev.csv, ece_media, linha tan], entra sem correção nas ações escolhidas. Isso é um desvio em relação à proposta, que prometia calibrar [fonte: docs/decisoes.md §4, P1].

## 5.9 Escopo das entregas

A análise exploratória se limita a uma tabela de descrição da base no capítulo 3, sem script próprio (decisão P12) [fonte: docs/decisoes.md §4, P12; monografia/cap3-metodos.md §3.1.1]. A demonstração mostra a conta da decisão (risco, utilidade de cada ação e fronteiras), mas não uma justificativa textual da recomendação (decisão P15) [fonte: docs/decisoes.md §4, P15]; o caso da Tabela 4.9 foi escolhido por ser o primeiro do arquivo, não por ser representativo [fonte: monografia/cap4-resultados.md §4.5]. A interface de uma tela, se existir, será construída só depois do experimento pronto e apenas lerá arquivos já gerados [fonte: docs/decisoes.md §4, linha da interface de uma tela; docs/decisoes.md §6].

## 5.10 Direções futuras

As direções a seguir decorrem das limitações acima, não das métricas do desenvolvimento, e não há promessa sobre o resultado de nenhuma delas:

- substituir a matriz demonstrativa por valores levantados com especialistas e modelar o erro do analista na análise manual, o que permitiria examinar a comparação sem a vantagem por construção discutida na seção 5.4;
- avaliar políticas com dados que registrem o desfecho das ações não tomadas, condição para falar em efeito, e não só em simulação;
- comparar modelos sob a mesma representação das variáveis, separando modelo e representação;
- estimar a incerteza incluindo a variação do treino.

O teste final não acrescenta direções: nenhuma das listadas decorre de suas métricas, e o resultado do teste não motiva mudança de modelo, parâmetro, faixa ou variável [fonte: docs/plano-de-analise.md §5, item 1].

# 6 CONCLUSÃO

Este trabalho perguntou se uma política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) tem (1) limiares explícitos, que qualquer pessoa reproduz a partir da matriz de utilidade e da probabilidade estimada, e (2) que efeito medido sobre as ações e a utilidade média, em comparação com um limiar fixo de 0,5 [fonte: PLANO.md §1; docs/plano-de-analise.md §1].

## 6.1 Limiares explícitos e reprodutíveis

A primeira parte é respondida pela construção da política, e não pelo desempenho dos modelos. Como a utilidade esperada de cada ação é linear na probabilidade estimada *p* de o caso ser ruim, a escolha da ação de maior utilidade equivale a uma regra de limiares sobre *p* (capítulo 3, seção 3.7). Com a matriz demonstrativa, pendente de aprovação do orientador [fonte: PLANO.md §11, item 2; config/utilidade.json], a análise manual é escolhida quando *c*/400 ≤ *p* ≤ 1 − *c*/100; com *c* = 40, a faixa vai de 0,10 a 0,60 [fonte: PLANO.md §5; config/utilidade.json]. Dadas a matriz em `config/utilidade.json` e a coluna de probabilidade, qualquer pessoa obtém a ação de cada caso e as fronteiras. A resposta à primeira parte é, portanto, afirmativa, com uma ressalva que o próprio plano registra: essa propriedade vale para qualquer escore de probabilidade e não distingue a rede bayesiana da regressão logística [fonte: PLANO.md §5].

## 6.2 Efeito medido nas ações e na utilidade média

A segunda parte é respondida pelo conjunto de teste, aberto uma única vez em 17/11/2026 sobre o commit de congelamento 49d77ff, com 200 casos, dos quais 60 ruins [fonte: resultados/predicoes_teste.csv, coluna kredit]. O critério de leitura é a diferença pareada de utilidade média entre a política de três ações por utilidade esperada e o corte 0,5 de duas ações, com intervalo de 95% por bootstrap (Tabela 4.7); o nível de 95% está a confirmar pelo autor [fonte: docs/plano-de-analise.md §8].

Na comparação principal, com o TAN, a diferença foi de 22,5, com intervalo de 9,2 a 37,2 [fonte: resultados/diferenca_politicas_teste.csv, linha tan, colunas dif_utilidade_media, dif_ic_inf, dif_ic_sup]. Pela regra pré-registrada: diferença observada a favor da política de utilidade, com intervalo que exclui zero; não se afirma causa. Nas ações, a política de três ações aprovou 92, rejeitou 48 e encaminhou 60 casos para análise manual, contra 145 aprovações e 55 rejeições do corte 0,5; os 60 casos que mudaram de ação são exatamente os encaminhados para análise manual [fonte: resultados/resumo_politicas_teste.csv, linhas tan/ue e tan/limiar, colunas n_aprovar, n_rejeitar, n_analise_manual, n_mudam_vs_outra_regra].

Esse resultado precisa ser lido com a ressalva que o acompanha desde o plano: a política de três ações ganha por construção, pois só ela tem a ação de análise manual, e a matriz supõe que o analista sempre acerta o estado do cliente (seção 5.4). A diferença mistura modelo, representação e conjunto de ações, e não é chamada de efeito da regra nem do modelo. Como a base não registra o desfecho das ações não tomadas, trata-se de uma simulação metodológica, e não da validação de uma política real.

Quanto ao risco estimado, o teste mostrou diferenças de ROC-AUC entre os três modelos de 0,001 a 0,022, todas abaixo de 0,03 e, pela regra pré-registrada, tratadas como ruído [fonte: resultados/metricas_teste.csv, roc_auc, linhas nb, tan e logreg]. O Brier do TAN, 0,215, foi maior que o da taxa base, 0,210: no teste, o TAN não foi melhor que prever a taxa base [fonte: resultados/metricas_teste.csv, brier, linhas tan e taxa_base]. As PR-AUC foram 0,490 (Naive Bayes), 0,480 (TAN) e 0,500 (regressão logística), contra 0,300 da taxa base; o plano deixa em aberto a regra para essa métrica, e os valores são apenas descritos [fonte: resultados/metricas_teste.csv, pr_auc]. O erro de calibração esperado foi 0,115, 0,157 e 0,078, respectivamente, e foi apenas medido [fonte: resultados/metricas_teste.csv, ece]. Os resultados de desenvolvimento e os do teste são distintos e não se substituem (seção 4.1).

## 6.3 Limitações essenciais

As conclusões acima valem dentro de limites discutidos no capítulo 5: a matriz de utilidade é demonstrativa, pendente de aprovação do orientador, e supõe analista infalível (seção 5.4); a camada de decisão é simulação, não política real (seção 5.3); o teste tem 200 casos e 60 ruins, o que deixa intervalos largos (seção 5.5); modelo e representação das variáveis variam juntos (seção 5.6); o intervalo não cobre a variação do treino (seção 5.7); e a calibração é só medida, sem correção (seção 5.8). Os resultados não autorizam generalizar para outras bases nem recomendar um modelo. As direções gerais de continuação estão na seção 5.10.

# Referências

<!-- Formato ABNT NBR 6023 (autor-data). Gerado de referencias.bib; só campos do .bib. -->
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

ELKAN, Charles. The foundations of cost-sensitive learning. In: INTERNATIONAL JOINT CONFERENCE ON ARTIFICIAL INTELLIGENCE, 17., 2001. **Proceedings** [...]. p. 973–978.
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

HECKERMAN, David; GEIGER, Dan; CHICKERING, David M. Learning Bayesian networks: The combination of knowledge and statistical data. **Machine Learning**, v. 20, n. 3, p. 197–243, 1995. DOI: 10.1007/BF00994016.
<!-- heckerman1995: Metadados conferidos em 17/11/2026 (Microsoft Research, DOI 10.1007/BF00994016); texto não lido. -->

HOFMANN, Hans. **Statlog (German Credit Data)**. UCI Machine Learning Repository, 1994. Disponível em: https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data).
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

NICULESCU-MIZIL, Alexandru; CARUANA, Rich. Predicting good probabilities with supervised learning. In: INTERNATIONAL CONFERENCE ON MACHINE LEARNING, 22., 2005. **Proceedings** [...]. p. 625–632.
<!-- niculescu2005: VERIFICAR: todos os campos. -->
<!-- FALTA: local do evento, local de publicação, editora -->

PEARL, Judea. **Probabilistic Reasoning in Intelligent Systems**: Networks of Plausible Inference. San Francisco: Morgan Kaufmann, 1988.
<!-- pearl1988: Bloco "referências da proposta": conferir edição e páginas no exemplar usado. -->

PEDREGOSA, Fabian et al. Scikit-learn: Machine learning in Python. **Journal of Machine Learning Research**, v. 12, p. 2825–2830, 2011.
<!-- pedregosa2011 -->

PLATT, John C. Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In: SMOLA, Alexander J. et al. (ed.). **Advances in Large Margin Classifiers**. Cambridge: MIT Press, 1999. p. 61–74.
<!-- platt1999: VERIFICAR: ano do livro (1999 na capa; algumas bases citam 2000) e páginas 61–74. -->

RUSSELL, Stuart; NORVIG, Peter. **Artificial Intelligence**: A Modern Approach. 3. ed. Upper Saddle River: Prentice Hall, 2010.
<!-- russell2010: VERIFICAR: trocada em 15/11/2026 da tradução brasileira para o original em inglês (3ª edição); título, editora, cidade e ano escritos de memória de um assistente de IA. -->

SIDDIQI, Naeem. **Credit Risk Scorecards**: Developing and Implementing Intelligent Credit Scoring. Hoboken: John Wiley & Sons, 2012.
<!-- siddiqi2012: Bloco "referências da proposta": conferir edição e páginas no exemplar usado. -->

THOMAS, Lyn C. A survey of credit and behavioural scoring: forecasting financial risk of lending to consumers. **International Journal of Forecasting**, v. 16, n. 2, p. 149–172, 2000.
<!-- thomas2000: Bloco "referências da proposta": conferir no original. -->

UCI MACHINE LEARNING REPOSITORY. **South German Credit (UPDATE)**. 2020. Conjunto de dados n. 573. DOI: 10.24432/C5QG88. Disponível em: https://archive.ics.uci.edu/dataset/573/south+german+credit+update. Acesso em: 10 nov. 2026.
<!-- uci573: Ano 2020 = criação do conjunto na UCI (decidido pelo autor, 17/11/2026). DOI conferido na API da UCI (docs/conferencia-referencias.md). -->

ZADROZNY, Bianca; ELKAN, Charles. Obtaining calibrated probability estimates from decision trees and naive Bayesian classifiers. In: INTERNATIONAL CONFERENCE ON MACHINE LEARNING, 18., 2001. **Proceedings** [...]. p. 609–616.
<!-- zadrozny2001: Anais e páginas conferidos em 17/11/2026 (mlanthology.org, ICML 2001, pp. 609–616); título, autores e resumo no PDF dos autores. -->
<!-- FALTA: local do evento, local de publicação, editora -->

ZADROZNY, Bianca; ELKAN, Charles. Transforming classifier scores into accurate multiclass probability estimates. In: ACM SIGKDD INTERNATIONAL CONFERENCE ON KNOWLEDGE DISCOVERY AND DATA MINING, 8., 2002. **Proceedings** [...]. p. 694–699.
<!-- zadrozny2002: VERIFICAR: todos os campos. -->
<!-- FALTA: local do evento, local de publicação, editora -->

## Conferência de citações

| Chave | Citada em | Situação |
|---|---|---|
| abnt10520 | — | não citada em nenhum capítulo (retirada da lista) |
| abnt14724 | — | não citada em nenhum capítulo (retirada da lista) |
| abnt6023 | — | não citada em nenhum capítulo (retirada da lista) |
| ankan2024 | cap3 | usada |
| brier1950 | cap2, cap3 | usada |
| chow1970 | cap2, cap5 | usada |
| chowliu1968 | cap2, cap3 | usada |
| efron1993 | cap3, cap5 | usada |
| elkan2001 | cap2, cap3, cap5 | usada |
| friedman1997 | cap2, cap3 | usada |
| gromping2019 | cap1, cap3 | usada |
| guo2017 | cap2 | usada |
| hand1997 | cap2 | usada |
| heckerman1995 | cap2, cap3 | usada |
| hofmann1994 | cap3 | usada |
| howard2005 | cap2, cap3 | usada |
| jensen2007 | cap2 | usada |
| kaufman2012 | cap3 | usada |
| koller2009 | cap2, cap3 | usada |
| naeini2015 | cap2, cap3 | usada |
| niculescu2005 | cap2, cap5 | usada |
| pearl1988 | cap1, cap2 | usada |
| pedregosa2011 | cap3 | usada |
| platt1999 | cap2, cap5 | usada |
| russell2010 | cap2, cap3 | usada |
| siddiqi2012 | cap1, cap2 | usada |
| thomas2000 | cap1, cap2 | usada |
| uci573 | cap3 | usada |
| zadrozny2001 | cap2, cap3, cap5 | usada |
| zadrozny2002 | cap2, cap5 | usada |

Chaves citadas nos capítulos e ausentes do .bib: nenhuma.

<!-- PENDÊNCIAS DO AUTOR (contagem por ocorrência de palavra, grep)
cap 1: LACUNA=8, confirmar=0, VERIFICAR=0, FALTA=0
cap 2: LACUNA=19, confirmar=44, VERIFICAR=0, FALTA=0
cap 3: LACUNA=8, confirmar=0, VERIFICAR=1, FALTA=0
cap 4: LACUNA=0, confirmar=0, VERIFICAR=0, FALTA=0
cap 5: LACUNA=0, confirmar=2, VERIFICAR=0, FALTA=0
cap 6: LACUNA=0, confirmar=1, VERIFICAR=0, FALTA=0
cap Ref: LACUNA=0, confirmar=0, VERIFICAR=9, FALTA=7
-->
