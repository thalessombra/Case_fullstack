import type { Metadata } from "next";
import "./globals.css";
import  ThemeProvider  from "../components/themeprovider"

export const metadata: Metadata = {
  title: "Meu App",
  description: "Frontend do Case Fullstack",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      
      <body>
        <ThemeProvider>
          <div className="flex min-h-screen">
            <aside className="border-r border-sidebar-border bg-sidebar p-4 space-y-2">
           
            </aside>
            <main className="flex-1 p-4">{children}</main>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
