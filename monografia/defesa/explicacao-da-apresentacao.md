# Explicação da apresentação, em português simples

Este texto é para você entender a sua própria apresentação e ensaiá-la. Ele segue os 24 slides na ordem. Leia em voz alta. Frases curtas, de propósito.

---

## A. A apresentação em 1 minuto

### Em 5 frases

1. Hoje, no crédito, um modelo dá uma nota e a nota é comparada com um corte; os custos de errar ficam escondidos nesse corte.
2. Você separou o trabalho em duas camadas: uma estima a chance de o crédito ser ruim, a outra escolhe a ação pelos custos.
3. Com a matriz de custos usada, a escolha vira duas fronteiras fáceis de conferir: aprovar abaixo de 0,10, mandar para análise manual até 0,60 e rejeitar acima.
4. No teste, os três modelos não se separaram: as diferenças de ROC-AUC ficaram abaixo de 0,03, que é ruído, e o TAN não foi melhor que a taxa base no Brier.
5. A política de três ações teve utilidade média 22,5 maior que o corte 0,5, mas essa vantagem vem da própria matriz (ganha por construção), não da rede.

### As 5 ideias que você precisa decorar

1. **Separar risco e ação.** Primeiro a probabilidade, depois a decisão. É a tese.
2. **0,10 e 0,60 saem de uma conta.** 40/400 = 0,10 e 1 − 40/100 = 0,60. Qualquer pessoa refaz.
3. **Abaixo de 0,03 é ruído.** Com só 60 casos ruins no teste, diferença pequena de ROC-AUC não quer dizer nada. A regra foi escrita antes.
4. **O TAN não foi melhor que a taxa base no Brier.** 0,215 contra 0,210. Resultado ruim entra como saiu.
5. **Os +22,5 são por construção.** Só a política de três ações tem a análise manual, e o analista é suposto infalível. Não é prova de que a rede é boa.

---

## B. Dicionário de rua

Cada termo: o que é, em uma ou duas frases, e uma comparação do dia a dia.

**Risco / probabilidade de crédito ruim (p, ou P(ruim)).** É um número entre 0 e 1 que diz a chance de o cliente não pagar. Analogia: a previsão do tempo diz "30% de chance de chuva"; aqui é "30% de chance de calote".

**Rede bayesiana.** Um desenho de setas entre variáveis, mais tabelas de probabilidade, que permite calcular a chance de uma coisa sabendo outras. Analogia: um mapa de "o que influencia o quê", tipo "nuvem escura → chuva → chão molhado", com números em cada seta.

**Naive Bayes (NB).** A rede mais simples: a classe (bom ou ruim) aponta para todas as variáveis, e elas não conversam entre si. Analogia: um médico que olha cada sintoma separado e soma as pistas, sem pensar que dois sintomas andam juntos.

**TAN (Naive Bayes aumentado por árvore).** É o Naive Bayes com setas extras entre as variáveis, formando uma árvore. Analogia: o mesmo médico, mas agora sabe que febre e calafrio costumam vir juntos e não conta a pista duas vezes.

**Regressão logística.** Um modelo clássico, sem desenho de setas, que transforma uma soma ponderada das variáveis em probabilidade. Aqui é a referência. Analogia: uma balança com pesos; cada característica do cliente puxa o ponteiro para "bom" ou "ruim".

**Prior BDeu (tamanho equivalente 5).** Um "chute inicial" suave nas tabelas da rede, para que nenhuma probabilidade saia zero só porque um caso não apareceu no treino. O 5 é o peso desse chute, como se fossem 5 casos imaginários. Analogia: antes de provar um restaurante novo, você dá nota média; poucas visitas mexem pouco nessa nota.

**Validação cruzada em 5 partições.** Os 800 casos de desenvolvimento viram 5 blocos de 160. Treina em 4, testa no 5º, e roda até cada bloco ter sido teste uma vez. Analogia: estudar com 5 provas antigas, sempre deixando uma de fora para se testar.

**Conjunto de teste, aberto uma vez só.** São 200 casos (60 ruins) guardados desde o começo. Ficaram trancados até tudo estar congelado e foram abertos uma única vez, em 17/11/2026. Se você abre antes, acaba ajustando o modelo à prova. Analogia: a prova final; se você vê a prova antes, a nota não vale.

**ROC-AUC.** Mede se o modelo põe os ruins acima dos bons na fila de risco. 0,5 é sorteio; 1 é perfeito. Analogia: pegue um ruim e um bom ao acaso; a ROC-AUC é a chance de o modelo dar nota de risco maior ao ruim.

**PR-AUC.** Mede o quanto, entre os que o modelo aponta como ruins, eles são mesmo ruins, ao longo de vários cortes. Aqui a referência é a taxa base, 0,300. Você só descreve: não há regra de ruído para ela. Analogia: de todos os alarmes que tocaram, quantos eram incêndio de verdade.

**Brier.** É o erro médio ao quadrado entre a probabilidade dada e o que aconteceu (0 ou 1). Quanto menor, melhor. Analogia: a nota de um meteorologista; quem diz "quase certo que chove" e não chove perde muitos pontos.

