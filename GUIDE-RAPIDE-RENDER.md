# 🚀 Render.com en 15 Minutes - Guide Express

## 🎯 Ce que vous allez obtenir
```
URL permanente : https://salescoach-frontend.onrender.com
Accessible 24/7 depuis n'importe où
100% GRATUIT
```

---

## ✅ CHECKLIST RAPIDE

### ☐ ÉTAPE 1 : GitHub (5 min)
1. Créer un compte sur https://github.com/signup
2. Créer un nouveau dépôt nommé `salescoach`
3. Copier l'URL du dépôt

### ☐ ÉTAPE 2 : Pousser le code (3 min)
Ouvrir PowerShell dans ce dossier et taper :
```powershell
git init
git add .
git commit -m "Premier déploiement"
git branch -M main
git remote add origin https://github.com/VOTRE-NOM/salescoach.git
git push -u origin main
```

### ☐ ÉTAPE 3 : Render (7 min)
1. Aller sur https://render.com
2. Se connecter avec GitHub
3. Cliquer "New +" → "Blueprint"
4. Sélectionner le dépôt `salescoach`
5. Cliquer "Apply"
6. **IMPORTANT** : Ajouter `GEMINI_API_KEY` dans le backend
   - Aller dans "salescoach-backend" → "Environment"
   - Éditer `GEMINI_API_KEY` et coller votre clé
   - Sauvegarder

### ☐ ÉTAPE 4 : Attendre (5 min)
Render va installer et déployer automatiquement.
Vous verrez des logs défiler - c'est normal !

### ☐ ÉTAPE 5 : Tester
Une fois terminé, ouvrez :
```
https://salescoach-frontend.onrender.com
```

---

## 🆘 Git pas installé ?

### Méthode 1 : Installer Git (recommandé)
1. Télécharger : https://git-scm.com/download/win
2. Installer avec les options par défaut
3. Redémarrer PowerShell
4. Suivre l'ÉTAPE 2 ci-dessus

### Méthode 2 : GitHub Desktop (plus simple)
1. Télécharger : https://desktop.github.com/
2. Installer et se connecter avec GitHub
3. "Add Existing Repository" → Sélectionner ce dossier
4. "Publish repository" → Publier
5. Continuer à l'ÉTAPE 3 (Render)

---

## 🔑 Où trouver ma clé GEMINI_API_KEY ?

Votre clé est dans le fichier `.env` du dossier `backend` :
```
backend/.env
```

Ou créez-en une nouvelle sur :
https://aistudio.google.com/apikey

---

## ⚡ Commandes PowerShell à copier-coller

### Pour pousser le code sur GitHub :
```powershell
cd "C:\Users\brigi\Desktop\SALESCOACH"
git init
git add .
git commit -m "Déploiement SalesCoach"
git branch -M main
git remote add origin https://github.com/VOTRE-NOM/salescoach.git
git push -u origin main
```

⚠️ **Remplacez** `VOTRE-NOM` par votre nom d'utilisateur GitHub !

---

## 🎯 Après le déploiement

### Mettre à jour l'application :
```powershell
git add .
git commit -m "Mes modifications"
git push
```
Render redéploie **automatiquement** ! ✨

### Voir les logs :
- Dashboard Render → Service → Onglet "Logs"

### Redémarrer un service :
- Dashboard Render → Service → "Manual Deploy" → "Deploy latest commit"

---

## 💡 Info importante

### Premier chargement lent ?
Les apps gratuites Render "s'endorment" après 15 min d'inactivité.
Le **premier chargement** met ~30 secondes (réveil).
Ensuite c'est **instantané** ! ⚡

---

## ✅ Vous êtes prêt !

**Fichiers créés :**
- ✅ `render.yaml` : Configuration Render
- ✅ `DEPLOYER-SUR-RENDER.md` : Guide détaillé
- ✅ `GUIDE-RAPIDE-RENDER.md` : Ce guide rapide

**Prochaine étape :**
👉 Suivez la checklist ci-dessus étape par étape

**Besoin d'aide ?**
Dites-moi à quelle étape vous êtes et je vous guide ! 🚀
