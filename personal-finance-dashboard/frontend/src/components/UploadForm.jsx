import { useState } from 'react'

export default function UploadForm({ onUpload, loading }) {
  const [selectedFile, setSelectedFile] = useState(null)

  function handleSubmit(event) {
    event.preventDefault()
    if (!selectedFile) return
    onUpload(selectedFile)
  }

  return (
    <section className="card">
      <h2>Upload bank CSV</h2>
      <p className="card-description">
        Import exported bank transactions to populate the dashboard.
      </p>
      <form className="upload-form" onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".csv"
          onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
        />
        <button className="primary-button" type="submit" disabled={!selectedFile || loading}>
          {loading ? 'Uploading...' : 'Upload CSV'}
        </button>
      </form>
    </section>
  )
}
