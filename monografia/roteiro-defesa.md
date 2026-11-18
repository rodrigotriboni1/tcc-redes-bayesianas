# Roteiro da defesa — slide a slide

Plano do deck (modo *Structured Argument* da skill academic-pptx). **Não é o .pptx**: a skill manda planejar e confirmar com o autor antes de construir.

## Premissas (a confirmar com o autor)

- Defesa de cerca de 20 minutos, seguida de arguição.
- 14 slides de corpo (cerca de 1,5 min cada; título e conclusões mais curtos) = cerca de 19 min falados, 1 min de folga.
- Referências logo depois das conclusões, como primeiro slide do apêndice (ver nota de estrutura abaixo); 9 slides de apêndice com as perguntas previstas.
- Formato 16:9.
- Instituição: Universidade Federal de Uberlândia (UFU), Faculdade de Engenharia Elétrica, curso de Engenharia de Controle e Automação. Orientador: Fabio Vincenzi.
- Visual: modelo da UFU, se o autor tiver; senão o padrão da skill: fundo branco, navy `1F4E79` (títulos), azul `2E75B6` (destaque), uma fonte sans-serif (Arial), título-ação 24–28 pt negrito, corpo ≥ 20 pt, citações 12–14 pt cinza `777777`. Título e conclusões com fundo navy (estrutura "sanduíche"). Sem ícones, sem imagens decorativas, sem linha sob o título.
- Números arredondados como na monografia (3 casas para métricas, 1 casa para utilidade).

**Nota de estrutura.** A skill tem duas regras que se chocam: "o slide de conclusões é o último fora do apêndice" e "o slide de referências é o último antes do apêndice". Prevalece a primeira (a conclusão fica na tela durante a arguição). As referências entram como slide R, primeiro do apêndice, logo depois das conclusões.

**Ressalvas de linguagem usadas em todo o deck** (docs/plano-de-analise.md §4, §5, §8, §9): nada de "melhor modelo", "vence", "superior"; diferença de ROC-AUC < 0,03 é ruído (só ROC-AUC); PR-AUC só descrita; diferença de utilidade lida pelo IC 95% por *bootstrap*; Brier ≥ taxa base = "não melhor que prever a taxa base"; nenhuma causa; nenhuma generalização; simulação, não política real.

---

## Corpo (14 slides)

### Slide 1 — Título (0:30)

- **Título:** Redes bayesianas e utilidade esperada aplicadas à seleção de *next best action* em sistemas automatizados de decisão
- **Subtítulo-afirmação:** Separar o risco da ação torna os limiares explícitos; o efeito medido vem com ressalvas
- **Exibição:** fundo navy; autor, orientador, UFU / FEELT / Engenharia de Controle e Automação, data da defesa.
- **Texto no slide:** só os itens acima.
- **So what:** a banca sabe de cara a tese e o tom (resultado com ressalvas).
- **Notas de fala:** "Bom dia. Sou Rodrigo Mialichi Triboni, orientado pelo professor Fabio Vincenzi. Este trabalho separa duas tarefas que a decisão de crédito costuma misturar: estimar o risco e escolher a ação. Vou mostrar que essa separação deixa os limiares explícitos, e qual efeito ela teve num conjunto de teste, com as ressalvas que acompanham esse número."

### Slide 2 — Problema (1:30)

- **Título-ação:** Na regra de escore com ponto de corte, estimar o risco e escolher a ação ficam fundidos, e os custos ficam implícitos
- **Exibição:** diagrama de duas caixas. À esquerda, "hoje": caso → escore → corte → aprovar/rejeitar (uma caixa só). À direita, "proposta": caso → **camada de risco** (P(ruim)) → **camada de decisão** (custos) → ação. Destaque azul na seta entre as duas camadas da direita.
- **Texto no slide (≈25 palavras):** "Escore + corte: prática da indústria, interpretável. / Custos não aparecem na regra. / Proposta: risco por rede bayesiana; ação por utilidade esperada."
- **Citação no slide:** (THOMAS, 2000; SIDDIQI, 2012; PEARL, 1988)
- **So what:** o problema é de arquitetura da decisão, não de acurácia.
- **Notas de fala:** "Na concessão de crédito, um modelo dá um escore e o escore é comparado com um corte; é a prática descrita por Thomas e por Siddiqi. Nessa regra, duas coisas diferentes viram uma: a probabilidade de o crédito ser ruim e a escolha do que fazer. O corte carrega os custos de errar, mas não os mostra. Redes bayesianas, no sentido de Pearl, servem para a primeira tarefa; para a segunda, uso a utilidade esperada. O trabalho testa essa separação num estudo de caso."

### Slide 3 — Pergunta de pesquisa (1:30)

- **Título-ação:** A pergunta tem duas partes: uma propriedade da política e um efeito medido contra o corte 0,5
- **Exibição:** caixa de destaque com o texto exato do PLANO.md §1 / monografia §1.2:
  > Uma política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) tem (1) limiares explícitos, que qualquer pessoa reproduz a partir da matriz de utilidade e de `p`, e (2) que efeito medido sobre as ações e a utilidade média, em comparação com um limiar fixo de 0,5?
