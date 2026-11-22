# Resposta à revisão 1 do orientador

Arquivo revisado: `TCC_Rodrigo_Final_Revisao_2.docx` (a base é a `Revisão_1` com os apontamentos). Nenhum resultado, hiperparâmetro, semente, faixa, modelo ou valor da matriz foi alterado. As mudanças são de texto; as verificações estão marcadas como tais.

## O que o orientador apontou e o que foi feito

| Apontamento | O que foi feito | Onde |
|---|---|---|
| ALTA: "vantagem garantida por construção" | As substituições sugeridas (amarelo para verde) foram aplicadas. A vantagem passou a ser descrita como prevista pela matriz na utilidade esperada do modelo, sem garantia de ganho realizado. | Resumo, abstract, 3.7.1, 5.2, 5.5, Cap. 6 |
| ALTA: o corte de 0,5 não é o ótimo de duas ações (0,2) | Declarado em 3.7.1 e em 5.5, com a ligação à interpretação dos 22,5: parte da diferença pode vir do corte de referência, e este trabalho não separa as contribuições. A política de utilidade esperada com duas ações e limiar 0,2 entrou como direção futura (5.10), sem medida. | 3.7.1, 5.5, 5.10 |
| ALTA: separar pré-registro de decisões posteriores | "Pré-registrado" foi trocado por "plano de análise" em todo o texto. O Apêndice B ganhou a §9 (16/11, depois das métricas de desenvolvimento) e uma cronologia. | 1.2, introdução do Cap. 3, 3.6, introdução dos Caps. 4 e 5, 4.1, 5.2, Cap. 6, Apêndice B |
| ALTA: raiz do TAN no pgmpy 1.1.2 | Verificado no código-fonte (`TreeSearch.py`, linhas 145–150) e nas 5 partições do projeto: a raiz é a coluna de maior soma de informação mútua não condicional, e a soma inclui a classe `kredit`, que nunca fica no topo. O texto foi mantido. | 3.5 |
| ALTA: políticas com conjuntos de ações diferentes | Texto novo em 3.7.1 e 5.5 (a diferença reúne ação adicional, corte de referência e método). | 3.7.1, 5.5 |
| ALTA: reprodutibilidade | Conferido: `49d77ff` está no histórico do ramo; `uv.lock` fixa pgmpy 1.1.2; `resultados/` está versionado. Entre `49d77ff` e `cc2badc` (resultados do teste) não houve mudança em código, configuração, dependências nem plano. Não conferido: a presença dos dados em `dados/`. | 3.2, Apêndice B |
| MÉDIA: linguagem de diferença simulada | Aplicada no resumo, no abstract e na conclusão. | Resumo, abstract, Cap. 6 |
| MÉDIA: regra de 0,03 não é teste de equivalência | Dita em 3.6 e repetida nos resultados, na discussão e no Apêndice B ("tratada como ruído", "sem apontar qual modelo é melhor"). | 3.6, 4.1, 5.2, B.2, B.4 |
| MÉDIA: referências | As 26 referências e as citações do texto se correspondem (primeiro autor e ano), sem órfãs. DOI e URL já tinham sido conferidos em 17/11 (`docs/conferencia-referencias.md`); seguem em aberto UCI 573, Siddiqi e Platt (páginas). | Referências |
| MÉDIA: pré-textuais | O relatório do orientador saiu do arquivo. O documento pede atualização dos campos (sumário e listas) ao abrir. Seguem em aberto: número de páginas e CDU da ficha catalográfica, folha de aprovação (só após a defesa). | Pré-textuais |
| MÉDIA: equações e figuras | As 11 equações foram comparadas com as definições e com o código (Brier, log loss, ECE de 10 faixas, limiar p* = G/(G+L)). As 3 figuras são idênticas byte a byte às de `resultados/`. | Cap. 2 a 4 |

## Também atualizados

Os capítulos em `.md` (`resumo.md`, `cap1` a `cap6`), o roteiro, o gerador e o `.pptx` dos slides e a explicação da apresentação, com as mesmas frases. A pergunta provável da banca "A vantagem é garantida?" substituiu "O que significa ganha por construção?".

## Para o autor decidir

- Medir ou não a política de utilidade esperada com duas ações (limiar 0,2) como análise exploratória posterior ao teste. Não foi feito: depende de rodar sobre o teste e é decisão do autor.
- Confirmar com o orientador se o prazo de 30/11 é entrega das cópias ou defesa (regulamento: 15 dias entre as duas).
- `config/utilidade.json` ainda diz "Matriz pendente de aprovação do orientador", enquanto o texto diz "aprovada". O arquivo é do autor e não foi alterado.
- Os parágrafos em amarelo (5.6, "diferenças pequenas dificilmente se distinguem de ruído") são redação própria para trecho marcado sem sugestão.
- `monografia/monografia.md`, `esqueleto.md` e `apendices.md` (cópia literal do plano) não foram atualizados: são cópias anteriores ou transcrições do plano, e o `.docx` é a referência.
