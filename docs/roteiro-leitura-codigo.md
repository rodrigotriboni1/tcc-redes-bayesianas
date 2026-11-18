# Roteiro de leitura do código

Para reler o código antes da banca. Os números de linha valem para o estado do ramo em 17/11/2026; se o código mudar, refaça com `grep -n "def " codigo/<script>.py`.

Convenções que valem para tudo (decore antes de abrir qualquer arquivo):

- `kredit`: 0 = ruim, 1 = bom. A classe positiva é **ruim**. Toda coluna `p_*`, `p_ruim` e `kredit_0` é a probabilidade de **ruim**.
- Semente 2026 em toda aleatoriedade; 5 partições estratificadas; 3 faixas por tercis; BDeu com tamanho equivalente 5 (exceto a grade do `--selecao`); `LogisticRegression(max_iter=1000)`; erro de calibração com 10 faixas.
- Só `dev.csv` é lido pelo código. `teste.csv`, `sgc.csv` e `dados/brutos/` só `preparar_sgc.py` toca; `--final` só o autor roda, uma vez.

Fluxo dos arquivos:

```
preparar_sgc.py -> dev.csv
modelos.py       -> predicoes_dev.csv, tan_arestas.csv, cortes.json
modelos.py --ocultar  -> predicoes_dev_oculta.csv
modelos.py --selecao  -> predicoes_selecao.csv
avaliar.py       -> metricas_dev.csv, calibracao_dev.png
avaliar.py --ocultar  -> evidencia_incompleta.csv
avaliar.py --selecao  -> selecao_escolha.csv, selecao_dev.csv
decisao.py       -> politicas_dev.csv, resumo_politicas_dev.csv
sensibilidade.py -> sensibilidade.csv, sensibilidade.png
demo.py          -> só terminal
(final, só o autor) modelos --final -> predicoes_teste.csv -> avaliar --final, decisao --final
```

---

## 1. `codigo/preparar_sgc.py` (63 linhas)

### (a) Entra e sai

- Entra: `dados/brutos/SouthGermanCredit.asc` (proibido para agentes; você pode abrir).
- Sai: `dados/processados/sgc.csv` (1000 linhas, com `record_id` = `sgc-0000`...), `dev.csv` (800), `teste.csv` (200), `SHA256SUMS`.

### (b) Ordem de leitura

1. `preparar_sgc.py:22` `converter()`: lê o `.asc` separado por espaço, confere 1000 linhas e grava `sgc.csv` com `record_id`.
2. `preparar_sgc.py:34` `dividir()`: divisão 80/20 estratificada em `kredit`, semente 2026, com asserts de tamanho, de 240/60 ruins, de disjunção e de categorias do teste existirem no dev.
3. `preparar_sgc.py:51` `main()`: roda os dois passos e grava os hashes SHA-256 dos três CSV.

### (c) Perguntas da banca

1. Por que estratificar a divisão? Para dev e teste terem a mesma taxa de ruins (30%): 240/800 e 60/200 (`:36`, `:41`).
2. Por que a divisão foi refeita com semente nova? A antiga (semente 42) teve o teste aberto antes para a regressão logística; a nova mantém o teste fechado (PLANO item 4; semente em `:18`).
3. Como garante que não há vazamento entre dev e teste? Assert de `record_id` disjuntos (`:42`) e assert de que toda categoria do teste existe no dev (`:43-45`), para a rede nunca ver estado inédito.
4. Para que servem os hashes? Provar depois que `dev.csv` e `teste.csv` não mudaram entre o experimento e o teste final (`:54-58`).
5. Por que `record_id` existe? Identifica o caso de forma estável entre scripts; é retirado antes do `pgmpy` (`modelos.py:112`).

### (d) Pontos sutis

- `sort_index()` (`:37`) mantém a ordem original da base; muitos testes dependem da ordem das linhas do dev.
- As 3 contínuas ficam de fora da checagem de categorias (`:43`), porque são discretizadas depois.
- Este é o único script que lê `sgc.csv` e `teste.csv`; nenhum outro pode.

---

## 2. `codigo/modelos.py` (433 linhas)

O maior e o mais importante. Leia com calma.

### (a) Entra e sai