**ECE / calibração.** Calibração é "o número bate com a realidade": dos clientes com 30% de risco, uns 30% devem ser ruins. O ECE mede o quanto isso falha, em 10 faixas. Menor é melhor. Analogia: uma balança que marca 1 kg a mais está descalibrada, mesmo que ordene certo quem é mais pesado.

**Utilidade esperada (UE).** É o ganho médio de uma ação, pesando cada resultado pela sua chance: UE = (1 − p) · ganho se bom + p · ganho se ruim. Escolhe-se a ação de maior UE. Analogia: decidir se leva guarda-chuva pesando o incômodo de carregar contra o risco de se molhar.

**Matriz de utilidade.** A tabela com quanto se ganha ou perde em cada combinação de ação e cliente. Aqui: aprovar bom = +100 (G); aprovar ruim = −400 (L); rejeitar = 0; análise manual custa c = 40 e o analista acerta sempre. É demonstrativa: aprovada pelo orientador, não medida em banco real. Analogia: a tabela de preços de um jogo, que você combinou antes de jogar.

**Limiares 0,10 e 0,60 e de onde vêm.** Com a matriz, cada ação vira uma reta em p:
- aprovar: 100 · (1 − p) − 400 · p = 100 − 500p
- rejeitar: 0
- análise manual: o analista aprova o bom (100 − 40 = 60) e recusa o ruim (0 − 40 = −40), então 60 · (1 − p) − 40 · p = 60 − 100p

Onde aprovar empata com análise manual: 100 − 500p = 60 − 100p → 400p = 40 → p = 40/400 = 0,10, ou seja, c/L.
Onde análise manual empata com rejeitar: 60 − 100p = 0 → p = 60/100 = 0,60, ou seja, 1 − 40/100 = 1 − c/G.
Regra final: p abaixo de 0,10 aprova; entre 0,10 e 0,60 manda para análise manual; acima de 0,60 rejeita. Analogia: as marcas de "frio, morno, quente" num termômetro, calculadas a partir do preço de errar.

**Análise manual.** A terceira ação: um analista humano olha o caso. Custa 40 e, na simulação, nunca erra. Analogia: chamar um especialista quando você está em dúvida; custa a consulta, mas acerta.

**Taxa base.** O "modelo burro" que dá a todo cliente a mesma probabilidade: a proporção de ruins, 30%. Tem ROC-AUC 0,5 e Brier 0,210. Serve de régua mínima. Analogia: o meteorologista que diz "30% de chuva" todo dia, porque chove em 30% dos dias.

**Bootstrap e intervalo de 95%.** Sorteia-se, com reposição, muitas versões do teste e recalcula-se a métrica em cada uma. O intervalo de 95% é a faixa onde cai o meio das contas. Mostra o quanto o número balança. Analogia: repetir uma pesquisa de opinião várias vezes com sorteios diferentes e ver a margem de erro.

**"Ruído" e a regra de 0,03.** Antes de ver qualquer resultado, ficou escrito: diferença de ROC-AUC menor que 0,03 é ruído, não diferença real. Com só 60 ruins no teste, o número balança mais que isso. Analogia: dois corredores que chegam com 1 centésimo de diferença num cronômetro de mão; não dá para dizer quem ganhou.

**"Ganha por construção".** A política de três ações tem uma ação a mais (análise manual), e essa ação, com analista infalível, nunca dá prejuízo grande. Então ela tende a ganhar do corte 0,5 com qualquer modelo. A vitória vem das regras do jogo, não da qualidade da rede. Analogia: um time que joga com um jogador a mais vai ganhar com frequência; isso não prova que o técnico é bom.

**Estudo de seleção e seu viés.** Um estudo extra, secundário: testou 8 versões (NB e TAN com BDeu 1, 5, 10 e 50) e deixou uma regra escolher a de menor log loss. Escolheu NB com BDeu 50 em todas as partições. O viés: a lista de 8 foi montada depois de você ver o desenvolvimento, e isso está declarado. Analogia: escolher o cardápio depois de provar os pratos; a escolha final pode ser justa, mas a lista já estava influenciada.

**Log loss (aparece nos apêndices).** Outra medida de erro da probabilidade, que pune muito quem tem certeza e erra. Menor é melhor.

---

## C. Slide a slide, linha a linha

Tempo total do corpo: cerca de 19 minutos. Os slides 15 a 24 são o apêndice: só aparecem se a banca perguntar.

### Slide 1 — Título (0:30)

**O que está escrito.**
- "Redes bayesianas e utilidade esperada aplicadas à seleção de next best action em sistemas automatizados de decisão"
- "Separar o risco da ação torna os limiares explícitos; o efeito medido vem com ressalvas"
- Seu nome, o orientador Fabio Vincenzi, UFU, FEELT, Engenharia de Controle e Automação.
- Campos ainda a preencher: titulação do orientador, data e local.

**O que quer dizer.**
- "Next best action" = "a melhor próxima ação" para cada cliente.
- O subtítulo já é a conclusão: separar dá fronteiras claras; o número medido tem limites.

**O que você fala.** "Bom dia. Sou Rodrigo Mialichi Triboni, orientado pelo professor Fabio Vincenzi. Este trabalho separa duas tarefas que a decisão de crédito costuma misturar: estimar o risco e escolher a ação. Vou mostrar que essa separação deixa os limiares explícitos e qual efeito ela teve num teste, com as ressalvas desse número."

