# Plano do TCC

Redes bayesianas e utilidade esperada aplicadas à seleção de *next best action* em sistemas automatizados de decisão.

Rodrigo Mialichi Triboni · Engenharia de Controle e Automação, UFU · Orientador: Fabio Vincenzi

Situação: **fechado em 15/11/2026**, salvo as respostas do orientador (item 11). O código é escrito pela software factory a partir das issues em `docs/issues/`; regras em [AGENTS.md](AGENTS.md) e [docs/criterios-de-aceite.md](docs/criterios-de-aceite.md).

## 1. Pergunta

Uma política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) tem (1) limiares explícitos, que qualquer pessoa reproduz a partir da matriz de utilidade e de `p`, e (2) que efeito medido sobre as ações e a utilidade média, em comparação com um limiar fixo de 0,5?

## 2. O que o trabalho entrega

- Um modelo de risco: rede bayesiana que estima a probabilidade de um crédito ser ruim.
- Uma camada de decisão: escolhe a ação de maior utilidade esperada.
- Uma comparação com regressão logística e regra de limiar.
- Uma análise de sensibilidade aos custos.
- A monografia.

Não entrega: produto, painel web, servidor, banco de dados nem modelo de linguagem.

## 3. Formato do software

Scripts Python que leem CSV e gravam tabelas e figuras. Sem frontend e sem backend.

Para a defesa, um script de terminal recebe um caso e mostra o risco estimado e a utilidade de cada ação.

Linguagem e bibliotecas: Python 3.12, `pgmpy` 1.1.2 (redes bayesianas), `scikit-learn` (baseline e métricas), `pandas`, `matplotlib`. Dependências travadas com `uv`:

```
uv init --bare --python 3.12
uv add "pgmpy==1.1.2" scikit-learn pandas matplotlib
```

Todo script roda como `uv run python codigo/<script>.py`. `pyproject.toml` e `uv.lock` entram no git.

A versão do `pgmpy` é fixa porque a API mudou entre 1.0 e 1.1.2 e a documentação do site está atrasada. Nomes conferidos por execução em 15/11/2026:

| Necessidade | Nome na 1.1.2 |
|---|---|
| Naive Bayes | Rede em estrela: `DiscreteBayesianNetwork([("kredit", f) for f in variaveis])`. A classe `pgmpy.models.NaiveBayes` treina, mas falha em `predict_probability` na 1.1.2 |
| TAN | `pgmpy.estimators.TreeSearch(df).estimate(estimator_type="tan", class_node="kredit")`; devolve um grafo, que vira `DiscreteBayesianNetwork(dag.edges())` |
| Prior BDeu | `pgmpy.parameter_estimator.DiscreteBayesianEstimator(state_names=..., prior_type="BDeu", equivalent_sample_size=5)`, passado como instância em `model.fit(df, estimator=...)` |
| Probabilidade por linha | `model.predict_probability(df_sem_kredit)`; a coluna `kredit_0` é a probabilidade de ruim |
| Variável escondida | Remover a coluna do DataFrame antes de `predict_probability`; nunca passar `NaN` |
| Inferência de um caso | `pgmpy.inference.VariableElimination(model).query(["kredit"], evidence={...})` |

Não conferido por execução: hill climbing (`pgmpy.causal_discovery.HillClimbSearch`, escore `"bic-d"`), que é opcional.

## 4. Dados

South German Credit, 1000 registros, 20 variáveis preditoras mais o alvo `kredit` (0 = ruim, 300 casos; 1 = bom, 700 casos). É a versão corrigida do German Credit Data citado na proposta.

- `dados/brutos/`: original da UCI e dicionário (`codetable.txt`).
- `dados/processados/sgc.csv`: base limpa.
- `dados/processados/dev.csv` (800, 240 ruins) e `teste.csv` (200, 60 ruins): divisão estratificada nova, semente 2026, gerada no passo 1.

