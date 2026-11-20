# APÊNDICES

## APÊNDICE A – Como reproduzir os resultados

Todos os arquivos de `resultados/` são gerados por sete scripts Python que leem CSV e gravam tabelas e figuras, sem servidor, banco de dados nem modelo salvo em arquivo. Os comandos abaixo partem da raiz do repositório, rodam sem interação e usam Python 3.12 com as dependências travadas pelo `uv`, inclusive o `pgmpy` 1.1.2.

### A.1 Ambiente

```bash
uv sync --frozen
```

A opção `--frozen` instala exatamente as versões do `uv.lock`. A versão do `pgmpy` não deve ser atualizada, porque a interface da biblioteca mudou entre as versões 1.0 e 1.1.2.

### A.2 Ordem de execução

Cada script grava apenas em `resultados/`; a exceção é `preparar_sgc.py`, que grava em `dados/processados/`. Toda fonte de aleatoriedade usa a semente 2026, e rodar o mesmo comando duas vezes gera arquivos CSV e JSON idênticos byte a byte. As figuras PNG não foram comparadas byte a byte entre execuções.

**Quadro A.1** – Comandos, em ordem, e arquivos gravados

| Passo | Comando | Grava |
|---|---|---|
| Divisão desenvolvimento/teste | `uv run python codigo/preparar_sgc.py` | `dados/processados/sgc.csv`, `dev.csv`, `teste.csv`, `SHA256SUMS` |
| Predições no desenvolvimento | `uv run python codigo/modelos.py` | `predicoes_dev.csv`, `cortes.json`, `tan_arestas.csv` |
| Métricas e calibração | `uv run python codigo/avaliar.py` | `metricas_dev.csv`, `calibracao_dev.png` |
| Evidência incompleta | `uv run python codigo/modelos.py --ocultar`, depois `uv run python codigo/avaliar.py --ocultar` | `predicoes_dev_oculta.csv`, `evidencia_incompleta.csv` |
| Camada de decisão | `uv run python codigo/decisao.py` | `politicas_dev.csv`, `resumo_politicas_dev.csv` |
| Sensibilidade | `uv run python codigo/sensibilidade.py` | `sensibilidade.csv`, `sensibilidade.png` |
| Estudo de seleção (secundário) | `uv run python codigo/modelos.py --selecao`, depois `uv run python codigo/avaliar.py --selecao` | `predicoes_selecao.csv`, `selecao_dev.csv`, `selecao_escolha.csv` |
| Demonstração | `uv run python codigo/demo.py <record_id> [--modelo nb\|tan\|logreg]` | nada; imprime no terminal |

### A.3 Autotestes e conferência

Os scripts `modelos.py`, `avaliar.py` e `sensibilidade.py` têm o modo `--verificar`, que confere contas com resposta conhecida e não grava nada; `test_decisao.py` usa apenas `assert` e inclui o exemplo da apresentação de 15/10/2026 (com p = 0,20, ganho de 100 e perda de 400, a utilidade esperada de aprovar é 0; com perda de 600, é −40).

```bash
uv run python codigo/modelos.py --verificar
uv run python codigo/avaliar.py --verificar
uv run python codigo/sensibilidade.py --verificar
uv run python codigo/test_decisao.py
```

Os arquivos gerados são versionados junto com o código. Depois de rodar tudo, a reprodução é confirmada se o comando abaixo não imprimir nada e terminar com código 0:

```bash
git diff --exit-code -- 'resultados/*.csv' 'resultados/*.json'
```

Esse teste confere que os arquivos são idênticos aos publicados, não que o modelo é bom.

### A.4 Teste final

O conjunto de teste foi usado uma única vez, em 17/11/2026, sobre o commit de congelamento `49d77ff`, e todos os comandos terminaram com código de saída 0. Os comandos, na ordem, foram:

```bash
uv run python codigo/modelos.py --final <arquivo do teste>
uv run python codigo/avaliar.py --final
uv run python codigo/decisao.py --final
```

Eles gravam `predicoes_teste.csv`, `metricas_teste.csv`, `calibracao_teste.png`, `politicas_teste.csv`, `resumo_politicas_teste.csv` e `diferenca_politicas_teste.csv`; os intervalos usam bootstrap com 2000 reamostras e semente 2026. O primeiro comando exige o caminho do arquivo de teste como argumento e recusa sobrescrever `predicoes_teste.csv` se ele já existir.

Quem reproduz sem o arquivo de teste obtém todos os resultados de desenvolvimento, mas não os `*_teste*`: a divisão é determinística (semente 2026) e sai de `dados/brutos/`, que não acompanha a descrição do código.

---

## APÊNDICE B – Plano de análise