**Pergunta provável.** "Por que 'next best action' se só há crédito?" Resposta: "O crédito é o estudo de caso. A ideia vale para qualquer escolha de ação a partir de um risco."

### Slide 2 — Problema (1:30)

**O que está escrito.**
- "Hoje: caso → escore → corte → aprovar/rejeitar"
- "Proposta: camada de risco: P(ruim) → camada de decisão: custos → ação"
- "Escore + corte: prática da indústria, interpretável."
- "Custos não aparecem na regra."
- "Proposta: risco por rede bayesiana; ação por utilidade esperada."

**O que quer dizer.**
- Hoje uma nota e um corte fazem tudo de uma vez.
- O corte esconde quanto custa errar.
- Você propõe duas caixas: uma só calcula a chance, a outra só decide.

**O que você fala.** "Na concessão de crédito, um modelo dá um escore e o escore é comparado com um corte. Nessa regra, duas coisas viram uma: a chance de o crédito ser ruim e a escolha do que fazer. O corte carrega os custos de errar, mas não os mostra. Uso uma rede bayesiana para a chance e a utilidade esperada para a ação."

**Pergunta provável.** "Isso é novo?" Resposta: "Não é uma regra nova. A contribuição é deixar os custos e as fronteiras explícitos e medir o efeito com cuidado."

### Slide 3 — Pergunta de pesquisa (1:30)

**O que está escrito.**
- A pergunta inteira: a política que separa risco e ação tem "(1) limiares explícitos, que qualquer pessoa reproduz a partir da matriz de utilidade e de p, e (2) que efeito medido sobre as ações e a utilidade média, em comparação com um limiar fixo de 0,5?"
- "(1) vale por construção, para qualquer escore."
- "(2) é o que o experimento mede."
- "Leitura fixada antes dos resultados."

**O que quer dizer.**
- Parte 1 é matemática: vale sempre, nem precisa de dados.
- Parte 2 é o experimento: comparar com o corte 0,5.
- Você escreveu como ia ler cada resultado antes de ver qualquer número.

**O que você fala.** "Esta é a pergunta, como está no capítulo 1. A parte 1 é uma propriedade da política: vale para qualquer escore, inclusive a logística. A parte 2 é o que medi: ações e utilidade média, contra um corte fixo de 0,5. A pergunta e a forma de ler cada resultado foram escritas antes de existir resultado."

**Pergunta provável.** "Se a parte 1 vale por construção, qual o mérito?" Resposta: "Mostrar a conta de forma que qualquer um refaça. O mérito é a transparência, não a descoberta."

### Slide 4 — Dados e protocolo (1:30)

**O que está escrito.**
- Barra P1 a P5 e Teste.
- "Dev: 800 (240 ruins)"; "Teste: 200 (60 ruins), aberto 1× em 17/11/2026 (49d77ff)"
- "Divisão estratificada, semente 2026."
- "Validação cruzada estratificada, 5 partições."
- "3 contínuas em 3 faixas por tercis, cortes só no treino."
- "Classe positiva: ruim (30%)."

**O que quer dizer.**
- 1.000 clientes alemães; 800 para treinar e testar em rodízio, 200 guardados.
- "Estratificada" = cada parte tem os mesmos 30% de ruins.
- "Semente 2026" = o sorteio é sempre o mesmo, dá para repetir.
- As 3 variáveis numéricas (como valor do crédito) viraram "baixo, médio, alto", com as fronteiras aprendidas só no treino.
- 49d77ff é o código da versão congelada do programa.

**O que você fala.** "A base é a South German Credit, a versão corrigida por Grömping. São 1.000 casos: 800 para desenvolvimento, com 240 ruins, e 200 para teste, com 60 ruins. No desenvolvimento usei validação cruzada em 5 partições, semente 2026. O teste foi aberto uma única vez, em 17/11/2026, depois de tudo congelado."

**Pergunta provável.** "Por que discretizar?" Resposta: "As redes aqui trabalham com categorias. As faixas por tercis foram fixadas antes, com cortes só do treino."

### Slide 5 — Modelos (1:30)

**O que está escrito.**
- Três desenhos: "NB: kredit pai de todas"; "TAN: + árvore entre preditoras; azul: verw"; "Regressão logística: sem grafo, contínuas originais".
- "Parâmetros: prior BDeu, tamanho equivalente 5."
- "Inferência exata (pgmpy 1.1.2)."
- "Logística: max_iter=1000."
- "Calibração só medida, não corrigida."

**O que quer dizer.**
- kredit é a coluna bom/ruim. No NB ela aponta para tudo.
- verw é o "propósito do crédito"; no TAN é a variável com mais setas saindo.
- Inferência exata = a conta é feita certinha, sem aproximação. pgmpy é a biblioteca usada.
- max_iter=1000 = o limite de passos de ajuste da logística.
- Você mediu a calibração mas não consertou.

**O que você fala.** "Comparo três modelos. O Naive Bayes trata as variáveis como independentes dada a classe; o TAN acrescenta uma árvore de dependências entre elas. As redes usam prior BDeu com tamanho equivalente 5, para não sair probabilidade zero. A logística é a referência e recebe as variáveis numéricas sem faixas, então a diferença mistura modelo e representação."

