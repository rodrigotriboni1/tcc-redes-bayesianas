# Critérios de aceite

Situação: **aceito pelo autor em 15/11/2026.** Base para as issues em `docs/issues/` e para o `factory/checks.sh`. O código é escrito pela software factory (uma issue do GitHub com o rótulo `factory` vira um PR); aqui ficam as regras que ela tem de cumprir.

Origem: levantamento feito por um subagente em 15/11/2026, lendo o `PLANO.md`, os scripts, o `dev.csv` e a factory. Os pontos marcados "conferido" foram executados de novo depois. O `teste.csv` não foi aberto.

## 1. Decisões do autor

As onze propostas abaixo foram aceitas em bloco em 15/11/2026.

| # | Questão | Decisão |
|---|---|---|
| D1 | A demonstração treina no dev inteiro, mas o plano pede "mesmo risco de `predicoes_dev.csv`". Os dois não coincidem | A demonstração treina nas 4 partições que não contêm o caso; reproduz o número da monografia |
| D2 | Na regressão logística com variável escondida, "moda" não serve para `hoehe` (753 valores distintos em 800 linhas, conferido) | Mediana do treino para as 3 contínuas; moda para as 17 categóricas |
| D3 | A tabela 2×2 fala em "rede bayesiana", mas há duas (Naive Bayes e TAN) | A factory calcula as políticas para os três modelos; o autor escolhe qual vai para o texto antes do commit de congelamento |
| D4 | "Calibrar se estiver ruim" depende do resultado | Fica fora das 6 issues; o autor decide depois de ver `metricas_dev.csv`; se entrar, é issue nova |
| D5 | Empate entre ações (com c = 80 e p = 0,20 as três empatam) | Prioridade: análise manual > rejeitar > aprovar, tolerância 1e-9 |
| D6 | Dois números da monografia não teriam arquivo | Criar `resumo_politicas_dev.csv` e `sensibilidade.csv` |
| D7 | Grade da sensibilidade | Perda em {200, 400, 600, 800} × custo da análise em {0, 5, …, 100} |
| D8 | Modelo padrão da demonstração | `tan` |
| D9 | O aprovador da factory faz merge sem humano (conferido em `approver.md`) | **Revista em 15/11/2026:** o merge fica automático. A factory permite configurar, e o autor optou por não parar cada PR. Em troca: o autor lê a descrição de cada PR depois do merge e relê todo o código antes do commit de congelamento |
| D10 | Nenhuma issue escreve o caminho do teste final (`--final`, passo 10) | Issue 07 pequena, feita pela factory e testada com um "teste falso" feito de linhas do dev. O autor só executa no dia |
| D11 | `sgc.csv` e `dados/brutos/` também contêm as 200 linhas do teste | A proibição de leitura cobre os três, não só `teste.csv` |

## 2. Princípios

Critério restringe a forma, nunca o resultado.

| Tipo de critério | Pode? | Exemplo |
|---|---|---|
| Formato da saída | Sim | `predicoes_dev.csv` tem 800 linhas e as colunas esperadas |
| Reprodutibilidade | Sim | Rodar duas vezes gera arquivos idênticos byte a byte |
| Consistência interna | Sim | As contagens das três ações somam 800 |
| Conta com resposta conhecida | Sim | p = 0,20, +100, −400 dá UE(aprovar) = 0 |
| Guarda contra vazamento | Sim | A predição de uma linha não muda se as outras linhas de validação forem retiradas |
| Valor de métrica | **Não** | "AUC acima de 0,75" |
| Ordem entre modelos ou variáveis | **Não** | "TAN melhor que Naive Bayes" |
| Presença de um efeito | **Não** | "As três ações aparecem" |
| Escolha feita pelo agente a partir de números | **Não** | "Usar o modelo de melhor Brier" |

Teste para separar os dois: *um modelo ruim, mas programado corretamente, passaria?* Se sim, é critério. Se só passa quando o modelo vai bem, vira aviso ou sai.

Itens do plano reclassificados:

| Item | Destino | Motivo |
|---|---|---|
| "Brier abaixo de 0,21" | Aviso no log. Entra uma linha `taxa_base` em `metricas_dev.csv`, cujo Brier tem de dar 0,21 exato | Como critério, convidaria o agente a mexer no prior até passar |
| "Esconder `laufkont` piora mais que `telef`" | Aviso. O critério passa a ser: para cada modelo e variável, ao menos uma predição muda ao esconder | É hipótese sobre os dados |
| "As três ações aparecem" | Aviso | Depende do modelo e da matriz, que ainda vai ao orientador |
| AUC abaixo de 0,5 | Aviso ("alvo pode estar invertido") | O teste de inversão é estrutural (critério 01.6a) |

