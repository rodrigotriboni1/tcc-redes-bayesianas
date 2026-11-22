# Ferramentas para gerar os slides da defesa

Os slides anteriores foram removidos do repositório e serão refeitos. Ficam aqui só as ferramentas e a documentação:

- `build.js`: gerador (pptxgenjs 4.0.1). Lê `../roteiro-defesa.md` e os valores de `resultados/*.csv` e falha se algum número divergir do roteiro. Grava `Defesa_TCC_Rodrigo_rascunho.pptx` nesta pasta, que não é versionado.
- `verify.py`: conferência estrutural de um `.pptx` (contagem de slides, fontes, limites, palavras proibidas).
- `explicacao-da-apresentacao.md`: explicação dos slides anteriores, a rever junto com os novos.

Para gerar e conferir, a partir da raiz do repositório:

```bash
NODE_PATH=$HOME/.local/node_modules node monografia/defesa/build.js
python3 monografia/defesa/verify.py monografia/defesa/Defesa_TCC_Rodrigo_rascunho.pptx
```

O arquivo gerado não é renderizado pelo script: quebras de linha, sobreposições e legibilidade das figuras só aparecem ao abrir no PowerPoint ou no Keynote. Os campos em amarelo (titulação do orientador, data e local, e-mail e link do repositório) são do autor. O `build.js` gera os slides com as etiquetas de arquivo; tirá-las é um passo manual depois.
