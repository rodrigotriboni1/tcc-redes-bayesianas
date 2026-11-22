# 6 CONCLUSÃO

Este trabalho perguntou (1) se uma política que separa a estimativa de risco da escolha da ação tem limiares explícitos e reprodutíveis e (2) que efeito ela produz, em ações e utilidade média, em comparação com um limiar fixo de 0,5. A estimativa de risco é feita por rede bayesiana, com calibração medida, e a escolha da ação, por utilidade esperada.

## 6.1 Limiares explícitos e reprodutíveis

A primeira parte é respondida pela construção da política, não pelo desempenho dos modelos. Como a utilidade esperada de cada ação é linear na probabilidade estimada *p* de o caso ser ruim, a escolha da ação de maior utilidade equivale a uma regra de limiares sobre *p* (Capítulo 3, Seção 3.7). Com a matriz demonstrativa, a análise manual é escolhida quando *c*/400 ≤ *p* ≤ 1 − *c*/100; com *c* = 40, a faixa vai de 0,10 a 0,60. Dadas a matriz em `config/utilidade.json` e a coluna de probabilidade, qualquer pessoa obtém a ação de cada caso e as fronteiras. A resposta à primeira parte é, portanto, afirmativa, com uma ressalva que o próprio plano registra: essa propriedade vale para qualquer escore de probabilidade e não distingue a rede bayesiana da regressão logística. Ela também é teoria conhecida, e não achado do experimento (Seção 1.4): o trabalho a implementa e a torna reprodutível.

Quanto aos objetivos de sensibilidade e de demonstração (Seção 1.3), os limiares se movem com a perda e o custo da análise (Tabela 4.7) e a demonstração mostra um caso (Tabela 4.8); nenhum valor foi escolhido.

## 6.2 Efeito medido nas ações e na utilidade média

A segunda parte é respondida pelo conjunto de teste, aberto uma única vez em 17/11/2026, com 200 casos, dos quais 60 ruins. O critério de leitura é a diferença pareada de utilidade média entre a política de três ações por utilidade esperada e o corte 0,5 de duas ações, com intervalo de 95% por *bootstrap* (Tabela 4.6); o nível de 95% segue a decisão do autor registrada na §8 do plano de análise.

Na comparação principal, com o TAN, a diferença foi de 22,5, com intervalo de 9,2 a 37,2. Pela regra pré-registrada, observa-se diferença a favor da política de três ações, com intervalo que exclui zero; não se afirma causa. Nas ações, a política de três ações aprovou 92, rejeitou 48 e encaminhou 60 casos para análise manual, contra 145 aprovações e 55 rejeições do corte 0,5; os 60 casos que mudaram de ação são exatamente os encaminhados para análise manual.

Vale a ressalva da Seção 5.5: a diferença mistura modelo, representação e conjunto de ações, e não é chamada de efeito da regra nem do modelo. Como a base não registra o desfecho das ações não tomadas, trata-se de uma simulação metodológica, não da validação de uma política real.

Quanto ao risco estimado, o teste mostrou diferenças de ROC-AUC entre os três modelos de 0,001 a 0,022, todas abaixo de 0,03 e, pela regra pré-registrada, tratadas como ruído. O Brier do TAN, 0,215, foi maior que o da taxa base, 0,210: no teste, o TAN não foi melhor que prever a taxa base. As PR-AUC foram 0,490 (*Naive Bayes*), 0,480 (TAN) e 0,500 (regressão logística), contra 0,300 da taxa base; por decisão do autor registrada em docs/decisoes.md, essa métrica não tem regra de ruído e os valores são apenas descritos. O ECE foi 0,115, 0,157 e 0,078, respectivamente, e foi apenas medido. Os resultados de desenvolvimento e os do teste são distintos e não se substituem (Seção 4.1).

## 6.3 Limitações essenciais

As conclusões acima valem dentro de limites discutidos no Capítulo 5: a matriz de utilidade é demonstrativa, aprovada pelo orientador, com valores não calibrados com dados reais, e supõe analista infalível (Seção 5.5); a camada de decisão é simulação, não política real (Seção 5.4); o teste tem 200 casos e 60 ruins, o que deixa intervalos largos (Seção 5.6); modelo e representação das variáveis variam juntos (Seção 5.7); o intervalo não cobre a variação do treino (Seção 5.8); e a calibração é só medida, sem correção (Seção 5.9). Os resultados não autorizam generalizar para outras bases nem recomendar um modelo. As direções gerais de continuação estão na Seção 5.10.
