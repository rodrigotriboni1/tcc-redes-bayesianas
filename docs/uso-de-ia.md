# Fluxo de uso de IA no TCC

## Acordo de trabalho

Rodrigo informou em 19/10/2026 que conversou com o professor e recebeu autorização para usar IA como apoio no TCC, com o objetivo de otimizar o tempo. A IA pode acelerar tarefas de pesquisa e execução, mas não substitui as decisões, a análise nem a responsabilidade do autor. Confirmar com o professor quais usos específicos são aceitos e como devem ser declarados segundo as normas aplicáveis ao curso.

A UFU publicou recomendações institucionais de uso ético e responsável de IA que orientam supervisão humana, transparência, privacidade e registro quando necessário para validação ou reprodução: [Portaria REITO nº 539/2026](https://sei.ufu.br/sei/publicacoes/controlador_publicacoes.php?acao=publicacao_visualizar&id_documento=8474675&id_orgao_publicacao=0). Normas específicas do curso e da atividade também devem ser observadas.

## Onde usar IA para ganhar tempo

- **Estudo:** pedir explicações graduais de redes bayesianas, inferência, calibração e utilidade esperada; depois resolver exercícios sem ajuda e conferir o raciocínio.
- **Literatura:** gerar termos de busca e organizar referências encontradas. Conferir cada referência na fonte original e ler o material citado antes de usá-lo.
- **Dados e código:** pedir esboços de scripts para checagens, análise exploratória e pipelines; revisar o código, executar em dados públicos e comparar as saídas com verificações independentes.
- **Depuração:** fornecer erro, trecho mínimo reproduzível e resultado esperado; manter a correção somente depois de entender e validar a causa.
- **Organização:** transformar decisões e anotações de orientação em próximos passos, mantendo explícito o que é decisão do professor e o que ainda é hipótese.
- **Texto:** usar como apoio para clareza, gramática, estrutura e tradução. O autor deve conferir cada afirmação, fonte e interpretação antes de incorporar o texto.

## Evidência e validação

Para cada resultado usado no TCC, manter o caminho de verificação:

1. **Afirmação:** o que será dito no texto.
2. **Evidência:** artigo, dado, cálculo, gráfico ou saída de código que sustenta a afirmação.
3. **Verificação:** como Rodrigo conferiu que a evidência e sua interpretação estão corretas.

Não tratar referências geradas por IA como reais sem verificá-las. Não usar texto ou código produzido por IA como comprovação de resultado. No German Credit, a IA pode ajudar a calcular e revisar a simulação, mas a base não fornece resultados contrafactuais das ações e, portanto, não comprova efeitos causais nem lucro real.

Usar somente dados públicos ou material que possa ser compartilhado com a ferramenta escolhida. Não enviar informações pessoais, confidenciais ou inéditas sem verificar as condições de privacidade e as orientações do professor.

## Registro de uso

Manter um registro resumido dos usos relevantes para transparência e reprodução. Não é necessário guardar conversas inteiras quando uma descrição objetiva da tarefa, ferramenta e validação for suficiente.

| Data | Ferramenta/versão | Tarefa | O que foi aproveitado | Como foi validado | Arquivo/resultado |
|---|---|---|---|---|---|
| 15/11/2026 | Subagente de IA (modelo não registrado) | Levantamento de critérios de aceite e redação das sete issues | `docs/criterios-de-aceite.md` e `docs/issues/` | O autor aceitou as propostas D1 a D11 em bloco; o documento diz que os pontos marcados "conferido" foram reexecutados. O `teste.csv` não foi aberto | `docs/criterios-de-aceite.md`, `docs/issues/` |
| 15/11/2026 | Claude Code (Sonnet 5.5; depois Fable 5.2) | Redação de `arquitetura.md`, `decisoes.md`, `glossario.md`, `reproduzir.md`, `decisoes-pendentes.md` e das seções de normas do curso; ajustes no `PLANO.md`, nos critérios e nas issues | O texto dos documentos, depois de decisões do autor | Conferido contra `PLANO.md` e critérios na própria sessão; o autor mergeou os PRs. **Não conferido:** a tradução das variáveis do glossário (de memória, depende do `codetable.txt`) e os diagramas Mermaid (não renderizados localmente) | `docs/*.md`, `PLANO.md` |
| 15/11/2026 | Quatro subagentes Claude (Sonnet 5.5, esforço médio) | Quatro correções pontuais de texto em `decisoes.md`, `reproduzir.md` e `arquitetura.md` | As quatro edições | `git diff` de cada commit nos ramos remotos | PRs #4, #5 e #7 |
| 15/11/2026 | opencode v2.3.0 com o modelo DeepSeek 4.1 flash (informado pelo autor) | Revisão do repositório: divergências entre documentos, aderência à proposta, organização, rigor do desenho e referências | Os achados, como lista de pendências | Cinco achados reconferidos no repositório na mesma sessão (pergunta "calibrada", `cortes.json` no demo, "6 issues", ordem de corte da issue 03 e o ECE do baseline); os demais constam como "só da revisão", sem conferência | `REVISAO.md` (fora do git), `docs/decisoes-pendentes.md` |
| 15/11/2026 | Subagente Claude Fable 5.2, esforço baixo | Julgamento independente das decisões P1 a P7 | Os vereditos, as ressalvas e o problema da primeira redação da nova pergunta | O autor decidiu em seguida; as contradições apontadas foram conferidas por leitura do `PLANO.md` | `docs/decisoes.md` |
| 15/11/2026 | Claude Code com busca web e leitura de PDFs | Pesquisa das normas do curso e da formatação do TCC na UFU | Estrutura exigida, regras de defesa e de formatação | PDFs oficiais da FEELT lidos diretamente. Sem data de vigência; falta confirmar com a coordenação que o documento de formatação vale para o curso | `docs/decisoes.md`, seção 7 |
| 15/11/2026 | Claude Code (Sonnet 5.5) | Ajustes no `.bib` e no mapa de referências (`russell2010` trocada para o original em inglês; coluna Verificar) | A estrutura do mapa. Título, editora, cidade e ano do `russell2010` foram escritos de memória | **Nada conferido no original.** A entrada está marcada `% VERIFICAR` | `monografia/referencias.bib`, `docs/mapa-de-referencias.md` |
| 15/11/2026 | Claude Code (Sonnet 5.5) | Atualização do gate (`factory/verificar_saidas.py`, `checks.sh`) para as saídas novas | O código das checagens | Teste sintético numa pasta temporária só com `dev.csv`: passa com saídas corretas e falha nos três defeitos injetados. Blocos das issues 02 a 07 e `checks.sh` completo **não testados** | `factory/` |
| 15/11/2026 | Software factory: agentes de intake e de spec (modelos da configuração da factory) | Intake e especificação da issue 01 (`modelos.py`) | `intake.md` e `spec.md`, em `factory/jobs/` (fora do git) | Ainda nenhum código gerado; o builder não rodou. O autor lê a spec antes do desenvolvimento | `factory/jobs/001-01-gerar-as-predi/` |
| 15/11/2026 | Software factory: agente de intake (modelo não registrado em `job.json` nem em `config.json`; a definição do agente indica Fable) | Decidir se cada issue 01 a 07 entra e com que escopo e risco | `intake.md` de cada job | Gate `factory/checks.sh` sobre o código final; o autor lê o PR depois do merge | `factory/jobs/*/intake.md` (fora do git) |
| 15/11/2026 | Software factory: agente spec-writer (modelo não registrado em `job.json` nem em `config.json`; a definição do agente indica Opus) | Transformar cada issue aceita em `spec.md` com critérios testáveis | `spec.md` de cada job | Gate `checks.sh`; o autor lê o PR depois do merge | `factory/jobs/*/spec.md` (fora do git) |
| 15/11/2026 | Software factory: agente builder (`config.json`, roteamento por risco: haiku para risco baixo, sonnet para médio e alto) | Implementar os scripts das issues 01 a 07 | O código de `codigo/` e os arquivos de `resultados/` | Gate `checks.sh` (autotestes `--verificar`); o autor lê o PR depois do merge e relê o código antes do congelamento | PRs das issues 01 a 07 |
| 15/11/2026 | Software factory: revisor de código (`job.json`, campo `agents.reviewers.code`: sonnet nas issues 01, 03, 04 e 07; haiku nas issues 02, 05 e 06) | Revisar correção, simplicidade e convenções de cada branch | O parecer PASS de cada job | Gate `checks.sh`; leitura do PR pelo autor | `factory/jobs/*/round-*/review-code.md` (fora do git) |
| 15/11/2026 | Software factory: agente aprovador (modelo não registrado em `job.json` nem em `config.json`; a definição do agente indica Opus) | Decidir se o PR é mergeado ou vai ao autor | A decisão de merge | Gate `checks.sh`; leitura do PR pelo autor depois do merge | `factory/jobs/*/decision.md` (fora do git) |
| 17/11/2026 | Software factory: intake, spec-writer, builder, revisor de código e aprovador (modelos conforme a configuração; não registrados por job) | Issues 08 (`--selecao`), 10 (`modelos.py --final` grava `p_sel`) e 11 (`sel` como modelo secundário em `avaliar.py` e `decisao.py`; `decisao.py --verificar`) | O código e os arquivos de `resultados/` dos PRs #45, #48 e #50, mergeados pela factory | Gate `checks.sh`; o autor ainda não leu esses PRs | PRs #45, #48, #50 |
| 17/11/2026 | Agentes avulsos Claude Code: Sonnet, Opus e Fable (este em modo de planejamento) | Trabalho de apoio fora da factory, entre eles os PRs de factory #43 e #47 | Os PRs e planos produzidos | **Não conferido pelo autor**: os PRs #43 e #47 foram feitos com o autor ausente, por delegação, e estão a rever | PRs #43 e #47 |
| 17/11/2026 | Claude Code, decisões por delegação e consulta ao advisor | Decisões tomadas com o autor ausente (inclusive o estudo de seleção da §9 do plano de análise) e uma consulta a um advisor | As decisões registradas em `docs/decisoes.md` e `docs/plano-de-analise.md` | Marcadas "decidido por delegação, a rever pelo autor". A consulta ao advisor é opinião, não validação | `docs/decisoes.md`, `docs/plano-de-analise.md` |
| 17/11/2026 | Claude Code (orquestrador), a pedido do autor | Execução do teste final (17/11/2026), a pedido do autor: Claude Code rodou `modelos.py --final`, `avaliar.py --final` e `decisao.py --final`, uma vez; não leu `teste.csv` | Os arquivos `*_teste*` de `resultados/` | Comandos com exit 0 sobre o commit `49d77ff` | `docs/decisoes.md` §1 |

**Pendente:** o professor ainda não confirmou quais usos são aceitos nem como devem ser declarados (ver o acordo de trabalho acima). A tabela registra o que foi feito até 17/11/2026; novos usos entram como novas linhas.
