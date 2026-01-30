"""Application FastAPI – route POST /api/analyze."""

from contextlib import asynccontextmanager
import logging

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from analyzer import analyze
from schemas import AnalyzeRequest, AnalyzeResponse

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(title="SalesCoach API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://salescoach-frontend.onrender.com",
        "https://*.onrender.com"  # Autorise tous les sous-domaines Render
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/analyze", response_model=AnalyzeResponse)
def api_analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    """Analyse une transcription de RDV client et retourne les signaux + note + étapes."""
    logger.info(f"Requête d'analyse reçue, longueur transcription: {len(req.transcription)} caractères")
    
    try:
        result = analyze(req.transcription)
        logger.info("Analyse réussie")
        return result
    except ValueError as e:
        # Erreurs attendues (validation, parsing, etc.)
        logger.warning(f"Erreur de validation: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # Erreurs inattendues
        logger.error(f"Erreur interne inattendue: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur interne: {str(e)}. Consulte les logs du backend pour plus de détails."
        )