O plano de análise foi escrito em 15/11/2026, antes de existir qualquer resultado, e fixa o que será reportado e como cada desfecho será lido. Segue a cópia integral do documento do repositório, com os títulos rebaixados um nível; os links relativos remetem a arquivos do repositório.

Escrito em 15/11/2026, **antes de existir qualquer resultado**. Diz o que será reportado e como cada desfecho será lido. O objetivo é que nenhuma decisão de análise dependa do que os números mostrarem.

Fontes: [PLANO.md](../PLANO.md), [decisoes.md](decisoes.md) e [criterios-de-aceite.md](criterios-de-aceite.md). Este arquivo não cria decisão de modelo: só fixa como ler o que o experimento produzir. Itens que dependem de um número e ainda não têm dono estão marcados **a confirmar pelo autor**.

### 1. Pergunta

A política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) tem (1) limiares explícitos, reproduzíveis a partir da matriz de utilidade e de `p`, e (2) que efeito medido sobre as ações e a utilidade média, em comparação com um limiar fixo de 0,5?

- **Parte 1** é uma propriedade da política: vale para qualquer escore e não depende de resultado. Fica demonstrada pelas fronteiras `c/400` e `1 − c/100` (na matriz demonstrativa) e pela tabela de sensibilidade.
- **Parte 2** é o que o experimento mede.

### 2. O que será reportado, qualquer que seja o resultado

| Item | Arquivo | Onde entra |
|---|---|---|
| ROC-AUC, PR-AUC, Brier, log loss e erro de calibração dos três modelos e da taxa base, com média e desvio entre as 5 partições | `metricas_dev.csv` | Capítulo 4.1 |
| Diagrama de calibração | `calibracao_dev.png` | Capítulo 4.1 |
| Queda por variável escondida | `evidencia_incompleta.csv` | Capítulo 4.2 |
| Utilidade média e distribuição das ações por modelo e regra | `resumo_politicas_dev.csv` | Capítulo 4.3 |
| Fronteiras de decisão por perda e custo da análise | `sensibilidade.csv`, `sensibilidade.png` | Capítulo 4.4 |
| Arestas do TAN em cada partição | `tan_arestas.csv` | Capítulo 4.1 |
| No teste final: métricas com intervalo, utilidade média com intervalo e a diferença pareada entre as regras | `metricas_teste.csv`, `resumo_politicas_teste.csv`, `diferenca_politicas_teste.csv` | Capítulos 4.1 e 4.3 |

Todos os três modelos aparecem em todas as tabelas, também os que não vão para o texto principal.

### 3. Comparação principal

Fixada antes de ver métricas (decisão P5):

- **Modelo:** TAN.
- **Regras comparadas:** a política de três ações por utilidade esperada e o corte 0,5 de duas ações.
- **Medida:** diferença pareada de utilidade média, com intervalo por bootstrap (2000 reamostras, semente 2026, percentis 2,5 e 97,5) no teste final.

Naive Bayes e regressão logística vão para o apêndice, na mesma estrutura. A tabela é descritiva: a diferença mistura modelo, representação e conjunto de ações, e não é chamada de "efeito do modelo" nem de "efeito da regra".

### 4. Como cada desfecho será lido

Regras de leitura definidas agora. Nenhuma depende do valor observado.

| Se o resultado for | O texto diz |
|---|---|
| O intervalo da diferença pareada exclui 0 a favor da utilidade esperada | "Diferença observada a favor da política de utilidade, com intervalo que exclui zero." Sem afirmar causa |
| O intervalo inclui 0 | "Sem evidência de diferença com 200 casos e 60 ruins." Não se conclui que as políticas são iguais |
| O intervalo exclui 0 a favor do limiar 0,5 | Reportado como saiu, junto com a ressalva de que a regra fixa só tem duas ações |
| A diferença de ROC-AUC entre dois modelos é menor que 0,03 | Tratada como ruído, como diz o plano (item 6). Nenhum modelo "vence" |
| O Brier de um modelo é igual ou maior que o da taxa base (0,21) | "Não melhor que prever a taxa base." Entra no texto |
| Alguma ação não aparece numa política | Reportado (é o `AVISO:` do script). Não se muda a matriz por isso |
| O erro de calibração de um modelo é alto | Reportado. A calibração só é medida; não há correção (decisão P1) |
| Esconder uma variável não muda nenhuma predição | Reportado como aviso |

### 5. O que não será feito

1. Ajustar modelo, parâmetro, semente, faixa ou variável por causa de uma métrica (`AGENTS.md`, regra 3).
2. Escolher o modelo do texto depois de ver as métricas (o TAN já está fixado).
3. Rodar o teste final mais de uma vez ou antes do commit de congelamento.
4. Abrir `teste.csv`, `sgc.csv` ou `dados/brutos/` fora do `preparar_sgc.py` e do teste final.
5. Remover casos, trocar a divisão ou mudar a matriz de utilidade porque o resultado incomodou.

