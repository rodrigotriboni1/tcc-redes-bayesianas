const fmt = (casas: number) =>
  new Intl.NumberFormat('pt-BR', { minimumFractionDigits: casas, maximumFractionDigits: casas })
const tres = fmt(3)
const uma = fmt(1)
const duas = fmt(2)
export const metrica = (v: number) => tres.format(v)
export const utilidade = (v: number) => uma.format(v)
export const prob = (v: number) => duas.format(v)
