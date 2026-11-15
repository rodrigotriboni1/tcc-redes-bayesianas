# Glossário

Termos do trabalho e dicionário das variáveis da base. Escrito em português simples; o código usa os nomes em alemão e a monografia usa a tradução.

## 1. Variáveis da South German Credit

São 20 variáveis mais o alvo. `record_id` é só identificador e sai antes de qualquer chamada ao `pgmpy`.

**Atenção: a tradução abaixo foi escrita de memória.** Só os nomes marcados com ✔ aparecem no `PLANO.md`, nos critérios ou no código com o significado que o texto dá. Antes de citar na monografia, confira cada linha no dicionário `codetable.txt`, em `dados/brutos/`. O agente não pode abrir essa pasta (regra 1 do `AGENTS.md`), então a conferência é do autor. Os códigos numéricos de cada categoria não estão neste arquivo pelo mesmo motivo.

| Nome no código | Tradução provável | Tipo | Conferido |
|---|---|---|---|
| `kredit` | Risco do crédito: **0 = ruim, 1 = bom**. É o alvo | Binária | ✔ |
| `laufzeit` | Duração do crédito (meses) | Contínua, 3 faixas por tercis | ✔ |
| `hoehe` | Valor do crédito | Contínua, 3 faixas por tercis | ✔ |
| `alter` | Idade | Contínua, 3 faixas por tercis | ✔ |
| `laufkont` | Situação da conta corrente | Categórica | só o nome |
| `verw` | Finalidade do crédito | Categórica | só o nome |
| `bishkred` | Número de créditos já existentes no banco | Categórica | só o nome |
| `telef` | Tem telefone registrado | Categórica | só o nome |
| `moral` | Histórico de crédito | Categórica | não |
| `sparkont` | Poupança | Categórica | não |
| `beszeit` | Tempo no emprego atual | Categórica | não |
| `rate` | Taxa da parcela em relação à renda | Categórica | não |
| `famges` | Estado civil e sexo (nome exato a conferir) | Categórica | não |
| `buerge` | Outros devedores ou fiadores | Categórica | não |
| `wohnzeit` | Tempo na residência atual | Categórica | não |
| `verm` | Patrimônio mais valioso | Categórica | não |
| `weitkred` | Outros planos de parcelamento | Categórica | não |
| `wohn` | Tipo de moradia | Categórica | não |
| `beruf` | Tipo de ocupação | Categórica | não |
| `pers` | Pessoas dependentes | Categórica | não |
| `gastarb` | Trabalhador estrangeiro | Categórica | não |

Cuidados já registrados no plano:
- **Alvo invertido.** 0 é ruim. Toda coluna `p_*` e `p_ruim` é a probabilidade de **ruim**.
- **Categorias raras.** Por exemplo `bishkred` = 4 (6 casos) e `verw` = 8 (9 casos). É por isso que se usa prior BDeu e uma lista fixa de estados com tudo que aparece no dev.
- **Tipos.** Todos os valores categóricos e faixas são inteiros.

## 2. Termos

### Dados e avaliação
- **dev e teste.** Divisão estratificada da base: 800 linhas para desenvolver (240 ruins) e 200 para o teste final (60 ruins). Semente 2026. O teste só é aberto uma vez, pelo autor.
- **Estratificada.** A proporção de bons e ruins é mantida em cada parte.
- **Validação cruzada em 5 partições.** O dev é dividido em 5 partes. Cada parte vira "validação" uma vez, enquanto as outras 4 treinam. Todo caso recebe uma predição de um modelo que não o viu.
- **Vazamento.** Quando informação da linha que está sendo prevista chega ao treino (por exemplo, aprender os cortes das faixas com ela). Os cortes são aprendidos só no treino de cada partição por isso.
- **Tercis.** Cortes que dividem uma variável contínua em 3 grupos de mesmo tamanho. São as "3 faixas" do plano.
- **Congelamento.** O commit feito antes do teste final, depois do qual nada mais muda. Registra o estado exato do código que foi avaliado.