- **Texto extra (≈20 palavras):** "(1) vale por construção, para qualquer escore. (2) é o que o experimento mede. Leitura fixada antes dos resultados."
- **So what:** a banca sabe o que cada resultado responde.
- **Notas de fala:** "Esta é a pergunta, como está no plano e no capítulo 1. A parte 1 é uma propriedade da política: vale para qualquer escore de probabilidade, inclusive a regressão logística, e não depende do experimento. A parte 2 é o que medi: ações e utilidade média, contra um corte fixo de 0,5. A pergunta e a forma de ler cada desfecho foram escritas antes de existir qualquer resultado [docs/plano-de-analise.md §1]."

### Slide 4 — Dados e protocolo (1:30)

- **Título-ação:** 1.000 casos da South German Credit: 800 para desenvolver em 5 partições e 200 de teste, abertos uma única vez
- **Exibição:** barra horizontal dividida: 800 dev (240 ruins) em 5 blocos de 160; 200 teste (60 ruins) separado, com cadeado e a data "aberto 1× em 17/11/2026, *commit* 49d77ff".
- **Texto no slide (≈30 palavras):** "Divisão estratificada, semente 2026. / Validação cruzada estratificada, 5 partições. / 3 contínuas em 3 faixas por tercis, cortes só no treino. / Classe positiva: ruim (30%)."
- **Citação no slide:** (GRÖMPING, 2019)
- **So what:** o teste não influenciou nenhuma escolha.
- **Notas de fala:** "A base é a South German Credit, a versão corrigida por Grömping da base alemã citada na proposta. São 1.000 casos; separei 800 para desenvolvimento, com 240 ruins, e 200 para teste, com 60 ruins [resultados/predicoes_teste.csv, kredit: 60 zeros em 200 linhas]. No desenvolvimento usei validação cruzada estratificada em 5 partições, semente 2026. As três variáveis contínuas viram três faixas por tercis, com cortes aprendidos só no treino; no teste, os cortes vêm do desenvolvimento inteiro [resultados/cortes.json]. O teste foi aberto uma única vez, em 17/11/2026, depois do *commit* de congelamento."

### Slide 5 — Modelos (1:30)

- **Título-ação:** Três modelos estimam P(ruim): Naive Bayes e TAN com prior BDeu 5, e a regressão logística como referência
- **Exibição:** três mini-grafos lado a lado: NB (estrela: `kredit` pai de todas), TAN (estrela + árvore entre preditoras, destaque em `verw`), regressão logística (caixa "sem grafo; contínuas originais").
- **Texto no slide (≈30 palavras):** "Parâmetros: prior BDeu, tamanho equivalente 5. / Inferência exata (pgmpy 1.1.2). / Logística: `max_iter=1000`. / Calibração só medida, não corrigida."
- **Citação no slide:** (FRIEDMAN; GEIGER; GOLDSZMIDT, 1997; HECKERMAN; GEIGER; CHICKERING, 1995; ANKAN; TEXTOR, 2024; PEDREGOSA et al., 2011)
- **So what:** modelo e representação variam juntos; a comparação entre famílias não isola o modelo.
- **Notas de fala:** "Comparo três modelos. O Naive Bayes trata as preditoras como independentes dada a classe; o TAN, de Friedman e colegas, acrescenta uma árvore de dependências entre elas. Os parâmetros das redes usam prior BDeu com tamanho equivalente 5, como em Heckerman, para evitar probabilidade zero. A regressão logística é a referência e recebe as contínuas sem discretizar; por isso a diferença entre redes e logística mistura modelo e representação. A calibração é só medida: corrigir exigiria escolher o método depois de ver as métricas."

### Slide 6 — Camada de utilidade esperada (1:45)

- **Título-ação:** Com a matriz demonstrativa, a utilidade esperada vira dois limiares: aprovar abaixo de 0,10, análise manual até 0,60, rejeitar acima
- **Exibição (gráfico a gerar):** linhas de UE(a) contra *p* ∈ [0, 1] para as três ações: aprovar = 100 − 500p; rejeitar = 0; análise manual = 60 − 100p. Eixo x "P(ruim)", eixo y "utilidade esperada". Faixas de fundo pela ação de maior UE; linhas verticais tracejadas em 0,10 e 0,60, rotuladas "c/L = 40/400" e "1 − c/G = 1 − 40/100". Ao lado, a matriz (Quadro 3.1) pequena. Dados: `config/utilidade.json`.
- **Texto no slide (≈30 palavras):** "UE(a) = (1−p)·U(a,bom) + p·U(a,ruim). / Matriz: G = 100, L = 400, c = 40. / Demonstrativa, aprovada pelo orientador, não calibrada com dados reais."
- **Citação no slide:** (ELKAN, 2001)
- **So what:** responde à parte 1: qualquer pessoa reproduz as fronteiras a partir da matriz e de *p*.
- **Notas de fala:** "A camada de decisão escolhe a ação de maior utilidade esperada. A matriz é demonstrativa: aprovar um bom vale 100, aprovar um ruim custa 400, rejeitar vale zero, e a análise manual custa c = 40 [config/utilidade.json]. Como cada utilidade esperada é uma reta em p, a escolha vira limiares, como Elkan mostra: análise manual entre c/400 e 1 − c/100, ou seja, de 0,10 a 0,60. Isso responde à primeira parte da pergunta, por construção, para qualquer escore. A contribuição não é uma regra nova, é derivar os limiares dos custos de forma explícita."

