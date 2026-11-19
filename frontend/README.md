# Painel do TCC (somente leitura)

Painel web para a defesa. Lê os arquivos já gerados em `resultados/` e `config/` e os exibe em quatro telas: resultados do teste, limiares e utilidade esperada, política de 3 ações vs corte 0,5, e um caso do desenvolvimento.

**Somente leitura:** não roda o experimento, não grava em `resultados/` nem altera nenhum número. Do teste, usa só os agregados.

```bash
cd frontend && npm install
npm run dev       # servidor de desenvolvimento
npm run build     # site estático em dist/
npm run preview   # serve dist/ (funciona offline)
npm test          # confere os dados copiados contra os CSV
```

`npm run dados` (rodado antes de `dev`, `build` e `test`) converte os CSV/JSON para `public/data/`.
