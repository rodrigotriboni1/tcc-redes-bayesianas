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
| Prazo: o autor informou "até o final do mês" (15/11/2026); falta dizer se é entrega ou defesa. Se for a defesa, as cópias têm de estar na secretaria 15 dias antes (seção 7) | Autor |
| Aceita a matriz de utilidade demonstrativa (c = 40)? Os valores `+100`, `−400` e `100 − c` são hipóteses | Orientador |
| Modelo de documento do Colegiado (Anexo 6, art. 6º, §5º): não foi encontrado; confirmar com a coordenação | Autor, à coordenação |
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