- Entra: `dados/processados/dev.csv`. Em `--final <arquivo>`: o arquivo dado, `resultados/cortes.json` e `resultados/selecao_escolha.csv`.
- Sai (padrão): `predicoes_dev.csv` (`record_id,kredit,fold,p_nb,p_tan,p_logreg`), `tan_arestas.csv`, `cortes.json`.
- `--ocultar`: `predicoes_dev_oculta.csv`. `--selecao`: `predicoes_selecao.csv` (32.000 linhas). `--final`: `predicoes_teste.csv` (com `p_sel`). `--verificar`: não grava nada.

### (b) Ordem de leitura

1. `modelos.py:57-75` constantes e `ESTADOS`: lista fixa de estados com tudo que aparece no dev; contínuas viram `[0, 1, 2]`.
2. `modelos.py:152` `particoes()`: 5 partições estratificadas, semente 2026; devolve o número da partição de cada linha.
3. `modelos.py:86` `cortes()`: cortes de tercil (1/3 e 2/3) de cada contínua, calculados no treino.
4. `modelos.py:90` `discretizar()`: aplica os cortes; `<= c1` vira 0, `<= c2` vira 1, senão 2.
5. `modelos.py:97` `montar_rede()`: Naive Bayes (estrela a partir de `kredit`) ou TAN (`TreeSearch`), com prior BDeu.
6. `modelos.py:109` `preparar_rede()`: aprende cortes no treino, tira `record_id`, discretiza, treina.
7. `modelos.py:78` `build()`: pipeline da regressão logística (padroniza contínuas, one-hot nas categóricas).
8. `modelos.py:116` `treinar()`: escolhe entre logreg e rede.
9. `modelos.py:130` `aplicar()`: P(ruim) de um modelo já treinado; trata a variável escondida.
10. `modelos.py:123` `preencher()`: regra D2 da logreg (mediana ou moda do treino) para a variável escondida.
11. `modelos.py:143` `prever()`: treina só no `treino` e prevê `alvo`; é a função que o `demo.py` reutiliza.
12. `modelos.py:159` `calcular()`: validação cruzada; monta `predicoes_dev.csv` e as arestas do TAN.
13. `modelos.py:178` `calcular_oculta()` e `:196` `main_oculta()`: esconde uma variável por vez e avisa se nada mudou.
14. `modelos.py:204` `selecao_particao()` e `:219` `main_selecao()`: validação cruzada aninhada da grade de 8 configurações.
15. `modelos.py:236` `final()`: treina no dev inteiro e prevê o arquivo dado; recusa sobrescrever.
16. `modelos.py:272` `verificar()`: leia por último; cada bloco comentado (5a, 6a...) é um critério de aceite.

### (c) Perguntas da banca

1. Como a validação cruzada evita vazamento? `calcular()` treina em `dev[folds != k]` e prevê `dev[folds == k]` (`:168`); os cortes de tercil também são aprendidos só no treino (`:111`, `:112`).
2. Por que `kredit_0` é a coluna usada? Porque 0 = ruim; `predict_probability` devolve `kredit_0` = P(ruim) (`:140`). Na regressão logística busca-se a coluna da classe 0 com `classes_.index(0)` (`:134`).
3. Qual a diferença entre o Naive Bayes e o TAN? NB: todas as variáveis filhas só de `kredit` (`:100`). TAN: `TreeSearch(..., "tan")` aprende uma árvore entre as variáveis, cada uma com `kredit` como pai (`:102-103`).
4. Para que serve o prior BDeu e o `ESTADOS`? Evita probabilidade zero em categorias raras, e a lista fixa de estados impede quebrar a inferência quando uma categoria falta no treino (`:72-75`, `:104`).
5. Como funciona a evidência incompleta? Rede: a coluna é removida e o `pgmpy` soma sobre seus valores (`:137-139`). Regressão logística: preenche com mediana ou moda do treino (`:123-127`). O treino é feito com as 20 variáveis; só a previsão esconde (`:187-190`).

### (d) Pontos sutis

