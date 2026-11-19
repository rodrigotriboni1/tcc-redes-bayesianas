// Copia os resultados do experimento (CSV/JSON) para public/data/ em JSON.
// Só lê agregados do teste; nunca lê predições linha a linha do teste.
// Uso: node scripts/copiar-dados.mjs
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
const destino = path.resolve(raiz, 'frontend/public/data')

// Os CSV do experimento não têm aspas nem vírgulas dentro de campos.
export function lerCsv(arquivo) {
  const [cab, ...linhas] = readFileSync(arquivo, 'utf8').trim().split(/\r?\n/)
  const colunas = cab.split(',')
  return linhas.map((l) => {
    const v = l.split(',')
    if (v.length !== colunas.length) throw new Error(`${arquivo}: linha com ${v.length} campos: ${l}`)
    return Object.fromEntries(colunas.map((c, i) => [c, v[i] !== '' && !isNaN(Number(v[i])) ? Number(v[i]) : v[i]]))
  })
}

mkdirSync(destino, { recursive: true })
const gravar = (nome, dados) => writeFileSync(path.join(destino, nome), JSON.stringify(dados))
const csv = (nome) => lerCsv(path.join(raiz, 'resultados', nome))

for (const nome of ['metricas_teste', 'diferenca_politicas_teste', 'resumo_politicas_teste', 'predicoes_dev']) {
  gravar(`${nome}.json`, csv(`${nome}.csv`))
}
gravar('utilidade.json', JSON.parse(readFileSync(path.join(raiz, 'config/utilidade.json'), 'utf8')))
gravar('cortes.json', JSON.parse(readFileSync(path.join(raiz, 'resultados/cortes.json'), 'utf8')))
console.log(`dados copiados para ${destino}`)
