import { useEffect, useState } from 'react'
import {
  clearTransactions,
  fetchCategoryBreakdown,
  fetchMonthlyTrends,
  fetchSummary,
  fetchTransactions,
  uploadCsv,
} from './api'
import UploadForm from './components/UploadForm'
import SummaryCards from './components/SummaryCards'
import SpendingByCategoryChart from './components/SpendingByCategoryChart'
import MonthlyTrendChart from './components/MonthlyTrendChart'
import TransactionsTable from './components/TransactionsTable'

export default function App() {
  const [summary, setSummary] = useState({ income: 0, spending: 0, net: 0, transaction_count: 0 })
  const [categoryData, setCategoryData] = useState([])
  const [monthlyData, setMonthlyData] = useState([])
  const [transactions, setTransactions] = useState([])
  const [statusMessage, setStatusMessage] = useState('')
  const [loading, setLoading] = useState(false)

  async function loadDashboard() {
    const [summaryRes, categoryRes, monthlyRes, transactionsRes] = await Promise.all([
      fetchSummary(),
      fetchCategoryBreakdown(),
      fetchMonthlyTrends(),
      fetchTransactions(),
    ])

    setSummary(summaryRes)
    setCategoryData(categoryRes)
    setMonthlyData(monthlyRes)
    setTransactions(transactionsRes)
  }

  useEffect(() => {
    loadDashboard()
  }, [])

  async function handleUpload(file) {
    try {
      setLoading(true)
      const result = await uploadCsv(file)
      setStatusMessage(`${result.message}. Imported ${result.imported_count} rows.`)
      await loadDashboard()
    } catch (error) {
      setStatusMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleClear() {
    try {
      setLoading(true)
      await clearTransactions()
      setStatusMessage('All imported transactions were cleared.')
      await loadDashboard()
    } catch (error) {
      setStatusMessage('Failed to clear transactions.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Full-Stack Finance App</p>
          <h1>Personal Finance Dashboard</h1>
          <p className="subtitle">
            Upload transaction CSVs, categorize spending, and visualize income and expense trends.
          </p>
        </div>
        <div className="hero-actions">
          <button className="secondary-button" onClick={handleClear} disabled={loading}>
            Clear Data
          </button>
        </div>
      </header>

      <UploadForm onUpload={handleUpload} loading={loading} />

      {statusMessage && <div className="status-banner">{statusMessage}</div>}

      <SummaryCards summary={summary} />

      <section className="chart-grid">
        <SpendingByCategoryChart data={categoryData} />
        <MonthlyTrendChart data={monthlyData} />
      </section>

      <TransactionsTable transactions={transactions} />
    </div>
  )
}
