# Elementos pré-textuais

Rascunho em Markdown, na ordem exigida pela FEELT (ver `monografia/esqueleto.md`). Os números de página são marcadores (`p. __`) e só podem ser preenchidos quando o texto for para Word ou LaTeX, com o modelo do Colegiado. Tudo o que não consta no repositório está como `[a preencher pelo autor]`.

<!-- Formatação final (esqueleto.md): Times New Roman ou Arial 12; capítulos em página ímpar; títulos de capítulo em 14, negrito, caixa alta. -->

---

## CAPA

**UNIVERSIDADE FEDERAL DE UBERLÂNDIA (UFU)** <!-- confirmar: o repositório traz apenas a sigla UFU (PLANO.md); nome por extenso e faculdade a conferir no modelo do Colegiado -->

[Faculdade e curso conforme o modelo do Colegiado — a preencher pelo autor]

Curso: Engenharia de Controle e Automação

**RODRIGO MIALICHI TRIBONI**

**REDES BAYESIANAS E UTILIDADE ESPERADA APLICADAS À SELEÇÃO DE *NEXT BEST ACTION* EM SISTEMAS AUTOMATIZADOS DE DECISÃO** <!-- confirmar: título conforme PLANO.md; conferir com a proposta -->

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

<!-- Ficha catalográfica (verso da folha de rosto): [a preencher pelo autor], se exigida pelo modelo do Colegiado. -->
<!-- Folha de aprovação: data da defesa, banca e notas — [a preencher pelo autor]. Não há dados no repositório. -->
<!-- Dedicatória e agradecimentos: opcionais (esqueleto.md); [a preencher pelo autor], se houver. -->

---

## LISTA DE FIGURAS

Figura 4.1 – Diagramas de confiabilidade no desenvolvimento (`resultados/calibracao_dev.png`). ........ p. __

Figura 4.2 – Diagramas de confiabilidade no conjunto de teste (n=200; 60 ruins) (`resultados/calibracao_teste.png`). ........ p. __

Figura 4.3 – Limiares da política em função da perda e do custo da análise manual (`resultados/sensibilidade.png`). ........ p. __

---

## LISTA DE TABELAS

<!-- Títulos copiados dos capítulos, sem a parte entre colchetes [fonte: ...]. Tabelas 3.1 e 3.2 aparecem no capítulo 3 como "Tabela 3.x — ..." (sem negrito, travessão longo); aqui seguem o padrão dos demais. Na 3.1 foi copiada só a primeira frase da legenda; o restante é nota sobre as categorias. -->

Tabela 3.1 – Dicionário das variáveis ........ p. __

Tabela 3.2 – Descrição do conjunto de desenvolvimento (n=800), calculada a partir de `dados/processados/dev.csv`. ........ p. __

Tabela 4.1 – Métricas por modelo no desenvolvimento, média (desvio) entre 5 partições ........ p. __

Tabela 4.2 – Arestas do TAN por partição ........ p. __

Tabela 4.3 – Métricas por modelo no conjunto de teste (n=200; 60 ruins), valor [intervalo de 95%] ........ p. __

Tabela 4.4 – Variação de métricas ao esconder uma variável, seleção de linhas ........ p. __

Tabela 4.5 – Política de três ações por utilidade esperada contra corte 0,5 de duas ações, desenvolvimento ........ p. __

Tabela 4.6 – Política de três ações contra corte 0,5 de duas ações, conjunto de teste (n=200; 60 ruins) ........ p. __

Tabela 4.7 – Diferença pareada de utilidade média (`ue` − `limiar`), conjunto de teste (n=200; 60 ruins) ........ p. __

Tabela 4.8 – Limiares da política por perda e custo da análise manual, seleção de linhas ........ p. __

Tabela 4.9 – Saída de `codigo/demo.py` para o caso sgc-0000 ........ p. __

Tabela 4.10 – Métricas das 8 configurações e da seleção aninhada, média (desvio) entre 5 partições externas ........ p. __

Tabela 4.11 – Log loss interno por partição externa, seleção de colunas ........ p. __

---

## LISTA DE QUADROS

<!-- Os capítulos e apêndices também têm quadros (numeração própria). Manter esta lista só se o modelo do Colegiado a admitir; senão, fundir com a lista de tabelas. -->

Quadro 3.1 – Matriz de utilidade demonstrativa ........ p. __

Quadro A.1 – Comandos, em ordem, e arquivos gravados ........ p. __

---

## LISTA DE SIGLAS E ABREVIATURAS

<!-- Só siglas que aparecem nos capítulos. Significado dado quando o próprio texto o traz; senão, "confirmar". -->

BDeu – *Bayesian Dirichlet equivalent uniform* (prior usado no aprendizado de parâmetros, seção 2.3)

