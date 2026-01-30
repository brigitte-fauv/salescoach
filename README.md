# SalesCoach

Application web qui coache les commerciaux en analysant une **transcription de RDV client** : note globale, étapes accomplies / manquantes, et signaux clés (besoin, craintes, contexte, budget, verbatims, prochaine action).

## Prérequis

- **Python 3.11+** (backend)
- **Node.js 18+** et **npm** (frontend)
- Clé API **OpenAI**, **Anthropic** ou **Google Gemini** (variable d’environnement)

## Installation

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
cp .env.example .env
```

Édite `backend/.env` et ajoute ta clé :

```env
OPENAI_API_KEY=sk-...
MODEL=gpt-4o-mini
```

Pour utiliser **Anthropic** à la place :

```env
ANTHROPIC_API_KEY=sk-ant-...
MODEL=claude-3-5-sonnet-20241022
LLM_PROVIDER=anthropic
```

Pour utiliser **Google Gemini** à la place :

```env
GEMINI_API_KEY=AIza...
MODEL=gemini-1.5-flash
LLM_PROVIDER=gemini
```

### Frontend

```bash
cd frontend
npm install
```

## Lancement

### Option 1 : tout en un (recommandé)

- **Double-clique** sur `Lancer-SalesCoach.bat` à la racine du projet,  
  **ou** ouvre **PowerShell** (hors Cursor), va dans le projet, puis exécute :

```powershell
cd chemin\vers\SALESCOACH
.\scripts\start-all.ps1
```

Au premier run, le script installe les deps (pip + npm), crée `backend\.env` si besoin, lance le backend dans une fenêtre dédiée et le frontend au premier plan. Ouvre **http://localhost:5173** dans ton navigateur. `Ctrl+C` arrête le frontend ; ferme la fenêtre du backend pour l’arrêter.

### Option 2 : manuelle

1. **Backend** (depuis `backend/`) :

```bash
cd backend
.venv\Scripts\activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

2. **Frontend** (depuis `frontend/`) :

```bash
cd frontend
npm run dev
```

3. Ouvre **http://localhost:5173**. Le frontend proxy les appels `/api` vers le backend sur le port 8000.

## Utilisation

- Colle la transcription du RDV dans la zone de texte, ou importe un fichier **.txt**.
- Clique sur **Analyser**.
- Consulte la **note globale** (/10), la **checklist** des étapes (✓ accomplies, ✗ manquantes) et le **détail des signaux**.

## Variables d’environnement

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Clé API OpenAI (si `LLM_PROVIDER=openai` ou non défini) |
| `ANTHROPIC_API_KEY` | Clé API Anthropic (si `LLM_PROVIDER=anthropic`) |
| `GEMINI_API_KEY` | Clé API Google Gemini (si `LLM_PROVIDER=gemini`) |
| `MODEL` | Modèle à utiliser (ex. `gpt-4o-mini`, `claude-3-5-sonnet-20241022`, `gemini-1.5-flash`) |
| `LLM_PROVIDER` | `openai`, `anthropic` ou `gemini` |
| `OPENAI_BASE_URL` | Optionnel ; URL de base pour l’API OpenAI |
| `REQUEST_TIMEOUT` | Timeout des appels LLM en secondes (défaut : 90) |

**Frontend (optionnel)** : `VITE_API_URL` pour l’URL de l’API (vide par défaut = même origine / proxy).

## Structure du projet

```
SALESCOACH/
├── backend/
│   ├── main.py           # FastAPI, route POST /api/analyze
│   ├── analyzer.py       # Appels LLM, parsing JSON, validation
│   ├── schemas.py        # Modèles Pydantic
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── api/          # Client fetch
│   │   ├── components/   # Formulaire, résultats, note, checklist
│   │   └── types.ts
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Sécurité

- Ne jamais committer le fichier `.env` ni les clés API (déjà dans `.gitignore`).
