const API_BASE_URL = 'http://127.0.0.1:8000'

export async function uploadCsv(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Upload failed')
  }

  return response.json()
}

export async function fetchSummary() {
  const response = await fetch(`${API_BASE_URL}/summary`)
  return response.json()
}

export async function fetchCategoryBreakdown() {
  const response = await fetch(`${API_BASE_URL}/category-breakdown`)
  return response.json()
}

export async function fetchMonthlyTrends() {
  const response = await fetch(`${API_BASE_URL}/monthly-trends`)
  return response.json()
}

export async function fetchTransactions() {
  const response = await fetch(`${API_BASE_URL}/transactions`)
  return response.json()
}

export async function clearTransactions() {
  const response = await fetch(`${API_BASE_URL}/transactions`, {
    method: 'DELETE',
  })
  return response.json()
}
