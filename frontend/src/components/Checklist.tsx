import type { AnalyzeResponse } from '../types'

const ETAPES: { key: keyof Omit<AnalyzeResponse, 'noteGlobale' | 'etapesAccomplies' | 'etapesManquantes'>; label: string }[] = [
  { key: 'besoinExprime', label: 'Besoin client clairement exprimé' },
  { key: 'craintesFreins', label: 'Craintes et freins collectés' },
  { key: 'infosContexte', label: 'Infos de contexte collectées' },
  { key: 'budgetEstime', label: 'Budget estimé ou fourchette' },
  { key: 'verbatimPersonnalite', label: 'Signaux d\'intérêt pour acheter' },
  { key: 'verbatimPositif', label: 'Verbatim positif / intérêt client' },
  { key: 'prochaineActionActee', label: 'Prochaine action actée avec le client' },
  { key: 'traitementObjections', label: 'Traitement des objections' },
]

interface ChecklistProps {
  data: AnalyzeResponse
}

function isPresent(
  v: AnalyzeResponse['besoinExprime'] | AnalyzeResponse['craintesFreins'] | AnalyzeResponse['budgetEstime'] | AnalyzeResponse['verbatimPersonnalite'] | AnalyzeResponse['verbatimPositif'] | AnalyzeResponse['prochaineActionActee'],
): boolean {
  return 'present' in v && !!v.present
}

export default function Checklist({ data }: ChecklistProps) {
  return (
    <div className="checklist">
      <h3>Étapes</h3>
      <ul className="checklist-list">
        {ETAPES.map(({ key, label }) => {
          const v = data[key]
          const present = isPresent(v as { present?: boolean })
          // Pour traitementObjections, la logique est inversée (present:true = problème)
          const ok = key === 'traitementObjections' ? !present : present
          return (
            <li key={key} className={ok ? 'done' : 'missing'}>
              <span className="check-icon" aria-hidden>{ok ? '✓' : '✗'}</span>
              {label}
            </li>
          )
        })}
      </ul>
    </div>
  )
}