### Slide 7 — Sensibilidade (1:15)

- **Título-ação:** Os limiares se movem com a perda e o custo da análise; com custo alto, a análise manual desaparece
- **Exibição:** `resultados/sensibilidade.png` (reaproveitada), refeita em fonte ≥ 16 pt se possível. Destaque: ponto (L = 400, c = 40) marcado com "0,10 / 0,60"; marcar onde as curvas se encontram (L = 200, c = 70; L = 400, c = 80).
- **Texto no slide (≈25 palavras):** "Grade: perda 200–800; custo 0–100. / c = 0: análise manual cobre 0 a 1. / Limiares coincidem → volta a duas ações. / Nenhum valor escolhido."
- **So what:** a política mostra para onde vai com outros custos; a escolha do custo é do negócio, não do trabalho.
- **Notas de fala:** "Variei a perda por inadimplência em 200, 400, 600 e 800 e o custo da análise de 0 a 100, de 5 em 5 [resultados/sensibilidade.csv, 84 linhas]. Com custo zero, a análise manual cobre todo o intervalo [sensibilidade.csv, linha 400/0: 0,000 e 1,000]. Quando os dois limiares coincidem a faixa some: com perda 200 a partir de c = 70, ambos 0,333; com perda 400 a partir de c = 80, ambos 0,200 [sensibilidade.csv, limiar_inferior e limiar_superior]. Essa figura não depende de modelo, e o trabalho não escolhe valor de custo."

### Slide 8 — Desenvolvimento (1:30)

- **Título-ação:** No desenvolvimento, o TAN ficou abaixo do Naive Bayes nas cinco métricas; NB e logística ficaram a 0,001 de ROC-AUC
- **Exibição (gráfico a gerar):** gráfico de pontos com barra de ±1 desvio, ROC-AUC média por modelo (NB, TAN, logística, taxa base). Destaque azul no TAN; chave "0,001 → ruído" entre NB e logística. Tabela de origem: `resultados/metricas_dev.csv` (roc_auc_media, roc_auc_desvio). Brier/ECE ficam no texto.
- **Texto no slide (≈30 palavras):** "ROC-AUC: NB 0,789; logística 0,788; TAN 0,742 (desvio 0,049). / ECE do TAN 0,152 (NB 0,093). / Média de 5 partições, sem intervalo."
- **So what:** o TAN, estrutura mais rica, não trouxe ganho aqui; o resultado entra como saiu.
- **Notas de fala:** "No desenvolvimento, a ROC-AUC média foi 0,789 no Naive Bayes, 0,788 na logística e 0,742 no TAN [resultados/metricas_dev.csv, roc_auc_media]. NB e logística diferem em 0,001, abaixo de 0,03, e pela regra pré-registrada é ruído. O TAN ficou abaixo do NB nas cinco métricas; o erro de calibração do TAN foi 0,152, contra 0,093 do NB e 0,095 da logística [metricas_dev.csv, ece_media]. O desvio do TAN entre partições foi 0,049 [roc_auc_desvio]. Não ajustei nada por causa disso: o resultado vai como saiu."

### Slide 9 — Teste: discriminação (1:30)

- **Título-ação:** No teste, as diferenças de ROC-AUC entre os três modelos ficaram entre 0,001 e 0,022, abaixo de 0,03: pela regra, são ruído
- **Exibição (gráfico a gerar):** *forest plot* horizontal de ROC-AUC com IC 95% (NB, TAN, logística; taxa base como linha vertical em 0,5). Faixa sombreada de largura 0,03 para mostrar a regra. Tabela de origem: `resultados/metricas_teste.csv` (roc_auc, roc_auc_ic_inf, roc_auc_ic_sup).
- **Texto no slide (≈30 palavras):** "n = 200; 60 ruins. / NB 0,728; TAN 0,706; logística 0,729. / IC 95% por *bootstrap*, largos e sobrepostos. / PR-AUC: 0,490; 0,480; 0,500 (taxa base 0,300), só descrita."
- **Citação no slide:** (EFRON; TIBSHIRANI, 1993)
- **So what:** o teste não distingue os modelos pela discriminação.
- **Notas de fala:** "No teste, a ROC-AUC foi 0,728 no NB, 0,706 no TAN e 0,729 na logística [resultados/metricas_teste.csv, roc_auc]. As diferenças são 0,001, 0,021 e 0,022; todas abaixo de 0,03 e, pela regra que fixei antes, ruído. Os intervalos de 95% por *bootstrap* são largos; o do TAN vai de 0,623 a 0,789 [roc_auc_ic_inf, roc_auc_ic_sup]. A PR-AUC foi 0,490, 0,480 e 0,500, contra 0,300 da taxa base [pr_auc]; para ela não fixei regra de ruído, então só descrevo. Também registro que todos caíram em relação ao desenvolvimento; não testei a causa."

