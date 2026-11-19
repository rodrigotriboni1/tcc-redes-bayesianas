import { useState } from 'react'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { MODELOS, NOME_MODELO, type Dados, type Modelo } from '@/lib/dados'
import { acaoRecomendada, NOME_ACAO, PRIORIDADE, utilidadeEsperada } from '@/lib/decisao'
import { metrica, utilidade } from '@/lib/formato'
import { Ressalvas } from './Ressalvas'

export function Caso({ dados }: { dados: Dados }) {
  const [id, setId] = useState(dados.predicoes[0].record_id)
  const [modelo, setModelo] = useState<Modelo>('tan')
  const caso = dados.predicoes.find((x) => x.record_id === id)!
  const matriz = dados.utilidade.acoes
  const p = caso[`p_${modelo}`]
  const ue = utilidadeEsperada(p, matriz)
  const acao = acaoRecomendada(p, matriz)
  return (
    <div className="space-y-6">
      <p role="note" className="rounded-md border-l-4 border-sky-700 bg-sky-50 px-4 py-2 font-medium text-sky-950 dark:bg-sky-950 dark:text-sky-50">
        Ilustração com dados de desenvolvimento; não é o teste.
      </p>
      <Ressalvas />
      <div className="flex flex-wrap gap-6">
        <label className="space-y-1">
          <span className="block">Caso (record_id)</span>
          {/* Lista nativa: 800 opções, busca por digitação, acessível por teclado. */}
          <select value={id} onChange={(e) => setId(e.target.value)}
            className="h-10 rounded-md border bg-background px-3 font-mono focus-visible:outline-2 focus-visible:outline-ring">
            {dados.predicoes.map((x) => <option key={x.record_id} value={x.record_id}>{x.record_id}</option>)}
          </select>
        </label>
        <div className="space-y-1">
          <span id="rotulo-modelo" className="block">Modelo</span>
          <Select value={modelo} onValueChange={(v) => setModelo(v as Modelo)}>
            <SelectTrigger aria-labelledby="rotulo-modelo" className="h-10 min-w-56"><SelectValue>{NOME_MODELO[modelo]}</SelectValue></SelectTrigger>
            <SelectContent>
              {MODELOS.map((m) => <SelectItem key={m} value={m}>{NOME_MODELO[m]}</SelectItem>)}
            </SelectContent>
          </Select>
        </div>
      </div>
      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>{caso.record_id}</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <p>Classe real (kredit): <b>{caso.kredit === 1 ? 'bom (1)' : 'ruim (0)'}</b> · partição: <b>{caso.fold}</b></p>
            <Table>
              <TableHeader><TableRow><TableHead>Modelo</TableHead><TableHead>P(ruim)</TableHead></TableRow></TableHeader>
              <TableBody>
                {MODELOS.map((m) => (
                  <TableRow key={m} className={m === modelo ? 'bg-muted font-semibold' : ''}>
                    <TableCell>{NOME_MODELO[m]}</TableCell><TableCell>{metrica(caso[`p_${m}`])}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Decisão com {NOME_MODELO[modelo]} (P(ruim) = {metrica(p)})</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <Table>
              <TableHeader><TableRow><TableHead>Ação</TableHead><TableHead>Utilidade esperada</TableHead></TableRow></TableHeader>
              <TableBody>
                {PRIORIDADE.map((a) => (
                  <TableRow key={a} className={a === acao ? 'bg-muted font-semibold' : ''}>
                    <TableCell>{NOME_ACAO[a]}</TableCell><TableCell>{utilidade(ue[a])}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            <p className="text-xl">Ação recomendada: <Badge className="text-lg">{NOME_ACAO[acao]}</Badge></p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