Avisos são impressos como `AVISO: ...`, nunca falham e nunca devem ser "consertados".

## 3. Regras comuns a todas as issues

Vão para o `AGENTS.md`; não se repetem em cada issue.

| # | Regra | Quem confere |
|---|---|---|
| G1 | Roda da raiz com `uv run python codigo/<script>.py`, saída 0, sem interação | gate |
| G2 | Não lê `teste.csv`, `sgc.csv` nem `dados/brutos/`; não lista pastas de dados | gate |
| G3 | Só grava em `resultados/`; os arquivos gerados são commitados e idênticos ao que o gate regenera | gate |
| G4 | Constantes congeladas: semente 2026, 5 partições, 3 faixas por tercis, BDeu com tamanho equivalente 5, `LogisticRegression(max_iter=1000)`, erro de calibração com 10 faixas. Precisar mudar uma delas é motivo para parar e perguntar | revisão |
| G5 | Sem dependência nova; sem arquivo novo em `codigo/` fora dos 7 do plano | gate |
| G6 | Sem `try/except` em volta de treino ou inferência; sem `fillna`, `clip` ou `nan_to_num` em probabilidades; entrada inválida termina com saída diferente de 0 e mensagem | gate e revisão |
| G7 | Cada arquivo abre com docstring em português: o que faz, entradas, saídas, linha `Uso:` | gate |
| G8 | A descrição do PR tem `## O que este script faz` (5 a 10 linhas, português simples), `## Como rodar` e `## Avisos impressos` | autor, depois do merge |
| G9 | Autoteste com `assert` fica no modo `--verificar` do próprio script e não grava nada | gate |

## 4. Critérios por issue

### 01. Predições no dev (`modelos.py`)

1. `uv run python codigo/modelos.py` grava só `resultados/predicoes_dev.csv` e `resultados/cortes.json`, em menos de 60 s.
2. `predicoes_dev.csv`: colunas exatas `record_id,kredit,fold,p_nb,p_tan,p_logreg`; 800 linhas na ordem do `dev.csv`; `record_id` único; `fold` inteiro de 0 a 4; `p_*` finito, estritamente entre 0 e 1, sem vazio.
3. Partições: uma única chamada `StratifiedKFold(5, shuffle=True, random_state=2026)` sobre o dev na ordem do arquivo, usada pelos três modelos. Cada partição tem 160 linhas e 48 ruins (conferido).
4. Existe `prever(treino, alvo, modelo, ocultar=None)` que devolve P(ruim) por linha de `alvo`. `alvo` não carrega `kredit`. Cortes, estrutura do TAN, parâmetros e escalonamento da regressão são aprendidos só em `treino`.
5. `--verificar`, guardas de vazamento:
   - (a) `prever(treino, alvo)` é igual a `prever(treino, alvo.iloc[[i]])` em 5 linhas, nos 3 modelos, tolerância 1e-12;
   - (b) para cada partição k, a coluna gravada é igual a `prever(dev[fold != k], dev[fold == k])`;
   - (c) os cortes de uma partição são `treino[c].quantile([1/3, 2/3])`; valor ≤ corte 1 vai para a faixa 0, ≤ corte 2 para a 1, o resto para a 2.
6. `--verificar`, respostas conhecidas (treino da partição 0), tolerância 1e-9:
   - (a) P(ruim) sem evidência = (192 + 2,5)/(640 + 5) = 0,3015503876 nas duas redes (conferido); pega alvo invertido e prior errado;
   - (b) em 5 linhas, `p_nb` é o produto normalizado das tabelas de `get_cpds()`, feito com numpy;
   - (c) `kredit_0` de `predict_probability` igual a `VariableElimination.query` em 5 linhas, nas duas redes;
   - (d) `kredit_0 + kredit_1 = 1`;
   - (e) na regressão, a coluna usada é a da classe ruim (`classes_`).
