import { useState, useCallback } from 'react'
import { analyzeTranscription } from './api/client'
import type { AnalyzeResponse } from './types'
import TranscriptionForm from './components/TranscriptionForm'
import ResultsPanel from './components/ResultsPanel'

export default function App() {
  const [transcription, setTranscription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<AnalyzeResponse | null>(null)

  const handleAnalyze = useCallback(async () => {
    setError(null)
    setResult(null)
    setLoading(true)
    try {
      const data = await analyzeTranscription(transcription)
      setResult(data)
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Erreur lors de l\'analyse.'
      if (/failed to fetch|network|load/i.test(String(msg)))
        setError('Impossible de joindre l\'API. Vérifie que le backend est accessible.')
      else
        setError(msg)
    } finally {
      setLoading(false)
    }
  }, [transcription])

  return (
    <div className="app">
      <header className="app-header">
        <h1>SalesCoach</h1>
        <p>Analyse tes RDV clients et identifie les étapes accomplies ou manquantes.</p>
      </header>

      <TranscriptionForm
        value={transcription}
        onChange={setTranscription}
        onAnalyze={handleAnalyze}
        loading={loading}
      />

      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}

      {result && <ResultsPanel data={result} />}
    </div>
  )
}
