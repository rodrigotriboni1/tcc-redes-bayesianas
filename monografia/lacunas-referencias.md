# Roteiro de conferência das referências (marcas LACUNA e confirmar)

Gerado em 18/11/2026. Este arquivo só organiza o que já está nos capítulos e em `docs/conferencia-referencias.md`. Nenhuma referência foi confirmada aqui e nenhuma marca foi removida dos capítulos.

## Como usar

1. Abra o original de uma chave do `.bib` (as seções abaixo estão em ordem de leitura sugerida por `docs/mapa-de-referencias.md`).
2. Para cada linha da tabela da chave, localize o trecho, confira a página, o capítulo ou a fórmula pedida e anote a página.
3. Só depois de conferir todas as linhas da chave, remova as marcas dela nos capítulos e, se houver, o `% VERIFICAR` da entrada no `.bib`.

**Contagem.** Há 79 marcas nos quatro arquivos (cap1: 8; cap2 2.1 a 2.5: 49; cap2 2.6 a 2.9: 14; cap3: 8), não cerca de 28. Dessas, 9 não dependem de referência (seção final) e 70 dependem de uma ou mais chaves. Uma marca que cita duas chaves aparece nas duas tabelas.

**Siglas de arquivo.** C1 = `monografia/cap1-introducao.md`; C2a = `monografia/cap2-secoes-2.1-2.5.md`; C2b = `monografia/cap2-secoes-2.6-2.9.md`; C3 = `monografia/cap3-metodos.md`. O número depois dos dois pontos é a linha; letra (a, b, c) separa marcas da mesma linha, na ordem em que aparecem.

**Estados (de `docs/conferencia-referencias.md`).** O veredito BATE vale só para os metadados (autores, título, periódico, ano, páginas). Ele não diz que a frase do capítulo é sustentada pelo texto. Estados usados:

- BATE: metadados conferidos na 1ª conferência (17/11/2026), texto da frase não conferido.
- MANTIDA: metadados conferidos, texto não aberto, LACUNA mantida.
- RESOLVIDA: conferida na fonte, `% VERIFICAR` ou LACUNA já retirada pelo registro de conferência. Se ainda há marca no capítulo, ela continua sendo do autor.
- NÃO ACHEI: dado do `.bib` não confirmado.
- DIVERGE: o `.bib` diverge da fonte (ver a última seção).

## Resumo por referência

| Chave | Estado | Marcas |
|---|---|---|
| `koller2009` | BATE | 20 |
| `heckerman1995` | MANTIDA | 7 (+ C2a:49c, que está em `koller2009`) |
| `friedman1997` | MANTIDA | 9 (+ C2a:29b, que está em `chowliu1968`) |
| `russell2010` | BATE | 5 próprias + 3 repetidas |
| `siddiqi2012` | BATE (DIVERGE no `.bib`) | 5 |
| `platt1999` | NÃO ACHEI | 2 |
| `guo2017` | BATE | 5 |
| `naeini2015` | BATE | 4 |
| `niculescu2005` | BATE | 4 |
| `zadrozny2002` | BATE | 2 |
| `zadrozny2001` | RESOLVIDA | 2 |
| `jensen2007` | BATE | 4 |
| `pearl1988` | BATE | 3 |
| `chowliu1968` | MANTIDA | 2 |
| `chow1970` | BATE | 2 |
| `thomas2000` | BATE | 4 |
| `hand1997` | BATE | 2 |
| `elkan2001` | RESOLVIDA | 1 |
| `brier1950` | BATE | 1 |
| `gromping2019` | BATE | 1 |
| sem chave | decisão do autor | 9 |

---

## Por referência

### `koller2009` (Koller & Friedman, *Probabilistic Graphical Models*, MIT Press, 2009). Estado: BATE