7. `cortes.json` é exatamente `{"laufzeit": [12.0, 24.0], "hoehe": [1553.0, 3384.0], "alter": [28.0, 38.0]}` (conferido).
8. Naive Bayes montado como rede em estrela, `DiscreteBayesianNetwork([("kredit", f) for f in variaveis])`: a classe `pgmpy.models.NaiveBayes` falha em `predict_probability` na 1.1.2 (conferido). TAN por `TreeSearch(...).estimate(estimator_type="tan", class_node="kredit")`, refeito em cada partição. Estados fixos: tudo que aparece no dev inteiro; contínuas sempre `[0, 1, 2]`.
9. `build()` vem de `baseline_logreg.py` sem alteração, e `baseline_logreg.py` é apagado neste PR.
10. Duas execuções geram arquivos idênticos byte a byte.
11. Categoria ausente no treino de uma partição não derruba o script.

Fora do escopo: `--ocultar`, `--final`, hill climbing, calibração, métricas, gráficos, salvar modelo em arquivo, busca de hiperparâmetros, seleção de variáveis, mexer em `preparar_sgc.py`, opções além de `--verificar`.

### 02. Métricas e calibração (`avaliar.py`)

1. `uv run python codigo/avaliar.py` lê só `resultados/predicoes_dev.csv`; grava `metricas_dev.csv` e `calibracao_dev.png`.
2. Nunca treina: `grep -nE "pgmpy|import modelos|\.fit\(" codigo/avaliar.py` não devolve nada.
3. `metricas_dev.csv`: 4 linhas (`nb`, `tan`, `logreg`, `taxa_base`) e colunas `modelo,roc_auc_media,roc_auc_desvio,brier_media,brier_desvio,log_loss_media,log_loss_desvio,ece_media,ece_desvio`. Classe positiva = ruim. Métrica por partição; média e desvio amostral das 5.
4. Linha `taxa_base` (previsão = proporção de ruins nas outras 4 partições, 0,30): Brier 0,21, AUC 0,5, log loss 0,610864, erro de calibração 0, desvios 0. Tolerância 1e-6.
5. Recalculando com `roc_auc_score`, `brier_score_loss` e `log_loss` por partição, as médias batem com o arquivo a 1e-9.
6. Erro de calibração: 10 faixas de mesma largura sobre P(ruim). `--verificar` confere: tudo 0,8 com nenhum ruim dá 0,8; tudo 0,3 com 30% de ruins dá 0.
7. AUC, Brier e erro de calibração em [0, 1]; log loss finito e ≥ 0; desvios ≥ 0.
8. PNG válido, gerado sem tela: diagonal e uma curva por modelo, 800 predições juntas, mesmas 10 faixas, eixos em português.
9. CSV idêntico ao repetir. O PNG não é comparado byte a byte.
10. Avisos: `AVISO: brier de <modelo> >= taxa_base`; `AVISO: roc_auc de <modelo> < 0,5`.
11. Entrada com coluna faltando, vazio ou p fora de [0, 1]: saída diferente de 0, mensagem, nenhum arquivo parcial.

Fora do escopo: calibração, intervalo por bootstrap (é do teste final), apontar "melhor modelo", testes estatísticos, métricas de política, mexer em `modelos.py`.

### 03. Evidência incompleta (`modelos.py --ocultar`, `avaliar.py --ocultar`)

1. `modelos.py --ocultar` grava só `predicoes_dev_oculta.csv`. `predicoes_dev.csv` e `cortes.json` continuam idênticos.
2. 48.000 linhas (800 × 3 modelos × 20 variáveis); colunas `record_id,modelo,variavel_oculta,p_ruim`; cada par (modelo, variável) tem os 800 casos uma vez; `p_ruim` entre 0 e 1; ordem fixa.
3. Mesmas partições e modelos da issue 01: treina com todas as variáveis e esconde só na inferência. Nas redes, remove a coluna; nunca passa `NaN`.
4. `--verificar`: (a) Naive Bayes com variável escondida = produto das tabelas sem aquele fator, 5 linhas, 1e-9; (b) nas duas redes, igual a `VariableElimination.query` com a evidência sem a variável; (c) regressão: igual a `prever` com a coluna preenchida conforme D2.
5. Para cada um dos 60 pares, ao menos uma predição difere da completa.
6. `avaliar.py --ocultar` grava `evidencia_incompleta.csv`: 60 linhas, colunas `modelo,variavel_oculta,roc_auc,brier,delta_roc_auc,delta_brier`; delta = escondido − completo; bate com `metricas_dev.csv` a 1e-9.
7. `avaliar.py` sem opção gera os mesmos arquivos de antes.
8. Aviso: `AVISO: ocultar laufkont não piorou mais que ocultar telef em <modelo>`.

Fora do escopo: esconder duas ou mais variáveis, valor ausente no treino, outras imputações, gráfico, texto de "importância" de variáveis.

