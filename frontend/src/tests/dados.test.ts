// Confere os JSON de public/data contra os CSV de origem, lidos aqui por um parser próprio.
import { readFileSync } from 'node:fs'
import path from 'node:path'
import { describe, expect, it } from 'vitest'
import { acaoRecomendada, limiares, parametrosDaMatriz, utilidadeEsperada } from '../lib/decisao'

const raiz = path.resolve(import.meta.dirname, '../../..')
const json = (nome: string) => JSON.parse(readFileSync(path.join(raiz, 'frontend/public/data', nome), 'utf8'))
function csv(nome: string): Record<string, string>[] {
  const linhas = readFileSync(path.join(raiz, 'resultados', nome), 'utf8').trim().split('\n')
  const cab = linhas[0].split(',')
  return linhas.slice(1).map((l) => Object.fromEntries(l.split(',').map((v, i) => [cab[i], v])))
}

describe('dados copiados', () => {
  it('ROC-AUC dos três modelos bate com metricas_teste.csv', () => {
    const origem = csv('metricas_teste.csv')
    for (const m of ['nb', 'tan', 'logreg']) {
      const a = json('metricas_teste.json').find((x: { modelo: string }) => x.modelo === m)
      const b = origem.find((x) => x.modelo === m)!
      expect(a.roc_auc).toBe(Number(b.roc_auc))
      expect(a.roc_auc_ic_inf).toBe(Number(b.roc_auc_ic_inf))
      expect(a.roc_auc_ic_sup).toBe(Number(b.roc_auc_ic_sup))
    }
  })

  it('diferença pareada do TAN é 22,5 [9,2; 37,2]', () => {
    const a = json('diferenca_politicas_teste.json').find((x: { modelo: string }) => x.modelo === 'tan')
    const b = csv('diferenca_politicas_teste.csv').find((x) => x.modelo === 'tan')!
    expect(a.dif_utilidade_media).toBe(Number(b.dif_utilidade_media))
    expect(a.dif_ic_inf).toBe(Number(b.dif_ic_inf))
    expect(a.dif_ic_sup).toBe(Number(b.dif_ic_sup))
    expect(a.dif_utilidade_media.toFixed(1)).toBe('22.5')
    expect(a.dif_ic_inf.toFixed(1)).toBe('9.2')
    expect(a.dif_ic_sup.toFixed(1)).toBe('37.2')
  })

  it('utilidade média do TAN bate com resumo_politicas_teste.csv (17,5 vs −5,0)', () => {
    const origem = csv('resumo_politicas_teste.csv')
    const copia = json('resumo_politicas_teste.json')
    for (const regra of ['ue', 'limiar']) {
      const a = copia.find((x: { modelo: string; regra: string }) => x.modelo === 'tan' && x.regra === regra)
      const b = origem.find((x) => x.modelo === 'tan' && x.regra === regra)!
      expect(a.utilidade_media).toBe(Number(b.utilidade_media))
    }
    expect(copia.find((x: { modelo: string; regra: string }) => x.modelo === 'tan' && x.regra === 'ue').utilidade_media).toBe(17.5)
  })

  it('predições de dev: 800 linhas, iguais ao CSV', () => {
    const a = json('predicoes_dev.json')
    const b = csv('predicoes_dev.csv')
    expect(a).toHaveLength(800)
    expect(a.map((x: { p_tan: number }) => x.p_tan)).toEqual(b.map((x) => Number(x.p_tan)))
  })
})

describe('decisão', () => {
  const matriz = json('utilidade.json').acoes

  it('limiares calculados do arquivo são 0,10 e 0,60', () => {
    const { inferior, superior } = limiares(parametrosDaMatriz(matriz))
    expect(inferior).toBeCloseTo(0.1, 12)
    expect(superior).toBeCloseTo(0.6, 12)
  })

  it('ação recomendada segue os limiares e o desempate do decisao.py', () => {
    expect(acaoRecomendada(0.05, matriz)).toBe('aprovar')
    expect(acaoRecomendada(0.3, matriz)).toBe('analise_manual')
    expect(acaoRecomendada(0.8, matriz)).toBe('rejeitar')
    // Nos limiares as UE empatam; vence análise manual.
    expect(acaoRecomendada(0.1, matriz)).toBe('analise_manual')
    expect(acaoRecomendada(0.6, matriz)).toBe('analise_manual')
    expect(utilidadeEsperada(0.3, matriz).analise_manual).toBeCloseTo(0.7 * 60 - 0.3 * 40, 12)
  })
})
