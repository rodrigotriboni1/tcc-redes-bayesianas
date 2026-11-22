# Registro de decisões

Uma linha por decisão: o que ficou decidido, por quê, e quem decidiu. Serve para responder à banca "por que foi feito assim" sem depender de memória.

Fontes: [PLANO.md](../PLANO.md) (itens 4, 5 e 10) e [criterios-de-aceite.md](criterios-de-aceite.md) (D1 a D11). Este arquivo não cria decisão: copia o que já está escrito. Onde o motivo não foi registrado em nenhum arquivo, a coluna diz **motivo não registrado**; preencha antes da defesa.

Quem decidiu:
- **Autor**: Rodrigo, em nome próprio.
- **Autor (proposta do levantamento)**: proposta feita por um subagente em 15/11/2026 e aceita pelo autor em bloco no mesmo dia.
- **Orientador**: ver "Respostas do orientador (18/11/2026)".
- **Agente**: escolha de implementação feita por um agente sem o autor ter decidido; vale até o autor rever. Quando o autor a aceita, a coluna diz como.

## 1. Dados e divisão

| Data | Decisão | Motivo | Quem |
|---|---|---|---|
| 14/11/2026 | Divisão dev/teste refeita, estratificada, semente 2026 (800/200; 240 e 60 ruins) | A divisão antiga (semente 42) tinha o teste já aberto em um trabalho anterior, com a regressão logística | Autor |
| 14/11/2026 | O teste novo fica fechado até o passo 10; todos os modelos, inclusive o baseline, são avaliados nele uma única vez | Motivo não registrado | Autor |
| 15/11/2026 | O código só lê `dev.csv`. `teste.csv`, `sgc.csv` e `dados/brutos/` são proibidos para o código (D11) | `sgc.csv` e os dados brutos também contêm as 200 linhas do teste | Autor (proposta do levantamento) |
| 15/11/2026 | O teste final é rodado pelo autor, à mão, uma vez. A factory só escreve o caminho `--final`, testado com linhas do dev (D10) | A proteção por busca e caixa de areia pega o acidente, não um agente decidido a olhar. A garantia final é o commit de congelamento mais o teste rodado pelo autor (critérios, seção 5) | Autor (proposta do levantamento) |

