import { useState } from 'react'
import { Sidebar, SidebarContent, SidebarGroup, SidebarHeader, SidebarInset, SidebarMenu, SidebarMenuButton, SidebarMenuItem, SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { useDados } from '@/lib/dados'
import { Caso } from '@/telas/Caso'
import { Limiares } from '@/telas/Limiares'
import { Politicas } from '@/telas/Politicas'
import { Resultados } from '@/telas/Resultados'

const TELAS = [
  { titulo: 'Resultados do teste', Tela: Resultados },
  { titulo: 'Limiares e utilidade esperada', Tela: Limiares },
  { titulo: 'Política de 3 ações vs corte 0,5', Tela: Politicas },
  { titulo: 'Um caso', Tela: Caso },
]

export default function App() {
  const [atual, setAtual] = useState(0)
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
