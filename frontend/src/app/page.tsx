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

export default function ClientDetail({ params }: { params: { id: string } }) {
  const [performance, setPerformance] = useState<DailyReturn[]>([]);
  const [price, setPrice] = useState<PriceData | null>(null);
  const token = localStorage.getItem("token") ?? "";

  useEffect(() => {
    async function fetchPerformance() {
      const res = await fetch(`http://localhost:8000/clients/${params.id}/performance`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setPerformance(data);
    }
    if (token) fetchPerformance();
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
        {performance.map((p) => (
          <li key={p.date}>
            {new Date(p.date).toLocaleDateString()}: {p.value.toFixed(2)}
          </li>
        ))}
        {performance.length === 0 && <li>Nenhum dado de performance encontrado.</li>}
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
