"use client";

import { useEffect, useState } from "react";

export default function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<string | null>(null);

  useEffect(() => {
    
    const saved = localStorage.getItem("theme") || "light";
    setTheme(saved);

    
    document.documentElement.classList.toggle("dark", saved === "dark");
  }, []);

  if (!theme) return null; 

  return <>{children}</>;
}
