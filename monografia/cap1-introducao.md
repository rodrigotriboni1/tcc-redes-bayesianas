# 1 INTRODUÇÃO

## 1.1 Contexto

Na concessão de crédito, decisões automatizadas costumam apoiar-se em modelos de escore que atribuem pesos a variáveis do solicitante, em geral por regressão logística, e a decisão de aprovar ou rejeitar resulta da comparação desse escore com um ponto de corte \cite{thomas2000,siddiqi2006}. A interpretabilidade e a facilidade de auditoria explicam a adoção dessa prática pela indústria \cite{thomas2000,siddiqi2006}. 

Nesse arranjo, duas tarefas de natureza distinta ficam fundidas em uma única regra. A primeira é estimar o risco do caso, isto é, a probabilidade de um desfecho desfavorável dada a evidência observada. A segunda é escolher uma ação diante dessa estimativa, o que depende dos custos e benefícios de cada combinação de ação e desfecho. Quando o ponto de corte é fixado sem referência explícita a esses custos, o critério que de fato governa a recomendação permanece implícito, e a sensibilidade da decisão a mudanças nos critérios de negócio não pode ser examinada.

As redes bayesianas são modelos gráficos probabilísticos que representam dependências condicionais entre variáveis e permitem inferência sob incerteza \cite{pearl1988}. São, portanto, adequadas à primeira tarefa. Uma probabilidade estimada não é uma ação recomendada, e passar do risco à ação exige uma camada de decisão separada, fundamentada na utilidade esperada. Este trabalho investiga essa separação em um estudo de caso de crédito, com uma camada probabilística, que estima a probabilidade de um crédito ser ruim, e uma camada de decisão, que escolhe a ação de maior utilidade esperada. Os conceitos envolvidos são apresentados no Capítulo 2.

## 1.2 Pergunta de pesquisa

A pergunta que orienta o trabalho é a seguinte:

> Uma política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) apresenta limiares explícitos e reproduzíveis a partir da matriz de utilidade e da probabilidade estimada `p`? Que diferenças são observadas nas ações escolhidas e na utilidade média simulada em relação a uma política de duas ações com limiar fixo de 0,5?

A primeira parte (limiares explícitos) é uma propriedade da política: vale para qualquer escore e não depende de resultado experimental. A segunda parte (diferenças observadas) é o que o experimento mede. A pergunta e o modo de ler cada desfecho foram fixados antes da obtenção dos resultados da análise primária, ressalvadas as decisões complementares posteriores descritas na Seção 3.6. Existe também um estudo de seleção secundário, desenhado depois de ver as métricas do desenvolvimento, cujo viés é declarado.

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

A avaliação do modelo de risco é feita separadamente da avaliação da política de decisão, como previsto na proposta. Como a base não registra o resultado das ações não tomadas, a camada de decisão é avaliada como simulação metodológica, não como validação de uma política real de concessão. O protocolo experimental é descrito no Capítulo 3.

## 1.4 O que o trabalho não faz

O trabalho é um experimento composto por *scripts* que leem arquivos de dados e gravam tabelas e figuras. Não desenvolve um produto operacional, painel web, servidor, banco de dados ou modelo de linguagem. A matriz de utilidade é demonstrativa: não representa a política de nenhuma instituição, e o trabalho não usa dados nem sistemas proprietários.

O trabalho também não propõe uma regra de tipo distinto do limiar: como a utilidade esperada de cada ação é uma reta em `p`, a política equivale a uma regra de limiares sobre `p`, e a contribuição é derivar esses limiares dos custos de forma explícita. A parte 1 da pergunta vale para qualquer escore e não distingue a rede da regressão logística. Os resultados não se generalizam a outras bases nem validam uma política real de concessão.

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

O Capítulo 2 apresenta a fundamentação: redes bayesianas, calibração, utilidade esperada, limiares derivados de custos e escore de crédito. O Capítulo 3 descreve a base de dados, o protocolo de validação, os modelos, as métricas e a política de decisão; o Capítulo 4 relata os resultados preditivos, os da política de decisão e os da análise de sensibilidade; o Capítulo 5 discute os resultados e as limitações; e o Capítulo 6 conclui, respondendo às duas partes da pergunta de pesquisa. Também são tratados a opção de rejeição (Seção 2.8), a evidência incompleta (Seção 4.2), a demonstração de um caso (Seções 3.9 e 4.5) e o estudo de seleção secundário (Seções 3.10 e 4.6).
