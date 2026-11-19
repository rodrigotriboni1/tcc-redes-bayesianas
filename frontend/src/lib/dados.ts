import { useEffect, useState } from 'react'
import type { Matriz } from './decisao'

export type Metrica = {
  modelo: string
  roc_auc: number; roc_auc_ic_inf: number; roc_auc_ic_sup: number
  pr_auc: number; pr_auc_ic_inf: number; pr_auc_ic_sup: number
  brier: number; brier_ic_inf: number; brier_ic_sup: number
  log_loss: number; ece: number
}
export type Diferenca = { modelo: string; dif_utilidade_media: number; dif_ic_inf: number; dif_ic_sup: number }
export type Resumo = {
  modelo: string; regra: 'ue' | 'limiar'; utilidade_media: number
  n_aprovar: number; n_rejeitar: number; n_analise_manual: number; n_mudam_vs_outra_regra: number
  utilidade_media_ic_inf: number; utilidade_media_ic_sup: number
}
export type PredicaoDev = { record_id: string; kredit: number; fold: number; p_nb: number; p_tan: number; p_logreg: number }
export type Dados = {
  metricas: Metrica[]
  diferencas: Diferenca[]
  resumo: Resumo[]
  utilidade: { acoes: Matriz; hipoteses: string }
  predicoes: PredicaoDev[]
}

// TAN é o modelo principal; a ordem de exibição segue o texto.
export const MODELOS = ['tan', 'nb', 'logreg'] as const
export type Modelo = (typeof MODELOS)[number]
export const NOME_MODELO: Record<string, string> = {
  tan: 'TAN', nb: 'Naive Bayes', logreg: 'Regressão logística', taxa_base: 'Taxa base',
}

const buscar = (nome: string) =>
  fetch(`${import.meta.env.BASE_URL}data/${nome}.json`).then((r) => {
    if (!r.ok) throw new Error(`falha ao ler data/${nome}.json (${r.status})`)
    return r.json()
  })

export function useDados() {
  const [estado, setEstado] = useState<{ dados?: Dados; erro?: string }>({})
  useEffect(() => {
    Promise.all(['metricas_teste', 'diferenca_politicas_teste', 'resumo_politicas_teste', 'utilidade', 'predicoes_dev'].map(buscar))
      .then(([metricas, diferencas, resumo, utilidade, predicoes]) =>
        setEstado({ dados: { metricas, diferencas, resumo, utilidade, predicoes } }))
      .catch((e: Error) => setEstado({ erro: e.message }))
  }, [])
  return estado
}
