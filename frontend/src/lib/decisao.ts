// Utilidade esperada e limiares, com a mesma regra de codigo/decisao.py.
export type Acao = 'aprovar' | 'rejeitar' | 'analise_manual'
export type Matriz = Record<Acao, { bom: number; ruim: number }>
export type Parametros = { G: number; L: number; c: number }

// Ordem de desempate de codigo/decisao.py: a primeira vence quando as UE empatam.
export const PRIORIDADE: Acao[] = ['analise_manual', 'rejeitar', 'aprovar']
const TOLERANCIA = 1e-9

export const NOME_ACAO: Record<Acao, string> = {
  aprovar: 'Aprovar',
  rejeitar: 'Rejeitar',
  analise_manual: 'Análise manual',
}

// G = ganho do bom aprovado, L = perda do ruim aprovado, c = custo da análise manual.
export function parametrosDaMatriz(m: Matriz): Parametros {
  const p = { G: m.aprovar.bom, L: -m.aprovar.ruim, c: m.aprovar.bom - m.analise_manual.bom }
  const esperada = matrizDosParametros(p)
  for (const a of PRIORIDADE) {
    if (esperada[a].bom !== m[a].bom || esperada[a].ruim !== m[a].ruim) {
      throw new Error(`config/utilidade.json não segue a forma (G, L, c): ação ${a}`)
    }
  }
  return p
}

export function matrizDosParametros({ G, L, c }: Parametros): Matriz {
  return {
    aprovar: { bom: G, ruim: -L },
    rejeitar: { bom: 0, ruim: 0 },
    analise_manual: { bom: G - c, ruim: -c },
  }
}

export function utilidadeEsperada(p: number, m: Matriz): Record<Acao, number> {
  if (!(p >= 0 && p <= 1)) throw new Error(`P(ruim) fora de [0, 1]: ${p}`)
  const ue = {} as Record<Acao, number>
  for (const a of PRIORIDADE) ue[a] = (1 - p) * m[a].bom + p * m[a].ruim
  return ue
}

export function acaoRecomendada(p: number, m: Matriz): Acao {
  const ue = utilidadeEsperada(p, m)
  const maior = Math.max(...Object.values(ue))
  return PRIORIDADE.find((a) => ue[a] >= maior - TOLERANCIA)!
}

// Limiares em P(ruim): aprova abaixo do inferior, rejeita acima do superior,
// análise manual entre os dois. Sem faixa de análise manual, os dois coincidem.
export function limiares({ G, L, c }: Parametros): { inferior: number; superior: number } {
  const inferior = c / L
  const superior = 1 - c / G
  if (inferior < superior) return { inferior, superior }
  const corte = G / (G + L)
  return { inferior: corte, superior: corte }
}
