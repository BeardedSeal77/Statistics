// app/statistics/layout.tsx
export default function StatisticsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-base">
      {children}
    </div>
  )
}