- **Vazamento**: cortes e estados dependem só do treino da partição; a exceção consciente é `ESTADOS` (`:73`), que usa o dev inteiro, mas só lista valores possíveis, não aprende probabilidade nenhuma.
- **Representação diferente**: a logreg usa as contínuas originais (padronizadas); as redes usam 3 faixas (`:81`, `:119`). A diferença entre modelos mistura modelo e representação (PLANO item 5).
- **`record_id`**: retirado antes do `pgmpy` (`:112`); na logreg não entra porque `VARIAVEIS` o exclui (`:70`).
- **TAN em `calcular()`** é montado direto (`:172`) para gravar o mesmo grafo que gera as predições; `verificar()` (5b) confirma que dá igual a `prever`.
- **Ordem de colunas**: `predict_probability` precisa das colunas dos nós da rede; a saída tem `kredit_0` e `kredit_1`. O teste 6d confere que somam 1 (`:305`).
- **`cortes.json`** é aprendido no dev inteiro (`:233`) e usado só no `--final`; o `demo.py` não usa, aprende nas 4 partições.
- **`--selecao`**: a grade (`:63-66`) é a exceção às constantes congeladas, só neste modo; as partições internas usam semente 2026 sobre o treino externo (`:208`). `fold_interno = -1` marca a predição externa.
- **`--final`**: cria `p_sel` com a configuração marcada `escolhida` no bloco `dev` (`:251-260`); falha se não houver exatamente uma (`:256`); recusa sobrescrever (`:245`); nb/tan/logreg continuam com ess = 5 (`:266`, `:267`). A recusa vem antes de qualquer treino.
- `verificar()` usa `try/except` só para testar que o código recusa (`:390-394`, `:412-416`); no código de treino e inferência não há `try/except`, como manda o AGENTS.md.
- Avisos (`:199`) informam o autor, não são erros.

---

## 3. `codigo/avaliar.py` (319 linhas)

### (a) Entra e sai

- Entra: `predicoes_dev.csv`. Com `--ocultar`: `predicoes_dev_oculta.csv` e `metricas_dev.csv`. Com `--selecao`: `predicoes_selecao.csv`. Com `--final`: `predicoes_teste.csv` e `dev.csv` (só para a taxa de ruins).
- Sai: `metricas_dev.csv`, `calibracao_dev.png`; `evidencia_incompleta.csv`; `selecao_escolha.csv` e `selecao_dev.csv`; `metricas_teste.csv` e `calibracao_teste.png`.
- Nunca treina nenhum modelo.

### (b) Ordem de leitura

1. `avaliar.py:75` `faixas()`: índice da faixa (0 a 9) de cada probabilidade; 1,0 cai na última faixa.
2. `avaliar.py:80` `ece()`: erro de calibração, média ponderada de |média de p − fração de ruins| por faixa.
3. `avaliar.py:86` `metricas()`: ROC-AUC, PR-AUC, Brier, log loss e ECE de um vetor.
4. `avaliar.py:90` `ler_csv()` e `:103` `ler()`: validam arquivo, colunas, vazios e p dentro de [0, 1].
5. `avaliar.py:112` `calcular()`: média e desvio (`ddof=1`) das métricas entre as 5 partições; inclui `taxa_base`.
6. `avaliar.py:131` `desenhar()`: diagrama de calibração com as 800 predições juntas.
7. `avaliar.py:150` `main()`: grava `metricas_dev.csv` e o gráfico; imprime os `AVISO`.
8. `avaliar.py:194` `calcular_oculta()` e `:214` `main_oculta()`: delta de ROC-AUC e Brier contra o modelo completo.
9. `avaliar.py:236` `escolher()` e `:241` `calcular_selecao()`: escolha da configuração por log loss interno e resumo "aninhado".
10. `avaliar.py:163` `calcular_final()` e `:185` `main_final()`: métricas no teste com bootstrap.
11. `avaliar.py:280` `verificar()`.

### (c) Perguntas da banca

1. Como é calculado o erro de calibração? Divide as p em 10 faixas; em cada uma compara a média de p com a fração observada de ruins; pondera pelo número de casos (`:80-83`).
2. O que é a linha `taxa_base`? Em cada partição, prevê a proporção de ruins das outras 4 (`:115-117`); é o piso: Brier de um modelo igual ou acima dele dispara aviso (`:155`).
3. Por que ROC-AUC com classe ruim como positiva? `y = (kredit == 0)` (`:114`); mantém coerência com `p_*` = P(ruim).
4. Como se obtém o intervalo no teste? Bootstrap de 2000 reamostras, semente 2026, percentis 2,5 e 97,5 (`:167`, `:180`); as mesmas reamostras valem para todos os modelos (`:167`).
5. Como a seleção aninhada escolhe a configuração? Pelo menor log loss interno; empate até 1e-9 vai para a primeira da grade (`:236-238`); o `aninhado` usa, em cada partição externa, a configuração escolhida naquele bloco (`:267`).

### (d) Pontos sutis

