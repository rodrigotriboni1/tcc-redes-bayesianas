# Plano de análise

Escrito em 15/11/2026, **antes de existir qualquer resultado**. Diz o que será reportado e como cada desfecho será lido. O objetivo é que nenhuma decisão de análise dependa do que os números mostrarem.

Fontes: [PLANO.md](../PLANO.md), [decisoes.md](decisoes.md) e [criterios-de-aceite.md](criterios-de-aceite.md). Este arquivo não cria decisão de modelo: só fixa como ler o que o experimento produzir. Itens que dependem de um número e ainda não têm dono estão marcados **a confirmar pelo autor**.

## 1. Pergunta

A política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) tem (1) limiares explícitos, reproduzíveis a partir da matriz de utilidade e de `p`, e (2) que efeito medido sobre as ações e a utilidade média, em comparação com um limiar fixo de 0,5?

- **Parte 1** é uma propriedade da política: vale para qualquer escore e não depende de resultado. Fica demonstrada pelas fronteiras `c/400` e `1 − c/100` (na matriz demonstrativa) e pela tabela de sensibilidade.
- **Parte 2** é o que o experimento mede.

## 2. O que será reportado, qualquer que seja o resultado

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

## 3. Comparação principal

Fixada antes de ver métricas (decisão P5):

- **Modelo:** TAN.
- **Regras comparadas:** a política de três ações por utilidade esperada e o corte 0,5 de duas ações.
- **Medida:** diferença pareada de utilidade média, com intervalo por bootstrap (2000 reamostras, semente 2026, percentis 2,5 e 97,5) no teste final.

Naive Bayes e regressão logística vão para o apêndice, na mesma estrutura. A tabela é descritiva: a diferença mistura modelo, representação e conjunto de ações, e não é chamada de "efeito do modelo" nem de "efeito da regra".

## 4. Como cada desfecho será lido

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

## 5. O que não será feito

1. Ajustar modelo, parâmetro, semente, faixa ou variável por causa de uma métrica (`AGENTS.md`, regra 3).
2. Escolher o modelo do texto depois de ver as métricas (o TAN já está fixado).
3. Rodar o teste final mais de uma vez ou antes do commit de congelamento.
4. Abrir `teste.csv`, `sgc.csv` ou `dados/brutos/` fora do `preparar_sgc.py` e do teste final.
5. Remover casos, trocar a divisão ou mudar a matriz de utilidade porque o resultado incomodou.

## 6. Limitações a declarar

1. A base não traz o resultado das ações que não foram tomadas: não há efeito causal nem lucro real, só simulação.
2. O teste tem 60 casos ruins; diferenças pequenas são ruído.
3. A matriz de utilidade é demonstrativa e "o analista sempre acerta".
4. A regressão logística usa as contínuas originais e as redes usam 3 faixas.
5. O intervalo por bootstrap não cobre a variação do treino (decisão P4).
6. O espaço de estados foi fixado no dev inteiro, um vazamento brando que não usa rótulo.
7. A comparação com o corte 0,5 não é um teste de "utilidade esperada contra qualquer limiar", porque a utilidade esperada já equivale a limiares.

## 7. Se algo mudar

Qualquer mudança neste plano depois de existirem resultados vira uma linha em [decisoes.md](decisoes.md), com data e motivo, **antes** de rodar de novo. A mudança também é declarada no texto como desvio do plano de análise.

## 8. A confirmar pelo autor

- Se o intervalo de 95% é o critério de leitura da diferença (seção 4) ou se prefere outro nível. Hoje está escrito 95%, o mesmo do bootstrap das métricas.
- Se o limite de 0,03 de AUC, que vem do plano, vale também para PR-AUC.
