# Slides da defesa (rascunho)

- `Defesa_TCC_Rodrigo_rascunho.pptx`: 24 slides (14 de corpo e 10 de apêndice), gerados a partir de `../roteiro-defesa.md`.
- `build.js`: gerador (pptxgenjs 4.0.1). Lê os valores de `resultados/*.csv` e falha se algum número divergir do roteiro.
- `verify.py`: conferência estrutural do `.pptx` (contagem de slides, fontes, limites, palavras proibidas).

Para regenerar, a partir da raiz do repositório:

```bash
NODE_PATH=$HOME/.local/node_modules node monografia/defesa/build.js
python3 monografia/defesa/verify.py monografia/defesa/Defesa_TCC_Rodrigo_rascunho.pptx
```

O arquivo **não foi renderizado**: quebras de linha, sobreposições e legibilidade das figuras só aparecem ao abrir no PowerPoint ou no Keynote. Os campos em amarelo (titulação do orientador, data e local, e-mail e link do repositório) são do autor.

O .pptx final foi pós-processado para tirar as etiquetas de arquivo; build.js regenera a versão anterior, com as etiquetas.