- **Média por partição, não global**: `metricas_dev.csv` é média e desvio entre partições (`:122-126`); o gráfico de calibração, ao contrário, junta as 800 predições (`:131`). Os números não são intercambiáveis.
- **Desvio amostral** `ddof=1` (`:126`, `:232`).
- **`log_loss(..., labels=[0, 1])`** (`:87`): evita erro se uma amostra só tiver uma classe.
- No teste, `taxa_base` é a taxa do **dev** para todas as linhas (`:169`, `:189`), e as métricas são sobre todas as linhas juntas, sem partições (`:174`).
- **Interpretação do `--selecao`**: no bloco `dev`, a perda é o log loss das 800 predições externas juntas (`:255-256`); nos blocos 0 a 4, a média dos 5 log loss internos (`:258-259`). `fold_interno >= 0` são internas, `-1` externa.
- `evidencia_incompleta`: o aviso compara `laufkont` com `telef` (`:221`); é só aviso, sem correção.
- Autoteste (`:282-284`) confere o ECE à mão: tudo 0,8 sem ruim dá 0,8; tudo 0,3 com 30% de ruins dá 0.
- O teste 08.8 só confere `nb_ess5`/`tan_ess5` contra `metricas_dev.csv` se os arquivos já existem (`:290`).

---

## 4. `codigo/decisao.py` (193 linhas)

### (a) Entra e sai

- Entra: `predicoes_dev.csv`, `config/utilidade.json`; em `--final`, `predicoes_teste.csv`.
- Sai: `politicas_dev.csv`, `resumo_politicas_dev.csv`; em `--final`, `politicas_teste.csv`, `resumo_politicas_teste.csv`, `diferenca_politicas_teste.csv`.

### (b) Ordem de leitura

1. `decisao.py:42-49` constantes; `PRIORIDADE` (`:45`) define o desempate.
2. `decisao.py:52` `carregar_utilidade()`: lê o JSON e valida a forma.
3. `decisao.py:64` `conferir_p()`: p precisa estar em [0, 1] e não ser NaN.
4. `decisao.py:69` `utilidade_esperada()`: a fórmula do plano, `(1-p)·U(a,bom) + p·U(a,ruim)`.
5. `decisao.py:75` `ordenar()`: ação de maior UE, segunda ação e diferença, com o desempate.
6. `decisao.py:84` `limiar()`: regra de 0,5 (aprova se p < 0,5).
7. `decisao.py:90` `ler()`: valida as predições.
8. `decisao.py:107` `calcular()`: tabela por caso, resumo por modelo e regra, e (só no teste) bootstrap e diferença.
9. `decisao.py:154` `main()`, depois `:167` `verificar()`.
10. Para completar: `codigo/test_decisao.py` (item 7 deste roteiro).

### (c) Perguntas da banca

1. Qual a regra de decisão? Maior UE entre aprovar, rejeitar e análise manual (`:69-72`, `:78`); a matriz vem de `config/utilidade.json` (`:40`), nunca do código.
2. Como o empate é resolvido? Tolerância 1e-9; prioridade análise manual, depois rejeitar, depois aprovar (`:45`, `:78`).
3. Por que a UE é equivalente a limiares? Cada UE é uma reta em p; o máximo de retas divide [0, 1] em intervalos, então a política é uma regra de limiares (PLANO item 5). A contribuição é derivá-los dos custos e medir a calibração.
4. Como se calcula a utilidade média? Média da utilidade **realizada**: `u[ação][estado real]` com estado `ruim` se `kredit == 0` (`:128`, `:141`), não a UE prevista.
5. O que significa `n_mudam_vs_outra_regra`? Quantos casos têm ação diferente entre a regra UE e o limiar de 0,5 (`:134`); é discordância, não consistência.

### (d) Pontos sutis

- **`p_ruim` é a probabilidade de ruim**: `estado` mapeia 0 para ruim (`:127-128`); inverter isso trocaria o sinal das utilidades.
- `limiar()` só tem duas ações; a análise manual nunca aparece nessa regra (`:135`, aviso `:139-140` só confere `aprovar`/`rejeitar` nela).
- **Dev e teste**: no dev não há bootstrap (`:129-131`, `:143`). O `sel` só entra no teste (`:119`) e `verificar()` confirma que o dev não ganha `sel` (`:181`).
- `conferir_p` levanta `ValueError`, e `ler()` termina com `sys.exit`; entrada inválida nunca gera resultado parcial.
- O intervalo da diferença é pareado: usa `por_linha["ue"] - por_linha["limiar"]` nas mesmas reamostras (`:149`), o que é mais estreito que subtrair dois intervalos.
- `por_linha[regra]` é sobrescrito a cada regra dentro do laço do modelo (`:145`); a diferença depende de a regra `ue` vir antes de `limiar` (`:135`) e de `linhas[-2]`/`linhas[-1]` (`:148`). Ao mexer na ordem, isso quebra.
- Os avisos `AVISO: a ação ... não aparece` informam o autor; não se muda código para sumirem.

