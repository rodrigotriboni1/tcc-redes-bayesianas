import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, XAxis, YAxis } from 'recharts'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { MODELOS, NOME_MODELO, type Dados } from '@/lib/dados'
import { NOME_ACAO } from '@/lib/decisao'
import { utilidade } from '@/lib/formato'
import { COR_ACAO } from './Limiares'
import { Ressalvas } from './Ressalvas'

const NOME_REGRA = { ue: 'Três ações (utilidade esperada)', limiar: 'Corte fixo 0,5' } as const
const ic = (inf: number, sup: number) => `[${utilidade(inf)}; ${utilidade(sup)}]`

export function Politicas({ dados }: { dados: Dados }) {
  return (
    <div className="space-y-6">
      <Ressalvas />
      <p>Utilidade média por cliente no teste (n = 200) para cada regra, com intervalo de 95% por bootstrap, e a diferença pareada (três ações − corte 0,5).</p>
      <div className="grid gap-6 xl:grid-cols-3">
        {MODELOS.map((modelo) => {
          const linhas = (['ue', 'limiar'] as const).map((r) => dados.resumo.find((x) => x.modelo === modelo && x.regra === r)!)
          const dif = dados.diferencas.find((x) => x.modelo === modelo)!
          const barras = linhas.map((l) => ({
            regra: l.regra === 'ue' ? 'Três ações' : 'Corte 0,5',
            aprovar: l.n_aprovar, rejeitar: l.n_rejeitar, analise_manual: l.n_analise_manual,
          }))
          const principal = modelo === 'tan'
          return (
            <Card key={modelo} className={principal ? 'ring-2 ring-primary' : ''}>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">{NOME_MODELO[modelo]} {principal && <Badge>principal</Badge>}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <dl className="space-y-2">
                  {linhas.map((l) => (
                    <div key={l.regra}>
                      <dt className="text-muted-foreground">{NOME_REGRA[l.regra]}</dt>
                      <dd className="text-2xl font-semibold">{utilidade(l.utilidade_media)} <span className="text-base font-normal">{ic(l.utilidade_media_ic_inf, l.utilidade_media_ic_sup)}</span></dd>
                    </div>
                  ))}
                  <div>
                    <dt className="text-muted-foreground">Diferença pareada</dt>
                    <dd className="text-2xl font-semibold">{utilidade(dif.dif_utilidade_media)} <span className="text-base font-normal">{ic(dif.dif_ic_inf, dif.dif_ic_sup)}</span></dd>
                  </div>
                </dl>
                <div className="h-56" role="img" aria-label={`Contagem de ações: ${barras.map((b) => `${b.regra}: aprovar ${b.aprovar}, rejeitar ${b.rejeitar}, análise manual ${b.analise_manual}`).join('; ')}`}>
                  <ResponsiveContainer>
                    <BarChart data={barras} layout="vertical" margin={{ left: 16, right: 16 }}>
                      <CartesianGrid horizontal={false} strokeDasharray="3 3" />
                      <XAxis type="number" tick={{ fontSize: 14 }} />
                      <YAxis type="category" dataKey="regra" width={90} tick={{ fontSize: 14 }} />
                      <Legend />
                      {(['aprovar', 'analise_manual', 'rejeitar'] as const).map((a) => (
                        <Bar key={a} dataKey={a} name={NOME_ACAO[a]} stackId="acoes" fill={COR_ACAO[a]} isAnimationActive={false}
                          label={{ position: 'center', fill: '#fff', fontSize: 13 }} />
                      ))}
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <p className="text-muted-foreground">Casos com ação diferente entre as regras: {linhas[0].n_mudam_vs_outra_regra}.</p>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