**Pergunta provável.** "Por que a logística com dados contínuos?" Resposta: "É como ela é usada na prática. Por isso não afirmo que a diferença é só do modelo."

### Slide 6 — Camada de utilidade esperada (1:45)

**O que está escrito.**
- "Limiares: 0,10 (c/L = 40/400) e 0,60 (1 − c/G = 1 − 40/100)"
- "UE(a) = (1−p)·U(a,bom) + p·U(a,ruim)."
- "Matriz: G = 100, L = 400, c = 40."
- "Demonstrativa, aprovada pelo orientador, não calibrada com dados reais."

**O que quer dizer.**
- Cada ação tem um ganho médio que depende de p.
- Ganho de aprovar um bom = 100; perda de aprovar um ruim = 400; custo da análise = 40.
- As retas se cruzam em 0,10 e 0,60 (a conta está no dicionário).
- Os valores são de exemplo, não de banco real.

**O que você fala.** "A camada de decisão escolhe a ação de maior utilidade esperada. A matriz é demonstrativa: aprovar um bom vale 100, aprovar um ruim custa 400, rejeitar vale zero e a análise manual custa 40. Cada utilidade esperada é uma reta em p, então a escolha vira dois limiares: 40 sobre 400 dá 0,10 e 1 menos 40 sobre 100 dá 0,60. Isso responde à parte 1, para qualquer escore."

**Pergunta provável.** "De onde saíram 100, 400 e 40?" Resposta: "São demonstrativos, aprovados pelo orientador. O slide seguinte mostra o que muda com outros valores."

### Slide 7 — Sensibilidade (1:15)

**O que está escrito.**
- "Grade: perda 200–800; custo 0–100."
- "c = 0: análise manual cobre 0 a 1."
- "Limiares coincidem → volta a duas ações."
- "Nenhum valor escolhido."

**O que quer dizer.**
- Você refez a conta para várias perdas e custos.
- Se a análise for de graça, vale mandar todo mundo para ela.
- Se for cara, as duas fronteiras se encontram e a análise manual some.
- Você não escolheu qual valor é o "certo".

**O que você fala.** "Variei a perda em 200, 400, 600 e 800 e o custo da análise de 0 a 100, de 5 em 5. Com custo zero, a análise manual cobre todo o intervalo. Com perda 200, a faixa some a partir de c = 70, com os dois limiares em 0,333; com perda 400, a partir de c = 80, ambos em 0,200. Isso não depende de modelo, e não escolho o custo."

**Pergunta provável.** "Qual custo é o real?" Resposta: "Essa escolha é do negócio. O trabalho mostra como a fronteira se move."

### Slide 8 — Desenvolvimento (1:30)

**O que está escrito.**
- "NB − logística: 0,001 → ruído"
- "ROC-AUC: NB 0,789; logística 0,788; TAN 0,742 (desvio 0,049)."
- "ECE do TAN 0,152 (NB 0,093)."
- "Média de 5 partições, sem intervalo."

**O que quer dizer.**
- Nos 800 casos, NB e logística quase empataram.
- O TAN ficou atrás e variou mais entre as partições.
- O TAN também ficou mais descalibrado.
- Aqui não há intervalo; é só a média das 5 rodadas.

**O que você fala.** "No desenvolvimento, a ROC-AUC média foi 0,789 no Naive Bayes, 0,788 na logística e 0,742 no TAN. NB e logística diferem em 0,001, abaixo de 0,03: ruído. O TAN ficou abaixo do NB nas cinco métricas; o erro de calibração do TAN foi 0,152, contra 0,093 do NB. Não ajustei nada por isso: o resultado vai como saiu."

**Pergunta provável.** "Por que o TAN, mais rico, foi pior?" Resposta: "Não sei a causa e não afirmo. Há uma hipótese registrada no apêndice, não testada."

### Slide 9 — Teste: discriminação (1:30)

**O que está escrito.**
- "n = 200; 60 ruins."
- "NB 0,728; TAN 0,706; logística 0,729."
- "IC 95% por bootstrap, largos e sobrepostos."
- "PR-AUC: 0,490; 0,480; 0,500 (taxa base 0,300), só descrita."

**O que quer dizer.**
- No teste, os três ficaram muito perto.
- As faixas de incerteza se encostam: não dá para separar.
- PR-AUC acima da taxa base, mas sem regra para julgar; só conta o número.

**O que você fala.** "No teste, a ROC-AUC foi 0,728 no NB, 0,706 no TAN e 0,729 na logística. As diferenças vão de 0,001 a 0,022, todas abaixo de 0,03: pela regra, ruído. Os intervalos de 95% são largos; o do TAN vai de 0,623 a 0,789. A PR-AUC foi 0,490, 0,480 e 0,500, contra 0,300 da taxa base, e só descrevo. Todos caíram em relação ao desenvolvimento; não testei a causa."

**Pergunta provável.** "Por que caiu do desenvolvimento para o teste?" Resposta: "Não testei a causa, então não afirmo. Registro a queda como saiu."

### Slide 10 — Teste: Brier e calibração (1:30)

**O que está escrito.**
- "Taxa base: 0,210"
- "Brier: NB 0,199; logística 0,191; TAN 0,215."
- "ECE: NB 0,115; TAN 0,157; logística 0,078."
- "Calibração só medida, sem correção."