### Slide 10 — Teste: Brier e calibração (1:30)

- **Título-ação:** No teste, o Brier do TAN (0,215) ficou acima do da taxa base (0,210): o TAN não foi melhor que prever a taxa base
- **Exibição (gráfico a gerar):** pontos com IC 95% do Brier por modelo; linha vertical tracejada em 0,210 (taxa base); TAN em azul, à direita da linha. Tabela de origem: `resultados/metricas_teste.csv` (brier, brier_ic_inf, brier_ic_sup). (`calibracao_teste.png` fica no apêndice A2.)
- **Texto no slide (≈30 palavras):** "Brier: NB 0,199; logística 0,191; TAN 0,215. / ECE: NB 0,115; TAN 0,157; logística 0,078. / Calibração só medida, sem correção."
- **Citação no slide:** (BRIER, 1950; NAEINI; COOPER; HAUSKRECHT, 2015)
- **So what:** a probabilidade do TAN, que alimenta a decisão principal, não supera a taxa base no teste.
- **Notas de fala:** "O Brier mede o erro da probabilidade. No teste, o do TAN foi 0,215, acima dos 0,210 de quem prevê a taxa base para todo caso [resultados/metricas_teste.csv, brier, linhas tan e taxa_base]. Pela regra pré-registrada, digo: o TAN não foi melhor que prever a taxa base. NB, com 0,199, e logística, com 0,191, ficaram abaixo [brier]. O erro de calibração foi 0,115, 0,157 e 0,078 [ece]. A calibração foi só medida; não corrigi."

### Slide 11 — Política de três ações contra corte 0,5 (2:00)

- **Título-ação:** Com o TAN, a política de três ações teve utilidade média 22,5 maior que o corte 0,5 (IC 95% de 9,2 a 37,2), uma vantagem que a matriz garante por construção
- **Exibição (gráfico a gerar):** *forest plot* da diferença pareada `ue − limiar` com IC 95%: TAN (principal, azul, rotulado), NB, logística e sel em cinza; linha vertical em zero. Barra empilhada pequena embaixo, TAN: três ações 92 aprovar / 48 rejeitar / 60 análise manual; corte 0,5: 145 / 55 / 0. Tabelas de origem: `resultados/diferenca_politicas_teste.csv` e `resultados/resumo_politicas_teste.csv` (linhas tan).
- **Texto no slide (≈35 palavras):** "IC exclui zero → diferença a favor das três ações; sem causa. / Os 60 que mudam = os 60 em análise manual. / Ressalvas: matriz demonstrativa; analista infalível; simulação, não política real."
- **So what:** responde à parte 2: há efeito medido, mas ele vem da ação extra e da matriz, não da rede.
- **Notas de fala:** "Esta é a comparação principal, fixada antes: TAN, política de três ações contra corte 0,5 de duas ações. A diferença pareada de utilidade média foi 22,5, com intervalo de 95% de 9,2 a 37,2 [resultados/diferenca_politicas_teste.csv, linha tan]. O intervalo exclui zero, então leio: diferença a favor da política de três ações, sem afirmar causa. A política aprovou 92, rejeitou 48 e mandou 60 para análise manual; o corte aprovou 145 e rejeitou 55; os 60 que mudaram são exatamente os da análise manual [resumo_politicas_teste.csv]. E a ressalva principal: com analista infalível, a análise manual quase não tem risco, então a política de três ações ganha do corte por construção; é consequência da matriz e do conjunto de ações, não evidência sobre a rede."

### Slide 12 — Estudo de seleção secundário (1:15)

- **Título-ação:** O estudo de seleção secundário escolheu NB com BDeu 50, a 0,001 de ROC-AUC da referência; a grade foi desenhada depois de ver o desenvolvimento
- **Exibição (gráfico a gerar):** pontos de *log loss* médio (± desvio) das 8 configurações (nb_ess1…tan_ess50) e da linha "aninhado"; `nb_ess50` circulada como "escolhida em 5/5 partições". Tabela de origem: `resultados/selecao_dev.csv` (log_loss_media, log_loss_desvio) e `resultados/selecao_escolha.csv` (escolhida).
- **Texto no slide (≈35 palavras):** "8 comparações; regra: menor *log loss* interno. / Escolhida: nb_ess50 em todas as partições. / **Viés declarado:** grade motivada pelas métricas do desenvolvimento. / Análise primária não muda."
- **So what:** a seleção não muda a leitura; serve para mostrar que o viés foi declarado, não escondido.
- **Notas de fala:** "Depois de ver o TAN abaixo do NB, desenhei um estudo secundário: 8 configurações, NB e TAN com tamanho equivalente 1, 5, 10 e 50, em validação cruzada aninhada. A regra escolheu nb_ess50 nas cinco partições externas e no desenvolvimento inteiro [resultados/selecao_escolha.csv, escolhida]. A ROC-AUC do aninhado, 0,788, difere em 0,001 da referência nb_ess5, 0,789: ruído [selecao_dev.csv, roc_auc_media]. O aninhamento corrige a escolha entre as 8, mas não o fato de a grade ter sido desenhada olhando o desenvolvimento; esse viés está declarado. A análise primária continua com NB e TAN de BDeu 5."

