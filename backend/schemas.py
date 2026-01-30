"""Modèles Pydantic pour les requêtes et réponses de l'API."""

from pydantic import BaseModel, Field


class SignalPresentResume(BaseModel):
    """Signal avec présent + résumé (besoin, contexte)."""
    present: bool = False
    resume: str = ""


class SignalPresentListe(BaseModel):
    """Signal avec présent + liste (craintes/freins)."""
    present: bool = False
    liste: list[str] = Field(default_factory=list)


class SignalPresentValeur(BaseModel):
    """Signal avec présent + valeur ou fourchette (budget)."""
    present: bool = False
    valeurOuFourchette: str = ""


class SignalPresentCitation(BaseModel):
    """Signal avec présent + citation (verbatims)."""
    present: bool = False
    citation: str = ""


class SignalPresentAction(BaseModel):
    """Signal avec présent + description (prochaine action)."""
    present: bool = False
    description: str = ""


class AnalyzeRequest(BaseModel):
    """Requête POST /api/analyze."""
    transcription: str = Field(..., min_length=1)


class AnalyzeResponse(BaseModel):
    """Réponse JSON de l'analyse."""
    besoinExprime: SignalPresentResume = Field(default_factory=SignalPresentResume)
    craintesFreins: SignalPresentListe = Field(default_factory=SignalPresentListe)
    infosContexte: SignalPresentResume = Field(default_factory=SignalPresentResume)
    budgetEstime: SignalPresentValeur = Field(default_factory=SignalPresentValeur)
    verbatimPersonnalite: SignalPresentCitation = Field(default_factory=SignalPresentCitation)
    verbatimPositif: SignalPresentCitation = Field(default_factory=SignalPresentCitation)
    prochaineActionActee: SignalPresentAction = Field(default_factory=SignalPresentAction)
    traitementObjections: SignalPresentListe = Field(default_factory=SignalPresentListe)
    noteGlobale: float = Field(ge=0, le=10, default=0)
    etapesAccomplies: list[str] = Field(default_factory=list)
    etapesManquantes: list[str] = Field(default_factory=list)