**O que quer dizer.**
- O TAN errou mais na probabilidade do que dizer "30%" para todo mundo.
- NB e logística ficaram melhores que essa régua.
- A logística foi a mais calibrada; o TAN, a menos.

**O que você fala.** "O Brier mede o erro da probabilidade. No teste, o do TAN foi 0,215, acima dos 0,210 de quem prevê a taxa base para todo caso. Pela regra, digo: o TAN não foi melhor que prever a taxa base. NB, com 0,199, e logística, com 0,191, ficaram abaixo. O erro de calibração foi 0,115, 0,157 e 0,078, e não corrigi."

**Pergunta provável.** "Então por que usar o TAN na decisão?" Resposta: "Porque foi fixado antes de ver resultado. Trocar agora seria escolher pelo resultado."

### Slide 11 — Três ações contra corte 0,5 (2:00)

**O que está escrito.**
- Título: utilidade média 22,5 maior que o corte 0,5 (IC 95%: 9,2 a 37,2), "vantagem que a matriz garante por construção".
- "IC exclui zero → diferença a favor das três ações; sem causa."
- "Os 60 que mudam = os 60 em análise manual."
- "Ressalvas: matriz demonstrativa; analista infalível; simulação, não política real."

**O que quer dizer.**
- Em média, cada cliente rendeu 22,5 a mais com três ações.
- A faixa de incerteza não chega a zero, então a diferença é a favor.
- Os únicos casos que mudaram de decisão foram os 60 mandados ao analista.
- E isso é esperado pela própria regra, não mérito da rede.

**O que você fala.** "Esta é a comparação principal, fixada antes: TAN com três ações contra o corte 0,5. A diferença de utilidade média foi 22,5, com intervalo de 9,2 a 37,2. A política aprovou 92, rejeitou 48 e mandou 60 para análise manual; o corte aprovou 145 e rejeitou 55. Os 60 que mudaram são os da análise manual. Com analista infalível, a política de três ações ganha por construção: é efeito da matriz, não evidência sobre a rede."

**Pergunta provável.** "Então o resultado não prova nada?" Resposta: "Prova que, com esta matriz, a ação extra rende mais. Não prova que a rede é boa."

### Slide 12 — Estudo de seleção secundário (1:15)

**O que está escrito.**
- "8 comparações; regra: menor log loss interno."
- "Escolhida: nb_ess50 em todas as partições."
- "Viés declarado: grade motivada pelas métricas do desenvolvimento."
- "Análise primária não muda."

**O que quer dizer.**
- 8 versões testadas, e uma regra automática escolheu.
- nb_ess50 = Naive Bayes com BDeu 50.
- A lista foi feita depois de olhar o desenvolvimento; você admite isso.
- A análise principal continua com BDeu 5.

**O que você fala.** "Depois de ver o TAN abaixo do NB, fiz um estudo secundário com 8 configurações: NB e TAN com tamanho equivalente 1, 5, 10 e 50. A regra escolheu nb_ess50 nas cinco partições. A ROC-AUC dele, 0,788, difere em 0,001 da referência, 0,789: ruído. A grade foi desenhada olhando o desenvolvimento, e esse viés está declarado."

**Pergunta provável.** "Por que não usar o escolhido como principal?" Resposta: "Seria decidir pelo resultado. O estudo diz o que a regra escolheu, não o que adotar."

### Slide 13 — Limitações (1:30)

**O que está escrito.**
- "Matriz demonstrativa; analista infalível."
- "Sem desfecho das ações não tomadas → simulação."
- "Teste: 200 casos, 60 ruins → IC largos."
- "Modelo e representação variam juntos."
- "IC não cobre variação do treino."
- "Calibração só medida."

**O que quer dizer.**
- Os custos são de exemplo e o analista nunca erra: é otimista.
- Não se sabe o que teria acontecido com quem foi rejeitado; por isso é simulação.
- Poucos ruins = muita incerteza.
- A logística usa dados diferentes das redes.
- O bootstrap sorteia só o teste; se o treino mudasse, mudaria mais.

**O que você fala.** "Seis limites acompanham tudo. A matriz é demonstrativa e supõe um analista que sempre acerta. A base não diz o que aconteceria com as ações não tomadas, então é simulação. O teste tem 200 casos e 60 ruins, e os intervalos são largos. Modelo e representação variam juntos, o intervalo não cobre o treino e a calibração foi só medida. Por isso não generalizo nem recomendo um modelo."

**Pergunta provável.** "Qual a limitação mais grave?" Resposta: "O analista infalível, porque é ela que faz as três ações ganharem por construção."

### Slide 14 — Conclusões (1:00, fica na tela na arguição)

**O que está escrito.**
- "1. Limiares 0,10 e 0,60 saem da matriz; valem para qualquer escore."
- "2. TAN: +22,5 de utilidade média [9,2; 37,2], por construção da matriz."
- "3. ROC-AUC: diferenças são ruído; Brier do TAN não melhor que taxa base."
- Contato e link ainda a preencher.

**O que quer dizer.**
- Item 1 responde à parte 1 da pergunta.
- Item 2 responde à parte 2, com a ressalva.
- Item 3 é o resultado do risco, como saiu.

