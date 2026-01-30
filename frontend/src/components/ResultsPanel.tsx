import type { AnalyzeResponse } from '../types'
import ScoreGauge from './ScoreGauge'
import Checklist from './Checklist'
import SignalDetails from './SignalDetails'

interface ResultsPanelProps {
  data: AnalyzeResponse
}

export default function ResultsPanel({ data }: ResultsPanelProps) {
  return (
    <section className="results-panel">
      <h2>Résultats de l&apos;analyse</h2>
      <div className="results-score">
        <h3>Note globale</h3>
        <ScoreGauge score={data.noteGlobale} />
      </div>
      <Checklist data={data} />
      <SignalDetails data={data} />
    </section>
  )
}
