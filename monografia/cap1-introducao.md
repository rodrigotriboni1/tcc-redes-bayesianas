# 1 Introdução

<!-- rascunho; fonte: proposta (docs/proposta/), PLANO.md itens 1 a 4, 11 e 12, docs/plano-de-analise.md §1, docs/decisoes.md -->

## 1.1 Contexto

A automação de decisões é uma das aplicações mais difundidas de técnicas estatísticas e de inteligência artificial em sistemas de negócio. A concessão de crédito é o exemplo clássico: modelos de escore atribuem pesos a variáveis do solicitante, em geral por regressão logística, e a decisão de aprovar ou recusar resulta da comparação desse escore com um ponto de corte \cite{thomas2000,siddiqi2012}. A interpretabilidade e a facilidade de auditoria explicam a adoção dessa prática pela indústria \cite{thomas2000,siddiqi2012}.

Nesse arranjo, duas tarefas de natureza distinta ficam fundidas em uma única regra. A primeira é estimar o risco do caso, isto é, a probabilidade de um desfecho desfavorável dada a evidência observada. A segunda é escolher uma ação diante dessa estimativa, o que depende dos custos e benefícios de cada combinação de ação e desfecho. Quando o ponto de corte é fixado sem referência explícita a esses custos, o critério que de fato governa a recomendação permanece implícito, e a sensibilidade da decisão a mudanças nos critérios de negócio não pode ser examinada [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §1 e §1.1].

As redes bayesianas são modelos gráficos probabilísticos que representam dependências condicionais entre variáveis e permitem inferência sob incerteza \cite{pearl1988}. São, portanto, adequadas à primeira tarefa. Uma probabilidade estimada, contudo, não é por si só uma ação recomendada: a passagem do risco à ação exige uma camada de decisão separada, fundamentada na utilidade esperada [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §1]. Este trabalho investiga essa separação em um estudo de caso de crédito, organizando o sistema em uma camada probabilística, que estima a probabilidade de um crédito ser ruim, e uma camada de decisão, que escolhe a ação de maior utilidade esperada [fonte: PLANO.md §2]. Os conceitos envolvidos são apresentados no Capítulo 2.

<!-- LACUNA: fonte para a afirmação de que a regra de limiar sobre o escore mistura estimativa de risco e escolha de ação sem explicitar a função de utilidade (a proposta afirma isso sem citar; ver se thomas2000 ou siddiqi2012 sustentam no original, com página) -->

## 1.2 Pergunta de pesquisa

A pergunta que orienta o trabalho é a seguinte [fonte: PLANO.md §1; docs/plano-de-analise.md §1]:

> Uma política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) tem (1) limiares explícitos, que qualquer pessoa reproduz a partir da matriz de utilidade e de `p`, e (2) que efeito medido sobre as ações e a utilidade média, em comparação com um limiar fixo de 0,5?

As duas partes têm naturezas distintas. A parte 1 é uma propriedade da política: vale para qualquer escore e não depende de resultado experimental. A parte 2 é o que o experimento mede [fonte: docs/plano-de-analise.md §1]. A pergunta e o modo de ler cada desfecho foram fixados antes de existir qualquer resultado [fonte: docs/plano-de-analise.md, abertura].

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

O trabalho é um experimento composto por scripts que leem arquivos de dados e gravam tabelas e figuras [fonte: PLANO.md §3]. Não entrega produto, painel web, servidor, banco de dados nem modelo de linguagem [fonte: PLANO.md §2]. A matriz de utilidade é demonstrativa: não representa a política de nenhuma instituição, e o trabalho não usa dados nem sistemas proprietários [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx §1 e §1.1; PLANO.md §11.2].

## 1.5 Mudanças em relação à proposta

Quatro pontos mudaram em relação à proposta submetida. Cada um é listado com o motivo registrado na documentação do projeto [fonte: PLANO.md §11.4; docs/decisoes.md].

**Base de dados.** A proposta previa a German Credit Data; o trabalho usa a South German Credit, que é a versão corrigida da base citada na proposta \cite{gromping2019} [fonte: PLANO.md §4 e §11.4]. A divisão entre desenvolvimento e teste também foi refeita, com nova semente, porque o teste da divisão anterior já havia sido aberto para a regressão logística em um trabalho anterior [fonte: PLANO.md §4].

<!-- LACUNA: motivo da troca de base além de "versão corrigida" não está registrado em docs/decisoes.md; conferir em gromping2019 o que foi corrigido, com página -->

**Protótipo.** O protótipo previsto na proposta, que mostraria evidência, risco estimado, ação recomendada e justificativa, passou a ser uma demonstração em terminal, que recebe um caso e mostra o risco estimado e a utilidade de cada ação [fonte: PLANO.md §3 e §11.4]. A justificativa textual da recomendação ficou de fora: a demonstração mostra a conta (risco, utilidade de cada ação e fronteiras), e não uma explicação em texto [fonte: docs/decisoes.md, P15]. Uma interface de uma tela foi deixada para depois do experimento pronto [fonte: PLANO.md §12; docs/decisoes.md].

<!-- LACUNA: motivo da troca do protótipo por demonstração em terminal não está registrado em docs/decisoes.md -->

**Calibração.** A proposta previa calibrar as probabilidades; o trabalho apenas mede o erro de calibração, sem aplicar correção [fonte: PLANO.md §5; docs/decisoes.md, D4 e P1]. O motivo registrado é que a escolha de calibrar ou não depende de um número, e essa decisão cabe ao autor; aplicar a correção dependeria de olhar as métricas do desenvolvimento [fonte: docs/decisoes.md, D4 e P1]. A exigência de probabilidade calibrada para a decisão por custos vem da literatura, e não do experimento [fonte: docs/decisoes.md, P2]; ela é discutida no Capítulo 2.

**Pergunta de pesquisa.** A proposta perguntava se a política baseada em probabilidades calibradas e utilidade esperada produz decisões mais consistentes e transparentes que a política por escore e limiar [fonte: docs/proposta/TCC_Research_Proposal_Rodrigo_English.docx, Resumo e §3, etapa A]. A pergunta foi reformulada nas duas partes da Seção 1.2 [fonte: docs/decisoes.md, P3]. O motivo registrado é que "consistentes" e "transparentes" não eram medidos; uma redação intermediária, "mais auditáveis", foi descartada porque contradizia a proposta, que chama regras e escores de auditáveis, valia por construção para qualquer escore e deixava a rede sem papel [fonte: docs/decisoes.md, P3]. A forma em duas partes separa a propriedade da política do efeito medido, e a troca de "calibrada" por "com calibração medida" acompanha a mudança anterior [fonte: docs/decisoes.md, P1 e P3].

Uma quinta redução também está registrada: a análise exploratória prevista na proposta limita-se a uma tabela de descrição da base, apresentada no Capítulo 3 [fonte: docs/decisoes.md, P12].

## 1.6 Organização do texto

O Capítulo 2 apresenta a fundamentação: redes bayesianas, calibração, utilidade esperada, limiares derivados de custos e escore de crédito. O Capítulo 3 descreve a base de dados, o protocolo de validação, os modelos, as métricas e a política de decisão. O Capítulo 4 relata os resultados preditivos, os da política de decisão e os da análise de sensibilidade. O Capítulo 5 discute os resultados e as limitações do trabalho. O Capítulo 6 conclui, respondendo às duas partes da pergunta de pesquisa [fonte: monografia/esqueleto.md].
