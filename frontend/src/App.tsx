import { useEffect, useState } from 'react'
import { Sidebar, SidebarContent, SidebarGroup, SidebarHeader, SidebarInset, SidebarMenu, SidebarMenuButton, SidebarMenuItem, SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { useDados } from '@/lib/dados'
import { Caso } from '@/telas/Caso'
import { Limiares } from '@/telas/Limiares'
import { Politicas } from '@/telas/Politicas'
import { Resultados } from '@/telas/Resultados'

const TELAS = [
  { hash: '#/resultados', titulo: 'Resultados do teste', Tela: Resultados },
  { hash: '#/limiares', titulo: 'Limiares e utilidade esperada', Tela: Limiares },
  { hash: '#/politicas', titulo: 'Política de 3 ações vs corte 0,5', Tela: Politicas },
  { hash: '#/caso', titulo: 'Um caso', Tela: Caso },
]

export default function App() {
  // A tela atual fica no hash da URL (#/limiares etc.), para links diretos.
  const daUrl = () => Math.max(0, TELAS.findIndex((t) => t.hash === window.location.hash))
  const [atual, setAtualEstado] = useState(daUrl)
  useEffect(() => {
    const ouvir = () => setAtualEstado(daUrl())
    window.addEventListener('hashchange', ouvir)
    return () => window.removeEventListener('hashchange', ouvir)
  }, [])
  const setAtual = (i: number) => { window.location.hash = TELAS[i].hash }
  const { dados, erro } = useDados()
  const { titulo, Tela } = TELAS[atual]
  return (
    <SidebarProvider>
      <Sidebar>
        <SidebarHeader className="px-4 py-3 text-lg font-semibold">Painel do TCC</SidebarHeader>
        <SidebarContent>
          <SidebarGroup>
            <SidebarMenu>
              {TELAS.map((t, i) => (
                <SidebarMenuItem key={t.titulo}>
                  <SidebarMenuButton isActive={i === atual} aria-current={i === atual ? 'page' : undefined}
                    onClick={() => setAtual(i)} className="h-auto py-2 text-base">{i + 1}. {t.titulo}</SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroup>
          <p className="px-4 text-sm text-muted-foreground">Somente leitura: exibe os arquivos de resultados/ e config/.</p>
        </SidebarContent>
      </Sidebar>
      <SidebarInset>
        <header className="flex items-center gap-3 border-b px-6 py-4">
          <SidebarTrigger aria-label="Mostrar ou ocultar o menu" />
          <h1 className="text-2xl font-bold">{titulo}</h1>
        </header>
        <main className="p-6">
          {erro && <p role="alert" className="text-destructive">Erro ao carregar os dados: {erro}</p>}
          {!dados && !erro && <p>Carregando dados…</p>}
          {dados && <Tela dados={dados} />}
        </main>
      </SidebarInset>
    </SidebarProvider>
  )
}