CSV – <!-- confirmar: o texto usa a sigla (cap. 3, seção 3.11) sem expandi-la -->

ECE – Erro esperado de calibração (seção 2.5)

NB – <!-- confirmar: usada nos capítulos 3 a 5 como abreviatura de *Naive Bayes*, mas a sigla não é introduzida no texto -->

PR-AUC – <!-- confirmar: o texto não expande a sigla; é a métrica de precisão e revocação (seção 3.6) -->

ROC-AUC – Área sob a curva ROC (seção 2.5)

TAN – *Tree-Augmented Naive Bayes*, Naive Bayes aumentado por árvore (seções 2.2 e 3.5)

UCI – <!-- confirmar: o texto cita o "repositório da UCI" (seção 3.1) sem expandir a sigla -->

FEELT – <!-- confirmar: não aparece mais no texto; retirar se continuar assim -->

UFU – <!-- confirmar: aparece só em PLANO.md, sem expansão; ver capa -->

---

## SUMÁRIO

RESUMO ........ p. __

ABSTRACT ........ p. __

LISTA DE FIGURAS ........ p. __

LISTA DE TABELAS ........ p. __

LISTA DE QUADROS ........ p. __

LISTA DE SIGLAS E ABREVIATURAS ........ p. __

**1 INTRODUÇÃO** ........ p. __

- 1.1 Contexto ........ p. __
- 1.2 Pergunta de pesquisa ........ p. __
- 1.3 Objetivos ........ p. __
- 1.4 O que o trabalho não faz ........ p. __
- 1.5 Mudanças em relação à proposta ........ p. __
- 1.6 Organização do texto ........ p. __

**2 FUNDAMENTAÇÃO** ........ p. __

- 2.1 Redes bayesianas ........ p. __
- 2.2 Naive Bayes e TAN ........ p. __
- 2.3 Aprendizado de parâmetros e prior BDeu ........ p. __
- 2.4 Inferência exata ........ p. __
- 2.5 Calibração ........ p. __
- 2.6 Utilidade esperada ........ p. __
- 2.7 Limiares derivados dos custos ........ p. __
- 2.8 Opção de rejeição ........ p. __
- 2.9 Escore de crédito e *next best action* ........ p. __

**3 MATERIAIS E MÉTODOS** ........ p. __

- 3.1 Base de dados ........ p. __
- 3.2 Divisão em desenvolvimento e teste ........ p. __
- 3.3 Validação cruzada ........ p. __
- 3.4 Discretização ........ p. __
- 3.5 Modelos de risco ........ p. __
- 3.6 Métricas ........ p. __
- 3.7 Camada de decisão por utilidade esperada ........ p. __
- 3.8 Análise de sensibilidade ........ p. __
- 3.9 Demonstração ........ p. __
- 3.10 Estudo de seleção aninhado (secundário) ........ p. __
- 3.11 Ambiente e reprodutibilidade ........ p. __

**4 RESULTADOS** ........ p. __

- 4.1 Desempenho preditivo ........ p. __
- 4.2 Evidência incompleta ........ p. __
- 4.3 Política de decisão ........ p. __
- 4.4 Sensibilidade ........ p. __
- 4.5 Demonstração ........ p. __
- 4.6 Estudo de seleção (secundário) ........ p. __

**5 DISCUSSÃO E LIMITAÇÕES** ........ p. __

- 5.1 Leitura do desenvolvimento ........ p. __
- 5.1b Leitura do teste final ........ p. __
- 5.2 Estudo de seleção ........ p. __
- 5.3 Simulação, não política real ........ p. __
- 5.4 Matriz demonstrativa e analista infalível ........ p. __
- 5.5 Tamanho do teste ........ p. __
- 5.6 Modelo e representação variam juntos ........ p. __
- 5.7 O que o intervalo não cobre ........ p. __
- 5.8 Calibração só medida ........ p. __
- 5.9 Escopo das entregas ........ p. __
- 5.10 Direções futuras ........ p. __

**6 CONCLUSÃO** ........ p. __

- 6.1 Limiares explícitos e reprodutíveis ........ p. __
- 6.2 Efeito medido nas ações e na utilidade média ........ p. __
- 6.3 Limitações essenciais ........ p. __

**REFERÊNCIAS** ........ p. __

**APÊNDICES** ........ p. __

- APÊNDICE A – Como reproduzir os resultados ........ p. __
- APÊNDICE B – Resultados dos três modelos ........ p. __
- APÊNDICE C – Plano de análise ........ p. __

<!-- Conferir no texto final: a seção "5.1b" tem numeração provisória (cap5-discussao.md). Os títulos do capítulo 2 vêm de dois arquivos (2.1–2.5 e 2.6–2.9). Os anexos (se houver) ainda não existem no repositório. -->