Livro. Sumário a conferir (`docs/mapa-de-referencias.md`: números de capítulo ainda "a confirmar no sumário"). Usada em 2.1, 2.3, 2.4, 2.6.

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:9a (2.1) | Rede bayesiana = grafo dirigido acíclico mais uma distribuição condicional por nó, dados os pais (cita pearl1988, koller2009) | confirmar | Capítulo de representação |
| C2a:15a (2.1) | A fatoração especifica a conjunta com muito menos parâmetros que a tabela completa (cita koller2009, russell2010) | confirmar | Página da fatoração |
| C2a:17 (2.1) | Independência de não descendentes dados os pais e critério de d-separação (cita pearl1988, koller2009) | confirmar | Seção de d-separação (e o capítulo correspondente em pearl1988) |
| C2a:19a (2.1) | A estrutura vem de especialistas, é aprendida ou fixada por família de modelos | confirmar | Capítulo de aprendizado de estrutura |
| C2a:39a (2.3) | A verossimilhança se decompõe por nó e configuração dos pais; cada tabela é estimada separadamente (cita koller2009, heckerman1995) | confirmar | Página da decomposição da verossimilhança |
| C2a:41a (2.3) | A estimativa de máxima verossimilhança é a frequência relativa $N_{ijk}/N_{ij}$ | confirmar | Capítulo de estimação de parâmetros |
| C2a:41b (2.3) | Com poucas ocorrências da configuração dos pais, a estimativa é instável e pode dar probabilidade zero | confirmar | Página |
| C2a:47a (2.3) | Posteriori Dirichlet (cita koller2009, heckerman1995) | confirmar | Página da posteriori Dirichlet |
| C2a:47c (2.3) | Hiperparâmetros como contagens imaginárias; o total mede o peso do prior | confirmar | Página |
| C2a:49c (2.3) | BDe/BDeu: força total do prior igual em todos os nós; menos pseudocontagem por célula em tabelas grandes (cita heckerman1995, koller2009) | confirmar | Página do BDe/BDeu |
| C2a:49d (2.3) | Estimador de Laplace ($\alpha_{ijk}=1$); a força total do prior cresce com o tamanho da tabela | confirmar | Página |
| C2a:49e (2.3) | Quanto maior $N'$, mais suavização; com contagens grandes a estimativa se aproxima da frequência relativa | confirmar | Página |
| C2a:53 (2.4) | Inferência exata: somar a conjunta sobre as variáveis fora da consulta e da evidência e normalizar (cita russell2010, koller2009) | confirmar | Capítulo de inferência exata (também em russell2010) |
| C2a:55a (2.4) | Eliminação de variáveis: somar só os fatores que mencionam a variável, guardar o resultado como novo fator | confirmar | Capítulo de eliminação de variáveis |
| C2a:55b (2.4) | Em Naive Bayes (estrela) e TAN (árvore) os fatores ficam pequenos | confirmar | Página |
| C2a:55c (2.4) | Inferência exata é NP-difícil em estruturas gerais | confirmar | Página do resultado de complexidade |
| C2a:59a (2.4) | Variável não observada é somada na marginalização, sem imputar valor (cita koller2009, jensen2007) | confirmar | Página (e em jensen2007) |
| C2a:59b (2.4) | Modelos discriminativos exigem valor para cada entrada e dependem de regra externa de preenchimento | confirmar | Página |
| C2b:11a (2.6) | Princípio da máxima utilidade esperada, $a^*=\arg\max_a EU(a)$ (cita russell2010, koller2009) | confirmar | Capítulo de decisão |
| C2b:13 (2.6) | Trocar a matriz muda a decisão sem retreinar; melhorar o modelo muda a decisão sem rediscutir valores | confirmar | Capítulo de decisão |

### `heckerman1995` (Heckerman, Geiger, Chickering; *Machine Learning* 20(3):197--243, 1995). Estado: MANTIDA