### 04. Camada de decisão (`decisao.py`, `test_decisao.py`, `config/utilidade.json`)

1. `config/utilidade.json` no formato do plano: `aprovar` 100 / −400, `rejeitar` 0 / 0, `analise_manual` 60 / −40 (c = 40), e `hipoteses` dizendo: valores demonstrativos, analista sempre acerta, pendente do orientador.
2. `decisao.py` não tem valor de utilidade escrito no código; tudo vem do JSON ou de argumento.
3. `uv run python codigo/test_decisao.py` sai com 0; só `assert`.
4. Exemplo da apresentação: p = 0,20, +100, −400 dá 0; com perda 600 dá −40.
5. Extremos: p = 0 dá U(a, bom); p = 1 dá U(a, ruim); UE(rejeitar) = 0 para todo p.
6. Fronteiras: para c em {0, 20, 40, 60}, numa grade de p com passo 0,001, a ação é aprovar se p < c/400, análise manual se c/400 ≤ p ≤ 1 − c/100, rejeitar acima.
7. Sem faixa: para c em {90, 100}, a análise manual não aparece e o corte aprovar/rejeitar é 0,20.
8. Outra matriz: perda 600 e c = 40 dão fronteiras 40/600 e 0,60. Garante que nada está fixo em 0,10 e 0,60.
9. Empate conforme D5.
10. p < 0, p > 1 ou `NaN` levanta `ValueError`.
11. Regra de limiar fixo: p < 0,5 aprova, p ≥ 0,5 rejeita.
12. `uv run python codigo/decisao.py` grava `politicas_dev.csv` (800 linhas: `record_id,kredit` e 6 colunas `acao_<nb|tan|logreg>_<ue|limiar>`) e `resumo_politicas_dev.csv` (6 linhas: `modelo,regra,utilidade_media,n_aprovar,n_rejeitar,n_analise_manual,n_mudam_vs_outra_regra`).
13. Consistência: contagens somam 800; nas linhas `limiar`, `n_analise_manual = 0`; `utilidade_media` recalculável a 1e-9.
14. Trocar a perda para 600 numa cópia do JSON muda as ações sem mexer no código.
15. Aviso: `AVISO: a ação <x> não aparece em <modelo>/<regra>`.
16. Arquivos idênticos ao repetir.

Fora do escopo: escolher modelo ou "melhor política", mudar valores da matriz, sensibilidade, gráficos, quarta ação, analista que erra, conjunto de teste, calibrar probabilidades.

### 05. Sensibilidade (`sensibilidade.py`)

1. `uv run python codigo/sensibilidade.py` lê só `config/utilidade.json` (é analítico, não usa predições); grava `sensibilidade.png` e `sensibilidade.csv`.
2. CSV: `perda,custo_analise,limiar_inferior,limiar_superior`; grade conforme D7 (84 linhas); o ganho vem do JSON.
3. Forma fechada (ganho G, perda L): se c < G·L/(G + L), inferior = c/L e superior = 1 − c/G; senão os dois valem G/(G + L). Linhas conhecidas: (400, 40) dá 0,10 e 0,60; (400, 80) e (400, 100) dão 0,20 e 0,20.
4. `--verificar`: em cada linha da grade, a função de `decisao.py` devolve aprovar logo abaixo do limiar inferior, análise manual no meio da faixa (quando existe) e rejeitar logo acima do superior.
5. Importa a conta de `decisao.py`; não reimplementa a utilidade esperada.
6. PNG válido, sem tela: custo no eixo x, risco no y, uma curva ou painel por perda, regiões nomeadas, rótulos em português.
7. CSV idêntico ao repetir.

Fora do escopo: sensibilidade com dados, variar o ganho, gráfico interativo, comparar modelos, mudar `decisao.py` ou o JSON.

### 06. Demonstração (`demo.py`)

1. `uv run python codigo/demo.py <record_id> [--modelo nb|tan|logreg]` imprime: o caso, os três `p_ruim` com 6 casas, a utilidade esperada de cada ação para o modelo escolhido, as fronteiras e a ação recomendada.
2. Não grava arquivo nem salva modelo.
3. Para 3 casos de partições diferentes, os três `p_ruim` são iguais aos de `predicoes_dev.csv` a 1e-6 e a ação é igual à de `politicas_dev.csv` (depende de D1).
4. Usa `modelos.prever` e as funções de `decisao.py`; não reimplementa.
5. `record_id` inexistente ou fora do dev: uma linha de mensagem em português, saída diferente de 0, sem traceback.
6. Sem argumento: mensagem de uso, saída 2.
7. Mesma saída ao repetir; menos de 30 s.

