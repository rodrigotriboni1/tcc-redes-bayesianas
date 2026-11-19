import { Bar, BarChart, CartesianGrid, ReferenceArea, ReferenceLine, ResponsiveContainer, XAxis, YAxis } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { MODELOS, NOME_MODELO, type Dados, type Metrica } from '@/lib/dados'
import { metrica } from '@/lib/formato'

// Limite de ruído para ROC-AUC fixado no PLANO.md, item 6 (60 ruins no teste).
const RUIDO_ROC = 0.03

type Chave = 'roc_auc' | 'brier' | 'ece'
const NOME_CURTO: Record<string, string> = { tan: 'TAN', nb: 'NB', logreg: 'Logística' }
// TAN (principal) em azul claro; NB e logística em azul escuro, como nos slides.
const COR = (modelo: string) => (modelo === 'tan' ? '#60a5fa' : '#1e3a8a')

const PAINEIS: { chave: Chave; titulo: string; ic: boolean; nota: string }[] = [
  { chave: 'roc_auc', titulo: 'ROC-AUC (maior é melhor)', ic: true, nota: 'Eixo começa na taxa base 0,5. Faixa cinza: 0,03 abaixo do maior valor, a margem que o plano trata como ruído.' },
  { chave: 'brier', titulo: 'Brier (menor é melhor)', ic: true, nota: '' },
  { chave: 'ece', titulo: 'Erro de calibração, ECE (menor é melhor)', ic: false, nota: 'Sem intervalo: o plano não prevê bootstrap para o ECE.' },
]

function Painel({ linhas, base, chave, titulo, ic, nota }: { linhas: Metrica[]; base?: Metrica } & (typeof PAINEIS)[number]) {
  const dados = linhas.map((m) => ({
    nome: NOME_CURTO[m.modelo],
    modelo: m.modelo,
    valor: m[chave],
    inf: ic ? (m as never)[`${chave}_ic_inf`] as number : undefined,
    sup: ic ? (m as never)[`${chave}_ic_sup`] as number : undefined,
  }))
  const maior = Math.max(...linhas.map((m) => m[chave]))
  const roc = chave === 'roc_auc'
  // ECE da taxa base é zero por construção e não serve de referência.
  const ref = base && chave !== 'ece' ? base[chave] : undefined
  const minimo = roc && ref !== undefined ? ref : 0
  // Barra com o intervalo de 95% desenhado por cima (linha de 3px com tampas).
  // A escala vem da própria barra: a base dela é o início do eixo (minimo).
  const barraComIc = (props: { x?: number; y?: number; width?: number; height?: number; payload?: (typeof dados)[number] }) => {
    const { x = 0, y = 0, width = 0, height = 0, payload } = props
    if (!payload) return <g />
    const base0 = y + height
    const k = height / (payload.valor - minimo)
    const py = (v: number) => base0 - (v - minimo) * k
    const cx = x + width / 2
    return (
      <g>
        <rect x={x} y={y} width={width} height={height} fill={COR(payload.modelo)} />
        {payload.inf !== undefined && payload.sup !== undefined && (
          <g stroke="#c2410c" strokeWidth={3}>
            <line x1={cx} x2={cx} y1={py(payload.inf)} y2={py(payload.sup)} />
            <line x1={cx - 10} x2={cx + 10} y1={py(payload.inf)} y2={py(payload.inf)} />
            <line x1={cx - 10} x2={cx + 10} y1={py(payload.sup)} y2={py(payload.sup)} />
          </g>
        )}
      </g>
    )
  }
  return (
    <Card>
      <CardHeader><CardTitle>{titulo}</CardTitle></CardHeader>
      <CardContent>
        <div className="h-64" role="img" aria-label={`${titulo}: ${dados.map((d) => `${d.nome} ${metrica(d.valor)}`).join('; ')}`}>
          <ResponsiveContainer>
            <BarChart data={dados} margin={{ top: 16, right: 16, left: 0, bottom: 0 }}>
              <CartesianGrid vertical={false} strokeDasharray="3 3" />
              <XAxis dataKey="nome" interval={0} tick={{ fontSize: 14 }} />
              <YAxis tickFormatter={metrica} tick={{ fontSize: 14 }} domain={roc ? [minimo, 1] : [0, (max: number) => Math.ceil(20 * Math.max(max, ...dados.map((d) => d.sup ?? 0))) / 20]} allowDataOverflow />
              {roc && <ReferenceArea y1={maior - RUIDO_ROC} y2={maior} fill="#9ca3af" fillOpacity={0.35} />}
              {ref !== undefined && !roc && <ReferenceLine y={ref} stroke="#b45309" strokeWidth={2} strokeDasharray="6 4" />}
              <Bar dataKey="valor" isAnimationActive={false} shape={barraComIc} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        {ref !== undefined && !roc && <p className="mt-2"><span className="font-semibold text-amber-700 dark:text-amber-400">- - -</span> taxa base: {metrica(ref)}</p>}
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
      <p>Barras: valor no teste (TAN, principal, em azul claro). Traço laranja com tampas: intervalo de 95% por bootstrap. Linha tracejada: taxa base.
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