Metadados confirmados na 3ª conferência. O artigo de periódico não foi aberto; a versão UAI 1994 (arXiv) foi lida e não traz a fórmula $N'/(r_i q_i)$. A fórmula não foi vista no original. Há também a versão UAI 1994, pp. 293--301, que não é a citada.

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:39b (2.3) | Decomposição da verossimilhança por nó (cita koller2009, heckerman1995) | LACUNA | O que o artigo diz sobre a decomposição |
| C2a:47b (2.3) | Posteriori Dirichlet (cita koller2009, heckerman1995) | LACUNA | Trecho correspondente |
| C2a:49a (2.3) | BDeu distribui o tamanho equivalente de modo uniforme: $\alpha_{ijk}=N'/(r_i q_i)$ | LACUNA | **Fórmula** e definição de $r_i$, $q_i$ |
| C2a:49b (2.3) | Força total do prior igual em todos os nós (cita heckerman1995, koller2009) | LACUNA | Trecho correspondente |
| C2a:49f (2.3) | "Equivalente" vem de atribuir o mesmo escore a estruturas que representam as mesmas independências; motivou a proposta no aprendizado de estrutura | LACUNA | Propriedade de equivalência e contexto da proposta |
| C3:91a (3.5) | Parâmetros por estimação bayesiana com prior BDeu de tamanho equivalente 5 | LACUNA | Que o BDeu é o do artigo |
| C3:91b (3.5) | Pseudocontagem $N'/(r_i q_i)$ por valor do nó e configuração dos pais | LACUNA | **Fórmula** (mesma de C2a:49a) |

Atenção: C2a:49c (BDe/BDeu, página em `koller2009`) está na tabela de `koller2009`. As linhas C2a:49a e C3:91b dependem da mesma fórmula; conferir uma vez.

### `friedman1997` (Friedman, Geiger, Goldszmidt; *Machine Learning* 29(2--3):131--163, 1997). Estado: MANTIDA

Metadados confirmados (1ª e 3ª conferências). O PDF da Springer pede login e as cópias dos autores estavam indisponíveis; o texto não foi aberto. Todas as LACUNAs destas linhas foram mantidas.

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:23 (2.2) | Naive Bayes: a classe é o único pai dos atributos, atributos independentes dada a classe | LACUNA | Definição do Naive Bayes |
| C2a:27 (2.2) | A independência raramente vale, mas o desempenho costuma ser competitivo; estrutura fixa dispensa aprender o grafo | LACUNA | Afirmação de desempenho competitivo |
| C2a:29a (2.2) | TAN: cada atributo tem no máximo um outro atributo como pai, formando uma árvore | LACUNA | Definição do TAN |
| C2a:29c (2.2) | No TAN, o peso de cada par de atributos é a informação mútua condicional à classe (fórmula logo abaixo) | LACUNA | **Fórmula** do peso $I(X_i;X_j\mid C)$ |
| C2a:33 (2.2) | A árvore é orientada a partir de uma raiz e a classe vira pai de todos os atributos | LACUNA | Procedimento de construção |
| C2a:35 (2.2) | O TAN capta parte das correlações, mas cada tabela ganha uma configuração de pais e tem menos exemplos por célula | LACUNA | Trecho sobre custo em parâmetros |
| C2a:57 (2.4) | No TAN, o produto inclui, por atributo, a probabilidade dado a classe e o atributo pai | LACUNA | Fatoração da posteriori no TAN |
| C3:84 (3.5) | Naive Bayes: alvo é pai de cada preditora, condicionalmente independentes dado o alvo | LACUNA | Idem C2a:23 |
| C3:85 (3.5) | TAN: árvore pela informação mútua condicional $I(X_i;X_j\mid C)$, orientada de uma raiz, classe pai de todas (cita friedman1997, chowliu1968) | LACUNA | Idem C2a:29c e C2a:33 |

O trecho do TAN em C2a:29b, também com LACUNA, está em `chowliu1968`.

### `chowliu1968` (Chow & Liu; *IEEE Trans. Inf. Theory* 14(3):462--467, 1968). Estado: MANTIDA

Metadados confirmados. Resumo via OpenAlex: aproximação por árvore de dependência de 1ª ordem, ótima em informação. O registro de conferência observa que o artigo não trata da versão condicional à classe (que é de friedman1997). Texto não aberto.

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:29b (2.2) | A árvore do TAN é escolhida por adaptação do método de Chow e Liu: árvore geradora de peso máximo com pesos de informação mútua | LACUNA | Método da árvore de peso máximo por informação mútua |
| C3:85 (3.5) | Mesma ideia, na descrição do TAN (cita friedman1997, chowliu1968) | LACUNA | Idem |

