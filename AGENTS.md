# AGENTS.md

Regras para qualquer agente que trabalhe neste repositório. Leia inteiro antes de começar.

## O que é

Experimento de um TCC: uma rede bayesiana estima o risco de crédito e uma camada de utilidade esperada escolhe a ação. É um conjunto de scripts Python que leem CSV e gravam tabelas e figuras. Não há frontend, backend nem banco de dados.

O código será defendido pelo autor diante de uma banca. Ele precisa conseguir ler e explicar cada linha.

## Leia antes

1. [PLANO.md](PLANO.md): pergunta, algoritmos, pastas, arquivos trocados entre scripts. **As decisões do plano são fixas.**
2. [docs/criterios-de-aceite.md](docs/criterios-de-aceite.md): critérios da sua issue e o que está fora do escopo dela.
3. A issue.

Para consulta, sem obrigação de ler tudo:

- [docs/arquitetura.md](docs/arquitetura.md): scripts, arquivos trocados e fluxo, em diagramas.
- [docs/decisoes.md](docs/decisoes.md): o que foi decidido, por quê e por quem. Antes de propor mudança em algo, veja se já foi decidido.
- [docs/glossario.md](docs/glossario.md): termos e dicionário das variáveis em alemão.
- [docs/reproduzir.md](docs/reproduzir.md): ordem dos comandos e como conferir os resultados.

Esses quatro arquivos são do autor: não os edite, a menos que a issue peça. Se o seu código contrariar o que eles dizem, pare e diga qual trecho.

Se o que você precisa fazer contraria uma decisão do plano, não troque em silêncio: pare e diga qual decisão e por quê.

## Comandos

| Para | Comando |
|---|---|
| Preparar o ambiente | `uv sync --frozen` |
| Rodar um script | `uv run python codigo/<script>.py` |
| Autoteste de um script | `uv run python codigo/<script>.py --verificar` |
| Validar o ramo | `bash factory/checks.sh` |

Tudo roda a partir da raiz do repositório, sem interação.

## Regras duras

Quebrar qualquer uma invalida o experimento.

1. **Dados proibidos.** Nunca leia, abra, liste ou copie `dados/processados/teste.csv`, `dados/processados/sgc.csv` nem nada em `dados/brutos/`. Os três contêm as linhas do teste final. O único arquivo de dados que o código lê é `dados/processados/dev.csv`. Só `codigo/preparar_sgc.py`, que já está pronto, toca nos outros.
2. **Nunca rode o teste final.** O caminho `--final` é escrito e testado com linhas do dev. Quem o executa sobre o teste é o autor, à mão, uma única vez.
3. **Não ajuste para o resultado.** Nunca mude modelo, parâmetro, semente, faixa ou variável porque uma métrica saiu ruim. Nunca justifique uma mudança por uma métrica. Resultado ruim é resultado e vai para a monografia como saiu.
4. **Constantes congeladas.** Semente 2026; 5 partições estratificadas; 3 faixas por tercis; prior BDeu com tamanho equivalente 5; `LogisticRegression(max_iter=1000)`; erro de calibração com 10 faixas. Se a tarefa parecer exigir mudar uma delas, pare e pergunte.
5. **Toda escolha que dependa de um número é do autor.** Qual modelo usar, calibrar ou não, que valor de custo adotar: pare e pergunte. Não escolha "o melhor".
6. **Avisos não são erros.** Linhas `AVISO: ...` informam o autor. Não mexa no código para fazê-las sumir.

Parar e perguntar, na factory, é responder `STATUS: BLOCKED` com a pergunta em uma linha.

## Escopo

- Os scripts são os 7 listados no item 7 do `PLANO.md`. Não crie outro arquivo em `codigo/`, outra pasta nem outro arquivo de teste. Autoteste fica no modo `--verificar` do próprio script e não grava nada.
- **Nenhuma dependência nova.** `pyproject.toml` e `uv.lock` não mudam.
- Não edite `PLANO.md`, `AGENTS.md`, `README.md`, `dados/`, `factory/` nem `codigo/preparar_sgc.py`.
- Faça só o que a issue pede. O que ela lista como fora do escopo fica fora.
- Scripts só gravam em `resultados/`. Os arquivos gerados são commitados junto com o código.

## Convenções

- Código, comentários, mensagens e descrição do PR em português. Nomes das variáveis da base ficam em alemão, como no arquivo (`laufkont`, `hoehe`, `kredit`).
- `kredit`: 0 = ruim, 1 = bom. A classe positiva é **ruim**. Toda coluna `p_*` e `p_ruim` é a probabilidade de ruim.
- Valores categóricos e faixas são inteiros. `record_id` é retirado antes de qualquer chamada ao `pgmpy`.
- `pgmpy` é a versão 1.1.2 e a documentação do site está desatualizada: use os nomes da tabela do item 3 do `PLANO.md`. Em dúvida, consulte `help()` do objeto instalado.
- Cada arquivo abre com uma docstring: o que faz, entradas, saídas e uma linha `Uso:`. O modelo é `codigo/preparar_sgc.py`.
- Prefira código direto e legível a abstração. Sem classes, camadas ou opções de linha de comando que a issue não peça.

## Proibido no código

- `try/except` em volta de treino ou inferência.
- `fillna`, `clip` ou `nan_to_num` sobre probabilidades.
- Salvar modelo em arquivo (`pickle`, `joblib`).
- Valores de utilidade escritos no código: vêm de `config/utilidade.json`.
- Entrada inválida tem de terminar com mensagem e código de saída diferente de 0, não com resultado parcial.

## Reprodutibilidade

Rodar o mesmo comando duas vezes gera arquivos CSV e JSON idênticos byte a byte. Toda fonte de aleatoriedade usa a semente 2026.

## Pull request

O merge é automático quando o aprovador da factory aprova. O autor lê cada PR depois do merge, pela descrição, e relê todo o código antes do commit de congelamento. Por isso a descrição precisa se sustentar sozinha. Ela traz, além do que a factory já põe:

- `## O que este script faz`: 5 a 10 linhas, português simples, sem jargão não explicado. O que entra, o que sai, como a conta é feita.
- `## Como rodar`: os comandos.
- `## Avisos impressos`: as linhas `AVISO:` copiadas da execução, ou "nenhum".