### Slide 13 — Limitações (1:30)

- **Título-ação:** Os resultados valem para esta base, esta matriz demonstrativa e um analista infalível: é simulação, não política real
- **Exibição:** lista em duas colunas, sem gráfico.
- **Texto no slide (≈40 palavras):** "Matriz demonstrativa; analista infalível. / Sem desfecho das ações não tomadas → simulação. / Teste: 200 casos, 60 ruins → IC largos. / Modelo e representação variam juntos. / IC não cobre variação do treino. / Calibração só medida."
- **So what:** antecipa as objeções da banca antes da arguição.
- **Notas de fala:** "Seis limites acompanham tudo o que mostrei. A matriz é demonstrativa e supõe um analista que sempre acerta. A base não registra o que teria acontecido com as ações não tomadas, então a camada de decisão é simulação. O teste tem 200 casos e 60 ruins, e os intervalos são largos; no TAN, a diferença vai de 9,2 a 37,2 [diferenca_politicas_teste.csv]. Modelo e representação das variáveis variam juntos, o intervalo reamostra só o teste e não o treino, e a calibração foi só medida. Por isso não generalizo para outras bases nem recomendo um modelo."

### Slide 14 — Conclusões (1:00; fica na tela durante a arguição)

- **Título-ação:** Separar risco e ação dá limiares explícitos por construção; o efeito medido favorece as três ações, sem causa e sem modelo recomendado
- **Exibição:** fundo navy, três itens numerados, contato no rodapé.
- **Texto no slide (≈40 palavras):** "1. Limiares 0,10 e 0,60 saem da matriz; valem para qualquer escore. / 2. TAN: +22,5 de utilidade média [9,2; 37,2], por construção da matriz. / 3. ROC-AUC: diferenças são ruído; Brier do TAN não melhor que taxa base. / [e-mail] · [link do repositório]"
- **So what:** as duas partes da pergunta respondidas numa tela.
- **Notas de fala:** "Concluindo. Parte 1: separar risco e ação dá limiares explícitos, 0,10 e 0,60 com esta matriz, que qualquer pessoa reproduz; isso vale por construção e não distingue a rede da logística. Parte 2: com o TAN, a política de três ações teve utilidade média 22,5 maior que o corte 0,5, com intervalo de 9,2 a 37,2, uma vantagem que a matriz garante por construção. No risco, as diferenças de ROC-AUC foram ruído, e o TAN não foi melhor que a taxa base no Brier. Fico à disposição para perguntas e comentários da banca."

---

## Apêndice (perguntas previstas)

### Slide R — Referências (primeiro slide do apêndice)

ABNT curta, 13 pt (do arquivo monografia/referencias-abnt.md):

- ANKAN, A.; TEXTOR, J. pgmpy: A Python Toolkit for Bayesian Networks. *JMLR*, v. 25, n. 265, 2024.
- BRIER, G. W. Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, v. 78, n. 1, 1950.
- EFRON, B.; TIBSHIRANI, R. J. *An Introduction to the Bootstrap*. Chapman & Hall, 1993.
- ELKAN, C. The foundations of cost-sensitive learning. In: IJCAI, 17., 2001. p. 973–978. **(entrada marcada "A CONFERIR NO ORIGINAL" no repositório)**
- FRIEDMAN, N.; GEIGER, D.; GOLDSZMIDT, M. Bayesian network classifiers. *Machine Learning*, v. 29, 1997.
- GRÖMPING, U. *South German Credit Data*: Correcting a Widely Used Data Set. Beuth Univ., 2019. **(VERIFICAR série/instituição)**
- HECKERMAN, D.; GEIGER, D.; CHICKERING, D. M. Learning Bayesian networks. *Machine Learning*, v. 20, 1995.
- NAEINI, M. P.; COOPER, G. F.; HAUSKRECHT, M. Obtaining well calibrated probabilities using Bayesian binning. AAAI, 2015.
- PEARL, J. *Probabilistic Reasoning in Intelligent Systems*. Morgan Kaufmann, 1988.
- PEDREGOSA, F. et al. Scikit-learn. *JMLR*, v. 12, 2011.
- SIDDIQI, N. *Credit Risk Scorecards*. Wiley, 2012.
- THOMAS, L. C. A survey of credit and behavioural scoring. *Int. J. Forecasting*, v. 16, n. 2, 2000.
- ZADROZNY, B.; ELKAN, C. Obtaining calibrated probability estimates from decision trees and naive Bayesian classifiers. ICML, 2001.