**O que você fala.** "Concluindo. Parte 1: separar risco e ação dá limiares explícitos, 0,10 e 0,60, que qualquer pessoa reproduz. Parte 2: com o TAN, as três ações tiveram utilidade média 22,5 maior que o corte 0,5, de 9,2 a 37,2, por construção da matriz. No risco, as diferenças de ROC-AUC foram ruído e o TAN não foi melhor que a taxa base no Brier. Fico à disposição."

**Pergunta provável.** "Qual modelo você recomenda?" Resposta: "Nenhum. Nenhuma regra fixada antes separou os modelos no teste."

### Slide 15 — Referências (apêndice)

**O que está escrito.** As 13 referências: Ankan e Textor (2024), Brier (1950), Efron e Tibshirani (1993), Elkan (2001), Friedman, Geiger e Goldszmidt (1997), Grömping (2019), Heckerman, Geiger e Chickering (1995), Naeini, Cooper e Hauskrecht (2015), Pearl (1988), Pedregosa et al. (2011), Siddiqi (2012), Thomas (2000), Zadrozny e Elkan (2001). Nota: Elkan (2001) e Grömping (2019) "a conferir".

**O que quer dizer.** Quem disse cada coisa. Elkan dá a conta dos limiares; Brier, a medida de erro; Efron, o bootstrap; Friedman, o TAN; Grömping, a base corrigida.

**O que você fala.** Só mostre se pedirem. "As referências estão aqui; Elkan é a base da conta dos limiares." (0:15)

**Pergunta provável.** "Onde está a fórmula dos limiares?" Resposta: "Em Elkan (2001), aprendizado sensível a custo."

### Slide 16 — A1: Por que o TAN saiu pior que o NB?

**O que está escrito.** "O TAN ficou abaixo do NB, e a hipótese sobre verw é registrada, mas não foi testada." Texto: "Não sei a causa e não afirmo." verw tem 7 a 9 setas de saída em todas as partições; log loss 0,704 e ECE 0,152 do TAN; no estudo de seleção o log loss do TAN cai de 0,825 (ess 1) para 0,583 (ess 50).

**O que quer dizer.** verw é ligada a muitas outras variáveis. Com 800 casos, as tabelas ficam com poucos exemplos em cada célula, e o modelo pode ficar confiante demais. É uma suspeita, não uma prova.

**O que você fala.** "Não sei a causa e não afirmo. A variável verw tem de 7 a 9 setas de saída em todas as partições. Tabelas com poucos casos seriam coerentes com o log loss de 0,704 e o ECE de 0,152 do TAN, mas nada testou isso." (0:45)

**Pergunta provável.** "Por que não testou?" Resposta: "Testar depois de ver o resultado seria ajustar ao resultado. Fica como trabalho futuro."

### Slide 17 — A2: Por que não calibrar?

**O que está escrito.** "Calibrar exigiria escolher o método depois de ver as métricas." A exigência de calibração vem da literatura (Zadrozny e Elkan, 2001). ECE no teste: 0,115 (NB), 0,157 (TAN), 0,078 (logística). "Calibrar é direção futura."

**O que quer dizer.** Existem vários jeitos de calibrar. Escolher um olhando os números seria trapacear o próprio plano.

**O que você fala.** "Corrigir pediria escolher entre métodos olhando o desenvolvimento. Por isso só medi: 0,115, 0,157 e 0,078 de ECE no teste. Calibrar é direção futura." (0:30)

**Pergunta provável.** "Mas a decisão por custos não precisa de probabilidade calibrada?" Resposta: "Precisa, e por isso medi e declarei. É uma limitação."

### Slide 18 — A3: Por que o corte 0,5?

**O que está escrito.** "O corte 0,5 foi fixado na pergunta antes dos resultados; não é o limiar de duas ações da matriz, que seria 0,2." Conta: G/(G+L) = 100/500 = 0,2. "A comparação não testa 'utilidade esperada contra qualquer limiar'."

**O que quer dizer.** 0,5 é a regra "sem custos", a mais comum. Se fosse só aprovar ou rejeitar com esta matriz, o ponto certo seria 0,2 (onde 100 − 500p = 0). Esse corte não foi comparado.

**O que você fala.** "O 0,5 representa a regra fixa sem custos e está no texto da pergunta. Com esta matriz, o limiar de duas ações seria 100 sobre 500, 0,2. A comparação não o inclui, então não testa utilidade esperada contra qualquer limiar." (0:30)

**Pergunta provável.** "Não é uma comparação fácil demais?" Resposta: "É uma comparação limitada, e eu digo isso. Ela responde à pergunta como foi fixada."

### Slide 19 — A4: O que muda se a matriz mudar?

**O que está escrito.** A fórmula já dá a resposta: análise manual entre c/L e 1 − c/G. Perda 400 e c = 80 zeram a faixa (0,200 e 0,200); perda 800 e c = 50 dão 0,063 e 0,5. A diferença de utilidade só foi medida com a matriz aprovada.

**O que quer dizer.** Mudou o custo, muda a fronteira, sem rodar nada. Mas o +22,5 vale só para a matriz usada.

