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
    <div className="p-6 space-y-6 bg-[#1B1B1B] text-[#F8F8F8] min-h-screen flex flex-col">
      <h1 className="text-4xl font-extrabold text-white">
        Performance do Cliente
      </h1>

      {price && <p>Preço atual (AAPL): {price.price.toFixed(2)}</p>}

      <ul className="space-y-2 flex-1">
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

      <div className="mt-auto">
  <button
    onClick={() => window.open("http://localhost:8000/clients/export", "_blank")}
    className="px-6 py-3 bg-[#f8f8f8] text-[#1e1e1e] font-semibold rounded hover:bg-[#5269D1] transition-colors"
  >
    Exportar clientes CSV
  </button>
</div>
    </div>
  );
}

