export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export type TokenResponse = {
  access_token: string;
  token_type: string; 
};

export async function login(username: string, password: string): Promise<TokenResponse> {
  const body = new URLSearchParams({ username, password });

  const res = await fetch(`${API_BASE}/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }
  return res.json();
}

export async function getClients(token: string) {
  const res = await fetch(`${API_BASE}/clients/`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(await res.text());
  }
  return res.json() as Promise<Array<{ id: number; name: string; email: string; is_active: boolean }>>;
}
