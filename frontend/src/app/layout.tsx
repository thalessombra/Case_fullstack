import Link from "next/link";// layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="bg-gray-50 text-gray-900">
        <div className="flex min-h-screen">
          {/* Sidebar / Navegação */}
          <aside className="border-r bg-white p-4 space-y-2">
            <nav className="flex flex-col gap-2">
              <Link className="px-3 py-2 rounded-lg hover:bg-gray-100" href="/">Home</Link>
              <Link className="px-3 py-2 rounded-lg hover:bg-gray-100" href="/clients">Clientes</Link>
            </nav>
          </aside>

          {/* Main */}
          <main className="p-4 md:p-6">{children}</main>
        </div>
      </body>
    </html>
  )
}
