interface ScoreGaugeProps {
  score: number
  max?: number
}

export default function ScoreGauge({ score, max = 10 }: ScoreGaugeProps) {
  const pct = Math.min(100, Math.max(0, (score / max) * 100))

  return (
    <div className="score-gauge">
      <div className="score-value">
        <span className="score-num">{score.toFixed(1)}</span>
        <span className="score-max">/ {max}</span>
      </div>
      <div className="score-bar" role="meter" aria-valuenow={score} aria-valuemin={0} aria-valuemax={max}>
        <div className="score-fill" style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}
