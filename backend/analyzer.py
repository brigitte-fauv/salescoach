"""Logique d'appel LLM, parsing JSON et validation."""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Any

import httpx
from pydantic import ValidationError

from schemas import AnalyzeResponse

# Configuration du logger avec fichier de debug
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler pour le fichier
log_file = Path(__file__).parent / "debug.log"
file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Handler pour la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Ajouter les handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Fonction helper pour écrire directement dans un fichier (fallback si logging ne marche pas)
def _write_debug(message: str):
    """Écrit directement dans un fichier pour debug."""
    try:
        debug_path = Path(__file__).parent / "debug_direct.txt"
        with open(debug_path, 'a', encoding='utf-8') as f:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp} | {message}\n")
            f.flush()
    except:
        pass

_write_debug("="*80)
_write_debug("Démarrage de l'analyseur SalesCoach - LOG DIRECT")
_write_debug("="*80)

logger.info("="*80)
logger.info("Démarrage de l'analyseur SalesCoach")
logger.info("="*80)

# Config depuis l'environnement
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4o-mini")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" | "anthropic" | "gemini"
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "90"))

ANALYSIS_PROMPT = """Tu es un coach commercial expert. Analyse la transcription d'un rendez-vous client ci-dessous et extrais les signaux suivants.

RÈGLES CRITIQUES POUR LA RÉPONSE:
- RÉPONDS UNIQUEMENT ET EXCLUSIVEMENT PAR UN OBJET JSON VALIDE
- AUCUN texte avant le JSON
- AUCUN texte après le JSON  
- AUCUN bloc de code markdown (pas de ```)
- AUCUN commentaire
- La réponse doit commencer par {{ et finir par }}
- Utilise des guillemets doubles " pour toutes les chaînes
- Échappe correctement les guillemets dans les citations avec \"
- Les retours à la ligne dans les textes doivent être échappés avec \\n

⚠️ RÈGLE CRITIQUE POUR LES VERBATIMS (verbatimPersonnalite, verbatimPositif, traitementObjections):

PROCESSUS DE VALIDATION OBLIGATOIRE:
1. Identifie QUI prononce la phrase :
   - Si c'est Brigitte, Adrien, Orlane ou Arno → CE SONT DES COMMERCIAUX → passe à l'étape 2
   - Si c'est une autre personne → c'est le CLIENT/PROSPECT → passe à l'étape 3

2. Si c'est un COMMERCIAL (Brigitte/Adrien/Orlane/Arno) :
   → NE PAS CAPTURER cette citation
   → ARRÊTER ICI

3. Si c'est le CLIENT/PROSPECT :
   → Vérifie le contenu de la phrase
   → Pour verbatimPersonnalite (signaux d'intérêt achat) : la phrase doit montrer une intention d'achat
   → Pour verbatimPositif : la phrase doit montrer de l'intérêt ou satisfaction
   → Pour traitementObjections : la phrase doit montrer une objection/crainte NON TRAITÉE par les commerciaux
   → Si validé :
     - Pour verbatimPersonnalite et verbatimPositif : Mettre "present": true et "citation": "[Nom du prospect] phrase exacte"
     - Pour traitementObjections : Mettre "present": true et ajouter "[Nom du prospect] phrase exacte" dans la liste
   → Le format est TOUJOURS : [Nom] Citation

EXEMPLES:
❌ INCORRECT : "Je suis ravie de voir..." (dit par Brigitte = COMMERCIAL → ne pas capturer)
✓ CORRECT pour signaux d'intérêt : "[Jean Dupont] Par quoi on commence pour la mise en place ?"
✓ CORRECT pour signaux d'intérêt : "[Marie Martin] Quand est-ce qu'on peut démarrer le projet ?"
✓ CORRECT pour verbatim positif : "[Sophie Durand] C'est exactement ce qu'il nous faut"
✓ CORRECT pour objections non traitées (LISTE) : 
  - "[Paul Legrand] Mais c'est vraiment trop cher pour nous"
  - "[Paul Legrand] Et si ça ne fonctionne pas ?"
  - "[Sophie Martin] Je ne comprends pas comment ça marche"

RÈGLES D'ANALYSE:
- Pour chaque signal, mets "present": true si tu l'as clairement identifié dans la transcription, false sinon.
- Si present est true, remplis le champ associé (resume, liste, valeurOuFourchette, citation, description). Sinon mets une chaîne vide ou une liste vide.
- IMPORTANT: Pour verbatimPersonnalite et verbatimPositif, la citation DOIT commencer par [Nom du prospect] suivi de la phrase
- IMPORTANT: Pour traitementObjections, chaque élément de la liste DOIT commencer par [Nom du prospect] suivi de la phrase
- ATTENTION: traitementObjections est un signal NÉGATIF : present: true = problème détecté (objections non traitées)
- ATTENTION: Pour traitementObjections, capture TOUTES les objections non traitées, pas seulement la première
- ⚠️ CRITIQUE: craintesFreins et traitementObjections sont COMPLÉMENTAIRES :
  * craintesFreins = TOUTES les craintes exprimées (traitées ou non)
  * traitementObjections = UNIQUEMENT les craintes NON traitées par les commerciaux
  * Si une crainte est exprimée mais non traitée, elle doit apparaître dans LES DEUX
- noteGlobale: mets toujours 0 (la note sera calculée automatiquement par le système)
- etapesAccomplies: liste des libellés en français des étapes ci-dessous pour lesquelles present est true.
- etapesManquantes: liste des libellés des étapes pour lesquelles present est false.

LES 8 ÉTAPES (et libellés à utiliser dans etapesAccomplies / etapesManquantes):
1. Besoin client clairement exprimé -> besoinExprime
2. Craintes et freins collectés -> craintesFreins
3. Infos de contexte collectées -> infosContexte
4. Budget estimé ou fourchette -> budgetEstime
5. Signaux d'intérêt pour acheter -> verbatimPersonnalite (FORMAT: citation = "[Nom du prospect] phrase exacte")
6. Verbatim positif / intérêt client -> verbatimPositif (FORMAT: citation = "[Nom du prospect] phrase exacte")
7. Prochaine action actée avec le client -> prochaineActionActee
8. Traitement des objections -> traitementObjections (FORMAT: liste = ["[Nom] phrase 1", "[Nom] phrase 2", ...])

DÉTAIL DU CRITÈRE "Signaux d'intérêt pour acheter" (verbatimPersonnalite):
⚠️ IMPORTANT : Ce critère concerne l'intérêt d'achat pour NOTRE entreprise/solution, PAS pour l'IA en général.

Ce critère est present: true si le CLIENT exprime des signaux d'intention d'achat POUR NOTRE OFFRE, notamment :
- Questions sur détails pratiques CHEZ NOUS : mise en œuvre, planning, "par quoi on commence", processus de déploiement
- Demandes de précisions sur NOTRE tarification, modalités de paiement, facturation
- Projection dans le futur AVEC NOUS : "Quand on démarre...", "Dans notre déploiement...", "Une fois en place..."
- Organisation d'une validation avec d'autres décideurs POUR NOTRE SOLUTION : "Je vais en parler à...", "On doit présenter à..."

❌ NE PAS capturer : intérêt général pour l'IA, questions théoriques, curiosité non commerciale
✓ CAPTURER : questions concrètes sur notre collaboration, notre mise en œuvre, nos tarifs

La citation doit être une phrase du CLIENT montrant un de ces signaux D'ACHAT CHEZ NOUS.

DÉTAIL DU CRITÈRE "Craintes et freins collectés" (craintesFreins):
⚠️ IMPORTANT : Ce critère capture TOUTES les craintes/freins/objections EXPRIMÉES par le client, QU'ELLES SOIENT TRAITÉES OU NON.

Ce critère est present: true si le CLIENT a exprimé des craintes, freins, doutes, objections, peu importe si les commerciaux y ont répondu.

Exemples de craintes/freins à capturer :
- Doutes sur le prix, le budget
- Inquiétudes sur la mise en œuvre, la complexité
- Craintes sur l'adoption par l'équipe
- Objections sur la compatibilité, l'adaptation
- Mentions de concurrents
- Expressions de sentiment mitigé

⚠️ RÈGLE CRITIQUE : Si le client exprime une crainte/objection dans la transcription, elle DOIT apparaître dans craintesFreins.liste, même si elle n'est pas traitée par les commerciaux.

DIFFÉRENCE avec traitementObjections :
- craintesFreins = TOUTES les craintes exprimées (traitées ou non) → liste descriptive des craintes
- traitementObjections = UNIQUEMENT les craintes/objections NON TRAITÉES → liste des verbatims avec format [Nom]

DÉTAIL DU CRITÈRE "Traitement des objections" (traitementObjections):
⚠️ ATTENTION : Ce critère est UN SIGNAL NÉGATIF / UN PROBLÈME

Ce critère est present: true si le CLIENT manifeste un sentiment négatif, une crainte ou une confusion sur les services de l'entreprise ET que les commerciaux (Brigitte/Adrien/Orlane/Arno) N'ONT PAS RÉPONDU à cette objection.

⚠️ IMPORTANT : Capture TOUTES les objections non traitées dans la liste, pas seulement une.
⚠️ CRITIQUE : Analyse la transcription JUSQU'À LA TOUTE FIN. Les objections en fin de conversation sont souvent laissées sans réponse.

Indicateurs d'objection NON traitée :
- Le client exprime une inquiétude, un doute, une confusion
- Le client pose une question critique ou montre du scepticisme
- Le client manifeste une réticence, une hésitation, un malaise
- Le client dit "oui mais...", "je ne suis pas sûr", "ça m'inquiète", "j'ai peur que"
- Le client exprime un sentiment mitigé : "je suis mitigé(e)", "j'ai des réserves", "je suis partagé(e)"
- Le client reste sur une note négative ou dubitative
- ⚠️ Le client mentionne un CONCURRENT ou une offre concurrente (nom d'entreprise, solution alternative)
- ET ensuite : les commerciaux ne répondent PAS ou changent de sujet ou ignorent l'objection

PROCESSUS DE VALIDATION POUR CHAQUE OBJECTION:
1. Identifier la phrase d'objection du client
2. Vérifier si APRÈS cette phrase, les commerciaux ont donné une réponse/réassurance
3. Si NON ou si l'objection est en toute fin sans réponse → CAPTURER dans la liste
4. Si OUI (réponse claire et rassurante) → NE PAS capturer

present: true = PROBLÈME détecté (une ou plusieurs objections non traitées)
present: false = PAS de problème (soit pas d'objection, soit toutes les objections bien traitées/répondues)

La liste doit contenir TOUTES les phrases exactes du CLIENT montrant des objections/craintes NON TRAITÉES avec le format [Nom] Citation.

EXEMPLES:
✓ present: true avec liste: ["[Marie Dubois] Mais c'est vraiment cher...", "[Marie Dubois] Et si ça ne marche pas ?"]
✓ present: true avec liste: ["[Jean Martin] Je ne comprends pas comment ça marche"]
✓ present: true avec liste: ["[Sophie] Oui mais j'ai quand même des doutes"] (même en fin de transcription)
✓ present: true avec liste: ["[Claire Durand] Je suis très mitigée"] (sentiment mitigé en fin, sans réponse commerciale)
✓ present: true avec liste: ["[Paul] J'ai des réserves sur ce point"]
✓ present: true avec liste: ["[Marie Legrand] Il y a une offre concurrente avec AI sisters"] (mention concurrent non traitée)
✓ present: true avec liste: ["[Jean Dupont] On regarde aussi d'autres solutions comme..."] (concurrent mentionné)
❌ present: false avec liste: [] (si les commerciaux ont bien répondu et rassuré le client)

Libellés exacts pour etapesAccomplies / etapesManquantes:
- "Besoin client clairement exprimé"
- "Craintes et freins collectés"
- "Infos de contexte collectées"
- "Budget estimé ou fourchette"
- "Signaux d'intérêt pour acheter"
- "Verbatim positif / intérêt client"
- "Prochaine action actée avec le client"
- "Traitement des objections"

Format JSON attendu (respecte exactement ces clés):
{{
  "besoinExprime": {{ "present": false, "resume": "" }},
  "craintesFreins": {{ "present": false, "liste": [] }},
  "infosContexte": {{ "present": false, "resume": "" }},
  "budgetEstime": {{ "present": false, "valeurOuFourchette": "" }},
  "verbatimPersonnalite": {{ "present": false, "citation": "" }},
  "verbatimPositif": {{ "present": false, "citation": "" }},
  "prochaineActionActee": {{ "present": false, "description": "" }},
  "traitementObjections": {{ "present": false, "liste": [] }},
  "noteGlobale": 0,
  "etapesAccomplies": [],
  "etapesManquantes": []
}}

NOTE SUR LE FORMAT DES CITATIONS:
- Pour verbatimPersonnalite et verbatimPositif : le champ "citation" doit TOUJOURS inclure le nom
- Pour traitementObjections : chaque élément de la "liste" doit TOUJOURS inclure le nom
- Format obligatoire : "[Nom du prospect] Citation exacte"
- Exemples : 
  - verbatimPersonnalite/verbatimPositif : "[Sophie Durand] Votre solution correspond parfaitement à nos besoins"
  - traitementObjections (liste) : ["[Marc Leblanc] Je ne suis pas sûr que ce soit adapté", "[Marc Leblanc] C'est trop cher"]

TRANSCRIPTION:
---
{transcription}
---
"""


