import type { AnalyzeResponse } from '../types'

const SIGNALS: {
  key: keyof Omit<AnalyzeResponse, 'noteGlobale' | 'etapesAccomplies' | 'etapesManquantes'>
  label: string
  render: (v: unknown) => React.ReactNode
}[] = [
  {
    key: 'besoinExprime',
    label: 'Besoin client',
    render: (v) => {
      const x = v as { present: boolean; resume: string }
      return x.present && x.resume ? <p className="signal-resume">{x.resume}</p> : <p className="signal-empty">Non identifié.</p>
    },
  },
  {
    key: 'craintesFreins',
    label: 'Craintes et freins',
    render: (v) => {
      const x = v as { present: boolean; liste: string[] }
      if (!x.present || !x.liste?.length) return <p className="signal-empty">Aucune collectée.</p>
      return (
        <ul className="signal-list">
          {x.liste.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      )
    },
  },
  {
    key: 'infosContexte',
    label: 'Contexte',
    render: (v) => {
      const x = v as { present: boolean; resume: string }
      return x.present && x.resume ? <p className="signal-resume">{x.resume}</p> : <p className="signal-empty">Non renseigné.</p>
    },
  },
  {
    key: 'budgetEstime',
    label: 'Budget',
    render: (v) => {
      const x = v as { present: boolean; valeurOuFourchette: string }
      return x.present && x.valeurOuFourchette ? <p className="signal-resume">{x.valeurOuFourchette}</p> : <p className="signal-empty">Non évoqué.</p>
    },
  },
  {
    key: 'verbatimPersonnalite',
    label: 'Signaux d\'intérêt pour acheter',
    render: (v) => {
      const x = v as { present: boolean; citation: string }
      return x.present && x.citation ? <blockquote className="signal-quote">{x.citation}</blockquote> : <p className="signal-empty">Aucun.</p>
    },
  },
  {
    key: 'verbatimPositif',
    label: 'Verbatim positif',
    render: (v) => {
      const x = v as { present: boolean; citation: string }
      return x.present && x.citation ? <blockquote className="signal-quote">{x.citation}</blockquote> : <p className="signal-empty">Aucun.</p>
    },
  },
  {
    key: 'prochaineActionActee',
    label: 'Prochaine action',
    render: (v) => {
      const x = v as { present: boolean; description: string }
      return x.present && x.description ? <p className="signal-resume">{x.description}</p> : <p className="signal-empty">Non actée.</p>
    },
  },
  {
    key: 'traitementObjections',
    label: 'Traitement des objections',
    render: (v) => {
      const x = v as { present: boolean; liste: string[] }
      if (x.present && x.liste?.length) {
        return (
          <div className="signal-warning">
            <p>⚠️ Objection{x.liste.length > 1 ? 's' : ''} non traitée{x.liste.length > 1 ? 's' : ''} :</p>
            <ul className="signal-list">
              {x.liste.map((objection, i) => (
                <li key={i}>
                  <blockquote className="signal-quote">{objection}</blockquote>
                </li>
              ))}
            </ul>
          </div>
        )
      }
      return <p className="signal-empty">Aucune objection non traitée.</p>
    },
  },
]

interface SignalDetailsProps {
  data: AnalyzeResponse
}

export default function SignalDetails({ data }: SignalDetailsProps) {
  return (
    <div className="signal-details">
      <h3>Détail des signaux</h3>
      <dl>
        {SIGNALS.map(({ key, label, render }) => (
          <div key={key} className="signal-item">
            <dt>{label}</dt>
            <dd>{render(data[key])}</dd>
          </div>
        ))}
      </dl>
    </div>
  )
}
