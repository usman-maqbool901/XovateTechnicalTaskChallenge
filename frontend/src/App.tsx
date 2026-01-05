import React, { useState, useRef } from 'react'
import './index.css'
import type { ValidationResponse } from './types'

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ValidationResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setError(null)
      setResult(null)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setError(null);
      setResult(null);
    }
  };

  const handleSubmit = async () => {
    if (!file) return

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/validate', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`)
      }

      const data: ValidationResponse = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="card">
        <header className="header">
          <h1>Data Validator</h1>
          <p>Professional CSV validation engine</p>
        </header>

        <div
          className={`upload-section ${isDragging ? 'dragging' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".csv"
            className="file-input"
          />
          <div className="upload-content">
            {file ? (
              <p style={{ color: '#818cf8', fontWeight: 600 }}>{file.name}</p>
            ) : (
              <>
                <p>Click to browse or drag and drop</p>
                <p style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>Only .csv files are supported</p>
              </>
            )}
          </div>
        </div>

        <div style={{ textAlign: 'center' }}>
          <button
            className="btn"
            disabled={!file || loading}
            onClick={handleSubmit}
          >
            {loading ? <span className="loading-spinner"></span> : 'Validate Data'}
          </button>
        </div>

        {error && (
          <div className="result-banner" style={{ background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
            Error: {error}
          </div>
        )}

        {result && result.status === 'pass' && (
          <div className="result-banner banner-success">
            ✨ Validation Successful: Data is clean.
          </div>
        )}

        {result && result.status === 'fail' && (
          <div className="error-table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Row</th>
                  <th>Column</th>
                  <th>Error Description</th>
                </tr>
              </thead>
              <tbody>
                {result.errors.map((err, i) => (
                  <tr key={i}>
                    <td className="col-id">{err.id ?? '-'}</td>
                    <td className="col-row">{err.row_index ?? '-'}</td>
                    <td className="col-column">{err.column ?? 'Global'}</td>
                    <td className="col-msg">{err.error_message}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