**O que você fala.** "A fórmula responde: análise manual entre c/L e 1 − c/G. Com perda 400 e custo 80, a faixa some; com perda 800 e custo 50, vai de 0,063 a 0,5. A diferença de utilidade teria de ser recalculada." (0:30)

**Pergunta provável.** "O +22,5 se mantém?" Resposta: "Não sei; só medi com a matriz aprovada."

### Slide 20 — A5: Por que 5 partições?

**O que está escrito.** "5 partições é convenção fixada antes dos resultados, não escolhida por desempenho." Constante congelada, como as 3 faixas e o BDeu 5. Cada partição tem 160 casos e 48 ruins.

**O que quer dizer.** 5 é um número usual. 800 / 5 = 160; 30% de 160 = 48.

**O que você fala.** "É convenção fixada antes, como as 3 faixas e o BDeu 5. Cada partição tem 160 casos de validação e 48 ruins. Não testei outros valores para não escolher pelo resultado." (0:20)

**Pergunta provável.** "E com 10?" Resposta: "Não testei, de propósito."

### Slide 21 — A6: Houve vazamento?

**O que está escrito.** "O teste ficou fechado até o congelamento; o único vazamento é brando e está declarado." Cortes das faixas só no treino; teste aberto uma vez em 17/11/2026 (49d77ff). A lista de categorias possíveis usa o desenvolvimento inteiro, sem o rótulo. A divisão com semente 42 foi descartada porque seu teste já tinha sido usado.

**O que quer dizer.** "Vazamento" = informação da prova passando para o estudo. O único caso: o modelo sabe que uma categoria rara existe, mas não sabe se ela é boa ou ruim. Você trocou a divisão antiga para não reaproveitar uma prova já vista.

**O que você fala.** "O teste ficou fechado até o congelamento e foi aberto uma vez, em 17/11/2026. O único vazamento é brando: a lista de categorias usa todo o desenvolvimento para uma categoria rara não quebrar a conta, sem usar o rótulo. A divisão com semente 42 foi descartada porque o teste dela já tinha sido usado." (0:40)

**Pergunta provável.** "Esse vazamento muda o resultado?" Resposta: "Não medi, mas ele não usa o bom/ruim, então é brando e está declarado."

### Slide 22 — A7: O que significa "ganha por construção"?

**O que está escrito.** Na análise manual o analista acerta sempre: ganha 60 num bom e perde 40 num ruim. Entre 0,10 e 0,60 essa reta fica acima de aprovar e rejeitar. As quatro diferenças no teste foram positivas, de 22,5 a 38,3. "A diferença não é evidência sobre a rede nem sobre o critério da utilidade esperada."

**O que quer dizer.** Com qualquer modelo, a ação extra rende mais. Todos os quatro modelos testados ganharam do corte.

**O que você fala.** "Na análise manual o analista acerta sempre: ganha 60 num bom e perde 40 num ruim. Entre 0,10 e 0,60 essa opção é a melhor, e o corte 0,5 não a tem. Por isso as quatro diferenças foram positivas, de 22,5 a 38,3. Não é evidência sobre a rede." (0:40)

**Pergunta provável.** "E se o analista errasse?" Resposta: "A vantagem diminuiria. Não simulei isso; é limitação declarada."

### Slide 23 — A8: 60 casos ruins bastam?

**O que está escrito.** "Com 60 ruins, diferenças pequenas são indistinguíveis de ruído, e por isso a regra de 0,03 foi fixada antes." ROC-AUC do TAN de 0,623 a 0,789; diferença de utilidade de 9,2 a 37,2. O intervalo reamostra só o teste.

**O que quer dizer.** Já se sabia, antes, que o teste era pequeno. A regra de 0,03 existe por isso.

**O que você fala.** "O plano já previa que, com 60 ruins, diferença de 0,02 a 0,03 é ruído. Os intervalos confirmam: o do TAN vai de 0,623 a 0,789. E o intervalo não cobre o treino, então a incerteza real é maior." (0:30)

**Pergunta provável.** "Por que não usou um teste maior?" Resposta: "A base tem 1.000 casos. Foi o que havia."

### Slide 24 — A9: Por que não há "melhor modelo"?

**O que está escrito.** "Nenhuma regra pré-registrada separou os modelos no teste, e escolher um seria decidir pelo resultado." Diferenças de ROC-AUC até 0,022; PR-AUC só descrita; no Brier, só o TAN não foi melhor que a taxa base; o TAN é o principal porque foi fixado antes; o estudo de seleção diz o que a regra escolheu, não o que adotar.

**O que quer dizer.** Sem regra que separe, qualquer escolha seria gosto pessoal olhando o placar.

**O que você fala.** "As diferenças de ROC-AUC foram até 0,022, ruído pela regra. A PR-AUC só foi descrita. No Brier, só o TAN não foi melhor que a taxa base. O TAN é o principal porque foi fixado antes, não por desempenho." (0:30)

**Pergunta provável.** "Mas a logística teve o melhor Brier?" Resposta: "Teve o menor número, 0,191. Não há regra fixada para dizer que isso a torna melhor."

---

## D. Se travar

### Frases de segurança (honestas)

