import { Bar, BarChart, CartesianGrid, ErrorBar, ReferenceArea, ReferenceLine, ResponsiveContainer, XAxis, YAxis } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { MODELOS, NOME_MODELO, type Dados, type Metrica } from '@/lib/dados'
import { metrica } from '@/lib/formato'

// Limite de ruído para ROC-AUC fixado no PLANO.md, item 6 (60 ruins no teste).
const RUIDO_ROC = 0.03

type Chave = 'roc_auc' | 'brier' | 'ece'
const PAINEIS: { chave: Chave; titulo: string; ic: boolean; nota: string }[] = [
  { chave: 'roc_auc', titulo: 'ROC-AUC (maior é melhor)', ic: true, nota: 'Faixa cinza: 0,03 abaixo do maior valor, a margem que o plano trata como ruído.' },
  { chave: 'brier', titulo: 'Brier (menor é melhor)', ic: true, nota: '' },
  { chave: 'ece', titulo: 'Erro de calibração, ECE (menor é melhor)', ic: false, nota: 'Sem intervalo: o plano não prevê bootstrap para o ECE.' },
]

function Painel({ linhas, base, chave, titulo, ic, nota }: { linhas: Metrica[]; base?: Metrica } & (typeof PAINEIS)[number]) {
  const dados = linhas.map((m) => ({
    nome: NOME_MODELO[m.modelo],
    valor: m[chave],
    erro: ic ? [m[chave] - (m as never)[`${chave}_ic_inf`], (m as never)[`${chave}_ic_sup`] - m[chave]] : [0, 0],
  }))
  const maior = Math.max(...linhas.map((m) => m[chave]))
  return (
    <Card>
      <CardHeader><CardTitle>{titulo}</CardTitle></CardHeader>
      <CardContent>
        <div className="h-64" role="img" aria-label={`${titulo}: ${dados.map((d) => `${d.nome} ${metrica(d.valor)}`).join('; ')}`}>
          <ResponsiveContainer>
            <BarChart data={dados} margin={{ top: 16, right: 16, left: 0, bottom: 0 }}>
              <CartesianGrid vertical={false} strokeDasharray="3 3" />
              <XAxis dataKey="nome" tick={{ fontSize: 14 }} />
              <YAxis tickFormatter={metrica} tick={{ fontSize: 14 }} domain={[0, 'auto']} />
              {chave === 'roc_auc' && <ReferenceArea y1={maior - RUIDO_ROC} y2={maior} fill="#9ca3af" fillOpacity={0.35} />}
              {base && <ReferenceLine y={base[chave]} stroke="#b45309" strokeDasharray="6 4" label={{ value: `taxa base ${metrica(base[chave])}`, position: 'insideTopRight', fontSize: 13 }} />}
              <Bar dataKey="valor" fill="#2563eb" isAnimationActive={false}>
                {ic && <ErrorBar dataKey="erro" width={10} stroke="#111827" strokeWidth={2} />}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        {nota && <p className="mt-2 text-muted-foreground">{nota}</p>}
      </CardContent>
    </Card>
  )
}

export function Resultados({ dados }: { dados: Dados }) {
  const linhas = MODELOS.map((m) => dados.metricas.find((x) => x.modelo === m)!)
  const base = dados.metricas.find((x) => x.modelo === 'taxa_base')
  const rocs = linhas.map((m) => m.roc_auc)
  return (
    <div className="space-y-6">
      <p className="text-xl font-semibold">O teste não distingue os modelos pela discriminação (n = 200; 60 ruins).</p>
      <p>Barras: valor no teste. Traço: intervalo de 95% por bootstrap. Linha tracejada: taxa base.
        Maior diferença de ROC-AUC entre os modelos: {metrica(Math.max(...rocs) - Math.min(...rocs))} (limite de ruído do plano: {metrica(RUIDO_ROC)}).</p>
      <div className="grid gap-6 xl:grid-cols-3">
        {PAINEIS.map((p) => <Painel key={p.chave} linhas={linhas} base={base} {...p} />)}
      </div>
      <Card>
        <CardHeader><CardTitle>Tabela de métricas no teste</CardTitle></CardHeader>
        <CardContent className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                {['Modelo', 'ROC-AUC [IC 95%]', 'PR-AUC [IC 95%]', 'Brier [IC 95%]', 'Log loss', 'ECE'].map((h) => <TableHead key={h}>{h}</TableHead>)}
              </TableRow>
            </TableHeader>
            <TableBody>
              {[...linhas, ...(base ? [base] : [])].map((m) => (
                <TableRow key={m.modelo}>
                  <TableCell className="font-medium">{NOME_MODELO[m.modelo]}</TableCell>
                  <TableCell>{metrica(m.roc_auc)} [{metrica(m.roc_auc_ic_inf)}; {metrica(m.roc_auc_ic_sup)}]</TableCell>
                  <TableCell>{metrica(m.pr_auc)} [{metrica(m.pr_auc_ic_inf)}; {metrica(m.pr_auc_ic_sup)}]</TableCell>
                  <TableCell>{metrica(m.brier)} [{metrica(m.brier_ic_inf)}; {metrica(m.brier_ic_sup)}]</TableCell>
                  <TableCell>{metrica(m.log_loss)}</TableCell>
                  <TableCell>{metrica(m.ece)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
