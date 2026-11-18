# Esqueleto da monografia

Estrutura provisória. Está em Markdown porque o modelo do Colegiado ainda não foi encontrado (ver `docs/decisoes.md`, seção 7); quando chegar, o conteúdo vai para Word ou LaTeX.

Como ler os comentários `<!-- -->`:
- **fonte:** arquivo de `resultados/` ou documento do repositório que preenche a seção. Todo número do texto tem de apontar para um arquivo.
- **refs:** chaves de `monografia/referencias.bib`, do mapa em `docs/mapa-de-referencias.md`.
- **pendente:** o que ainda não existe.

Estrutura exigida pela FEELT: capa, folha de rosto, sumário, listas, resumo e abstract (150 a 500 palavras, cinco palavras-chave), capítulos, referências ABNT NBR 6023-2018, anexos e apêndices. Times New Roman ou Arial 12; capítulos em página ímpar; títulos de capítulo em 14, negrito, caixa alta.

---

## Pré-textuais

- Capa e folha de rosto
- Dedicatória e agradecimentos (opcionais)
- Resumo (150 a 500 palavras, cinco palavras-chave)
- Abstract (150 a 500 palavras, cinco keywords)
- Sumário
- Lista de figuras, lista de tabelas e lista de siglas

<!-- pendente: escrever por último, depois dos capítulos. Modelo do Colegiado. -->

---

## 1 Introdução

<!-- fonte: proposta (docs/proposta/), PLANO.md itens 1 e 2, docs/plano-de-analise.md seção 1 -->
<!-- refs: thomas2000, siddiqi2012, pearl1988 -->

- 1.1 Contexto: decisão automatizada mistura estimativa de risco e escolha de ação
- 1.2 Pergunta de pesquisa (as duas partes)
- 1.3 Objetivos
- 1.4 O que o trabalho não faz (produto, painel, servidor, banco de dados, modelo de linguagem)
- 1.5 Mudanças em relação à proposta, com o motivo: base South German Credit, protótipo em terminal, calibração só medida, nova pergunta

---

## 2 Fundamentação

<!-- fonte: proposta, docs/mapa-de-referencias.md -->

- 2.1 Redes bayesianas <!-- refs: pearl1988, koller2009, russell2010 -->
- 2.2 Naive Bayes e TAN <!-- refs: friedman1997, chowliu1968 -->
- 2.3 Aprendizado de parâmetros e prior BDeu <!-- refs: koller2009, heckerman1995 -->
- 2.4 Inferência exata <!-- refs: koller2009, jensen2007 -->
- 2.5 Calibração: Platt e isotônica como métodos da literatura, sem aplicar <!-- refs: brier1950, naeini2015, guo2017, platt1999, zadrozny2002, niculescu2005 -->
- 2.6 Utilidade esperada <!-- refs: russell2010, jensen2007, howard2005, koller2009 -->
- 2.7 Limiares derivados dos custos <!-- refs: elkan2001 --> (a exigência de probabilidade calibrada vem da literatura, não do experimento)
- 2.8 Opção de rejeição <!-- refs: chow1970 -->
- 2.9 Escore de crédito e *next best action* <!-- refs: thomas2000, siddiqi2012, hand1997 -->

<!-- pendente: as 15 referências a conferir no original antes de citar -->

---

## 3 Materiais e métodos

<!-- fonte: PLANO.md itens 3 a 8, docs/arquitetura.md, docs/decisoes.md, docs/glossario.md -->

- 3.1 Base de dados: South German Credit; 20 variáveis e o alvo; 800 casos de desenvolvimento e 200 de teste <!-- refs: hofmann1994, gromping2019, uci573 --> <!-- fonte do dicionário: docs/glossario.md (tradução a conferir) -->
- 3.2 Análise exploratória: tabela de descrição da base (contagens, categorias raras, as três contínuas) <!-- fonte: dev.csv e dicionário; sem script (decisão P12) --> <!-- pendente: contagens da base completa a conferir no sgc.csv -->
- 3.3 Divisão e validação: semente 2026, 5 partições estratificadas; o teste fica fechado até o passo 10 <!-- refs: kaufman2012 -->
- 3.4 Discretização por tercis, cortes aprendidos só no treino <!-- fonte: resultados/cortes.json -->
- 3.5 Modelos: Naive Bayes, TAN, regressão logística; prior BDeu de tamanho 5; o espaço de estados fixado no dev inteiro, declarado como vazamento brando <!-- refs: ankan2024, pedregosa2011 -->
- 3.6 Métricas e intervalos <!-- refs: brier1950, naeini2015, efron1993 --> <!-- fonte: docs/plano-de-analise.md seções 2 e 4 -->
- 3.7 Camada de decisão: matriz de utilidade, hipóteses, desempate <!-- fonte: config/utilidade.json (criado na issue 04) -->
- 3.8 Reprodutibilidade <!-- fonte: docs/reproduzir.md -->