| 17/11/2026 | Commit de congelamento: `49d77ff0eec74de98d7ce7ec83a9d0d2907bb207` (`main` após o PR #51). O código dos 7 scripts, `--selecao`, `--final` e `sel` não muda depois deste commit. `bash factory/checks.sh` passou nele ("tudo certo", `resultados/` idêntico byte a byte). Nenhum arquivo `*_teste*` existe | O autor releu todo o código (declarado em 17/11/2026) e liberou o congelamento; o teste final só é rodado sobre este commit | Autor |
| 17/11/2026 | O teste final foi rodado pelo orquestrador (Claude), a pedido explícito do autor na conversa, em vez de pelo autor à mão. Os 3 comandos (`modelos.py --final`, `avaliar.py --final`, `decisao.py --final`) rodaram uma vez, sobre o commit `49d77ff`, todos com exit 0. O orquestrador não leu `teste.csv` (só o script o leu) | Desvio da decisão D10 ("o autor roda à mão, uma vez"), por ordem do autor; a proteção da regra 2 do `AGENTS.md` era contra acidente, e o autor decidiu delegar a execução | Autor |

## 2. Constantes congeladas

Regra G4 do critério de aceite: mudar uma delas é motivo para parar e perguntar, nunca para ajustar a um resultado.

| Constante | Valor | Motivo |
|---|---|---|
| Semente | 2026 | Divisão nova, ver acima. Para as demais fontes de aleatoriedade: motivo não registrado |
| Partições da validação cruzada | 5, estratificadas, só no dev | "Não gasta o teste" (plano, item 5). Por que 5 e não 10: motivo não registrado |
| Faixas das variáveis contínuas | 3, por tercis, cortes aprendidos só no treino de cada partição | "A rede discreta exige" e o corte só no treino evita vazamento (plano, item 5). Por que 3 e não 4 ou 5: motivo não registrado |
| Prior | BDeu, tamanho equivalente 5 | Evita probabilidade zero em combinações raras (plano, item 5). Por que 5: motivo não registrado |
| Regressão logística | `LogisticRegression(max_iter=1000)` | Herdada do baseline anterior (`build()` do `baseline_logreg.py`) |
| Erro de calibração | 10 faixas de mesma largura | Só o número de faixas (10) é herdado do `baseline_logreg.py`. A definição mudou: o `baseline_logreg.py` (linhas ~32-40) calcula o ECE top-label (confiança max(p, 1-p) contra acerto), e o critério 02.6 de `docs/criterios-de-aceite.md` define o ECE sobre P(ruim) contra a taxa observada de ruins. Motivo da mudança de definição: não registrado |

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

### Decidido depois da revisão do repositório (15/11/2026)

Decididas em conversa com o autor; um avaliador independente (subagente) julgou as sete antes do registro. Veredito dele entre parênteses; as ressalvas viram texto obrigatório na monografia.

| Data | Decisão | Motivo | Quem |
|---|---|---|---|
| 15/11/2026 | **Calibração só é medida**, sem correção isotônica (P1). A pergunta troca "calibrada" por "com calibração medida" | Nenhuma issue nova; a correção dependeria de olhar `metricas_dev.csv`. Desvio da proposta, que promete "calibrar": avisar o orientador (plano, item 11.4). (Aceitável com ressalva) | Autor |
| 15/11/2026 | A monografia não afirma que o experimento mostra que a política exige probabilidade calibrada; isso vem da literatura, e o experimento mede o erro de calibração (P2) | Alegação menor e honesta. Citar a fonte conferida no original. (Sólida) | Autor |
| 15/11/2026 | **Pergunta reformulada em duas partes** (P3): (1) limiares explícitos e reproduzíveis a partir da matriz e de `p`; (2) efeito medido sobre as ações e a utilidade média contra o limiar fixo de 0,5 | "Consistentes e transparentes" não eram medidos. A primeira redação, "mais auditáveis", foi julgada problemática: contradiz a proposta (que chama regras e escores de auditáveis), vale por construção para qualquer escore e deixa a rede sem papel. A forma em duas partes separa a propriedade do efeito medido. Aviso ao orientador no item 11.4 | Autor |
| 15/11/2026 | Bootstrap (2000 reamostras, semente 2026, percentis 2,5 e 97,5, as mesmas para todos os modelos e regras) também para a utilidade média no teste final (P4). Entra em `resumo_politicas_teste.csv` (critério 07.9) | A utilidade é a métrica da pergunta e não tinha intervalo. Ressalva: o intervalo é por política, não da diferença entre políticas, e não cobre a variação do treino; dizer isso no texto, ou decidir gravar o intervalo da diferença pareada (não decidido) | Autor |
| 15/11/2026 | **O TAN vai para a tabela 2×2** do texto; os três modelos ficam no apêndice (P5) | Escolha pré-especificada, feita antes de existir `metricas_dev.csv`, então não depende de resultado. Fecha a D3. (Sólida) | Autor |
| 15/11/2026 | A regressão logística mantém as 3 contínuas originais; as redes usam 3 faixas (P6) | Baseline usual; discretizar enfraqueceria o baseline e mudaria a issue 01 e a D2. Ressalva: a diferença TAN × logística mistura modelo e representação; escrever "modelo e representação", não "efeito do modelo". (Aceitável com ressalva) | Autor |
| 15/11/2026 | Matriz de utilidade mantida (+100, −400, c = 40) como hipótese pendente do orientador; "o analista sempre acerta" vai para as limitações (P7) | Sem custo de código. Ressalva: com analista infalível, a política de três ações ganha por construção do corte de duas ações; dizer isso junto da tabela 2×2, não só nas limitações. (Aceitável com ressalva) | Autor |
| 15/11/2026 | A tabela 2×2 é descrita como "política de três ações por utilidade esperada contra corte 0,5 de duas ações", sem linguagem causal (P8) | A regra fixa não tem análise manual, então a diferença mistura modelo, representação e conjunto de ações. `arquitetura.md` ajustado | Autor |
| 15/11/2026 | Evidência incompleta: mesma tabela, com ressalva na legenda de que as redes marginalizam a variável e a regressão logística imputa mediana ou moda; as quedas não são comparáveis entre famílias (P9) | A comparação direta seria enganosa. Sem mudar issue | Autor |
| 15/11/2026 | O espaço de estados das variáveis é fixado no dev inteiro; a seção de materiais e métodos declara isso (P10) | Estabilidade (categoria rara fora do treino de uma partição não derruba a inferência, critério 01.11). Não usa rótulo, mas é um vazamento brando, e o texto precisa dizer | Autor |
| 15/11/2026 | A monografia usa só o ECE novo (sobre P(ruim)). Se o número do baseline antigo aparecer, vem rotulado "top-label, protocolo anterior" (P11) | Os dois não são comparáveis e o baseline antigo usa outra divisão (semente 42). Sem recálculo | Autor |
| 15/11/2026 | Etapa B da proposta (análise exploratória): uma tabela de descrição da base no capítulo 3 da monografia, feita a partir do `dev.csv` e do dicionário, sem script novo. A monografia declara que a análise exploratória se limita a isso (P12) | O plano fixa 7 scripts; uma análise exploratória em código seria exceção. Aviso ao orientador | Autor |
| 15/11/2026 | `politicas_dev.csv` grava a segunda melhor ação e a diferença de utilidade esperada, para a regra de utilidade (P13). Muda a issue 04 e o critério 04.12 | Cumpre a etapa D da proposta e dá arquivo de origem à resposta "por que não a segunda ação?" | Autor |
| 15/11/2026 | PR-AUC entra em `metricas_dev.csv` e `metricas_teste.csv` (P14). Custo esperado fica dito no texto como o negativo da utilidade esperada | Com 30% de ruins PR-AUC é pertinente; a proposta a cita. Métrica a mais, não escolha por resultado. Muda as issues 02 e 07 | Autor |
| 15/11/2026 | Justificativa textual da recomendação no demo fica de fora; a monografia diz que o demo mostra a conta (risco, utilidade de cada ação, fronteiras) e não a explicação textual (P15) | Corte registrado da etapa F. Aviso ao orientador junto com a troca de protótipo | Autor |
| 15/11/2026 | O TAN grava as arestas de cada partição em `resultados/tan_arestas.csv` (P16). Muda a issue 01 e o critério 01.12 | O grafo aprendido é resultado num TCC de redes bayesianas; permite mostrar a estabilidade da estrutura entre partições | Autor |
| 15/11/2026 | O bootstrap da issue 07 também grava a diferença pareada de utilidade média entre a regra de utilidade e o limiar fixo (`diferenca_politicas_teste.csv`, ressalva da P4). Intervalos por política seguem em `resumo_politicas_teste.csv` | Responde à parte 2 da pergunta sem comparar intervalos que se sobrepõem. Ainda não cobre a variação do treino | Autor |
| 15/11/2026 | O gate passa a buscar `clip(` em `codigo/` (P17) | Impõe por máquina a regra do `AGENTS.md`; um `clip` legítimo em outro contexto vira falha a explicar | Autor |
| 15/11/2026 | O critério 03.5 (alguma predição muda ao esconder a variável) vira aviso (P19) | É presença de efeito, que os critérios proíbem. O critério estrutural 03.4 continua | Autor |
| 15/11/2026 | O verificador passa a conferir as falhas esperadas de `--final` e as utilidades do demo, além dos arquivos novos (P20) | Tudo de forma, não de resultado | Autor |
| 15/11/2026 | `AGENTS.md` registra as exceções: `preparar_sgc.py` grava em `dados/processados/` e `test_decisao.py` é o único arquivo de teste previsto (P21) | Alinha o `AGENTS.md` ao plano e à G3 | Autor |
| 15/11/2026 | Prazo informado pelo autor: "até o final do mês" (P22). Falta dizer se é entrega ou defesa | Pelo Anexo 6, a defesa só pode ser agendada 15 dias depois da entrega das cópias | Autor |
| 15/11/2026 | O autor pediu pesquisa do modelo de documento da UFU (P22). Resultado na seção 7: não foi achado o modelo do Colegiado; as regras de formatação da FEELT aceitam Word, LibreOffice, Google Docs ou LaTeX | Fica a confirmar com a coordenação | Autor |
| 15/11/2026 | Os avisos ao orientador (troca de base, de protótipo, de pergunta e de calibração) seguem em uma única mensagem, com rascunho escrito na conversa (P23) | Cumpre o item 11.4 do plano | Autor |
| 15/11/2026 | O placeholder "[Supervisor's Name]" só existe na cópia local da proposta; a versão submetida está correta (P24) | Informação do autor | Autor |
| 15/11/2026 | As contagens de categorias raras do plano e do glossário passam a ser rotuladas "da base completa, a conferir pelo autor no `sgc.csv`" (P25) | Não batem com o dev e o agente não pode abrir a base completa | Autor |
| 15/11/2026 | A interface de uma tela só será construída no fim, depois do experimento pronto. Esboço escolhido: layout "mapa de sensibilidade do caso" (grade perda × custo colorida pela ação), que só mostra e lê `sensibilidade.csv` e `predicoes_dev.csv` por `fetch` com servidor local, sem script novo | Cumpre o item 12 do plano sem quebrar os 7 scripts. Até lá vale a demonstração de terminal | Autor |
| 15/11/2026 | `russell2010` passa a ser o original em inglês (3ª ed., Prentice Hall, 2010), não a tradução brasileira (P26) | O `.bib` misturava título e editora da tradução com o ano do original. A entrada ganha `% VERIFICAR`: os dados foram escritos de memória de um assistente de IA | Autor |
| 15/11/2026 | Na seção 2.5 do mapa, Platt (sigmoide) e regressão isotônica são métodos da literatura citados sem aplicar; o trabalho só mede a calibração (P27) | Evita sugerir que a isotônica é de Platt e fica coerente com a P1 | Autor |
| 15/11/2026 | O mapa de referências ganha a coluna "Verificar" com o que falta conferir em cada entrada; o plano passa a dizer 15 entradas a conferir, não 9 (P28) | Cinco marcas `% VERIFICAR` do `.bib` não apareciam no mapa. A conferência no original continua sendo do autor | Autor |
| 15/11/2026 | O log de uso de IA registra uma linha por tipo de uso (nove linhas), com o que foi aproveitado e o que **não** foi conferido (P29) | Transparência e reprodução, como pede `uso-de-ia.md`. Confirmar com o professor os usos aceitos e a forma de declarar | Autor |
| 15/11/2026 | O `README.md` ganha índice da documentação, comandos, mapa das pastas e um parágrafo dizendo que `factory/` e `.claude/` são ferramenta de processo, não parte do experimento (P30) | Quem abre o repositório, incluindo a banca, via sete linhas e oito agentes sem explicação | Autor |
| 18/11/2026 | Plano de análise §8: o intervalo de 95% (*bootstrap*) é o critério de leitura da diferença pareada de utilidade; o limite de 0,03 vale só para ROC-AUC, e PR-AUC fica só descrita, sem conclusão de ruído | Confirma o que o texto já aplica; PR-AUC fica só descrita para não criar regra nova depois de aberto o teste | Autor |

## 5. Processo

| Data | Decisão | Motivo | Quem |
|---|---|---|---|
| 15/11/2026 | O código é escrito pela software factory, uma issue por PR. A sessão interativa só define critérios e escreve os `.md` | Motivo não registrado | Autor |
| 15/11/2026 | Critério de aceite restringe a forma, nunca o resultado | Um agente que veja "AUC acima de 0,75" é convidado a mexer no modelo até passar | Autor |
| 15/11/2026 | Merge automático quando o aprovador da factory aprova (D9). O autor lê a descrição de cada PR depois do merge e relê todo o código antes do commit de congelamento | O autor optou por não parar cada PR. Substitui a decisão anterior, que parava o merge para revisão humana | Autor |
| 15/11/2026 | Dois arquivos de resultado a mais: `resumo_politicas_dev.csv` e `sensibilidade.csv` (D6) | Dois números da monografia não teriam arquivo de origem | Autor (proposta do levantamento) |

## Estudo de seleção

Decidido por delegação em 16/11/2026, a rever pelo autor. Detalhe em [plano-de-analise.md](plano-de-analise.md), §9.

| Data | Questão | Decisão | Motivo | Quem |
|---|---|---|---|---|
| 16/11/2026 | Q1 | B: estudo secundário; a análise primária não muda | Preserva a comparação pré-definida (P5) e ainda testa a hipótese levantada no dev | Por delegação, a rever pelo autor |
| 16/11/2026 | Q2 | Grade fechada {NB, TAN} × BDeu {1, 5, 10, 50}: `nb_ess1`, `nb_ess5`, `nb_ess10`, `nb_ess50`, `tan_ess1`, `tan_ess5`, `tan_ess10`, `tan_ess50` | Grade pequena e fechada limita as comparações a 8 | Por delegação, a rever pelo autor |
| 16/11/2026 | Q3 | Escolha pelo menor log loss médio interno; empate (< 1e-9) pela ordem da grade | Regra fixada antes de rodar; log loss mede a probabilidade, que é o que a decisão usa | Por delegação, a rever pelo autor |
| 16/11/2026 | Q4 | Não reverter P1 | O estudo é secundário; nada da análise primária muda | Por delegação, a rever pelo autor |
| 16/11/2026 | Q5 | Exceção às regras 3 e 4 do `AGENTS.md` só no modo `--selecao` | Fora desse modo as constantes seguem congeladas | Por delegação, a rever pelo autor |
| 16/11/2026 | Q6 | Medir o tempo da execução e registrar, sem limite fixado | Não há base para fixar limite antes de medir | Por delegação, a rever pelo autor |
| 16/11/2026 | Q7 | Em aberto; não bloqueia o estudo | Fica para o autor | Em aberto |
| 16/11/2026 | Q8 | Em aberto; não bloqueia o estudo | Fica para o autor | Em aberto |

Viés declarado: a grade foi desenhada depois de ver `metricas_dev.csv`; o aninhamento não corrige isso.

## Respostas do orientador (18/11/2026)

| Data | Decisão | Motivo | Quem |
|---|---|---|---|
| 18/11/2026 | Prazo informado pelo autor: até 30/11/2026 (não foi dito se é entrega ou defesa) | Resposta ao item 1 da §11 do `PLANO.md` | Autor, informado pelo orientador |
| 18/11/2026 | Matriz de utilidade demonstrativa (+100, −400, c = 40) aprovada ("pode fazer"). Os valores continuam demonstrativos, não calibrados com dados reais, e o analista continua suposto infalível | Resposta ao item 2 da §11 do `PLANO.md` | Autor, informado pelo orientador |
| 18/11/2026 | Modelo de documento: o modelo de TCC da FEELT enviado pelo orientador (`template_tcc_final.docx`, 2017): margens esquerda 2,75 cm e direita 1,73 cm, Tahoma nos títulos e Georgia no corpo, numeração "Figura 1"/"Tabela 1" e referências com "Citado na página" | Resposta ao item 3 da §11 do `PLANO.md` | Autor, informado pelo orientador |
| 18/11/2026 | A monografia não precisa mencionar o uso de inteligência artificial em nenhum lugar; o registro interno `docs/uso-de-ia.md` continua no repositório | Dispensa dada pelo orientador | Autor, informado pelo orientador |

## Análise posterior ao teste (22/11/2026)

Registrada antes de rodar, como pede a §7 do [plano de análise](plano-de-analise.md). A decisão de medir veio depois de conhecer o resultado do teste (22,5 [9,2; 37,2]), por isso a análise é exploratória e será declarada no texto como desvio do plano.

| Data | Decisão | Motivo | Quem |
|---|---|---|---|
| 22/11/2026 | Medir no teste a política de utilidade esperada restrita a aprovar e rejeitar (limiar 0,2, derivado da matriz), com `decisao.py --final`, ao lado de `ue` (três ações) e do corte 0,5. Saídas novas: `duas_acoes_teste.csv` e `diferenca_duas_acoes_teste.csv`; os 6 arquivos do teste não mudam | Separar o efeito do conjunto de ações do efeito do corte de referência: o corte 0,5 não é o limiar de duas ações da matriz demonstrativa (G/(G+L) = 100/500 = 0,2), apontado pelo orientador na revisão 1 | Autor, motivado pelo apontamento do orientador |
| 22/11/2026 | Leitura, definida antes de rodar e para cada diferença (`ue − limiar`, `ue − ue2`, `ue2 − limiar`): se o intervalo de 95% exclui zero, "diferença observada a favor de X, com intervalo que exclui zero", sem afirmar causa; se inclui zero, "sem evidência de diferença com 200 casos e 60 ruins", sem concluir que as políticas são iguais; se exclui zero a favor da política de duas ações ou do corte, reportado como saiu | Mesma estrutura da §4 do plano, sem depender do valor observado | Autor |
| 22/11/2026 | A comparação principal (TAN, `ue` × corte 0,5), a matriz, os modelos e a leitura anterior não mudam, qualquer que seja o resultado. A política de duas ações não é adotada nem recomendada por causa dele | Regras 3 e 5 do `AGENTS.md`: nada se ajusta por métrica; a escolha de política depende de número e é do autor | Autor |
| 22/11/2026 | `factory/checks.sh`, passo 7: as 2 tabelas novas são opcionais, mas vêm juntas; as 6 do teste continuam obrigatórias | Não reprovar o ramo antes de o autor rodar `--final` e manter a checagem de que não sobra arquivo de teste fora da lista | Autor |

## Sensibilidade das ações à calibração (22/11/2026)

Registrada **depois** de rodar, ao contrário da seção anterior: a §7 do [plano de análise](plano-de-analise.md) pede a linha aqui antes de rodar de novo, e isso não foi feito. A análise é posterior ao plano e ao resultado do teste, e já está declarada como tal na Seção 4.8, na Seção 3.6 e no Apêndice B (B.5) da monografia.

| Data | Decisão | Motivo | Quem |
|---|---|---|---|
| 22/11/2026 | Medir a sensibilidade das ações ao erro de calibração com `decisao.py --calibracao`: trocar `p` por `p − ECE`, `p` e `p + ECE` (ECE médio de cada modelo em `metricas_dev.csv`) e refazer a ação de utilidade esperada de cada caso do desenvolvimento. Saída nova: `sensibilidade_calibracao_dev.csv`. Não treina, não recalibra e não abre o teste | Parecer do orientador, ponto 4 (ALTA): quantificar ou discutir a sensibilidade das ações à calibração sem alterar retrospectivamente o protocolo primário. A calibração segue só medida (P1) | Autor, motivado pelo parecer; método recomendado pelo agente e aceito pelo autor |
| 22/11/2026 | Rodar só nas predições do desenvolvimento (`predicoes_dev.csv`), não nas do teste | O teste já foi aberto uma vez; usá-lo para ver o efeito de uma correção seria ajustar ao resultado (§5, item 1, do plano; regra 3 do `AGENTS.md`) | Autor, a partir da recomendação do agente |
| 22/11/2026 | O deslocamento `p ± ECE` não é cortado em [0, 1]: a ação só depende de `p` frente às fronteiras da matriz | O `AGENTS.md` proíbe `clip` sobre probabilidades; com `acao_deslocada()` o corte não é necessário | Agente, ao implementar; a rever pelo autor |
| 22/11/2026 | Implementada como modo `--calibracao` de `decisao.py`, e não como script novo. `factory/checks.sh` passa a rodar o modo, e `auditoria_independente.py` entra em `PERMITIDOS` | O plano limita os scripts a 7 e proíbe outro arquivo em `codigo/`; sem a linha no `checks.sh`, o passo 12 reprovava o arquivo novo ("nenhum script o gera") | Agente, aceito pelo autor no merge do #98 e do #100 |
| 22/11/2026 | Leitura: cenário simétrico, só no desenvolvimento, sem intervalo; não é recalibração, não escolhe modelo, parâmetro nem matriz, e os resultados dos Capítulos 4 e 5 seguem com as probabilidades sem correção. A utilidade média não segue direção única (Tabela 14 do `.docx`, Tabela 4.13 dos `.md`) | Declarar o limite da medida: o erro real de calibração não é um deslocamento constante | Agente (texto da Seção 4.8), aprovado pelo autor no merge do #99 |
| 22/11/2026 | Recalibrar (Platt ou regressão isotônica) em dados separados continua fora do protocolo. Fica como direção futura na Seção 5.10, comparável ao deslocamento pelo ECE | A escolha do método depende de número e é do autor (decisão P1, D4); corrigir depois de ver o teste seria ajustar o modelo ao resultado | Autor |
| 22/11/2026 | Registrar esta análise aqui depois de rodar, e dizer isso no Apêndice B | A §7 do plano exige o registro antes; não foi feito, e o texto declara o desvio em vez de omiti-lo | Autor |

## Esclarecimentos e delegações do autor (22/11/2026)

| Data | Decisão | Motivo | Quem |
|---|---|---|---|
| 22/11/2026 | O prazo de 30/11/2026 é de **entrega das cópias**, não de defesa (completa a linha de 18/11/2026, que não dizia qual dos dois). Pelo regulamento (Art. 6º, §6º a §8º), a defesa só pode ser agendada 15 dias depois da entrega: com entrega em 30/11, em 15/12/2026 ou depois | Resposta do autor | Autor |
| 22/11/2026 | O CDU e o número de páginas da ficha catalográfica e a folha de aprovação da banca ficam com o orientador. Na versão de entrega, a ficha mantém os marcadores `[nº de páginas]` e `[CDU: a preencher pela biblioteca]` | Resposta do autor | Autor |
| 22/11/2026 | Sumário e listas de ilustrações e de tabelas passam a ser campos do Word: os 67 títulos ganham nível de estrutura, sem mudar a aparência, e as listas usam referência cruzada às legendas. Ao abrir `TCC_Rodrigo_Final_Revisao_4.docx`, o Word pergunta se deve atualizar os campos; a resposta é "Sim", e as páginas aparecem | A entrega é encadernada e o sumário e as listas não tinham número de página | Autor, pedido ao agente |
| 22/11/2026 | Referências, por delegação ao agente, a rever pelo autor. UCI 573: título "South German Credit" (o "(UPDATE)" é só o final do URL) e ano 2020 mantido, o do campo de criação do registro (a UCI indica doação em 28/11/2019). Siddiqi: mantido como 1ª edição, Wiley, 2006. Platt: corrigido para 2000, o ano do livro (MIT Press); o capítulo circulou em 1999 e muitos catálogos citam 1999, mas a referência é ao livro. As páginas 61–74 não foram confirmadas (o acesso ao Crossref e à UCI foi bloqueado nesta sessão, e o Platt não consta no Crossref). Corrigido na Revisão 5 do TCC | `docs/conferencia-referencias.md` (17/11/2026): "o autor decide" | Por delegação, a rever pelo autor |
| 22/11/2026 | `config/utilidade.json`: o campo `hipoteses` deixa de dizer "pendente de aprovação do orientador" e passa a dizer que a matriz foi aceita em 18/11/2026 apenas para fins demonstrativos. Os valores da matriz não mudam | Coerência com a linha de 18/11/2026 e com o painel de defesa, que exibe o campo | Autor, pedido ao agente |

## 6. Em aberto

| Questão | Depende de |
|---|---|
| Avisar a troca de base (SGC), a troca do protótipo, a nova pergunta e a calibração só medida | Autor, ao orientador (rascunho da mensagem na conversa de 15/11/2026) |
| Construir a interface de uma tela (plano, item 12). Esboço escolhido em 15/11/2026: mapa de sensibilidade do caso, lendo os CSV por `fetch` com servidor local; fica para depois do experimento | Autor, só depois de o experimento estar pronto |

## 7. Normas do curso (pesquisado em 15/11/2026)

Duas fontes oficiais da FEELT/UFU, lidas nos PDFs. Nenhuma tem data de vigência clara; confirmar com a coordenação.

**Anexo 6, normas gerais do curso de Engenharia de Controle e Automação** (`feelt.ufu.br`, `ea_anexo_06_...pdf`):
- Art. 6º: a monografia é elaborada, escrita, apresentada e defendida em sessão pública perante banca; §5º: o formato é "o modelo estabelecido pelo Colegiado do Curso".
- Art. 6º, §6º a §8º: a defesa é agendada na secretaria com a entrega de cópias encadernadas e a composição da banca feita pelo orientador; o intervalo mínimo é de **15 dias** entre a entrega das cópias e a defesa.
- Art. 7º: banca de 3 membros, o orientador preside; apresentação oral de 20 a 30 minutos; o arguido é o último a ser arguido pelo presidente.
- Art. 8º: resultado APROVADO, APROVADO CONDICIONALMENTE (correções em até 30 dias, com apreciação do Colegiado) ou REPROVADO; o aprovado entrega cópia em mídia eletrônica para publicação, sem a qual a disciplina não encerra.
- Art. 9º: sem defesa até o fim do semestre letivo, o conceito é NÃO CONCLUIU, que não entra no CRA.

**Regras de formatação do TCC** (`feelt.ufu.br`, `4_-_formatacao_do_projeto_final_de_curso.pdf`; o título do documento diz "Curso de Engenharia Elétrica", então falta confirmar que vale para Controle e Automação):
- Formato eletrônico; editores recomendados: Word, LibreOffice Writer, Google Docs, TeXstudio e Overleaf (LaTeX serve).
- Estrutura: capa, folha de rosto, dedicatória e agradecimentos (opcionais), sumário, listas de figuras, tabelas e siglas, lista de símbolos (opcional), **resumo de 150 a 500 palavras com cinco palavras-chave e abstract equivalente em inglês com cinco keywords**, introdução, corpo, conclusões, referências, anexos, apêndices e glossário (opcionais).
- Times New Roman ou Arial, tamanho 12, frente e verso; cada elemento pré-textual, capítulo e elemento pós-textual começa em página ímpar; títulos de capítulo em 14, negrito, caixa alta.
- Referências em ABNT NBR 6023-2018, citação por sobrenome e ano, ordem alfabética.

Efeito no plano: os capítulos do item 9 do `PLANO.md` cabem nessa estrutura. O plano ainda não prevê resumo, abstract, listas e glossário; entram no texto, sem código.

## Como acrescentar uma decisão

Uma linha na tabela da seção certa, com data, motivo e quem decidiu. Decisão sobre constante congelada ou sobre escolha que dependa de número é do autor: se a factory ou um agente propuser, registre como proposta e só depois como decisão.
