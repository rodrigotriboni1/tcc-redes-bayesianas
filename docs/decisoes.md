# Registro de decisões

Uma linha por decisão: o que ficou decidido, por quê, e quem decidiu. Serve para responder à banca "por que foi feito assim" sem depender de memória.

Fontes: [PLANO.md](../PLANO.md) (itens 4, 5 e 10) e [criterios-de-aceite.md](criterios-de-aceite.md) (D1 a D11). Este arquivo não cria decisão: copia o que já está escrito. Onde o motivo não foi registrado em nenhum arquivo, a coluna diz **motivo não registrado**; preencha antes da defesa.

Quem decidiu:
- **Autor**: Rodrigo, em nome próprio.
- **Autor (proposta do levantamento)**: proposta feita por um subagente em 15/11/2026 e aceita pelo autor em bloco no mesmo dia.
- **Orientador**: ainda em aberto, ver o fim do arquivo.

## 1. Dados e divisão

| Data | Decisão | Motivo | Quem |
|---|---|---|---|
| 14/11/2026 | Divisão dev/teste refeita, estratificada, semente 2026 (800/200; 240 e 60 ruins) | A divisão antiga (semente 42) tinha o teste já aberto em um trabalho anterior, com a regressão logística | Autor |
| 14/11/2026 | O teste novo fica fechado até o passo 10; todos os modelos, inclusive o baseline, são avaliados nele uma única vez | Motivo não registrado | Autor |
| 15/11/2026 | O código só lê `dev.csv`. `teste.csv`, `sgc.csv` e `dados/brutos/` são proibidos para o código (D11) | `sgc.csv` e os dados brutos também contêm as 200 linhas do teste | Autor (proposta do levantamento) |
| 15/11/2026 | O teste final é rodado pelo autor, à mão, uma vez. A factory só escreve o caminho `--final`, testado com linhas do dev (D10) | A proteção por busca e caixa de areia pega o acidente, não um agente decidido a olhar. A garantia final é o commit de congelamento mais o teste rodado pelo autor (critérios, seção 5) | Autor (proposta do levantamento) |

## 2. Constantes congeladas

Regra G4 do critério de aceite: mudar uma delas é motivo para parar e perguntar, nunca para ajustar a um resultado.

| Constante | Valor | Motivo |
|---|---|---|
| Semente | 2026 | Divisão nova, ver acima. Para as demais fontes de aleatoriedade: motivo não registrado |
| Partições da validação cruzada | 5, estratificadas, só no dev | "Não gasta o teste" (plano, item 5). Por que 5 e não 10: motivo não registrado |
| Faixas das variáveis contínuas | 3, por tercis, cortes aprendidos só no treino de cada partição | "A rede discreta exige" e o corte só no treino evita vazamento (plano, item 5). Por que 3 e não 4 ou 5: motivo não registrado |
| Prior | BDeu, tamanho equivalente 5 | Evita probabilidade zero em combinações raras (plano, item 5). Por que 5: motivo não registrado |
| Regressão logística | `LogisticRegression(max_iter=1000)` | Herdada do baseline anterior (`build()` do `baseline_logreg.py`) |
| Erro de calibração | 10 faixas de mesma largura | Herdada do protocolo anterior (v0.2), como diz o `baseline_logreg.py` |

## 3. Modelo de risco

| Data | Decisão | Motivo | Quem |
|---|---|---|---|
| 14/11/2026 | Duas redes (Naive Bayes e TAN) mais a regressão logística como baseline; hill climbing é opcional | Naive Bayes é a referência simples, TAN permite dependência entre variáveis, a logística separa o efeito do modelo | Autor |
| 15/11/2026 | Naive Bayes montado como rede em estrela, não com `pgmpy.models.NaiveBayes` | A classe falha em `predict_probability` na `pgmpy` 1.1.2 (conferido por execução) | Autor |
| 15/11/2026 | `pgmpy` fixa em 1.1.2 | A API mudou entre 1.0 e 1.1.2 e a documentação do site está atrasada | Autor |
| 15/11/2026 | Calibração só é medida. Corrigir com regressão isotônica depende do autor, depois de ver `metricas_dev.csv`; se entrar, é issue nova (D4) | A escolha depende de um número, e número não é decisão do agente | Autor (proposta do levantamento) |
| 15/11/2026 | Regressão logística com variável escondida: mediana do treino para as 3 contínuas, moda para as 17 categóricas (D2) | `hoehe` tem 753 valores distintos em 800 linhas, então a moda não serve | Autor (proposta do levantamento) |
| 14/11/2026 | Evidência incompleta entra em versão pequena: uma variável escondida por vez | Se o prazo apertar, corta-se nesta ordem: hill climbing, depois evidência incompleta. Motivo de a versão ser pequena: não registrado | Autor |