def _call_openai(transcription: str) -> str:
    """Appel API OpenAI (Chat Completions)."""
    url = f"{OPENAI_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Tu es un assistant qui répond UNIQUEMENT en JSON valide. Ta réponse doit commencer par {{ et finir par }}. AUCUN texte avant ou après. AUCUN markdown. AUCUN bloc de code."},
            {"role": "user", "content": ANALYSIS_PROMPT.format(transcription=transcription)},
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }
    try:
        with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
            r = client.post(url, headers=headers, json=payload)
            r.raise_for_status()
    except httpx.TimeoutException as e:
        raise ValueError(f"Timeout lors de l'appel au LLM ({REQUEST_TIMEOUT}s). Réessaie.") from e
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Erreur API LLM (HTTP {e.response.status_code}): {e.response.text[:200]}") from e
    except httpx.HTTPError as e:
        raise ValueError(f"Erreur réseau ou LLM: {e}") from e
    data = r.json()
    content = (data.get("choices") or [{}])[0].get("message", {}).get("content") or ""
    return content.strip()


def _call_anthropic(transcription: str) -> str:
    """Appel API Anthropic (Messages)."""
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "max_tokens": 4096,
        "system": "Tu es un assistant qui répond UNIQUEMENT en JSON valide. Ta réponse doit commencer par {{ et finir par }}. AUCUN texte avant ou après. AUCUN markdown. AUCUN bloc de code.",
        "messages": [{"role": "user", "content": ANALYSIS_PROMPT.format(transcription=transcription)}],
        "temperature": 0.1,
    }
    try:
        with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
            r = client.post(url, headers=headers, json=payload)
            r.raise_for_status()
    except httpx.TimeoutException as e:
        raise ValueError(f"Timeout lors de l'appel au LLM ({REQUEST_TIMEOUT}s). Réessaie.") from e
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Erreur API LLM (HTTP {e.response.status_code}): {e.response.text[:200]}") from e
    except httpx.HTTPError as e:
        raise ValueError(f"Erreur réseau ou LLM: {e}") from e
    data = r.json()
    blocks = data.get("content") or []
    content = ""
    for b in blocks:
        if b.get("type") == "text":
            content += b.get("text", "")
    return content.strip()


