/** Types alignés sur le schéma backend. */

export interface SignalPresentResume {
  present: boolean
  resume: string
}

export interface SignalPresentListe {
  present: boolean
  liste: string[]
}

export interface SignalPresentValeur {
  present: boolean
  valeurOuFourchette: string
}

export interface SignalPresentCitation {
  present: boolean
  citation: string
}

export interface SignalPresentAction {
  present: boolean
  description: string
}

export interface AnalyzeResponse {
  besoinExprime: SignalPresentResume
  craintesFreins: SignalPresentListe
  infosContexte: SignalPresentResume
  budgetEstime: SignalPresentValeur
  verbatimPersonnalite: SignalPresentCitation
  verbatimPositif: SignalPresentCitation
  prochaineActionActee: SignalPresentAction
  traitementObjections: SignalPresentListe
  noteGlobale: number
  etapesAccomplies: string[]
  etapesManquantes: string[]
}