Fora do escopo: digitar um caso novo, esconder variável, interface web, cores, explicação textual da decisão, casos do teste.

### 07. Caminho do teste final (`--final` em `modelos.py`, `avaliar.py`, `decisao.py`)

A factory escreve e testa o caminho com linhas do dev. Quem o executa sobre o teste é o autor (passo 10 do plano).

1. `uv run python codigo/modelos.py --final <arquivo>` treina os três modelos no dev inteiro e grava só `resultados/predicoes_teste.csv`. O caminho do arquivo é argumento obrigatório; nenhum nome de arquivo de teste aparece no código.
2. `predicoes_teste.csv`: colunas `record_id,kredit,p_nb,p_tan,p_logreg`; uma linha por linha do arquivo de entrada, na mesma ordem; `p_*` finito, estritamente entre 0 e 1.
3. Os cortes usados são os de `resultados/cortes.json` (dev inteiro); estados fixos como na issue 01.
4. Se `resultados/predicoes_teste.csv` já existe, o script termina com mensagem e saída diferente de 0, sem sobrescrever.
5. `--final` não altera nenhum arquivo `*_dev*` nem `cortes.json`.
6. `--verificar` cobre o caminho com um arquivo falso: as 160 linhas da partição 0 do dev, gravadas em pasta temporária. O resultado tem 160 linhas e é igual a `prever(dev, falso)` a 1e-12.
7. `uv run python codigo/avaliar.py --final` lê `predicoes_teste.csv` e grava `metricas_teste.csv` e `calibracao_teste.png`: uma linha por modelo e a linha `taxa_base` (previsão = proporção de ruins do dev, 0,30), colunas `modelo,roc_auc,roc_auc_ic_inf,roc_auc_ic_sup,brier,brier_ic_inf,brier_ic_sup,log_loss,ece`.
8. Intervalo por bootstrap: 2000 reamostras das linhas com reposição, semente 2026, percentis 2,5 e 97,5. O valor pontual fica dentro do intervalo.
9. `uv run python codigo/decisao.py --final` lê `predicoes_teste.csv` e grava `politicas_teste.csv` e `resumo_politicas_teste.csv`, no mesmo formato dos arquivos do dev.
10. Sem `predicoes_teste.csv`, `avaliar.py --final` e `decisao.py --final` terminam com mensagem e saída diferente de 0.
11. Nenhum arquivo `*_teste*` é commitado pelo PR; o gate confere que não existem em `resultados/`.
12. Os comandos sem `--final` geram os mesmos arquivos de antes, idênticos.

Fora do escopo: executar sobre o teste de verdade, escolher modelo, calibrar, evidência incompleta no teste, sensibilidade no teste, qualquer mudança no treino dos modelos.

## 5. `factory/checks.sh`

O gate roda o `checks.sh` da cópia principal com a pasta de trabalho no ramo do job, então o ramo não troca o próprio juiz. Ele e um `factory/verificar_saidas.py` são escritos antes da issue 01, já com os blocos das 7 issues; cada bloco só roda se o script existir.

| # | Checagem | Tempo |
|---|---|---|
| 1 | Hashes dos dados (`shasum -a 256 -c SHA256SUMS`) | < 1 s |
| 2 | Nada apagado em `codigo`, `config`, `resultados`, exceto `baseline_logreg.py` | < 1 s |
| 3 | Busca por `teste.csv`, `sgc.csv`, `dados/brutos`, listagem de pastas em `codigo/` (fora `preparar_sgc.py`): tem de vir vazia | < 1 s |
| 4 | Busca por `fillna`, `nan_to_num`, `pickle`, `joblib`; e por `pgmpy` ou `.fit(` em `avaliar.py` | < 1 s |
| 5 | `uv sync --frozen` | segundos (não medido) |
| 6 | Caixa de areia: pasta temporária só com `codigo/`, `config/` e `dev.csv` | < 1 s |
| 7 | Autotestes (`--verificar`) e `test_decisao.py` | ~10 s |
| 8 | Todos os scripts do zero, na ordem; `demo.py` com caso inexistente tem de falhar | ~30 a 50 s (estimado) |
| 9 | Cada CSV e JSON gerado é idêntico ao commitado em `resultados/` | < 1 s |
| 10 | `verificar_saidas.py`: colunas, contagens, cruzamentos; imprime os avisos sem falhar | ~3 s |
| 11 | Cada script tem docstring com `Uso:` | < 1 s |

