// frontend/src/app/layout.tsx
import React from "react";
import Link from "next/link";
import "./globals.css";

export const metadata = {
  title: "Case Fullstack",
  description: "Projeto Fullstack Next.js + FastAPI",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-br">
      <body className="flex min-h-screen bg-gray-50">
        {/* Sidebar */}
        <aside className="w-64 border-r bg-white p-4 space-y-2">
          <nav className="flex flex-col gap-2">
            <Link
              href="/"
              className="px-3 py-2 rounded-lg hover:bg-gray-100"
            >
              Home
            </Link>
            <Link
              href="/clients"
              className="px-3 py-2 rounded-lg hover:bg-gray-100"
            >
              Clientes
            </Link>
          </nav>
        </aside>

        {/* Conteúdo principal */}
        <main className="flex-1 p-6">{children}</main>
      </body>
    </html>
  );
}