def _call_gemini(transcription: str) -> str:
    """Appel API Google Gemini (generateContent)."""
    _write_debug("Appel à l'API Gemini en cours...")
    
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent"
    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "systemInstruction": {
            "parts": [{"text": "Tu es un assistant qui répond UNIQUEMENT en JSON valide. Ta réponse doit commencer par {{ et finir par }}. AUCUN texte avant ou après. AUCUN markdown. AUCUN bloc de code. Réponds directement avec l'objet JSON, sans aucun formatage."}],
        },
        "contents": [
            {"parts": [{"text": ANALYSIS_PROMPT.format(transcription=transcription)}]},
        ],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json",
        },
    }
    try:
        with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
            _write_debug(f"Envoi requête à Gemini (timeout: {REQUEST_TIMEOUT}s)...")
            r = client.post(url, headers=headers, json=payload)
            _write_debug(f"Réponse reçue - Status: {r.status_code}")
            r.raise_for_status()
    except httpx.TimeoutException as e:
        _write_debug(f"TIMEOUT Gemini après {REQUEST_TIMEOUT}s")
        raise ValueError(f"Timeout lors de l'appel au LLM ({REQUEST_TIMEOUT}s). Réessaie.") from e
    except httpx.HTTPStatusError as e:
        error_detail = e.response.text[:500]
        _write_debug(f"ERREUR HTTP Gemini {e.response.status_code}: {error_detail}")
        raise ValueError(f"Erreur API LLM (HTTP {e.response.status_code}): {e.response.text[:200]}") from e
    except httpx.HTTPError as e:
        _write_debug(f"ERREUR RÉSEAU Gemini: {str(e)}")
        raise ValueError(f"Erreur réseau ou LLM: {e}") from e
    
    data = r.json()
    _write_debug(f"JSON parsé - Clés: {list(data.keys())}")
    
    candidates = data.get("candidates") or []
    if not candidates:
        _write_debug("ERREUR: Pas de candidat dans la réponse")
        raise ValueError("Réponse Gemini sans candidat. Réessaie.")
    
    parts = (candidates[0].get("content") or {}).get("parts") or []
    if not parts:
        _write_debug("ERREUR: Pas de parts dans le candidat")
        raise ValueError("Réponse Gemini sans partie texte. Réessaie.")
    
    content = parts[0].get("text") or ""
    _write_debug(f"Contenu extrait - Longueur: {len(content)} caractères")
    _write_debug(f"Premiers 200 chars: {content[:200]}")
    
    return content.strip()


