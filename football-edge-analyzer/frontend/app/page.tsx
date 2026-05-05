const cards = [
  {
    title: "Value Betting",
    text: "Calcule odd justa, probabilidade implicita, EV e edge.",
  },
  {
    title: "Flashscore autorizado",
    text: "Consuma JSON exportado pelo coletor ou integre endpoint autorizado.",
  },
  {
    title: "Backtesting",
    text: "Teste filtros de EV, confiança e odds com stake fixa.",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <section className="mx-auto max-w-5xl">
        <div className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl">
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">MVP v0.1</p>
          <h1 className="mt-4 text-4xl font-bold text-white">Football Edge Analyzer</h1>
          <p className="mt-4 max-w-3xl text-lg text-slate-300">
            Central de decisão para analisar partidas, odds, probabilidade, valor esperado e risco.
          </p>
          <div className="mt-8 grid gap-4 md:grid-cols-3">
            {cards.map((card) => (
              <article key={card.title} className="rounded-2xl border border-white/10 bg-slate-950/60 p-5">
                <h2 className="text-xl font-semibold text-white">{card.title}</h2>
                <p className="mt-2 text-sm text-slate-300">{card.text}</p>
              </article>
            ))}
          </div>
          <div className="mt-8 rounded-2xl bg-amber-500/10 p-4 text-sm text-amber-100">
            Aviso: este software nao promete lucro. Ele classifica oportunidades com base em dados, filtros e hipoteses do modelo.
          </div>
        </div>
      </section>
    </main>
  );
}