A divisão antiga (semente 42) foi descartada porque o teste dela já tinha sido aberto para a regressão logística em um trabalho anterior. O teste novo fica fechado até o passo 10 e todos os modelos, inclusive o baseline, são avaliados nele uma única vez.

Cuidados com a base:

- **Alvo invertido:** 0 é ruim. Toda coluna `p_*` gravada é a probabilidade de **ruim**.
- **Contínuas (3):** `laufzeit` (duração), `hoehe` (valor), `alter` (idade), em 3 faixas por tercis. As outras 17 já são categóricas.
- **Categorias raras:** por exemplo `bishkred`=4 (6 casos), `verw`=8 (9), `verw`=4 e `verw`=10 (12 cada). Por isso o prior BDeu e a lista fixa de estados (`state_names`) com tudo que aparece no dev.
- **Tipos:** manter todos os valores como inteiros; tirar `record_id` antes de chamar o `pgmpy`.
- **Nomes em alemão** ficam no código; a tradução entra só na monografia.

## 5. Algoritmos

| Etapa | Escolha | Motivo |
|---|---|---|
| Discretização | Valor, duração e idade em 3 faixas por tercis, com cortes aprendidos só no treino de cada parte da validação cruzada | A rede discreta exige; as outras variáveis já são categóricas |
| Estrutura 1 | Naive Bayes | Referência mais simples |
| Estrutura 2 | TAN (Naive Bayes aumentado por árvore) | Permite dependência entre variáveis |
| Estrutura 3 (opcional) | Busca hill climbing com BIC | Estrutura livre, aprendida dos dados |
| Probabilidades | Estimação bayesiana com prior BDeu | Evita probabilidade zero em combinações raras |
| Inferência | Eliminação de variáveis, exata | A rede é pequena |
| Calibração | Só medir (decidido em 15/11/2026). Não há correção de calibração; a necessidade de calibrar vem da literatura e o experimento mede o erro de calibração. Se o autor mudar de ideia depois de ver `metricas_dev.csv`, é issue nova | Naive Bayes costuma exagerar a confiança; a escolha não pode ser do agente |
| Decisão | Utilidade esperada de cada ação; escolhe a maior | Núcleo do trabalho |
| Comparação | {Naive Bayes, TAN, regressão logística} × {limiares derivados da utilidade, limiar fixo de 0,5}. O TAN vai para a tabela 2×2 do texto (decidido em 15/11/2026, antes de qualquer métrica); os três modelos ficam no apêndice | Compara uma política de três ações por utilidade com um corte de duas ações. A diferença mistura modelo, representação (a regressão logística usa as contínuas originais, as redes usam 3 faixas) e conjunto de ações |
| Validação | Cruzada estratificada em 5 partes, só no dev | Não gasta o teste |
| Evidência incompleta | Esconder uma variável por vez na inferência e medir a queda de ROC-AUC e Brier | A rede infere sem a variável; na regressão logística a variável escondida é preenchida com a mediana do treino (3 contínuas) ou a moda do treino (17 categóricas), para haver comparação |

Utilidade esperada de uma ação `a`, com risco `p` de o caso ser ruim:

```
UE(a) = (1 − p) · U(a, bom) + p · U(a, ruim)
```

Ações: aprovar, rejeitar, encaminhar para análise manual. A matriz `U` é demonstrativa; as hipóteses ficam escritas em `config/utilidade.json`.

Proposta de matriz para levar ao orientador, com os valores da apresentação de 15/10/2026 e custo `c` da análise manual (hipótese: o analista acerta):

| Ação | Caso bom | Caso ruim |
|---|---|---|
| Aprovar | +100 | −400 |
| Rejeitar | 0 | 0 |
| Análise manual | 100 − c | −c |

Com essa matriz, a análise manual é escolhida quando `c/400 ≤ p ≤ 1 − c/100`. Com c = 40, a faixa vai de 0,10 a 0,60; com c > 80, nunca é escolhida. Em caso de empate, a prioridade é análise manual, depois rejeitar, depois aprovar (tolerância 1e-9).