---

## 5. `codigo/sensibilidade.py` (107 linhas)

### (a) Entra e sai

- Entra: `config/utilidade.json` (só o ganho `G = acoes.aprovar.bom` e a linha `rejeitar`). Não lê dados nem predições.
- Sai: `sensibilidade.csv` (84 linhas = 4 perdas × 21 custos) e `sensibilidade.png`.

### (b) Ordem de leitura

1. `sensibilidade.py:32-33` a grade: perdas {200, 400, 600, 800}; custos de 0 a 100 de 5 em 5.
2. `sensibilidade.py:40` `limiares()`: forma fechada dos dois limiares.
3. `sensibilidade.py:47` `tabela()`: aplica `limiares()` em toda a grade.
4. `sensibilidade.py:52` `desenhar()`: um painel por perda, regiões coloridas por ação.
5. `sensibilidade.py:36` `matriz()` e `:82` `verificar()`: usam o `decisao.ordenar` para conferir a forma fechada.
6. `sensibilidade.py:74` `main()`.

### (c) Perguntas da banca

1. De onde vêm `c/L` e `1 - c/G`? Igualando UE(aprovar) = UE(análise manual) e UE(análise manual) = UE(rejeitar); com G=100 e L=400 dão `c/400` e `1 - c/100` (`:44` e a docstring).
2. Quando a análise manual nunca é escolhida? Quando `c > G·L/(G+L)` (`:42`); então os dois limiares coincidem em `G/(G+L)` (`:44`). Com G=100 e L=400, isso é c > 80; em c = 80 só no ponto de empate p = 0,20 (três ações empatam e a prioridade, `decisao.py:45`, dá análise manual).
3. Como a forma fechada é testada? Contra `decisao.ordenar`, em cada ponto da grade, logo abaixo, no meio e logo acima dos limiares (`:87-94`).
4. Por que não usa dados? A fronteira só depende da matriz e não do modelo; a página do plano compara o risco de cada caso contra estes limiares.
5. Por que essa grade? É a decisão D7 (`:31`); valores da grade são decisão do autor, não do código.

### (d) Pontos sutis

- O gráfico é por **fronteira** de risco, não por caso.
- `import decisao` (`:27`) só funciona porque o script roda com `codigo/` no path; é reuso, não duplicação, de `carregar_utilidade` e `ordenar`.
- Valores de utilidade vêm do JSON, exceto os que variam na grade (`perda`, `custo`), que são os parâmetros do estudo.
- A matriz de rejeitar é passada ao teste (`:88`), não assumida como zero.
- Em `verificar()` (`:96-97`), as linhas conhecidas (400, 40), (400, 80), (400, 100) usam G=100 fixo; esses números são os que você pode refazer à mão na banca.

---

## 6. `codigo/demo.py` (85 linhas)

### (a) Entra e sai

- Entra: `dev.csv` (via `modelos.dev`), `predicoes_dev.csv` (só para a partição do caso), `config/utilidade.json`.
- Sai: só terminal.

### (b) Ordem de leitura

1. `demo.py:44` `main()`: valida o `record_id`, escolhe a partição do caso e treina nas outras 4.
2. `demo.py:26` `fronteiras()`: calcula os cruzamentos das retas de UE no envelope superior.
3. Para fechar: `demo.py:69` chama `modelos.prever` e `:74-81` mostra UE e ação.

### (c) Perguntas da banca

1. O que acontece quando você roda o demo? Treina nas 4 partições que não contêm o caso e imprime as variáveis, P(ruim) dos três modelos, UE por ação, fronteiras e a ação recomendada (`:61-81`).
2. Por que treina de novo e não carrega um modelo? Não há modelo salvo (regra do repositório); treinar leva segundos e dá o mesmo valor de `predicoes_dev.csv` (`:61`, `:69`).
3. Como é calculada cada fronteira? Resolve UE(a) = UE(b) para p, que é uma reta (`:30-35`), e guarda só os cruzamentos que estão no topo (`:38-40`).
4. Qual o modelo padrão? TAN (`:47`); `--modelo` troca.
5. Se o caso não está no dev? Termina com `ERRO` e código diferente de 0 (`:51-52`).

