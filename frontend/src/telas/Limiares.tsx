import { useState } from 'react'
import { CartesianGrid, Legend, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Slider } from '@/components/ui/slider'
import type { Dados } from '@/lib/dados'
import { limiares, matrizDosParametros, NOME_ACAO, parametrosDaMatriz, PRIORIDADE, utilidadeEsperada, type Parametros } from '@/lib/decisao'
import { prob, utilidade } from '@/lib/formato'
import { Ressalvas } from './Ressalvas'

export const COR_ACAO = { aprovar: '#15803d', rejeitar: '#b91c1c', analise_manual: '#1d4ed8' } as const

const CONTROLES: { chave: keyof Parametros; rotulo: string }[] = [
  { chave: 'G', rotulo: 'G: ganho ao aprovar um bom' },
  { chave: 'L', rotulo: 'L: perda ao aprovar um ruim' },
  { chave: 'c', rotulo: 'c: custo da análise manual' },
]

export function Limiares({ dados }: { dados: Dados }) {
  const doArquivo = parametrosDaMatriz(dados.utilidade.acoes)
  const [p, setP] = useState(doArquivo)
  const matriz = matrizDosParametros(p)
  const { inferior, superior } = limiares(p)
  const pontos = Array.from({ length: 101 }, (_, i) => ({ p: i / 100, ...utilidadeEsperada(i / 100, matriz) }))
  // Faixa dos sliders: até 2x o maior valor do arquivo, para não fixar números no código.
  const teto = 2 * Math.max(doArquivo.G, doArquivo.L, doArquivo.c)
  return (
    <div className="space-y-6">
      <Ressalvas />
      <p>UE(a) = (1 − p)·U(a, bom) + p·U(a, ruim), com p = P(ruim). A ação escolhida é a de maior UE.</p>
      <div className="grid gap-6 xl:grid-cols-[2fr_1fr]">
        <Card>
          <CardHeader><CardTitle>Utilidade esperada por ação</CardTitle></CardHeader>
          <CardContent>
            <div className="h-96" role="img" aria-label={`Retas de utilidade esperada. Limiar inferior ${prob(inferior)}, superior ${prob(superior)}.`}>
              <ResponsiveContainer>
                <LineChart data={pontos} margin={{ top: 24, right: 24, left: 8, bottom: 16 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="p" type="number" domain={[0, 1]} tickFormatter={prob} tick={{ fontSize: 14 }}
                    label={{ value: 'P(ruim)', position: 'insideBottom', offset: -8 }} />
                  <YAxis tickFormatter={utilidade} tick={{ fontSize: 14 }} />
                  <Tooltip formatter={(v) => utilidade(Number(v))} labelFormatter={(v) => `P(ruim) = ${prob(Number(v))}`} />
                  <Legend verticalAlign="top" />
                  {PRIORIDADE.map((a) => (
                    <Line key={a} dataKey={a} name={NOME_ACAO[a]} stroke={COR_ACAO[a]} strokeWidth={3} dot={false} isAnimationActive={false} />
                  ))}
                  <ReferenceLine x={inferior} stroke="#111827" strokeDasharray="6 4" label={{ value: prob(inferior), position: 'top' }} />
                  {superior !== inferior && <ReferenceLine x={superior} stroke="#111827" strokeDasharray="6 4" label={{ value: prob(superior), position: 'top' }} />}
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Parâmetros da matriz</CardTitle></CardHeader>
          <CardContent className="space-y-6">
            {CONTROLES.map(({ chave, rotulo }) => (
              <div key={chave} className="space-y-2">
                <div className="flex justify-between"><span id={`rotulo-${chave}`}>{rotulo}</span><span className="font-mono">{p[chave]}</span></div>
                <Slider aria-labelledby={`rotulo-${chave}`} min={5} max={teto} step={5} value={[p[chave]]}
                  onValueChange={(v) => setP({ ...p, [chave]: Array.isArray(v) ? v[0] : v })} />
              </div>
            ))}
            <div className="rounded-md bg-muted p-3 text-lg">
              {superior !== inferior ? (
                <>Aprovar se P(ruim) &lt; <b>{prob(inferior)}</b> (c/L); rejeitar se &gt; <b>{prob(superior)}</b> (1 − c/G); análise manual entre os dois.</>
              ) : (
                <>Sem faixa de análise manual: aprovar se P(ruim) &lt; <b>{prob(inferior)}</b>, senão rejeitar.</>
              )}
            </div>
            <Button variant="outline" onClick={() => setP(doArquivo)}>Restaurar valores do arquivo</Button>
            <p className="text-muted-foreground">Arquivo: G = {doArquivo.G}, L = {doArquivo.L}, c = {doArquivo.c} (config/utilidade.json). Mudar os sliders não altera o experimento.</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