### `russell2010` (Russell & Norvig, *AIMA*, 3ª ed., Prentice Hall, 2010). Estado: BATE

O `.bib` mantém `% VERIFICAR` (entrada trocada em 15/11/2026 da tradução brasileira para o original em inglês, de memória): conferir título, editora, cidade e ano. Capítulos de raciocínio probabilístico e de decisões simples.

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:9b (2.1) | Em variáveis discretas, a distribuição condicional é uma tabela com uma linha por combinação dos pais | confirmar | Capítulo de raciocínio probabilístico |
| C2a:15b (2.1) | Exemplo: $2^n-1$ parâmetros livres na conjunta completa contra $n\cdot 2^k$ com no máximo $k$ pais | confirmar | Página do exemplo de contagem de parâmetros |
| C2a:53 (2.4) | Somar a conjunta sobre as variáveis fora da consulta e normalizar | confirmar | Capítulo de inferência exata (mesma marca que em `koller2009`) |
| C2b:7 (2.6) | Estados possíveis $y$, utilidade $U(a,y)$ como valor da consequência da ação $a$ | confirmar | Capítulo de decisões simples |
| C2b:11b (2.6) | Agente com preferências que obedecem aos axiomas (ordenabilidade, transitividade, continuidade, substitutibilidade, monotonicidade, decomponibilidade) maximiza utilidade esperada | confirmar | Seção dos axiomas da utilidade |
| C2a:7 (2.1) | Redes bayesianas foram propostas para explorar a estrutura de independências e tornar a representação compacta (cita pearl1988, russell2010) | confirmar | Ver em `pearl1988` (a marca pede o capítulo de pearl1988) |
| C2a:19b (2.1) | Responde consultas sobre qualquer variável dado qualquer subconjunto das demais (cita russell2010, jensen2007) | confirmar | Ver em `jensen2007` (a marca pede o capítulo de jensen2007) |
| C2b:11a (2.6) | Máxima utilidade esperada (cita russell2010, koller2009) | confirmar | Ver em `koller2009` (a marca pede o capítulo de decisão em koller2009) |

Esta tabela repete três marcas cuja pergunta é sobre outra chave (as três últimas linhas), só para você saber que a mesma frase cita `russell2010`.

### `siddiqi2012` (Siddiqi, *Credit Risk Scorecards*, Wiley). Estado: BATE no resumo; DIVERGE na entrada (ver última seção)

Ainda sem edição no `.bib` (`edition` removido por decisão do autor). Antes de anotar páginas, defina qual exemplar e qual edição você tem.

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C1:7 (1.1) | Escores atribuem pesos a variáveis, em geral por regressão logística, e a decisão compara o escore com um ponto de corte; interpretabilidade e auditoria explicam a adoção (cita thomas2000, siddiqi2012) | LACUNA | Página em thomas2000/siddiqi2012 |
| C1:13 (1.1) | A regra de limiar sobre o escore mistura estimativa de risco e escolha de ação sem explicitar a utilidade (a proposta afirma sem citar) | LACUNA | Se siddiqi2012 (ou thomas2000) sustenta isso, com página |
| C2b:41 (2.9) | Scorecard: regressão logística sobre variáveis em faixas; coeficientes viram pontos aditivos | confirmar | Capítulos de desenvolvimento e de escalonamento do scorecard |
| C2b:43a (2.9) | Decisão por pontos de corte sobre o escore, por taxa de aprovação, perda esperada, lucratividade | confirmar | Capítulo de ponto de corte |
| C2b:43b (2.9) | Faixa intermediária de escores vai para análise humana (equivale a opção de rejeição) | confirmar | Menção à faixa de revisão manual |

### `platt1999` (Platt, em *Advances in Large Margin Classifiers*, MIT Press). Estado: NÃO ACHEI

