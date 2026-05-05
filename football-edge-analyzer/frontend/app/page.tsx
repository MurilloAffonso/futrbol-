"use client";

import { useMemo, useState } from "react";
import { api } from "../lib/api";

type Tab = "dashboard" | "analysis" | "valuebets" | "backtest" | "imports" | "status";

export default function Home() {
  const [tab, setTab] = useState<Tab>("dashboard");
  const [analysis, setAnalysis] = useState({ market: "", selection: "", offered_odd: "2.2", model_probability: "0.57", confidence_score: "70" });
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [valueBets, setValueBets] = useState<any[]>([]);
  const [apiStatus, setApiStatus] = useState("unknown");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [backtestRows, setBacktestRows] = useState([{ odd: "2.0", model_probability: "0.55", result: "win" }]);
  const [backtestResult, setBacktestResult] = useState<any>(null);
  const [importResult, setImportResult] = useState<any>(null);

  const counts = useMemo(() => ({
    valueBets: valueBets.length,
    analyzed: analysisResult ? 1 : 0,
  }), [valueBets.length, analysisResult]);

  const runAnalysis = async () => {
    setLoading(true); setMessage("");
    try {
      const result = await api.analyzeValueBet({
        market: analysis.market,
        selection: analysis.selection,
        offered_odd: Number(analysis.offered_odd),
        model_probability: Number(analysis.model_probability),
        confidence_score: Number(analysis.confidence_score),
      });
      setAnalysisResult(result);
      const newList = [result, ...valueBets];
      setValueBets(newList);
      localStorage.setItem("value_bets_cache", JSON.stringify(newList));
      setMessage("Análise calculada com sucesso.");
    } catch (e: any) { setMessage(`Erro: ${e.message}`); }
    setLoading(false);
  };

  const checkApi = async () => {
    setLoading(true);
    try { await api.health(); setApiStatus("online"); } catch { setApiStatus("offline"); }
    setLoading(false);
  };

  const runBacktest = async () => {
    setLoading(true); setMessage("");
    try {
      const bets = backtestRows.map((row) => ({ odd: Number(row.odd), model_probability: Number(row.model_probability), result: row.result as "win"|"loss" }));
      const result = await api.runBacktest(bets);
      setBacktestResult(result);
    } catch (e: any) { setMessage(`Erro backtest: ${e.message}`); }
    setLoading(false);
  };

  const handleImport = async (file?: File) => {
    if (!file) return;
    setLoading(true);
    try { setImportResult(await api.importFlashscoreJson(file)); }
    catch (e: any) { setMessage(`Erro importação: ${e.message}`); }
    setLoading(false);
  };

  return <main className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-8">
    <header className="mb-6 border-b border-slate-700 pb-4">
      <h1 className="text-2xl font-bold">Football Edge Analyzer</h1>
      <p className="text-sm text-amber-300">Risco e variância existem. Sem promessa de lucro. A IA apenas explica análises do motor matemático.</p>
    </header>
    <nav className="flex flex-wrap gap-2 mb-6">
      {(["dashboard","analysis","valuebets","backtest","imports","status"] as Tab[]).map(t => <button key={t} onClick={() => setTab(t)} className={`px-3 py-2 rounded ${tab===t?"bg-emerald-600":"bg-slate-800"}`}>{t}</button>)}
    </nav>

    {tab === "dashboard" && <section className="grid gap-4 md:grid-cols-3">
      <div className="bg-slate-800 p-4 rounded">Value Bets calculadas: {counts.valueBets}</div>
      <div className="bg-slate-800 p-4 rounded">Análises recentes: {counts.analyzed}</div>
      <div className="bg-slate-800 p-4 rounded">Status API: {apiStatus}</div>
      <div className="md:col-span-3 bg-slate-900 p-4 rounded">O sistema calcula probabilidade implícita, odd justa, EV e edge para apoiar análise técnica.</div>
      <button onClick={() => setTab("analysis")} className="md:col-span-3 bg-emerald-600 rounded p-3">Nova Análise</button>
    </section>}

    {tab === "analysis" && <section className="space-y-3 max-w-2xl">
      <input className="w-full p-2 rounded bg-slate-800" placeholder="Mercado" value={analysis.market} onChange={(e)=>setAnalysis({...analysis, market:e.target.value})}/>
      <input className="w-full p-2 rounded bg-slate-800" placeholder="Seleção" value={analysis.selection} onChange={(e)=>setAnalysis({...analysis, selection:e.target.value})}/>
      <input className="w-full p-2 rounded bg-slate-800" placeholder="Odd oferecida" value={analysis.offered_odd} onChange={(e)=>setAnalysis({...analysis, offered_odd:e.target.value})}/>
      <input className="w-full p-2 rounded bg-slate-800" placeholder="Probabilidade modelo" value={analysis.model_probability} onChange={(e)=>setAnalysis({...analysis, model_probability:e.target.value})}/>
      <button disabled={loading} onClick={runAnalysis} className="bg-emerald-600 rounded px-4 py-2">Calcular</button>
      {analysisResult && <div className="grid grid-cols-2 gap-2">
        <div className="bg-slate-800 p-3 rounded">Implícita: {analysisResult.implied_probability?.toFixed(4)}</div>
        <div className="bg-slate-800 p-3 rounded">Odd justa: {analysisResult.fair_odd?.toFixed(2)}</div>
        <div className="bg-slate-800 p-3 rounded">EV: {analysisResult.expected_value?.toFixed(4)}</div>
        <div className="bg-slate-800 p-3 rounded">Edge: {analysisResult.edge_percentage?.toFixed(2)}%</div>
        <div className="bg-slate-800 p-3 rounded col-span-2">Status: <span className="font-bold">{analysisResult.status}</span></div>
      </div>}
    </section>}

    {tab === "valuebets" && <section>
      {valueBets.length === 0 ? <p>Sem oportunidades ainda.</p> : <table className="w-full text-sm"><thead><tr><th>Mercado</th><th>Seleção</th><th>Odd</th><th>Fair</th><th>EV</th><th>Edge</th><th>Status</th></tr></thead><tbody>{valueBets.map((v,idx)=><tr key={idx}><td>{v.market}</td><td>{v.selection}</td><td>{v.offered_odd}</td><td>{v.fair_odd?.toFixed(2)}</td><td>{v.expected_value?.toFixed(4)}</td><td>{v.edge_percentage?.toFixed(2)}%</td><td>{v.status}</td></tr>)}</tbody></table>}
    </section>}

    {tab === "backtest" && <section className="space-y-2">
      {backtestRows.map((row, i)=><div key={i} className="grid grid-cols-3 gap-2"><input className="bg-slate-800 p-2 rounded" value={row.odd} onChange={(e)=>{const rows=[...backtestRows]; rows[i].odd=e.target.value; setBacktestRows(rows);}}/><input className="bg-slate-800 p-2 rounded" value={row.model_probability} onChange={(e)=>{const rows=[...backtestRows]; rows[i].model_probability=e.target.value; setBacktestRows(rows);}}/><select className="bg-slate-800 p-2 rounded" value={row.result} onChange={(e)=>{const rows=[...backtestRows]; rows[i].result=e.target.value; setBacktestRows(rows);}}><option>win</option><option>loss</option></select></div>)}
      <button onClick={()=>setBacktestRows([...backtestRows,{odd:"2.0",model_probability:"0.5",result:"loss"}])} className="bg-slate-700 px-3 py-2 rounded">Adicionar aposta</button>
      <button onClick={runBacktest} className="bg-emerald-600 px-3 py-2 rounded">Rodar backtest</button>
      {backtestResult && <pre className="bg-slate-900 p-3 rounded overflow-auto">{JSON.stringify(backtestResult, null, 2)}</pre>}
    </section>}

    {tab === "imports" && <section className="space-y-3">
      <input type="file" accept="application/json" onChange={(e)=>handleImport(e.target.files?.[0])}/>
      {importResult && <pre className="bg-slate-900 p-3 rounded">{JSON.stringify(importResult, null, 2)}</pre>}
    </section>}

    {tab === "status" && <section className="space-y-2">
      <button onClick={checkApi} className="bg-emerald-600 px-3 py-2 rounded">Testar API</button>
      <p>Status atual: <b>{apiStatus}</b></p>
    </section>}

    {message && <p className="mt-6 text-sm text-amber-300">{message}</p>}
  </main>;
}
