import Link from 'next/link';

export default function Home(){
  return <main className="hero-glow min-h-screen text-white">
    <div className="mx-auto flex min-h-screen max-w-7xl items-center px-6 py-16 lg:px-10">
      <div className="grid w-full gap-14 lg:grid-cols-[1.05fr_.95fr] lg:items-center">
        <div className="float-in">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs font-semibold text-slate-300"><span className="status-dot bg-emerald-400"/> Field service operations SaaS</div>
          <h1 className="max-w-3xl text-5xl font-black tracking-[-.055em] sm:text-6xl lg:text-7xl">Run field operations without the chaos.</h1>
          <p className="mt-6 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">A complete operational workspace for service requests, dispatch, technicians, proof of work, customers and invoicing.</p>
          <div className="mt-9 flex flex-wrap gap-3"><Link className="btn btn-primary" href="/app/dashboard">Open Operations Console →</Link><Link className="btn border border-white/15 bg-white/5 text-white hover:bg-white/10" href="/portal">View Customer Portal</Link></div>
          <div className="mt-10 grid max-w-2xl grid-cols-2 gap-3 sm:grid-cols-4">
            {['24 jobs today','3 unassigned','91% SLA on time','AED 18,420 revenue'].map(x=><div key={x} className="rounded-2xl border border-white/10 bg-white/5 p-4"><div className="text-sm font-semibold text-white">{x.split(' ')[0]} {x.split(' ')[1]}</div><div className="mt-1 text-xs text-slate-400">{x.split(' ').slice(2).join(' ') || 'live metric'}</div></div>)}
          </div>
        </div>
        <div className="float-in rounded-3xl border border-white/10 bg-slate-950/40 p-4 shadow-2xl shadow-black/30 backdrop-blur-xl">
          <div className="flex items-center justify-between border-b border-white/10 pb-4"><div><div className="text-xs uppercase tracking-[.18em] text-slate-500">Operations Command Center</div><div className="mt-1 text-sm font-bold">Today, 18 Sep 2026</div></div><div className="rounded-full bg-emerald-400/10 px-3 py-1.5 text-xs font-bold text-emerald-300">LIVE</div></div>
          <div className="grid grid-cols-2 gap-3 py-4 sm:grid-cols-4">{[['24','Jobs'],['3','Unassigned'],['8','In progress'],['13','Completed']].map(([n,l])=><div key={l} className="rounded-2xl border border-white/10 bg-white/[.03] p-4"><div className="text-2xl font-black">{n}</div><div className="mt-1 text-xs text-slate-500">{l}</div></div>)}</div>
          <div className="space-y-3">{['WO-1045 · ABC Trading · Ahmed · ON SITE','WO-1046 · Nexa Facilities · Sara · IN PROGRESS','WO-1047 · Greenline Cafe · Omar · EN ROUTE'].map((x,i)=><div key={x} className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/[.025] px-4 py-3"><div className="text-xs font-semibold text-slate-200">{x}</div><span className={`h-2.5 w-2.5 rounded-full ${i===0?'bg-amber-400':i===1?'bg-orange-400':'bg-cyan-400'}`}/></div>)}</div>
        </div>
      </div>
    </div>
  </main>
}