O `.bib` mantém `% VERIFICAR`: ano (1999 na capa; algumas bases citam 2000) e páginas 61--74 não foram confirmados. Conferir no capítulo 5 do livro.

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:75a (2.5) | Escalonamento de Platt: sigmoide sobre a saída do modelo, regressão logística com uma entrada | confirmar | Seção de método e páginas |
| C2a:75c (2.5) | Os métodos exigem conjunto separado do treino para ajustar a recalibração (cita platt1999, zadrozny2002) | confirmar | Seção de método |

### `guo2017` (Guo, Pleiss, Sun, Weinberger; ICML, PMLR 70:1321--1330, 2017). Estado: BATE

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:63a (2.5) | Definição de classificador calibrado (cita guo2017, naeini2015) | confirmar | Seção de definição |
| C2a:63c (2.5) | Métricas de ordenação não mudam sob transformação estritamente crescente e não detectam erro de calibração (cita guo2017, naeini2015) | confirmar | Página (também em naeini2015) |
| C2a:73a (2.5) | ECE por faixas: forma da fórmula (cita naeini2015, guo2017) | confirmar | Forma exata da fórmula |
| C2a:73b (2.5) | Em problemas binários usa-se a probabilidade de uma classe fixa e a frequência dela | confirmar | Forma exata da fórmula |
| C2a:73c (2.5) | Diagrama de confiabilidade: frequência contra probabilidade média por faixa; calibrado fica na diagonal | confirmar | Seção do diagrama |

A frase em C2a:63b (cita guo2017, niculescu2005) tem LACUNA sobre `niculescu2005` e está lá.

### `naeini2015` (Naeini, Cooper, Hauskrecht; AAAI-29, pp. 2901--2907, 2015). Estado: BATE

Páginas confirmadas pelo registro PMC (página do AAAI bloqueada para robô).

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:63a (2.5) | Definição de classificador calibrado | confirmar | Ver em `guo2017`; conferir também aqui |
| C2a:63c (2.5) | Métricas de ordenação não detectam erro de calibração | confirmar | Página |
| C2a:73a (2.5) | Fórmula do ECE com $M$ faixas, $\mathrm{freq}(B_m)$ e $\mathrm{conf}(B_m)$ | confirmar | Forma exata da fórmula |
| C2a:73b (2.5) | Variante binária (classe fixa) | confirmar | Forma exata da fórmula |

### `niculescu2005` (Niculescu-Mizil & Caruana; ICML 22, pp. 625--632, 2005). Estado: BATE nos metadados; conteúdo não sustentou a frase

O `.bib` mantém `% VERIFICAR` (todos os campos). Segundo a 2ª conferência, só o artigo de 2005 sobre boosting foi aberto, e ele não sustenta a frase sobre calibração (a frase de calibração foi movida para `zadrozny2001`).

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:63b (2.5) | Boa ordenação não garante calibração: o modelo pode superestimar ou subestimar probabilidades (cita guo2017, niculescu2005) | LACUNA | Que o artigo sustenta isso |
| C2a:75b (2.5) | Regressão isotônica: função monótona por partes constantes, sem forma paramétrica, exige mais dados (cita zadrozny2002, niculescu2005) | LACUNA | Descrição da isotônica e o comentário sobre dados |
| C2a:75f (2.5) | Em Naive Bayes, probabilidades empurradas para os extremos pela suposição de independência (cita zadrozny2001, niculescu2005) | LACUNA | Que o artigo relata isso |
| C2b:27 (2.7) | Se as probabilidades não correspondem a frequências, o limiar derivado da matriz é aplicado na escala errada (cita zadrozny2001, niculescu2005) | confirmar | Seção de motivação |

### `zadrozny2002` (Zadrozny & Elkan; KDD 8, pp. 694--699, 2002). Estado: BATE

O `.bib` mantém `% VERIFICAR` (todos os campos).

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:75b (2.5) | Regressão isotônica por partes constantes, sem forma paramétrica (cita zadrozny2002, niculescu2005) | LACUNA | Descrição do método |
| C2a:75d (2.5) | Ambos os métodos pedem conjunto separado do treino para recalibrar (cita platt1999, zadrozny2002) | LACUNA | Trecho correspondente |

### `zadrozny2001` (Zadrozny & Elkan; ICML 2001, pp. 609--616). Estado: RESOLVIDA (registro de 17/11/2026)