### Modelos
- **Rede bayesiana.** Grafo que liga variáveis por dependência, com uma tabela de probabilidades por nó. Aqui estima P(ruim | características do caso).
- **Naive Bayes.** Rede mais simples: `kredit` aponta para cada variável e as variáveis são tratadas como independentes entre si dado `kredit`. No `pgmpy` 1.1.2 é montada como rede em estrela.
- **TAN** (Naive Bayes aumentado por árvore). Naive Bayes mais uma árvore de dependências entre as variáveis. Permite que duas variáveis dependam uma da outra, além de `kredit`.
- **Hill climbing.** Busca a estrutura da rede sem restrição, melhorando um escore (BIC) aos poucos. Opcional neste trabalho.
- **Regressão logística.** Modelo linear usado como baseline. Recebe as 3 contínuas sem faixas.
- **Prior BDeu.** Contagem inicial "de mentira" somada às contagens dos dados, para que combinação rara nunca tenha probabilidade zero. O tamanho equivalente 5 diz quanto pesa essa contagem inicial.
- **Inferência exata (eliminação de variáveis).** Calcula a probabilidade pedida sem aproximação. É viável porque a rede é pequena.
- **Evidência incompleta.** Esconder uma variável na hora de prever. A rede infere sem ela; na regressão logística ela é preenchida com a mediana (contínuas) ou a moda (categóricas) do treino.

### Métricas
- **ROC-AUC.** Chance de o modelo dar risco maior a um caso ruim do que a um bom, escolhidos ao acaso. 0,5 é sorteio.
- **Brier.** Média do quadrado do erro entre a probabilidade dada e o que aconteceu (0 ou 1). Menor é melhor. Prever sempre a taxa base de ruins (0,30) dá 0,21.
- **Log loss.** Penaliza com força o modelo que erra com muita confiança.
- **Calibração.** Um modelo é calibrado se, entre os casos em que disse "30% de risco", cerca de 30% foram mesmo ruins.
- **Erro de calibração (ECE).** Média, ponderada pelo tamanho de cada faixa, da diferença entre o risco dado e a taxa observada. Aqui, 10 faixas de mesma largura.
- **Diagrama de calibração.** Gráfico do risco dado contra a taxa observada; a diagonal é o ideal.
- **Taxa base.** Previsão que ignora o caso e dá sempre a proporção de ruins. É a referência mínima.
- **Bootstrap.** Reamostrar as linhas com reposição muitas vezes para obter um intervalo de confiança. Só no teste final.

### Decisão
- **Utilidade.** Valor, positivo ou negativo, de tomar uma ação num caso que se revela bom ou ruim.
- **Utilidade esperada (UE).** Média das utilidades ponderada pelas probabilidades: `UE(a) = (1 − p)·U(a, bom) + p·U(a, ruim)`. Escolhe-se a ação de maior UE.
- **Matriz de utilidade.** A tabela de `U` por ação e resultado. Fica em `config/utilidade.json`. Os valores atuais são demonstrativos e dependem do orientador.
- **Limiar.** Valor de `p` a partir do qual a decisão muda. Como cada UE é uma reta em `p`, a política de utilidade esperada equivale a limiares; a diferença é que aqui eles saem dos custos.
- **Política.** A regra que leva de `p` a uma ação.
- **Next best action.** Escolher, para cada caso, a melhor próxima ação entre as disponíveis (aprovar, rejeitar, encaminhar para análise manual).
- **Análise manual.** Terceira ação: um analista revisa o caso, a um custo `c`. A hipótese do plano é que o analista acerta.

### Processo
- **Software factory.** Pipeline de agentes que transforma cada issue com o rótulo `factory` em um PR: intake, spec, build, gate, revisão, aprovação e merge.
- **Gate.** Script que roda `factory/checks.sh`; se falhar, nenhum revisor roda.
- **`AVISO:`.** Linha impressa que informa o autor e nunca falha o script. Não se "conserta".
- **`--verificar`.** Modo de autoteste de cada script. Confere contas com resposta conhecida e não grava nada.
