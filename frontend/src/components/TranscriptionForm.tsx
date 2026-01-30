import { useCallback, useRef } from 'react'

interface TranscriptionFormProps {
  value: string
  onChange: (v: string) => void
  onAnalyze: () => void
  loading: boolean
  disabled?: boolean
}

export default function TranscriptionForm({
  value,
  onChange,
  onAnalyze,
  loading,
  disabled,
}: TranscriptionFormProps) {
  const inputRef = useRef<HTMLInputElement>(null)

  const onFile = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const f = e.target.files?.[0]
      if (!f) return
      const r = new FileReader()
      r.onload = () => {
        const t = (r.result as string) ?? ''
        onChange(t)
      }
      r.readAsText(f, 'utf-8')
      e.target.value = ''
    },
    [onChange],
  )

  return (
    <section className="form-section">
      <div className="form-header">
        <h2>Transcription du RDV</h2>
        <div className="form-actions">
          <input
            ref={inputRef}
            type="file"
            accept=".txt,text/plain"
            onChange={onFile}
            className="file-input"
            aria-label="Choisir un fichier .txt"
          />
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => inputRef.current?.click()}
            disabled={disabled || loading}
          >
            Importer .txt
          </button>
          <button
            type="button"
            className="btn btn-primary"
            onClick={onAnalyze}
            disabled={disabled || loading || !value.trim()}
          >
            {loading ? 'Analyse en cours…' : 'Analyser'}
          </button>
        </div>
      </div>
      <textarea
        className="transcription-input"
        placeholder="Colle ici la transcription du rendez-vous client ou importe un fichier .txt…"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        rows={12}
      />
    </section>
  )
}