Páginas 609--616 conferidas, `% VERIFICAR` já retirado do `.bib`. O resumo diz que estimativas bem calibradas são necessárias para decisão sensível a custo. O que resta é a página das frases abaixo.

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:75e (2.5) | Em Naive Bayes, a literatura relata probabilidades empurradas para os extremos (cita zadrozny2001, niculescu2005) | confirmar | Página em zadrozny2001 |
| C2b:27 (2.7) | Probabilidades sem calibração tornam o limiar derivado inadequado (cita zadrozny2001, niculescu2005) | confirmar | Seção de motivação |

### `jensen2007` (Jensen & Nielsen, *Bayesian Networks and Decision Graphs*, Springer, 2007). Estado: BATE

Número da edição (2ª) não confirmado pelo Crossref. O `.bib` ainda tem `edition = {2}`.

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:19b (2.1) | Responde consultas sobre qualquer variável dado qualquer subconjunto das demais (cita russell2010, jensen2007) | confirmar | Capítulo de redes bayesianas |
| C2a:55d (2.4) | Propagação em árvore de junção organiza o cálculo para muitas consultas | confirmar | Capítulo de inferência |
| C2a:59a (2.4) | Variável não observada é somada, sem imputar valor (cita koller2009, jensen2007) | confirmar | Página (e em koller2009) |
| C2b:15 (2.6) | Diagrama de influência: nós de decisão e de utilidade (cita howard2005, jensen2007) | confirmar | Capítulo de diagramas de influência |

Nota sobre `howard2005` (Howard & Matheson, *Decision Analysis* 2(3):127--143, 2005; estado BATE): é co-citada em C2b:15 e não tem marca própria nos capítulos. O `.bib` mantém `% VERIFICAR` (a proposta cita a reimpressão de 2005 do trabalho original de 1984). Conferir o artigo inteiro e a data na capa.

### `pearl1988` (Pearl, *Probabilistic Reasoning in Intelligent Systems*, Morgan Kaufmann, 1988). Estado: BATE

Cidade varia entre catálogos (San Mateo ou San Francisco). Usada só como citação de origem.

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:7 (2.1) | Redes bayesianas propostas para tornar compacta a representação da conjunta (cita pearl1988, russell2010) | confirmar | Capítulo introdutório |
| C2a:9a (2.1) | Definição de rede bayesiana (cita pearl1988, koller2009) | confirmar | Capítulo de representação (a marca nomeia koller2009; conferir pearl1988 junto) |
| C2a:17 (2.1) | d-separação (cita pearl1988, koller2009) | confirmar | Capítulo correspondente em pearl1988 |

### `chow1970` (Chow; *IEEE Trans. Inf. Theory* 16(1):41--46, 1970). Estado: BATE

O `.bib` mantém `% VERIFICAR` (todos os campos). Artigo curto; ele sustenta a afirmação central do trabalho junto com `elkan2001`.

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2b:31a (2.8) | Admitir uma ação além das classes remonta à opção de rejeição de Chow | LACUNA | Que o artigo introduz a opção de rejeição |
| C2b:31b (2.8) | A regra rejeita quando a maior posteriori fica abaixo de um limiar determinado pela razão entre o custo de rejeitar e o de errar | confirmar | **Enunciado da regra ótima e forma do limiar** |

### `thomas2000` (Thomas; *Int. J. Forecasting* 16(2):149--172, 2000). Estado: BATE

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C1:7 (1.1) | Escore por regressão logística comparado a ponto de corte; interpretabilidade e auditoria (cita thomas2000, siddiqi2012) | LACUNA | Página |
| C1:13 (1.1) | Regra de limiar sobre o escore mistura risco e ação sem explicitar utilidade | LACUNA | Se sustenta, com página |
| C2b:39a (2.9) | Escore de crédito estima a probabilidade de inadimplência e usa para decidir (cita thomas2000, hand1997) | LACUNA | Trecho correspondente |
| C2b:39b (2.9) | Vários métodos já usados (discriminante, logística, árvores, vizinhos, redes neurais), nenhum domina uniformemente (cita hand1997, thomas2000) | confirmar | Seções de comparação de métodos |

