import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Football Edge Analyzer",
  description: "Analise odds, EV e oportunidades de futebol.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
