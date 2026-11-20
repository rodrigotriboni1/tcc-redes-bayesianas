# Elementos pré-textuais

Rascunho em Markdown, na ordem exigida pela FEELT (ver `monografia/esqueleto.md`). Os números de página são marcadores (`p. __`) e só podem ser preenchidos quando o texto for para Word ou LaTeX, com o modelo do Colegiado. Tudo o que não consta no repositório está como `[a preencher pelo autor]`.

---

## CAPA

**UNIVERSIDADE FEDERAL DE UBERLÂNDIA (UFU)** 

[Faculdade e curso conforme o modelo do Colegiado — a preencher pelo autor]

Curso: Engenharia de Controle e Automação

**RODRIGO MIALICHI TRIBONI**

**REDES BAYESIANAS E UTILIDADE ESPERADA APLICADAS À SELEÇÃO DE *NEXT BEST ACTION* EM SISTEMAS AUTOMATIZADOS DE DECISÃO** 

[Local — a preencher pelo autor]

[Ano — a preencher pelo autor]

<!-- quebra de página -->

---

## FOLHA DE ROSTO

**RODRIGO MIALICHI TRIBONI**

**REDES BAYESIANAS E UTILIDADE ESPERADA APLICADAS À SELEÇÃO DE *NEXT BEST ACTION* EM SISTEMAS AUTOMATIZADOS DE DECISÃO**

[Natureza do trabalho e objetivo (por exemplo, trabalho de conclusão de curso, grau pretendido), instituição e curso, conforme o modelo do Colegiado — a preencher pelo autor]

Curso: Engenharia de Controle e Automação

Orientador: Fabio Vincenzi

[Titulação do orientador — a preencher pelo autor]

[Local — a preencher pelo autor]

[Ano — a preencher pelo autor]

---

## LISTA DE FIGURAS

Figura 4.1 – Diagramas de confiabilidade no desenvolvimento (`resultados/calibracao_dev.png`)......... p. __

Figura 4.2 – Diagramas de confiabilidade no conjunto de teste (n=200; 60 ruins) (`resultados/calibracao_teste.png`)......... p. __

Figura 4.3 – Limiares da política em função da perda e do custo da análise manual (`resultados/sensibilidade.png`)......... p. __

---

## LISTA DE TABELAS

Tabela 3.1 – Dicionário das variáveis........ p. __

Tabela 3.2 – Descrição do conjunto de desenvolvimento (n=800), calculada a partir de `dados/processados/dev.csv`......... p. __

Tabela 4.1 – Métricas por modelo no desenvolvimento, média (desvio) entre 5 partições........ p. __


Tabela 4.2 – Métricas por modelo no conjunto de teste (n=200; 60 ruins), valor [intervalo de 95%]........ p. __

Tabela 4.3 – Variação de métricas ao esconder uma variável, seleção de linhas........ p. __

Tabela 4.4 – Política de três ações por utilidade esperada contra corte 0,5 de duas ações, desenvolvimento........ p. __

Tabela 4.5 – Política de três ações contra corte 0,5 de duas ações, conjunto de teste (n=200; 60 ruins)........ p. __

Tabela 4.6 – Diferença pareada de utilidade média (`ue` − `limiar`), conjunto de teste (n=200; 60 ruins)........ p. __

Tabela 4.7 – Limiares da política por perda e custo da análise manual, seleção de linhas........ p. __

Tabela 4.8 – Saída de `codigo/demo.py` para o caso sgc-0000........ p. __

Tabela 4.9 – Métricas das 8 configurações e da seleção aninhada, média (desvio) entre 5 partições externas........ p. __

Tabela 4.10 – Log loss interno por partição externa, seleção de colunas........ p. __

---

## LISTA DE QUADROS

Quadro 3.1 – Matriz de utilidade demonstrativa........ p. __

Quadro A.1 – Comandos, em ordem, e arquivos gravados........ p. __

---

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

---

## SUMÁRIO

RESUMO........ p. __

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
- 2.2 Naive Bayes e TAN........ p. __
- 2.3 Aprendizado de parâmetros e prior BDeu........ p. __
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
- 3.6 Métricas........ p. __
- 3.7 Camada de decisão por utilidade esperada........ p. __
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
- 5.2 Estudo de seleção........ p. __
- 5.3 Simulação, não política real........ p. __
- 5.4 Matriz demonstrativa e analista infalível........ p. __
- 5.5 Tamanho do teste........ p. __
- 5.6 Modelo e representação variam juntos........ p. __
- 5.7 O que o intervalo não cobre........ p. __
- 5.8 Calibração só medida........ p. __
- 5.9 Escopo das entregas........ p. __
- 5.10 Direções futuras........ p. __

**6 CONCLUSÃO**........ p. __

- 6.1 Limiares explícitos e reprodutíveis........ p. __
- 6.2 Efeito medido nas ações e na utilidade média........ p. __
- 6.3 Limitações essenciais........ p. __

**REFERÊNCIAS**........ p. __

**APÊNDICES**........ p. __

- APÊNDICE A – Como reproduzir os resultados........ p. __
- APÊNDICE B – Plano de análise........ p. __
