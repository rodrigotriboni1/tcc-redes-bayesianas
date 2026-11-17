# Mapa de referências

Liga cada seção da monografia às referências que a sustentam. As chaves são as de `monografia/referencias.bib`.

Situação de cada referência:

- **Proposta:** estava na proposta submetida.
- **Herdada:** já estava no arquivo de referências e continua servindo.
- **A conferir:** sugerida por IA de memória; só citar depois de abrir o original e conferir título, ano e páginas.

A coluna **Verificar** da tabela por referência diz o que falta conferir no original em cada entrada: 15 entradas ao todo (9 sugeridas por IA, 5 com marca `% VERIFICAR` no arquivo e `russell2010`, trocada em 15/11/2026).

Regra do trabalho (`uso-de-ia.md`): toda citação sai do original lido, com página. Resumo gerado por IA não é fonte.

## Por seção da monografia

| Seção | O que precisa ser sustentado | Referências |
|---|---|---|
| 1 Introdução | Decisão automatizada mistura risco e ação; escore de crédito como prática | `thomas2000`, `siddiqi2012`, `pearl1988` |
| 2.1 Redes bayesianas | Definição, grafo, tabelas de probabilidade, independência condicional | `pearl1988`, `koller2009`, `russell2010` |
| 2.2 Naive Bayes e TAN | Classificadores bayesianos; árvore de dependência | `friedman1997`, `chowliu1968` |
| 2.3 Aprendizado de parâmetros | Estimação bayesiana, prior BDeu, contagens pequenas | `koller2009`, `heckerman1995` |
| 2.4 Inferência | Eliminação de variáveis; evidência parcial | `koller2009`, `jensen2007` |
| 2.5 Calibração | O que é probabilidade calibrada; Brier; erro de calibração; Platt (sigmoide) e regressão isotônica como métodos da literatura, citados sem aplicar (o trabalho só mede a calibração) | `brier1950`, `naeini2015`, `guo2017`, `platt1999`, `zadrozny2002`, `niculescu2005` |
| 2.6 Utilidade esperada e diagramas de influência | Critério de máxima utilidade esperada; nós de decisão e de utilidade | `russell2010`, `jensen2007`, `howard2005`, `koller2009` |
| 2.7 Limiares derivados de custos | Com probabilidade calibrada, a decisão ótima é um limiar que sai da matriz de custos | `elkan2001` |
| 2.8 Opção de rejeição | Terceira ação (análise manual) como rejeição com custo | `chow1970` |
| 2.9 Escore de crédito e next best action | Regressão logística e scorecard como referência da indústria | `thomas2000`, `siddiqi2012`, `hand1997` |
| 3.1 Base de dados | Origem e correção da base | `hofmann1994`, `gromping2019`, `uci573` |
| 3.2 Divisão e validação | Vazamento de informação; validação cruzada | `kaufman2012` |
| 3.3 Modelos e ferramentas | Bibliotecas usadas | `ankan2024`, `pedregosa2011` |
| 3.4 Métricas e intervalos | Brier, calibração, bootstrap | `brier1950`, `naeini2015`, `efron1993` |
| Formatação | Normas | `abnt14724`, `abnt6023`, `abnt10520` |

As seções 2.7 e 2.8 sustentam a afirmação central do trabalho (item 5 do `PLANO.md`): a política por utilidade esperada equivale a limiares derivados dos custos. São resultados conhecidos e precisam estar citados.

## Por referência