### A1 — Por que o TAN saiu pior que o NB?

- **Título-ação:** O TAN ficou abaixo do NB, e a hipótese sobre `verw` é registrada, mas não foi testada
- **Exibição:** `resultados/calibracao_dev.png` (reaproveitada) com o painel do TAN destacado; contagem de arestas saindo de `verw` (7 a 9 por partição).
- **Resposta curta:** "Não sei a causa e não afirmo. Em todas as partições `verw` é, fora `kredit`, a variável com mais arestas de saída, 7 a 9 [resultados/tan_arestas.csv, origem]; tabelas esparsas e excesso de confiança seriam coerentes com o *log loss* 0,704 e o ECE 0,152 do TAN [metricas_dev.csv], mas nenhuma análise testou isso. No estudo de seleção, o *log loss* do TAN cai de 0,825 (ess 1) para 0,583 (ess 50) [selecao_dev.csv], o que também não testa a hipótese."

### A2 — Por que não calibrar?

- **Título-ação:** Calibrar exigiria escolher o método depois de ver as métricas, o que quebraria a pré-especificação
- **Exibição:** `resultados/calibracao_teste.png` (reaproveitada).
- **Resposta curta:** "Decisão P1: corrigir pediria escolher entre métodos olhando o desenvolvimento. A exigência de probabilidade calibrada para decidir por custos vem da literatura (ZADROZNY; ELKAN, 2001), não do experimento. Medi: ECE no teste 0,115 (NB), 0,157 (TAN), 0,078 (logística) [metricas_teste.csv, ece]. Calibrar é direção futura."

### A3 — Por que o corte 0,5 é a comparação?

- **Título-ação:** O corte 0,5 foi fixado na pergunta antes dos resultados; não é o limiar de duas ações da matriz, que seria 0,2
- **Resposta curta:** "O corte 0,5 representa a regra fixa sem referência a custos e está no texto da pergunta [PLANO.md §1]. Com esta matriz, o limiar de duas ações seria G/(G+L) = 100/500 = 0,2; a comparação não o inclui, e isso decorre da Seção 2.7, não de uma métrica. A comparação, portanto, não testa 'utilidade esperada contra qualquer limiar'."

### A4 — O que muda se a matriz mudar?

- **Título-ação:** Mudar perda ou custo desloca os limiares de forma previsível; acima de certo custo a análise manual some
- **Exibição:** `resultados/sensibilidade.png`.
- **Resposta curta:** "A fórmula dá a resposta sem rodar nada: análise manual entre c/L e 1 − c/G. Na grade, perda 400 e c = 80 já zeram a faixa (0,200 e 0,200); perda 800 e c = 50 dão 0,063 e 0,5 [sensibilidade.csv]. A diferença de utilidade no teste só foi medida com a matriz aprovada; com outra matriz, ela teria de ser recalculada."

### A5 — Por que 5 partições?

- **Título-ação:** 5 partições é convenção fixada antes dos resultados, não escolhida por desempenho
- **Resposta curta:** "Constante congelada, como as 3 faixas e o BDeu 5 [docs/decisoes.md §2; monografia §3.3]. Com 800 casos, cada partição tem 160 casos de validação e 48 ruins (estratificada). Não testei outros valores para não escolher pelo resultado."

### A6 — Houve vazamento?

- **Título-ação:** O teste ficou fechado até o congelamento; o único vazamento é brando e está declarado
- **Resposta curta:** "Cortes das faixas aprendidos só no treino de cada partição; teste aberto uma vez, em 17/11/2026, sobre o *commit* 49d77ff. O espaço de estados de cada variável usa todos os valores do desenvolvimento inteiro, para uma categoria rara não quebrar a inferência; não usa o rótulo, mas é um vazamento brando, declarado [decisões P10; plano-de-análise §6, item 6]. A divisão com semente 42 foi descartada porque seu teste já tinha sido usado antes."

### A7 — O que significa "ganha por construção"?

- **Título-ação:** Com analista infalível, a análise manual garante um resultado intermediário que o corte de duas ações não tem
- **Exibição:** gráfico do slide 6, com a reta da análise manual destacada entre 0,10 e 0,60.
- **Resposta curta:** "Na análise manual o analista acerta sempre: ganha 60 num bom e perde 40 num ruim. Entre 0,10 e 0,60 essa reta fica acima de aprovar e de rejeitar. O corte 0,5 não tem essa ação, então a política de três ações tende a ganhar dele qualquer que seja o modelo; no teste, as quatro diferenças foram positivas, de 22,5 a 38,3 [diferenca_politicas_teste.csv]. Por isso a diferença não é evidência sobre a rede nem sobre o critério da utilidade esperada."

### A8 — 60 casos ruins bastam?

