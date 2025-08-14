
"use client";

import { useEffect, useState } from "react";

interface DailyReturn {
  date: string;
  value: number;
}

interface PriceData {
  symbol: string;
  price: number;
}

interface ClientDetailProps {
  params: {
    id: string;
  };
}

export default function ClientDetail({ params }: ClientDetailProps) {
  const [performance, setPerformance] = useState<DailyReturn[]>([]);
  const [price, setPrice] = useState<PriceData | null>(null);

  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") ?? "" : "";

  useEffect(() => {
    if (!token) return;

    async function fetchPerformance() {
      try {
        const res = await fetch(
          `http://localhost:8000/clients/${params.id}/performance`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        if (!res.ok) throw new Error("Falha ao carregar performance");

        const data: DailyReturn[] = await res.json();
        setPerformance(data);
      } catch (err) {
        console.error(err);
        setPerformance([]);
      }
    }

    fetchPerformance();
  }, [params.id, token]);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/prices/AAPL`);

    ws.onmessage = (event) => {
      const data: PriceData = JSON.parse(event.data);
      setPrice(data);
    };

    return () => ws.close();
  }, []);

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">Performance do Cliente</h1>

      {price && <p>Preço atual (AAPL): {price.price.toFixed(2)}</p>}

      <ul>
        {performance.length > 0 ? (
          performance.map((p) => (
            <li key={p.date}>
              {new Date(p.date).toLocaleDateString()}: {p.value.toFixed(2)}
            </li>
          ))
        ) : (
          <li>Nenhum dado de performance encontrado.</li>
        )}
      </ul>

      <a
        href="http://localhost:8000/clients/export"
        className="px-4 py-2 bg-black text-white rounded hover:bg-gray-800"
        target="_blank"
        rel="noopener noreferrer"
      >
        Exportar clientes CSV
      </a>
    </div>
  );
}