def _extract_json(raw: str) -> dict[str, Any]:
    """
    Extrait un objet JSON du texte avec nettoyage ultra-robuste.
    Gère ```json ... ```, retours à la ligne, caractères cachés, etc.
    """
    original_raw = raw
    raw = raw.strip()
    
    # Log de la réponse brute COMPLÈTE dans le fichier
    logger.debug("="*80)
    logger.debug("RÉPONSE LLM BRUTE COMPLÈTE:")
    logger.debug(raw)
    logger.debug("="*80)
    logger.info(f"Longueur réponse LLM: {len(raw)} caractères")
    
    # Stratégie 1 : Chercher un bloc de code markdown ```json ... ```
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
    if m:
        raw = m.group(1).strip()
        logger.info("✓ JSON extrait depuis un bloc markdown")
    
    # Stratégie 2 : Chercher directement un objet JSON { ... }
    if not raw.startswith("{"):
        json_match = re.search(r"\{[\s\S]*\}", raw)
        if json_match:
            raw = json_match.group(0)
            logger.info("✓ JSON extrait via recherche d'objet { ... }")
    
    # NETTOYAGE ULTRA-ROBUSTE
    # 1. Normaliser les retours à la ligne
    raw = raw.replace('\r\n', '\n').replace('\r', '\n')
    
    # 2. Supprimer les espaces/retours à la ligne AVANT le premier {
    raw = re.sub(r'^[\s\n]*(\{)', r'\1', raw)
    
    # 3. Supprimer les espaces/retours à la ligne APRÈS le dernier }
    raw = re.sub(r'(\})[\s\n]*$', r'\1', raw)
    
    # 4. Supprimer les caractères de contrôle invisibles (sauf \n, \t qui sont légitimes dans JSON)
    raw = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', raw)
    
    # 5. Vérifier qu'on a bien un objet JSON
    if not raw.startswith('{') or not raw.endswith('}'):
        logger.error(f"✗ Le texte ne commence pas par {{ ou ne finit pas par }}")
        logger.error(f"Début: {raw[:50]}")
        logger.error(f"Fin: {raw[-50:]}")
    
    # Log du JSON nettoyé
    logger.debug("="*80)
    logger.debug("JSON NETTOYÉ COMPLET:")
    logger.debug(raw)
    logger.debug("="*80)
    logger.info(f"Longueur JSON nettoyé: {len(raw)} caractères")
    
    # Tentative de parsing avec plusieurs stratégies
    try:
        # Stratégie principale : parsing standard
        parsed = json.loads(raw)
        logger.info(f"✓ JSON parsé avec succès, clés trouvées: {list(parsed.keys())}")
        return parsed
    except json.JSONDecodeError as e:
        # Log direct
        _write_debug("="*80)
        _write_debug(f"ERREUR JSON DECODE - position: {e.pos}")
        _write_debug(f"Message: {e.msg}")
        _write_debug(f"Ligne {e.lineno}, colonne {e.colno}")
        _write_debug(f"Réponse brute (200 premiers chars): {original_raw[:200]}")
        _write_debug("="*80)
        
        logger.error("="*80)
        logger.error(f"✗ ERREUR JSON DECODE à la position {e.pos}")
        logger.error(f"Message d'erreur: {e.msg}")
        logger.error(f"Ligne {e.lineno}, colonne {e.colno}")
        
        # Contexte autour de l'erreur
        error_start = max(0, e.pos - 100)
        error_end = min(len(raw), e.pos + 100)
        error_context = raw[error_start:error_end]
        
        # Marquer la position exacte de l'erreur
        marker_pos = min(100, e.pos - error_start)
        error_with_marker = error_context[:marker_pos] + " <<<ERREUR ICI>>> " + error_context[marker_pos:]
        
        logger.error("Contexte autour de l'erreur (200 chars):")
        logger.error(error_with_marker)
        logger.error("="*80)
        logger.error("RÉPONSE COMPLÈTE QUI A CAUSÉ L'ERREUR:")
        logger.error(original_raw[:2000])  # Premiers 2000 chars pour ne pas surcharger
        logger.error("="*80)
        
        # Flush explicite pour s'assurer que les logs sont écrits
        for handler in logger.handlers:
            handler.flush()
        
        raise