---

## 4 Resultados

<!-- fonte: resultados/. Nenhum número entra sem apontar para um arquivo. Resultado ruim entra como saiu. -->

### 4.1 Desempenho preditivo
<!-- fonte: metricas_dev.csv, calibracao_dev.png, tan_arestas.csv; no teste: metricas_teste.csv, calibracao_teste.png -->
<!-- feito: issues 01 e 02 (resultados/metricas_dev.csv etc.). Falta: passo 10 (teste final, só o autor) -->

### 4.2 Evidência incompleta
<!-- fonte: evidencia_incompleta.csv; ressalva: redes marginalizam, logística imputa (decisão P9) -->
<!-- feito: issue 03 (resultados/evidencia_incompleta.csv) -->

### 4.3 Política de decisão
<!-- fonte: resumo_politicas_dev.csv, politicas_dev.csv; no teste: resumo_politicas_teste.csv, diferenca_politicas_teste.csv -->
<!-- texto da tabela 2×2: "política de três ações por utilidade esperada contra corte 0,5 de duas ações" (decisão P8) -->
<!-- feito: issues 04 e 07 (resumo_politicas_dev.csv, politicas_dev.csv). Falta: passo 10 -->

### 4.4 Sensibilidade
<!-- fonte: sensibilidade.csv, sensibilidade.png -->
<!-- feito: issue 05 (resultados/sensibilidade.csv) -->

### 4.5 Demonstração
<!-- fonte: saída de codigo/demo.py para um caso -->
<!-- feito: issue 06 (codigo/demo.py) -->

### 4.6 Estudo de seleção (secundário)
<!-- fonte: resultados/selecao_dev.csv (8 configurações, linha "aninhado"), resultados/selecao_escolha.csv (escolha por externa e linha dev) -->
<!-- relatar as 8 linhas, o número de comparações (8) e a linha "aninhado", qualquer que seja o resultado (plano de análise §9) -->
<!-- declaração obrigatória de viés (§9): a grade foi definida depois de ver metricas_dev.csv e motivada por ele (TAN pior que NB; hipótese verw). O aninhamento corrige o viés de escolher entre as 8 configurações, não o de desenhar a grade olhando o mesmo dev -->
<!-- feito: issues 08, 10 e 11 (resultados/selecao_dev.csv etc.). Falta: p_sel no teste, só o autor -->

---

## 5 Discussão e limitações

<!-- fonte: docs/plano-de-analise.md seção 6 -->

- Simulação, não política real: a base não traz o resultado das ações não tomadas
- Teste com 60 casos ruins: diferenças pequenas são ruído
- Matriz demonstrativa e analista infalível; a política de três ações ganha por construção do corte de duas ações
- Logística com contínuas originais contra redes com faixas: modelo e representação variam juntos
- Intervalo por bootstrap não cobre a variação do treino
- Calibração só medida, sem correção
- Análise exploratória limitada à descrição da base; sem justificativa textual da recomendação no demo; a interface de uma tela, se existir, vem depois do experimento

---

## 6 Conclusão

<!-- fonte: capítulo 4 e a pergunta do capítulo 1. Responder às duas partes. Escrever por último. -->

---

## Referências

<!-- fonte: monografia/referencias.bib; ABNT NBR 6023-2018, autor e ano, ordem alfabética -->

---

## Apêndices

- A: como reproduzir <!-- fonte: docs/reproduzir.md -->
- B: resultados dos três modelos em todas as tabelas
- C: plano de análise <!-- fonte: docs/plano-de-analise.md -->