Tudo acima vale exceto o estudo da §9, que é secundário, pré-registrado e roda só no modo `--selecao`.

### 6. Limitações a declarar

1. A base não traz o resultado das ações que não foram tomadas: não há efeito causal nem lucro real, só simulação.
2. O teste tem 60 casos ruins; diferenças pequenas são ruído.
3. A matriz de utilidade é demonstrativa e "o analista sempre acerta".
4. A regressão logística usa as contínuas originais e as redes usam 3 faixas.
5. O intervalo por bootstrap não cobre a variação do treino (decisão P4).
6. O espaço de estados foi fixado no dev inteiro, um vazamento brando que não usa rótulo.
7. A comparação com o corte 0,5 não é um teste de "utilidade esperada contra qualquer limiar", porque a utilidade esperada já equivale a limiares.

### 7. Se algo mudar

Qualquer mudança neste plano depois de existirem resultados vira uma linha em [decisoes.md](decisoes.md), com data e motivo, **antes** de rodar de novo. A mudança também é declarada no texto como desvio do plano de análise.

### 8. Decidido pelo autor em 18/11/2026

- O intervalo de 95% é o critério de leitura da diferença (seção 4), o mesmo nível do bootstrap das métricas. Decidido em 18/11/2026: confirma o que já estava escrito.
- O limite de 0,03 de AUC, que vem do plano, vale só para ROC-AUC. PR-AUC é apenas descrita, sem conclusão de ruído. Decidido em 18/11/2026; registro em `docs/decisoes.md`.

### 9. Estudo de seleção (secundário, pré-registrado)

Status: estudo secundário pré-registrado em 16/11/2026, antes da execução do teste final.

**Grade fechada, 8 configurações** ({NB, TAN} × tamanho equivalente BDeu {1, 5, 10, 50}):

| id | Modelo | Tamanho equivalente |
|---|---|---|
| `nb_ess1` | NB | 1 |
| `nb_ess5` | NB | 5 (baseline) |
| `nb_ess10` | NB | 10 |
| `nb_ess50` | NB | 50 |
| `tan_ess1` | TAN | 1 |
| `tan_ess5` | TAN | 5 (baseline) |
| `tan_ess10` | TAN | 10 |
| `tan_ess50` | TAN | 50 |

A ordem da tabela é a ordem da grade. Fora da grade: K2, outras faixas, seleção de variáveis, hill climbing, Platt/isotônica e reponderação.

**Validação cruzada aninhada.** Partições externas = as 5 atuais. Em cada externa, as 640 linhas de treino são divididas por `StratifiedKFold(5, shuffle=True, random_state=2026)`; cada configuração é treinada e avaliada nas partições internas.

**Regra de escolha.** Menor log loss médio nas partições internas. Empate (diferença < 1e-9) resolvido pela ordem da grade. A configuração escolhida em cada externa prevê as 160 linhas dela; daí saem `p_sel` (as linhas com `fold_interno` = -1 da configuração escolhida) e a linha "aninhado". A escolha também é recalculada no dev inteiro (linha `dev` de `selecao_escolha.csv`), só para relato.

**Relato obrigatório.** As 8 linhas da grade, o número de comparações (8) e a linha "aninhado", qualquer que seja o resultado.

**Declaração obrigatória de viés.** A grade foi definida depois de ver `metricas_dev.csv` e motivada por ele (TAN pior que NB; hipótese `verw` em [resultados-dev.md](resultados-dev.md)). O aninhamento corrige o viés de escolher entre as 8 configurações, mas não o de ter desenhado a grade olhando o mesmo dev. O texto da monografia declara isso.

**Leitura dos desfechos.** Diferença de ROC-AUC menor que 0,03 é ruído, como na §4. Não se fala em "melhor modelo": relata-se qual configuração a regra escolheu e quanto ela difere do baseline.

**O que não muda.** A tabela 2×2 e a análise primária continuam com NB e TAN de BDeu 5 (P5 intacta). `p_sel` é análise secundária e aparece rotulada como tal.

Saídas:

- `resultados/predicoes_selecao.csv`: `config, record_id, fold_externo, fold_interno, p_ruim`; `fold_interno` = -1 é a predição externa; 32.000 linhas.
- `resultados/selecao_dev.csv`: as 8 configurações e a linha `aninhado` (sem linha `dev`).
- `resultados/selecao_escolha.csv`: `fold_externo` (0 a 4 e `dev`) × 8 configurações, com `log_loss_interno` e `escolhida`; 48 linhas.