- "O teste tem só 60 casos ruins, então diferenças pequenas são ruído."
- "Isso está no apêndice; posso mostrar."
- "Não afirmo que um modelo é melhor."
- "Não testei a causa, então não afirmo."
- "Essa regra foi fixada antes de ver os resultados."
- "A matriz é demonstrativa; com outra matriz, a conta teria de ser refeita."
- "O resultado entra como saiu."
- "É uma boa sugestão; fica como trabalho futuro."
- "Não sei. Posso dizer o que medi."

### O que NUNCA dizer

- "O melhor modelo é ..." (nenhuma regra separou os modelos).
- "O TAN foi pior porque ..." como certeza (a causa não foi testada).
- "A queda do desenvolvimento para o teste aconteceu porque ..." (não testado).
- "Isso funciona em operação real" ou "num banco funcionaria" (é simulação).
- "A política de três ações vence de verdade" ou "a rede bayesiana melhora a decisão" (ela ganha por construção: só ela tem a análise manual e o analista é suposto infalível).
- "O TAN é bom no Brier" (não foi melhor que a taxa base).
- "A PR-AUC mostra que ..." (só descrita).
- "Escolhi esses custos porque deram melhor resultado" (não escolheu; são demonstrativos).

---

## E. Plano de ensaio em 5 dias

A entrega é em 30/11. A defesa só pode ser marcada 15 dias depois, a partir de 15/12/2026. Não há data fixa ainda; faça os 5 dias nos dias antes da data que for marcada.

**Dia 1 — Entender.** Leia o dicionário (parte B) em voz alta. Refaça no papel a conta de 0,10 e 0,60 sem olhar. Explique "ganha por construção" para alguém de fora.

**Dia 2 — Slides 1 a 7.** Fale cada slide com o cronômetro. Meta: cerca de 9 minutos. Decore os números: 1.000, 800, 240, 200, 60, 2026, 100, 400, 40, 0,10, 0,60.

**Dia 3 — Slides 8 a 14.** Mesma coisa. Meta: cerca de 10 minutos. Decore: 0,789; 0,788; 0,742; 0,728; 0,706; 0,729; 0,215; 0,210; 22,5; 9,2; 37,2.

**Dia 4 — Ensaio completo e apêndice.** Corpo inteiro, sem parar, em até 20 minutos. Se passar, corte o slide 12 e depois o 7 (vão para resposta). Depois, peça a alguém que leia as perguntas prováveis e responda cada uma em até 30 segundos.

**Dia 5 — Simulação de banca.** Ensaio completo em pé, com alguém fazendo perguntas difíceis. Treine as frases de segurança. Releia "O que NUNCA dizer". Durma cedo.

---

## Números conferidos: slide → valor → arquivo

Conferidos com pandas nesta versão. Só para o .md.

| Slide | Valor | Arquivo (coluna) |
|---|---|---|
| 4 | 200 casos, 60 ruins no teste | resultados/predicoes_teste.csv (kredit == 0) |
| 8 | ROC-AUC NB 0,789; logística 0,788; TAN 0,742; desvio TAN 0,049 | resultados/metricas_dev.csv (roc_auc_media, roc_auc_desvio) |
| 8 | ECE TAN 0,152; NB 0,093 | resultados/metricas_dev.csv (ece_media) |
| 9 | ROC-AUC NB 0,728; TAN 0,706; logística 0,729 | resultados/metricas_teste.csv (roc_auc) |
| 9, 23 | IC TAN 0,623 a 0,789 | resultados/metricas_teste.csv (roc_auc_ic_inf, roc_auc_ic_sup) |
| 9 | PR-AUC 0,490; 0,480; 0,500; taxa base 0,300 | resultados/metricas_teste.csv (pr_auc) |
| 10 | Brier NB 0,199; logística 0,191; TAN 0,215; taxa base 0,210 | resultados/metricas_teste.csv (brier) |
| 10, 17 | ECE NB 0,115; TAN 0,157; logística 0,078 | resultados/metricas_teste.csv (ece) |
| 11, 14, 23 | +22,5 [9,2; 37,2] | resultados/diferenca_politicas_teste.csv (linha tan) |
| 11 | 92 / 48 / 60; corte 145 / 55; 60 mudam | resultados/resumo_politicas_teste.csv (linhas tan) |
| 22 | diferenças de 22,5 a 38,3 (quatro positivas) | resultados/diferenca_politicas_teste.csv |
| 12 | nb_ess50 escolhida em 5/5 e no dev | resultados/selecao_escolha.csv (escolhida) |
| 12 | aninhado 0,788 vs nb_ess5 0,789 | resultados/selecao_dev.csv (roc_auc_media) |
| 16 | log loss TAN 0,704 (dev); 0,825 (ess 1) a 0,583 (ess 50) | resultados/metricas_dev.csv; resultados/selecao_dev.csv (log_loss_media) |
| 16 | verw com 7 a 9 arestas de saída por partição | resultados/tan_arestas.csv (origem; 9, 8, 8, 7, 8) |
| 7, 19 | 84 linhas; 400/0 → 0 e 1; 400/40 → 0,10 e 0,60; 200/70 → 0,333; 400/80 → 0,200; 800/50 → 0,0625 e 0,5 | resultados/sensibilidade.csv |
| 6, 18 | 40/400 = 0,10; 1 − 40/100 = 0,60; 100/500 = 0,2 | conta da matriz (G = 100, L = 400, c = 40) |
