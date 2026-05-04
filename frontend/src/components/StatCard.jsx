export default function StatCard({ title, value, icon: Icon, tone = "bg-aqua/15 text-aqua" }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm dark:border-white/10 dark:bg-slate-900">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">{title}</p>
          <p className="mt-2 text-2xl font-black">{value}</p>
        </div>
        {Icon && (
          <span className={`grid h-11 w-11 place-items-center rounded-lg ${tone}`}>
            <Icon size={21} />
          </span>
        )}
      </div>
    </div>
  );
}