**O que o trabalho afirma e o que não afirma.** Como a utilidade esperada de cada ação é uma reta em `p`, a política resultante equivale a uma regra de limiares sobre `p`. A contribuição não é uma regra de outro tipo: é **derivar os limiares dos custos, de forma explícita, e medir a calibração das probabilidades** (que a política exige probabilidade calibrada é resultado da literatura, não um achado deste experimento). Por isso a comparação é a tabela 2×2 acima, e não "utilidade esperada contra limiar".

Como os termos da pergunta são observados: *limiares explícitos e reproduzíveis* é, dadas a matriz em `config/utilidade.json` e `p`, qualquer pessoa obter a ação e as fronteiras (na matriz demonstrativa, `c/400` e `1 − c/100`); isso vale para qualquer escore e não distingue a rede da regressão logística. *Efeito medido* é a utilidade média e a distribuição das ações, com intervalo no teste, e o número de casos que mudam de ação entre as políticas (discordância, não consistência).

## 6. Métricas

- **Modelo de risco:** ROC-AUC, PR-AUC, Brier, log loss, erro de calibração, diagrama de calibração. No dev, média e desvio da validação cruzada; no teste, intervalo por bootstrap para ROC-AUC, PR-AUC, Brier e utilidade média, e para a diferença pareada de utilidade entre a regra de utilidade e o limiar fixo. Com 60 casos ruins no teste, diferença de AUC de 0,02 a 0,03 é ruído e não define vencedor.
- **Política:** utilidade média, distribuição das ações, casos que mudam de ação entre as políticas.
- **Sensibilidade:** ação recomendada em função do risco, da perda por inadimplência e do custo da análise manual.

## 7. Pastas e scripts

```
PLANO.md
README.md
pyproject.toml, uv.lock
codigo/
  preparar_sgc.py     base bruta → sgc.csv → dev.csv e teste.csv
  modelos.py          discretiza, treina Naive Bayes, TAN e regressão logística, grava probabilidades
  avaliar.py          métricas e diagrama de calibração; nunca treina
  decisao.py          utilidade esperada, regra de limiar, comparação das políticas
  sensibilidade.py    varia perda e custo da análise manual, gera o gráfico
  demo.py             um record_id → risco, utilidade de cada ação, ação recomendada
  test_decisao.py     confere a conta da utilidade com assert
config/
  utilidade.json      matriz de utilidade e hipóteses
dados/
  brutos/
  processados/
resultados/           tabelas e figuras geradas
monografia/
docs/
  proposta/           proposta submetida e apresentação de 15/10/2026
  pesquisa/
  uso-de-ia.md
```

São 7 scripts. Nenhum script fora dessa lista; ideia nova vai para o item 12.

- Não há `discretizar.py`: a proposta promete aprender os cortes só no treino de cada parte, então a discretização é uma função dentro de `modelos.py`.
- `baseline_logreg.py` (copiado do projeto antigo) sai depois que a função `build()` dele for levada para `modelos.py`. A regressão logística precisa usar as mesmas partições que as redes.
- `demo.py` treina de novo ao abrir (segundos), nas 4 partições que não contêm o caso pedido, para mostrar o mesmo risco de `predicoes_dev.csv`; não existe arquivo de modelo salvo. Modelo padrão: TAN.
- Autotestes ficam no modo `--verificar` de cada script; não há arquivo de teste além de `test_decisao.py`.

Arquivos passados entre scripts:

| Arquivo | Conteúdo |
|---|---|
| `resultados/predicoes_dev.csv` | Uma linha por caso: `record_id, kredit, fold, p_nb, p_tan, p_logreg` |
| `resultados/predicoes_dev_oculta.csv` | Formato longo: `record_id, modelo, variavel_oculta, p_ruim` |
| `resultados/resumo_politicas_dev.csv` | Seis linhas (modelo × regra): utilidade média e contagem de cada ação |
| `resultados/sensibilidade.csv` | Fronteiras para perda em {200, 400, 600, 800} × custo da análise em {0, 5, …, 100} |
| `resultados/tan_arestas.csv` | Arestas do TAN aprendido em cada partição: `fold, origem, destino` |
| `resultados/cortes.json` | Cortes das 3 variáveis contínuas, aprendidos no dev inteiro; usados só pelo teste final (o `demo.py` aprende os cortes nas 4 partições, via `prever`) |
| `config/utilidade.json` | `{"acoes": {"aprovar": {"bom": 100, "ruim": -400}, ...}, "hipoteses": "..."}` |

## 8. Passos, em ordem

| # | Passo | Script | Saída | Como conferir | Depende do orientador |
|---|---|---|---|---|---|
| 0 | Mensagem ao orientador | — | Respostas no item 11 | Enviada | — |
| 1 | Ambiente, primeiro commit e nova divisão | `preparar_sgc.py` | `dev.csv`, `teste.csv`, hashes em `dados/processados/SHA256SUMS` | 800/200, 240/60 ruins, nenhum `record_id` nos dois; toda categoria do teste existe no dev | Não |
| 2 | Teste de fumaça do `pgmpy` | começo de `modelos.py` | Nada | Naive Bayes e TAN treinam; `predict_probability` bate com `VariableElimination` em 5 linhas | Não |
| 3 | Predições no dev, validação cruzada em 5 partes | `modelos.py` | `predicoes_dev.csv`, `cortes.json`, `tan_arestas.csv` | 800 linhas, sem vazio, valores entre 0 e 1; autoteste `--verificar` passa | Não |
| 4 | Métricas e calibração | `avaliar.py` | `metricas_dev.csv`, `calibracao_dev.png` | Linha `taxa_base` dá Brier 0,21 exato. Brier de um modelo igual ou acima disso gera aviso, não falha | Não |
| 5 | Evidência incompleta | `modelos.py --ocultar`, `avaliar.py` | `predicoes_dev_oculta.csv`, `evidencia_incompleta.csv` | Para cada modelo e variável, ao menos uma predição muda. A comparação `laufkont` × `telef` é só aviso | Não |
| 6 | Camada de decisão | `decisao.py`, `test_decisao.py` | `politicas_dev.csv`, `resumo_politicas_dev.csv` | Testes passam; contagens somam 800. Ação ausente gera aviso | Código não; números finais sim (matriz) |
| 7 | Sensibilidade | `sensibilidade.py` | `sensibilidade.csv`, `sensibilidade.png` | Fronteiras batem com a conta à mão | Código não; valores sim |
| 8 | Demonstração | `demo.py` | Texto no terminal | Mesmo risco de `predicoes_dev.csv` para o mesmo caso | Não |
| 9 | Hill climbing (opcional) | `modelos.py` | Coluna a mais nas predições | Treina em poucos minutos | Não |
| 10 | Teste final | `modelos.py --final`, `avaliar.py`, `decisao.py` | `predicoes_teste.csv`, `metricas_teste.csv`, `calibracao_teste.png`, `politicas_teste.csv`, `resumo_politicas_teste.csv`, `diferenca_politicas_teste.csv` | Commit de congelamento antes; **rodado pelo autor, à mão, uma vez**; hash do commit anotado. O caminho `--final` é escrito pela factory (issue 07) e testado só com linhas do dev | Sim (matriz aprovada) |
| 11 | Monografia | — | Texto | Todo número aponta para um arquivo de `resultados/` | Formatação sim (modelo) |

Os capítulos de fundamentação e de método podem ser escritos em paralelo desde o passo 1.

Se o prazo apertar, cortar nesta ordem: passo 9, depois passo 5. A terceira ação não sai. Os passos 3, 6 e 11 não saem.

Na coluna "Como conferir", nada exige valor de resultado: critério restringe a forma, e resultado ruim é resultado (ver `docs/criterios-de-aceite.md`).

