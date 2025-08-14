"use client"

import { useEffect, useState } from "react"
import { login, getClients } from "@/lib/api"

type Client = { id: number; name: string; email: string; is_active: boolean }

export default function ClientsPage() {
  const [username, setUsername] = useState("admin")
  const [password, setPassword] = useState("Suasenha123")
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [clients, setClients] = useState<Client[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const t = localStorage.getItem("token")
    if (t) setToken(t)
  }, [])

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const data = await login(username, password)
      localStorage.setItem("token", data.access_token)
      setToken(data.access_token)
    } catch (err: unknown) {
      if (err instanceof Error) console.log(err.message)
      else console.log(err)
    } finally {
      setLoading(false)
    }
  }

  async function loadClients() {
    if (!token) return
    setLoading(true)
    setError(null)
    try {
      const list = await getClients(token)
      setClients(list)
    } catch (err: unknown) {
      if (err instanceof Error) console.log(err.message)
      else console.log(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (token) loadClients()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token])

  return (
    <div className="space-y-6">
      {/* Autenticação */}
      <div className="rounded-xl border bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold mb-3">Autenticação</h2>
        <form onSubmit={handleLogin} className="flex flex-wrap items-end gap-3">
          <div className="flex flex-col">
            <label className="text-sm mb-1">Usuário</label>
            <input
              className="border rounded-lg px-3 py-2"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="username"
            />
          </div>
          <div className="flex flex-col">
            <label className="text-sm mb-1">Senha</label>
            <input
              className="border rounded-lg px-3 py-2"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 rounded-lg bg-black text-white disabled:opacity-50"
            disabled={loading}
          >
            {loading ? "Entrando..." : "Entrar"}
          </button>

          {token && (
            <button
              type="button"
              onClick={loadClients}
              className="px-4 py-2 rounded-lg border"
              disabled={loading}
            >
              Recarregar clientes
            </button>
          )}

          {token && (
            <span className="text-xs text-green-700 bg-green-50 border border-green-200 rounded px-2 py-1">
              Token carregado
            </span>
          )}
        </form>

        {error && (
          <p className="mt-3 text-sm text-red-700 bg-red-50 border border-red-200 rounded px-3 py-2">
            {error}
          </p>
        )}
      </div>

      {/* Listagem de clientes */}
      <div className="rounded-xl border bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold mb-3">Clientes</h2>

        <div className="overflow-x-auto">
          <table className="min-w-full border rounded-lg overflow-hidden">
            <thead className="bg-gray-100">
              <tr>
                <th className="text-left px-3 py-2 border-b">ID</th>
                <th className="text-left px-3 py-2 border-b">Nome</th>
                <th className="text-left px-3 py-2 border-b">Email</th>
                <th className="text-left px-3 py-2 border-b">Ativo</th>
                <th className="text-left px-3 py-2 border-b">Detalhes</th>
              </tr>
            </thead>
            <tbody>
              {clients.map((c) => (
                <tr key={c.id} className="odd:bg-white even:bg-gray-50">
                  <td className="px-3 py-2 border-b">{c.id}</td>
                  <td className="px-3 py-2 border-b">{c.name}</td>
                  <td className="px-3 py-2 border-b">{c.email}</td>
                  <td className="px-3 py-2 border-b">{c.is_active ? "Sim" : "Não"}</td>
                  <td className="px-3 py-2 border-b">
                    <a
                      className="text-blue-500 hover:underline"
                      href={`/clients/${c.id}`}
                    >
                      Ver detalhes
                    </a>
                  </td>
                </tr>
              ))}
              {clients.length === 0 && (
                <tr>
                  <td className="px-3 py-6 text-center text-sm text-gray-500" colSpan={5}>
                    {token ? "Nenhum cliente encontrado." : "Autentique para listar clientes."}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
