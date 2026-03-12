function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value)
}

export default function SummaryCards({ summary }) {
  const cards = [
    { label: 'Income', value: formatCurrency(summary.income || 0) },
    { label: 'Spending', value: formatCurrency(summary.spending || 0) },
    { label: 'Net Cash Flow', value: formatCurrency(summary.net || 0) },
    { label: 'Transactions', value: summary.transaction_count || 0 },
  ]

  return (
    <section className="summary-grid">
      {cards.map((card) => (
        <div className="summary-card" key={card.label}>
          <p>{card.label}</p>
          <h3>{card.value}</h3>
        </div>
      ))}
    </section>
  )
}