## 4. Decisão e política

| Data | Decisão | Motivo | Quem |
|---|---|---|---|
| 14/11/2026 | Três ações: aprovar, rejeitar, análise manual. A terceira ação não sai | Motivo não registrado além de "a terceira ação não sai" (plano, item 8) | Autor |
| 15/11/2026 | Empate: análise manual > rejeitar > aprovar, tolerância 1e-9 (D5) | Com c = 80 e p = 0,20 as três ações empatam; por que essa ordem: motivo não registrado | Autor (proposta do levantamento) |
| 15/11/2026 | A política é calculada para os três modelos; o autor escolhe qual vai para a tabela 2×2 do texto, antes do commit de congelamento (D3) | O plano fala em "rede bayesiana", mas há duas | Autor (proposta do levantamento) |
| 15/11/2026 | Grade da sensibilidade: perda em {200, 400, 600, 800} × custo da análise em {0, 5, …, 100} (D7) | Motivo da grade não registrado. Fato do plano: com a matriz demonstrativa, acima de c = 80 a análise manual nunca é escolhida | Autor (proposta do levantamento) |
| 15/11/2026 | Demonstração treina nas 4 partições que não contêm o caso e usa `tan` por padrão (D1, D8) | Reproduz o mesmo número de `predicoes_dev.csv`, que é o da monografia. Por que `tan` e não `nb`: motivo não registrado | Autor (proposta do levantamento) |
| 15/11/2026 | O trabalho afirma derivar limiares dos custos e mostrar que isso exige probabilidade calibrada. Não afirma que utilidade esperada seja regra de outro tipo que o limiar | A utilidade esperada de cada ação é uma reta em `p`, então a política equivale a limiares | Autor |

## 5. Processo

| Data | Decisão | Motivo | Quem |
|---|---|---|---|
| 15/11/2026 | O código é escrito pela software factory, uma issue por PR. A sessão interativa só define critérios e escreve os `.md` | Motivo não registrado | Autor |
| 15/11/2026 | Critério de aceite restringe a forma, nunca o resultado | Um agente que veja "AUC acima de 0,75" é convidado a mexer no modelo até passar | Autor |
| 15/11/2026 | Merge automático quando o aprovador da factory aprova (D9). O autor lê a descrição de cada PR depois do merge e relê todo o código antes do commit de congelamento | O autor optou por não parar cada PR. Substitui a decisão anterior, que parava o merge para revisão humana | Autor |
| 15/11/2026 | Dois arquivos de resultado a mais: `resumo_politicas_dev.csv` e `sensibilidade.csv` (D6) | Dois números da monografia não teriam arquivo de origem | Autor (proposta do levantamento) |

## 6. Em aberto

| Questão | Depende de |
|---|---|
| Prazo de entrega e de defesa | Orientador |
| Aceita a matriz de utilidade demonstrativa (c = 40)? Os valores `+100`, `−400` e `100 − c` são hipóteses | Orientador |
| Modelo de documento da monografia (LaTeX, Word, normas ABNT da UFU) | Orientador |
| Avisar que a base passou a ser a South German Credit (versão corrigida) e que o protótipo virou demonstração em terminal | Autor, ao orientador |
| Calibrar ou não | Autor, depois de ver `metricas_dev.csv` |
| Qual modelo vai para a tabela 2×2 | Autor, antes do commit de congelamento |
| Interface de uma tela (plano, item 12) | Autor, só depois de o experimento estar pronto |

## Como acrescentar uma decisão

Uma linha na tabela da seção certa, com data, motivo e quem decidiu. Decisão sobre constante congelada ou sobre escolha que dependa de número é do autor: se a factory ou um agente propuser, registre como proposta e só depois como decisão.