`test_decisao.py` inclui o exemplo da apresentação: com p = 0,20, +100 e −400, UE(aprovar) = 0; com perda de 600, UE(aprovar) = −40.

## 9. Monografia

| Capítulo | Conteúdo | De onde vem |
|---|---|---|
| 1 Introdução | Problema, pergunta, objetivos, limites | Proposta e itens 1 e 2 |
| 2 Fundamentação | Redes bayesianas, Naive Bayes e TAN, prior, inferência, calibração, utilidade esperada, escore de crédito | Proposta e `monografia/referencias.bib` |
| 3 Materiais e métodos | Base, divisão, discretização, modelos, validação, métricas, matriz e hipóteses, reprodutibilidade | Itens 4 a 8 |
| 4.1 Desempenho preditivo | Tabela de métricas e diagrama de calibração | Passos 4 e 10 |
| 4.2 Evidência incompleta | Queda por variável escondida | Passo 5 |
| 4.3 Política de decisão | Tabela 2×2, distribuição das ações | Passos 6 e 10 |
| 4.4 Sensibilidade | Gráfico das fronteiras | Passo 7 |
| 5 Discussão e limitações | Simulação, não política real; base pequena; utilidades demonstrativas | — |
| 6 Conclusão | Resposta à pergunta | Capítulo 4 |
| Apêndices | Como reproduzir; declaração de uso de IA | `docs/reproduzir.md` e `docs/uso-de-ia.md` |

A estrutura é a usual; o modelo exigido pela UFU ainda não foi conferido.

Referências de cada seção: [docs/mapa-de-referencias.md](docs/mapa-de-referencias.md). O arquivo `monografia/referencias.bib` tem 29 entradas; as 9 marcadas "A CONFERIR" foram sugeridas por IA de memória e só podem ser citadas depois de conferidas no original.

## 10. Decidido em 14/11/2026

- **Teste:** divisão refeita com semente nova (item 4).
- **Ações:** três (item 5).
- **Evidência incompleta:** entra em versão pequena, uma variável escondida por vez (item 5).

### Decidido em 15/11/2026

- **Quem escreve o código:** a software factory, uma issue por PR. A sessão interativa define critérios e escreve os `.md`.
- **Critério de aceite restringe a forma, nunca o resultado.**
- **Merge automático:** a factory faz merge quando o aprovador dela aprova (o merge é configurável; o autor optou por deixar automático). O autor lê a descrição de cada PR depois do merge e relê todo o código antes do commit de congelamento do passo 10.
- **Dados proibidos para o código:** `teste.csv`, `sgc.csv` e `dados/brutos/` (os três contêm as linhas do teste). Só `preparar_sgc.py` os lê.
- **Teste final:** rodado pelo autor; a factory só escreve o caminho.
- As demais decisões do dia (D1 a D11) estão em `docs/criterios-de-aceite.md`.

## 11. Em aberto, depende do orientador

1. **Prazo:** datas de entrega e de defesa.
2. **Matriz de utilidade:** ele aceita a matriz demonstrativa do item 5, com c = 40?
3. **Monografia:** modelo de documento exigido pelo curso (LaTeX, Word, normas ABNT da UFU).
4. **Avisos a dar:** a base passou a ser a South German Credit, versão corrigida da citada na proposta; o protótipo previsto na proposta virou demonstração em terminal; a pergunta foi reformulada em duas partes e deixou de falar em "calibrada", "consistentes" e "transparentes" (a calibração é só medida, e a contribuição é derivar limiares dos custos de forma explícita e medir o efeito). Ver `docs/decisoes.md`.

## 12. Para depois

Ideias que surgirem no caminho entram aqui, não no código.

- **Interface de uma tela** (15/11/2026): página única que mostra caso, risco, ação recomendada e controles de custo. Cumpriria o "protótipo" da proposta melhor que o terminal. Decidir só depois de o experimento estar pronto; até lá vale a demonstração de terminal. Se entrar: última issue, um arquivo, só mostra e não calcula, e é a única exceção à regra de não acrescentar dependência.