### (d) Pontos sutis

- Treino sem o fold do caso: o P(ruim) é **fora da amostra** para aquele caso, igual ao de `predicoes_dev.csv`. Se treinasse com todo o dev, o risco do caso seria otimista.
- Importa `modelos`, que lê `dev.csv` ao ser importado (`modelos.py:69`).
- `alvo` perde `kredit` (`:62`), de modo que a classe real nunca chega à previsão.
- Não usa `cortes.json`; os cortes saem do treino das 4 partições (`prever`).
- Para demonstrar na banca: compare o `p_tan` impresso com a linha do `record_id` em `resultados/predicoes_dev.csv`.

---

## 7. `codigo/test_decisao.py` (89 linhas)

### (a) Entra e sai

- Entra: nada (matrizes montadas no próprio arquivo). Sai: só uma linha no terminal.

### (b) Ordem de leitura

1. `test_decisao.py:17` `matriz(c, perda)`: a matriz demonstrativa.
2. `test_decisao.py:29-30` o exemplo da apresentação (p = 0,20): UE(aprovar) = 0, e −40 com perda 600.
3. `test_decisao.py:33-38` extremos: p = 0 e p = 1 e rejeitar sempre zero.
4. `test_decisao.py:41-52` fronteiras `c/400` e `1 - c/100`, em uma grade de 1001 pontos.
5. `test_decisao.py:55-60` sem faixa de análise manual (c = 90, 100); `:63-68` outra matriz.
6. `test_decisao.py:71-74` empates; `:77-84` p inválida; `:87` limiar fixo.

### (c) Perguntas da banca

1. Que conta o teste confirma à mão? Com p = 0,2: 0,8·100 + 0,2·(−400) = 0 (`:29`).
2. Como se verifica que a fronteira está certa? Varre p de 0 a 1 em passos de 0,001 e compara com a ação esperada em cada intervalo (`:41-52`).
3. O que o teste de empate garante? Que o desempate segue análise manual > rejeitar > aprovar (`:71-73`).
4. O que acontece com p inválido? `ValueError` em todas as funções (`:77-84`).
5. O que o limiar fixo faz em 0,5? Rejeita; aprova só se p < 0,5 (`:87`).

### (d) Pontos sutis

- Nas fronteiras exatas (`abs(p - baixo) < 1e-9`), o esperado é análise manual por causa do desempate (`:44-45`).
- O teste não lê `config/utilidade.json`; a matriz está dentro do teste, de propósito, para o teste não depender do que o autor escolher como valor final.
- Roda direto (`uv run python codigo/test_decisao.py`); é a única exceção a "autoteste em `--verificar`".

---

## Ordem de leitura recomendada e tempo

Leia nesta ordem. Os tempos supõem leitura atenta, com o autoteste ao lado.

| # | Script | Por quê nesta posição | Tempo |
|---|---|---|---|
| 1 | `preparar_sgc.py` | Origem dos dados e da divisão; curto | 10 min |
| 2 | `test_decisao.py` | Mostra a conta da utilidade com números que você refaz à mão | 15 min |
| 3 | `decisao.py` | A camada de decisão, núcleo do trabalho | 30 min |
| 4 | `sensibilidade.py` | Forma fechada dos limiares; depende de `decisao.py` | 20 min |
| 5 | `modelos.py` | O mais longo; leia as linhas 1-175 e 236-270, deixe `--ocultar`/`--selecao`/`verificar()` para depois | 60 min |
| 6 | `avaliar.py` | Métricas e calibração; leia `ece`, `calcular`, `calcular_final`; deixe `--selecao` para o fim | 40 min |
| 7 | `demo.py` | Junta as peças; é o roteiro da demonstração | 10 min |

Total: cerca de 3 h 05. Depois, uma segunda passada de 45 min só nos blocos de `--selecao`, `--ocultar` e `--final` (`modelos.py:178-270`, `avaliar.py:194-278`, `decisao.py:107-151`), que são os que a banca provavelmente pergunta por último.

Antes da banca, rode (não grava nada) `uv run python codigo/<script>.py --verificar` em `modelos`, `avaliar`, `decisao` e `sensibilidade`, e `uv run python codigo/test_decisao.py`.