### `hand1997` (Hand & Henley; *JRSS A* 160(3):523--541, 1997). Estado: BATE

O `.bib` mantém `% VERIFICAR` (todos os campos).

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2b:39a (2.9) | Estimar a probabilidade de inadimplência e decidir sobre a concessão | LACUNA | Trecho correspondente |
| C2b:39b (2.9) | Comparação de métodos de escore, sem dominância uniforme | confirmar | Seções de comparação de métodos |

### `elkan2001` (Elkan; IJCAI 17, pp. 973--978, 2001). Estado: RESOLVIDA (registro de 17/11/2026)

O PDF do autor confirmou título, autor e IJCAI-01; a §2 dá o limiar ótimo derivado da matriz de custos. `% VERIFICAR` e uma LACUNA já foram retirados; resta a marca abaixo, que é do autor.

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2b:19 (2.7) | A decisão de máxima utilidade esperada equivale a regra de limiar sobre $p$, determinado pela matriz de custos | confirmar | Seção (o registro de conferência indica a §2; a marca é do autor) |

### `brier1950` (Brier; *Monthly Weather Review* 78(1):1--3, 1950). Estado: BATE

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C2a:69 (2.5) | Escore de Brier: valores menores são melhores | confirmar | Página (artigo de 3 páginas) |

### `gromping2019` (Grömping; Report 4/2019, Beuth University of Applied Sciences Berlin). Estado: BATE (fonte secundária; PDF existe, texto não lido)

O `.bib` mantém `% VERIFICAR` (série do relatório e instituição).

| Local | Frase afetada (resumida) | Marca | Conferir no original |
|---|---|---|---|
| C1:51 (1.5) | Troca da base original pela versão corrigida; o motivo além de "versão corrigida" não está em `docs/decisoes.md` | LACUNA | O que foi corrigido, com página |

---

## Marcas sem chave do `.bib` (decisão ou dado do autor)

Não dependem de abrir uma fonte bibliográfica.

| Local | Assunto | Marca |
|---|---|---|
| C1:55 (1.5) | Motivo da troca do protótipo por demonstração em terminal | LACUNA: motivo não registrado em `docs/decisoes.md` |
| C1:63 (1.5) | Quatro ações da proposta contra três ações no trabalho | LACUNA: motivo não registrado |
| C1:65 (1.5) | Abandono da estrutura de domínio (Naive Bayes e TAN no lugar) | LACUNA: motivo não registrado |
| C1:67 (1.5) | Regressão logística da proposta calibrada; no trabalho não é | LACUNA: motivo não registrado para a logística (D4 e P1 tratam da calibração em geral) |
| C1:69 (1.5) | Diagramas de influência, Streamlit e explicação da evidência fora do trabalho | LACUNA: motivo não registrado; o autor decide se a revisão de diagramas entra no Cap. 2 |
| C3:44 (3.1) | Contagem das categorias pequenas na base completa (n=1000) | LACUNA: conferir no `sgc.csv` (`docs/decisoes.md` §4, P25) |
| C3:123 (3.6) | Limite de 0,03 para PR-AUC e nível de 95% | LACUNA: não confirmado (`docs/plano-de-analise.md` §8) |
| C3:147 (3.7) | Aprovação da matriz de custos (c = 40) pelo orientador | LACUNA: em aberto (`PLANO.md` §11, item 2) |
| C3:185 (3.11) | Hash do commit de congelamento | LACUNA: anotar no passo 10 (`PLANO.md` §8) |

---

## Divergências do .bib

Copiadas de `docs/conferencia-referencias.md`, seção "Divergências e pendências" e conferências seguintes, sem acréscimo.

**Estado atual (17-18/11/2026), do mesmo arquivo.** `ankan2015` foi substituída por `ankan2024` (Ankan & Textor, JMLR 25(265)). O `.bib` não tem `edition` em `siddiqi2012` (removido por decisão do autor). `zadrozny2001` e as entradas heckerman/friedman/chow foram atualizadas na 2ª e 3ª conferência. O resumo "26/2/1" é da 1ª conferência.