| Chave | Obra | Situação | Verificar | Onde ler | Usada em |
| --- | --- | --- | --- | --- | --- |
| `koller2009` | Koller e Friedman, *Probabilistic Graphical Models* | Proposta | — | Capítulos de representação, eliminação de variáveis, estimação de parâmetros, aprendizado de estrutura e decisão (números a confirmar no sumário) | 2.1, 2.3, 2.4, 2.6 |
| `jensen2007` | Jensen e Nielsen, *Bayesian Networks and Decision Graphs* | Proposta | — | Parte de redes bayesianas e parte de grafos de decisão | 2.4, 2.6 |
| `russell2010` | Russell e Norvig, *Artificial Intelligence: A Modern Approach* (3ª ed., original) | Proposta | título, editora, cidade e ano (trocados da tradução para o original, de memória) | Capítulos de raciocínio probabilístico e de decisões simples | 2.1, 2.6 |
| `pearl1988` | Pearl, *Probabilistic Reasoning in Intelligent Systems* | Proposta | — | Só citação de origem | 1, 2.1 |
| `howard2005` | Howard e Matheson, *Influence diagrams* | Proposta | a proposta cita a reimpressão de 2005 do trabalho original de 1984 | Artigo inteiro | 2.6 |
| `siddiqi2012` | Siddiqi, *Credit Risk Scorecards* | Proposta | — | Capítulos de desenvolvimento do scorecard e de ponto de corte | 1, 2.9 |
| `thomas2000` | Thomas, *A survey of credit and behavioural scoring* | Proposta | — | Artigo inteiro | 1, 2.9 |
| `hofmann1994` | Base German Credit original | Proposta | — | Página da UCI | 3.1 |
| `brier1950` | Brier, escore de Brier | Proposta | — | Artigo (3 páginas) | 2.5, 3.4 |
| `gromping2019` | Grömping, correção da base | Herdada | série do relatório e instituição | Relatório inteiro; explica os códigos das variáveis | 3.1 |
| `uci573` | Base South German Credit | Herdada | ano de doação (2020) e forma de autoria recomendada pela UCI | Página da UCI | 3.1 |
| `platt1999` | Calibração por sigmoide (Platt); alternativa citada, o trabalho não a aplica | Herdada | ano do livro (1999 na capa; algumas bases citam 2000) e páginas | Seção de método | 2.5 |
| `naeini2015`, `guo2017` | Calibração | Herdada | — | Seções de método | 2.5, 3.4 |
| `kaufman2012` | Vazamento de informação | Herdada | número do artigo (15) e paginação | Seções de definição e de prevenção | 3.2 |
| `efron1993` | Bootstrap | Herdada | — | Capítulo de intervalos de confiança | 3.4 |
| `pedregosa2011` | scikit-learn | Herdada | — | Só citação | 3.3 |
| `friedman1997` | Classificadores bayesianos (TAN) | A conferir | tudo: título, ano, volume e páginas | Artigo; seções de Naive Bayes e TAN | 2.2 |
| `chowliu1968` | Árvores de dependência | A conferir | tudo: título, ano, volume e páginas | Artigo | 2.2 |
| `heckerman1995` | Prior BDeu | A conferir | tudo: título, ano, volume e páginas | Seções sobre o prior | 2.3 |
| `elkan2001` | Aprendizado sensível a custo | A conferir | tudo: título, ano, volume e páginas | Artigo (6 páginas); seção do limiar ótimo | 2.7 |
| `chow1970` | Opção de rejeição | A conferir | tudo: título, ano, volume e páginas | Artigo | 2.8 |
| `zadrozny2002`, `niculescu2005` | Calibração por regressão isotônica | A conferir | tudo: título, ano, volume e páginas | Seções de método | 2.5 |
| `hand1997` | Revisão de métodos de escore de crédito | A conferir | tudo: título, ano, volume e páginas | Artigo | 2.9 |
| `ankan2024` | pgmpy (Ankan & Textor) | Conferido no CITATION.cff do pgmpy | número do artigo no JMLR | Autor decidiu citar esta em 17/11/2026 | 3.3 |

## Ordem de leitura sugerida

1. `russell2010` (original em inglês), capítulos de raciocínio probabilístico e decisões simples: visão geral.
2. `jensen2007`: redes bayesianas e decisão, mais didático.
3. `friedman1997`: Naive Bayes e TAN, que são os dois modelos do trabalho.
4. `elkan2001` e `chow1970`: curtos, sustentam a afirmação central.
5. `koller2009`: consulta pontual para parâmetros, prior e inferência.
6. `gromping2019`: antes de escrever a seção da base.

## Livros em PDF

Ficam em `docs/livros/`, fora do git. Só de fonte legítima (biblioteca da UFU, Periódicos CAPES, cópia própria).