Total estimado: cerca de 1 minuto. Não criar modo rápido.

Arquivos protegidos contra alteração (`protected_paths`): `dados/*`, `codigo/preparar_sgc.py`, `factory/*`, `PLANO.md`, `pyproject.toml`, `uv.lock`; depois da issue 04, também `config/utilidade.json` e `codigo/test_decisao.py`.

**Quanto vale a proteção do teste.** A caixa de areia e a busca pegam bem o acidente, que é o risco real (por exemplo, o agente usar `sgc.csv` para listar categorias). Não seguram um agente decidido a olhar: os dados brutos estão no git e a divisão se reproduz com a semente. A garantia final é o commit de congelamento e o teste final rodado pelo autor.

## 6. Ordem das issues

| Onda | Issues | Motivo |
|---|---|---|
| 1 | 01 | Tudo lê `predicoes_dev.csv` |
| 2 | 02 e 04, em paralelo | Arquivos diferentes; só leem a saída da 01 |
| 3 | 03, 05 e 06, em paralelo | 03 altera `modelos.py` e `avaliar.py`; 05 e 06 só importam |
| 4 | 07 | Altera `modelos.py`, `avaliar.py` e `decisao.py`; precisa de 03 e 04 já no `main` |

A factory roda até 3 jobs por vez e não controla dependência entre issues: só pôr o rótulo `factory` nas issues da onda atual. Nenhum PR edita `AGENTS.md` nem `README.md`.

Antes da issue 01, nesta ordem:

1. Criar o repositório no GitHub e enviar o `main`.
2. Instalar a factory com `factory/install.sh <este repositório>` (script da `triboni_factory`, em construção em 15/11/2026). Ele copia agentes, skill e `factory/bin/`, cria os 3 rótulos e ajusta o `.gitignore`. Sobrescreve os agentes a cada execução; cria `config.json` e `checks.sh` só se faltarem e depois os preserva.
3. Substituir o `factory/checks.sh` gerado: o modelo da factory procura npm, pytest ou cargo e, neste repositório, falha de propósito. Escrever o da seção 5 e o `factory/verificar_saidas.py`.
4. Editar `factory/config.json`: `protected_paths` da seção 5. O merge fica automático (D9).
5. Só então rotular a issue 01.

## 7. Riscos de agente escrevendo código de experimento

| Risco | Mitigação |
|---|---|
| Ajustar até o resultado ficar bonito | Constantes congeladas (G4); nenhum critério com valor de resultado; regra "nunca justifique uma mudança por uma métrica" |
| Vazamento sem intenção | Critérios 01.3 a 01.5; caixa de areia |
| Fazer o teste passar em vez de fazer a conta | Testes com outra matriz (04.8, 04.14); G6; resposta conhecida do prior (01.6a) |
| Código que o autor não consegue defender | G7 e G8; leitura de cada PR depois do merge; releitura completa antes do commit de congelamento |
| Decisão de pesquisa tomada pelo agente | D3 e D4 fora do escopo; regra "toda escolha que dependa de um número é do autor: pare e pergunte" |

## 8. Modelo de issue

```markdown
# NN: <título curto, no imperativo>

## Objetivo
Uma ou duas frases. Passo N do PLANO.md.

## Contexto
- Ler antes: PLANO.md (itens X e Y), AGENTS.md.
- Arquivos que este PR cria ou altera: `codigo/...`
- Depende de (já no main): issue NN.
- Tamanho: um PR só. Não dividir e não ampliar.

## Entradas
| Arquivo | Colunas usadas |

## Saídas
| Arquivo | Colunas, tipos, número de linhas |

## Comportamento
Lista numerada do que o script faz, na ordem. Sem resultado esperado.

## Critérios de aceitação
Cada item: o que se observa + o comando que confere.

## Já conferido pelo gate (não repetir na especificação)

## Avisos (não são critérios)

## Fora do escopo

## Decisões já tomadas (não perguntar, não mudar)

## Hipóteses a confirmar pelo autor

## Descrição do PR deve conter
`## O que este script faz`, `## Como rodar`, `## Avisos impressos`.
```

## 9. Não conferido

Tempo de `uv sync` num ramo novo; tempo total do modo `--ocultar`; se o PNG sai idêntico entre execuções; a regressão logística (não foi executada no levantamento); o comportamento do orquestrador da factory além de busca por palavra.
