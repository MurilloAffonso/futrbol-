const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      ...(init?.headers || {}),
    },
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `HTTP ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export type ValueBetRequest = {
  market: string;
  selection: string;
  offered_odd: number;
  model_probability: number;
  confidence_score: number;
};

export const api = {
  health: () => request<{ status: string }>("/health"),
  analyzeValueBet: (payload: ValueBetRequest) =>
    request<any>("/analysis/value-bet", {
      method: "POST",
      body: JSON.stringify(payload),
      headers: { "Content-Type": "application/json" },
    }),
  runBacktest: (bets: Array<{ odd: number; model_probability: number; result: "win" | "loss" }>) =>
    request<any>("/analysis/backtest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ bets }),
    }),
  importFlashscoreJson: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<any>("/import/flashscore-json", { method: "POST", body: form });
  },
  getValueBets: () => request<any[]>("/value-bets"),
};
