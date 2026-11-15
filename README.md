# TCC: redes bayesianas e utilidade esperada

Trabalho de conclusão de curso de Rodrigo Mialichi Triboni (Engenharia de Controle e Automação, UFU).

Uma rede bayesiana estima o risco de um crédito ser ruim, e uma camada de utilidade esperada escolhe a ação (aprovar, rejeitar ou encaminhar para análise manual). O repositório é um conjunto de scripts Python que leem CSV e gravam tabelas e figuras. Não há frontend, servidor nem banco de dados.

Comece por [PLANO.md](PLANO.md). A proposta submetida está em `docs/proposta/`.

## Documentos

| Para | Leia |
|---|---|
| Pergunta, algoritmos, pastas e passos | [PLANO.md](PLANO.md) |
| Regras de quem escreve código aqui | [AGENTS.md](AGENTS.md) |
| Como os scripts se encaixam | [docs/arquitetura.md](docs/arquitetura.md) |
| O que foi decidido, por quê e por quem | [docs/decisoes.md](docs/decisoes.md) |
| O que ainda depende do autor | [docs/decisoes-pendentes.md](docs/decisoes-pendentes.md) |
| Termos e dicionário das variáveis | [docs/glossario.md](docs/glossario.md) |
| Critérios de aceite de cada script | [docs/criterios-de-aceite.md](docs/criterios-de-aceite.md) |
| Como cada resultado será lido (escrito antes dos resultados) | [docs/plano-de-analise.md](docs/plano-de-analise.md) |
| Como reproduzir os resultados | [docs/reproduzir.md](docs/reproduzir.md) |
| Referências por seção da monografia | [docs/mapa-de-referencias.md](docs/mapa-de-referencias.md) |
| Uso de IA no trabalho | [docs/uso-de-ia.md](docs/uso-de-ia.md) |

## Como rodar

```bash
uv sync --frozen
uv run python codigo/<script>.py
```

A ordem dos scripts e o que cada um grava estão em [docs/reproduzir.md](docs/reproduzir.md). Os scripts do experimento ainda estão sendo escritos; o que existe hoje é o `codigo/preparar_sgc.py`.

## Pastas

- `codigo/`: os scripts do experimento.
- `dados/`: a base South German Credit e a divisão em dev e teste. O teste final só é aberto pelo autor, uma vez.
- `resultados/`: tabelas e figuras geradas, commitadas junto com o código.
- `monografia/`: as referências e, depois, o texto.
- `docs/`: a documentação acima.
- `factory/` e `.claude/`: **ferramentas de processo**, não fazem parte do experimento. A software factory transforma cada issue em um pull request: agentes de IA escrevem o código, um script de verificação confere o resultado e o autor lê cada PR. As regras que ela segue estão no `AGENTS.md`.

Este repositório substitui os repositórios `lazylabel` e `lazylabel-v2`, que ficam como arquivo.