- **Título-ação:** Com 60 ruins, diferenças pequenas são indistinguíveis de ruído, e por isso a regra de 0,03 foi fixada antes
- **Resposta curta:** "O plano já previa que, com 60 ruins, diferença de AUC de 0,02 a 0,03 é ruído [PLANO.md §6]. Os intervalos confirmam: ROC-AUC do TAN de 0,623 a 0,789; diferença de utilidade de 9,2 a 37,2 [metricas_teste.csv; diferenca_politicas_teste.csv]. E o intervalo reamostra só o teste, não o treino, então a incerteza total é maior."

### A9 — Por que não há "melhor modelo"?

- **Título-ação:** Nenhuma regra pré-registrada separou os modelos no teste, e escolher um seria decidir pelo resultado
- **Resposta curta:** "As diferenças de ROC-AUC no teste foram até 0,022, ruído pela regra [metricas_teste.csv]. PR-AUC só descrita. No Brier, só o TAN foi não melhor que a taxa base. A comparação principal usa o TAN porque foi fixada antes (P5), não por desempenho. O estudo de seleção diz o que a regra escolheu, não o que adotar."

---

## Ghost deck test

Títulos-ação em sequência:

1. Separar o risco da ação torna os limiares explícitos; o efeito medido vem com ressalvas
2. Na regra de escore com ponto de corte, estimar o risco e escolher a ação ficam fundidos, e os custos ficam implícitos
3. A pergunta tem duas partes: uma propriedade da política e um efeito medido contra o corte 0,5
4. 1.000 casos da South German Credit: 800 para desenvolver em 5 partições e 200 de teste, abertos uma única vez
5. Três modelos estimam P(ruim): Naive Bayes e TAN com prior BDeu 5, e a regressão logística como referência
6. Com a matriz demonstrativa, a utilidade esperada vira dois limiares: aprovar abaixo de 0,10, análise manual até 0,60, rejeitar acima
7. Os limiares se movem com a perda e o custo da análise; com custo alto, a análise manual desaparece
8. No desenvolvimento, o TAN ficou abaixo do Naive Bayes nas cinco métricas; NB e logística ficaram a 0,001 de ROC-AUC
9. No teste, as diferenças de ROC-AUC entre os três modelos ficaram entre 0,001 e 0,022, abaixo de 0,03: pela regra, são ruído
10. No teste, o Brier do TAN (0,215) ficou acima do da taxa base (0,210): o TAN não foi melhor que prever a taxa base
11. Com o TAN, a política de três ações teve utilidade média 22,5 maior que o corte 0,5 (IC 95% de 9,2 a 37,2), uma vantagem que a matriz garante por construção
12. O estudo de seleção secundário escolheu NB com BDeu 50, a 0,001 de ROC-AUC da referência; a grade foi desenhada depois de ver o desenvolvimento
13. Os resultados valem para esta base, esta matriz demonstrativa e um analista infalível: é simulação, não política real
14. Separar risco e ação dá limiares explícitos por construção; o efeito medido favorece as três ações, sem causa e sem modelo recomendado

**Resultado: passa.** Ajustes feitos na revisão: (a) o slide 1 tinha só o título oficial, que é rótulo de tema; ganhou o subtítulo-afirmação; (b) o slide 11 dizia só o número, e a banca leria "a proposta é melhor": entrou "que a matriz garante por construção" no próprio título; (c) o slide 3 era "Pergunta de pesquisa" e virou afirmação sobre as duas partes; (d) a estrutura sugerida foi mantida (ordem e número), sem fundir nem cortar slides.

**Para cortar se o tempo apertar:** slide 12 (vai para o apêndice), depois slide 7 (sensibilidade vira resposta A4).

---

## Tabela de conferência: slide → arquivo/coluna → valor

Conferida com pandas (`uv run python -I -c`, só leitura) em 18/11/2026.

