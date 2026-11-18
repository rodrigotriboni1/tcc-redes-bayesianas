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