def analyze(transcription: str) -> AnalyzeResponse:
    """
    Analyse la transcription via le LLM configuré, parse le JSON et valide avec Pydantic.
    Lève ValueError en cas d'erreur LLM ou de JSON invalide.
    """
    # Log du provider utilisé
    provider = (LLM_PROVIDER or "openai").lower()
    
    # Log direct
    _write_debug("="*80)
    _write_debug(f"NOUVELLE REQUÊTE - Provider: {provider}, Modèle: {MODEL}")
    _write_debug(f"Longueur transcription: {len(transcription)} caractères")
    _write_debug("="*80)
    
    logger.info("="*80)
    logger.info(f"NOUVELLE REQUÊTE D'ANALYSE - Provider: {provider}, Modèle: {MODEL}")
    logger.info(f"Longueur transcription: {len(transcription)} caractères")
    logger.info("="*80)
    # Flush immédiat pour capturer la requête
    for handler in logger.handlers:
        handler.flush()
    
    if provider == "anthropic":
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY manquante. Définis-la dans ton .env.")
        raw = _call_anthropic(transcription)
    elif provider == "gemini":
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY manquante. Définis-la dans ton .env.")
        raw = _call_gemini(transcription)
    else:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY manquante. Définis-la dans ton .env.")
        raw = _call_openai(transcription)

    logger.info(f"Réponse LLM reçue, longueur: {len(raw)} caractères")
    # Flush pour s'assurer que les logs sont écrits immédiatement
    for handler in logger.handlers:
        handler.flush()
    
    try:
        obj = _extract_json(raw)
        logger.info(f"JSON parsé avec succès, clés: {list(obj.keys())}")
        # Flush après succès
        for handler in logger.handlers:
            handler.flush()
    except json.JSONDecodeError as e:
        # Message d'erreur plus détaillé avec un extrait de la réponse
        raw_preview = raw[:500] if len(raw) > 500 else raw
        error_msg = (
            f"Réponse LLM invalide (JSON illisible): {e}\n"
            f"Extrait de la réponse: {raw_preview}..."
        )
        logger.error(error_msg)
        raise ValueError(error_msg) from e

    try:
        result = AnalyzeResponse.model_validate(obj)
        logger.info("Validation Pydantic réussie")
        
        # Calcul automatique de la note basée sur les étapes accomplies
        # Pour chaque étape present=true, on compte 1 point
        # SAUF pour traitementObjections où present=false compte 1 point (logique inversée)
        points = 0
        if result.besoinExprime.present:
            points += 1
        if result.craintesFreins.present:
            points += 1
        if result.infosContexte.present:
            points += 1
        if result.budgetEstime.present:
            points += 1
        if result.verbatimPersonnalite.present:
            points += 1
        if result.verbatimPositif.present:
            points += 1
        if result.prochaineActionActee.present:
            points += 1
        # Logique inversée pour traitementObjections: pas d'objection = bon
        if not result.traitementObjections.present:
            points += 1
        
        # Note sur 10 = (points / 8) * 10
        total_etapes = 8
        result.noteGlobale = round((points / total_etapes) * 10, 1)
        
        logger.info(f"Note calculée automatiquement: {points}/{total_etapes} = {result.noteGlobale}/10")
        
        return result
    except ValidationError as e:
        error_msg = f"Réponse LLM ne respecte pas le schéma attendu: {e}\nObjet reçu: {obj}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e