| Slide | Arquivo | Linha / coluna | Valor |
|---|---|---|---|
| 4, 11, 13 | resultados/predicoes_teste.csv | kredit (contagem de 0) | 200 linhas, 60 ruins |
| 4 | resultados/cortes.json | laufzeit, hoehe, alter | [12, 24], [1553, 3384], [28, 38] |
| 6, A7 | config/utilidade.json | acoes | aprovar 100/−400; rejeitar 0/0; análise 60/−40 (c = 40) |
| 6, 14 | derivado de config/utilidade.json | c/L, 1 − c/G | 0,10 e 0,60 |
| 7, A4 | resultados/sensibilidade.csv | 400/0 | 0,000 / 1,000 |
| 7, A4 | resultados/sensibilidade.csv | 400/40 | 0,100 / 0,600 |
| 7 | resultados/sensibilidade.csv | 200/70 | 0,333 / 0,333 |
| 7, A4 | resultados/sensibilidade.csv | 400/80 e 400/100 | 0,200 / 0,200 |
| A4 | resultados/sensibilidade.csv | 800/50 | 0,063 / 0,5 (da Tabela 4.8) |
| 8 | resultados/metricas_dev.csv | roc_auc_media nb / logreg / tan | 0,789 / 0,788 / 0,742 |
| 8 | resultados/metricas_dev.csv | roc_auc_desvio tan | 0,049 |
| 8, A1 | resultados/metricas_dev.csv | ece_media nb / tan / logreg | 0,093 / 0,152 / 0,095 |
| A1 | resultados/metricas_dev.csv | log_loss_media tan | 0,704 |
| 9 | resultados/metricas_teste.csv | roc_auc nb / tan / logreg | 0,7277 / 0,7063 / 0,7287 |
| 9 | resultados/metricas_teste.csv | diferenças | 0,001 / 0,021 / 0,022 |
| 9, A8 | resultados/metricas_teste.csv | roc_auc_ic_inf / sup tan | 0,623 / 0,789 |
| 9 | resultados/metricas_teste.csv | pr_auc nb / tan / logreg / taxa_base | 0,490 / 0,480 / 0,500 / 0,300 |
| 10, 14 | resultados/metricas_teste.csv | brier tan / taxa_base | 0,215 / 0,210 |
| 10 | resultados/metricas_teste.csv | brier nb / logreg | 0,199 / 0,191 |
| 10, A2 | resultados/metricas_teste.csv | ece nb / tan / logreg | 0,115 / 0,157 / 0,078 |
| 11, 13, 14 | resultados/diferenca_politicas_teste.csv | tan: dif, ic_inf, ic_sup | 22,5 / 9,2 / 37,2 |
| 11, A7 | resultados/diferenca_politicas_teste.csv | nb / logreg / sel | 29,5 / 38,3 / 34,4 |
| 11 | resultados/resumo_politicas_teste.csv | tan/ue: aprovar, rejeitar, análise, mudam | 92 / 48 / 60 / 60 |
| 11 | resultados/resumo_politicas_teste.csv | tan/limiar: aprovar, rejeitar | 145 / 55 |
| 12 | resultados/selecao_escolha.csv | escolhida (folds 0–4 e dev) | nb_ess50 em todas |
| 12 | resultados/selecao_dev.csv | roc_auc_media aninhado / nb_ess5 | 0,788 / 0,789 |
| A1 | resultados/selecao_dev.csv | log_loss_media tan_ess1 / tan_ess50 | 0,825 / 0,583 |
| A1 | resultados/tan_arestas.csv | arestas por fold; origem = verw | 39 cada; 9, 8, 8, 7, 8 |

Números que **não** vêm de CSV: data 17/11/2026 e *commit* 49d77ff (docs/decisoes.md §1, via monografia §3.2); 800 dev / 240 ruins (monografia §3.2; não conferido em `dados/processados/dev.csv`, que este plano não abriu).

---

## Academic QA checklist (aplicado a este plano)

- [x] Every content slide has an action title (complete sentence stating the takeaway)
- [x] Ghost deck test passes (action titles alone tell the full argument)
- [x] One exhibit per results slide; each exhibit has a "so what" annotation (slides 8–12; a calibração do teste foi para o A2 para manter um exibidor no slide 10)
- [x] Every borrowed figure or data point has an in-slide citation (slides 2, 4, 5, 6, 9, 10; as figuras são todas próprias)
- [x] A References slide exists at the end (slide R, logo após as conclusões; ver nota de estrutura)
- [x] Conclusions slide is the last non-appendix slide (slide 14)
- [ ] Contact information and/or QR code/link on the final slide: lugar previsto, **dado a preencher pelo autor**
- [x] Font sizes are readable from the back of a room (≥ 20 pt body text): previsto; `sensibilidade.png` e os `calibracao_*.png` precisam ser conferidos ou refeitos em fonte ≥ 16 pt
- [x] No decorative elements that don't carry content
- [x] Section dividers or breadcrumb bar present for decks > 15 slides: não se aplica (14 slides de corpo); barra de seções opcional

---

## O que o autor decide

1. Tempo real da defesa e da arguição (este plano supõe ~20 min); se for 15 min, cortar 12 e 7.
2. Modelo de slides da UFU/FEELT (cores, logotipo, rodapé), ou o padrão da skill.
3. Contato no slide 14: e-mail, link do repositório ou QR code; foto, se quiser.
4. Data e local da defesa (capa da monografia ainda tem "[a preencher]").
5. Nome por extenso da faculdade na capa (a monografia marca "confirmar").
6. Se o estudo de seleção (slide 12) fica no corpo ou vai para o apêndice.
7. Se cita no slide R as entradas ainda marcadas para conferência (ELKAN, 2001 "A CONFERIR NO ORIGINAL"; GRÖMPING, 2019 "VERIFICAR").
8. Aviso: o campo `hipoteses` de `config/utilidade.json` ainda diz "Matriz pendente de aprovação do orientador"; a monografia e o slide 6 dizem "aprovada". Não foi alterado (fora do escopo).
9. Na monografia, o estudo de seleção aparece como "decidido por delegação, a rever pelo autor"; os slides e notas omitem essa expressão. Confirmar se o autor já revisou e como quer dizer isso à banca.
