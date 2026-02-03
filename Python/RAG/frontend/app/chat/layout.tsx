import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/app/components/app-sidebar"

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <SidebarProvider defaultOpen={false}>
            <AppSidebar />
            <main className="relative flex flex-col flex-1 h-screen overflow-hidden bg-background">
                <header className="flex h-14 items-center gap-4 border-b px-6 bg-white/50 backdrop-blur-md">
                    <SidebarTrigger />
                    <h1 className="text-sm font-medium text-muted-foreground">Rag Application V 0.1</h1>
                </header>
                <div className="flex-1 overflow-auto">
                    {children}
                </div>
            </main>
        </SidebarProvider>
    )
}