- **siddiqi2012**: o título com o subtítulo "Developing and Implementing Intelligent Credit Scoring" é da 1ª edição (Wiley, Hoboken; ISBN 978-0-471-75451-0). A 2ª edição se chama *Intelligent Credit Scoring: Building and Implementing Better Credit Risk Scorecards* (Wiley, 2016/2017). Corrigir para uma das duas: 1ª edição sem `edition` e com o ano do exemplar usado (conferir na folha de rosto), ou 2ª edição com o título novo e ano 2017 (o Crossref registra 23/12/2016, online).
- **uci573**: o nome atual no repositório é "South German Credit" (sem "(UPDATE)", que é só o final do URL). O ano 2020 vem do campo de criação do registro; o texto da UCI indica doação em 28/11/2019. Autor corporativo não consta: o registro não lista criadores (a autoria é de Grömping). DOI: 10.24432/C5QG88. Sugestão: título "South German Credit", e o autor decide entre 2019 e 2020.
- **platt1999**: páginas 61--74 e ano 1999 não foram confirmados; fontes dão 1999 e 2000. Conferir no capítulo 5 do livro.
- **ankan2015 / ankan2024** (2ª conferência): a página da SciPy confirma autores, título, 2015 e o DOI 10.25080/Majora-7b98e3ed-001 (as páginas não aparecem nela; na 1ª conferência: acrescentar `pages = {6--11}`). Mas o `CITATION.cff` do pgmpy pede outra citação: Ankan & Textor, "pgmpy: A Python Toolkit for Bayesian Networks", JMLR 25, 2024, pp. 1--8. Ficava com o autor decidir qual citar. Na 3ª conferência: `ankan2024` RESOLVIDA, JMLR 25(265):1--8, 2024, `number = {265}` acrescentado, LACUNA removida. `docs/mapa-de-referencias.md` registra que o autor decidiu citar esta em 17/11/2026.
- **hofmann1994**: URL antigo no `.bib`; o atual é https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data (UCI id 144, criador Hans Hofmann, ano 1994; veredito BATE).
- **pearl1988**: San Francisco ou San Mateo conforme o catálogo.
- **kaufman2012**: título do Crossref sem o subtítulo ("Formulation, detection, and avoidance"); número 15 do artigo não confirmado (o `.bib` mantém `% VERIFICAR` para número do artigo e paginação 1--21).
- **jensen2007**: número da edição não confirmado.
- **ABNT** (`abnt14724`, `abnt6023`, `abnt10520`): conferi título e ano, não a vigência de cada edição (um resultado cita atualização de 2025 da NBR 6023, não confirmada).
- **friedman1997 / chowliu1968 / heckerman1995** (2ª e 3ª conferências): metadados confirmados; texto não aberto (Springer com login; cópias em huji, technion, academia.edu, scispace e Wayback deram 404/403/vazio/bloqueio). `chowliu1968` não trata da versão condicional à classe (que é de friedman1997). Em `heckerman1995`, a página da MSR dá "March 1994", o volume é de 1995, DOI 10.1007/BF00994016; MSR-TR-94-09 não encontrado.
- **gromping2019**: confirmado só por referência em pacote R (fonte secundária); o PDF existe no URL, mas o texto não foi lido.
- **Calibração (P2)**: MANTIDA, COM CANDIDATA na 2ª conferência; `zadrozny2001` adicionada e, na 3ª conferência, RESOLVIDA (ICML 2001, pp. 609--616). Niculescu-Mizil & Caruana: só o artigo de 2005 sobre boosting foi aberto, e ele não sustenta a frase.

### Entradas com `% VERIFICAR` ainda no `.bib` (conferido em `monografia/referencias.bib`)

`platt1999`, `gromping2019`, `kaufman2012`, `russell2010`, `howard2005`, `chow1970`, `zadrozny2002`, `niculescu2005`, `hand1997`. As do `.bib` sem `% VERIFICAR` hoje: `elkan2001`, `zadrozny2001` (retirados após conferência).
