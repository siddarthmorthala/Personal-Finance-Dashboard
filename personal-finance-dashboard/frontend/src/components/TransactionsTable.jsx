import { useMemo, useState } from 'react'

function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value)
}

export default function TransactionsTable({ transactions }) {
  const [query, setQuery] = useState('')

  const filteredTransactions = useMemo(() => {
    const normalized = query.toLowerCase().trim()
    if (!normalized) return transactions

    return transactions.filter((transaction) => {
      return (
        transaction.description.toLowerCase().includes(normalized) ||
        transaction.category.toLowerCase().includes(normalized)
      )
    })
  }, [transactions, query])

  return (
    <section className="card">
      <div className="table-header">
        <div>
          <h2>Transactions</h2>
          <p className="card-description">Search imported transactions by merchant or category.</p>
        </div>
        <input
          className="search-input"
          placeholder="Search transactions"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Description</th>
              <th>Category</th>
              <th>Amount</th>
            </tr>
          </thead>
          <tbody>
            {filteredTransactions.length === 0 ? (
              <tr>
                <td colSpan="4">No transactions found.</td>
              </tr>
            ) : (
              filteredTransactions.map((transaction) => (
                <tr key={transaction.id}>
                  <td>{transaction.date}</td>
                  <td>{transaction.description}</td>
                  <td>{transaction.category}</td>
                  <td>{formatCurrency(transaction.amount)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  )
}
