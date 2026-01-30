# 🚀 Guide Complet : Déployer SalesCoach sur Render.com

## ✅ Fichiers créés
- `render.yaml` : Configuration automatique pour Render

---

## 📝 ÉTAPE 1 : Créer un compte GitHub (5 min)

### Si vous n'avez PAS encore de compte GitHub :

1. Allez sur **https://github.com/signup**
2. Créez un compte gratuit avec votre email
3. Vérifiez votre email
4. Connectez-vous à GitHub

---

## 📤 ÉTAPE 2 : Créer un dépôt GitHub (2 min)

1. Sur GitHub, cliquez sur le **bouton vert "New"** (en haut à gauche)
2. Nom du dépôt : `salescoach`
3. Description : "Application d'analyse de ventes avec IA"
4. Laissez **Public**
5. **NE cochez PAS** "Add a README file"
6. Cliquez **"Create repository"**

📋 **Notez l'URL** qui apparaît (exemple : `https://github.com/VOTRE-NOM/salescoach.git`)

---

## 💻 ÉTAPE 3 : Pousser le code sur GitHub (5 min)

### Option A : Avec Git installé

Ouvrez PowerShell dans le dossier `SALESCOACH` et exécutez :

```powershell
# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Créer le premier commit
git commit -m "Initial commit - SalesCoach"

# Renommer la branche en main
git branch -M main

# Lier à votre dépôt GitHub (REMPLACEZ par VOTRE URL)
git remote add origin https://github.com/VOTRE-NOM/salescoach.git

# Pousser le code
git push -u origin main
```

### Option B : Sans Git (méthode manuelle)

1. Téléchargez **GitHub Desktop** : https://desktop.github.com/
2. Installez-le et connectez-vous avec votre compte GitHub
3. Cliquez **"Add an Existing Repository"**
4. Sélectionnez le dossier `SALESCOACH`
5. Cliquez **"Publish repository"**

---

## 🌐 ÉTAPE 4 : Déployer sur Render (5 min)

### 1. Créer un compte Render

1. Allez sur **https://render.com**
2. Cliquez **"Get Started for Free"**
3. Choisissez **"Sign in with GitHub"**
4. Autorisez Render à accéder à GitHub

### 2. Créer un Blueprint

1. Dans le dashboard Render, cliquez **"New +"** (en haut à droite)
2. Sélectionnez **"Blueprint"**
3. Connectez votre compte GitHub si demandé
4. Cherchez et sélectionnez votre dépôt **"salescoach"**
5. Cliquez **"Connect"**

### 3. Configuration automatique

Render va détecter le fichier `render.yaml` et vous montrer :
- ✅ Backend : `salescoach-backend`
- ✅ Frontend : `salescoach-frontend`

Cliquez **"Apply"** pour démarrer le déploiement

### 4. Ajouter la clé API Gemini

⚠️ **IMPORTANT** : Pendant le déploiement, vous verrez un message pour configurer `GEMINI_API_KEY`

1. Cliquez sur **"salescoach-backend"** dans la liste
2. Allez dans l'onglet **"Environment"**
3. Trouvez `GEMINI_API_KEY`
4. Cliquez **"Edit"** et collez votre clé API Gemini
5. Cliquez **"Save Changes"**

---

## ⏱️ ÉTAPE 5 : Attendre le déploiement (5-10 min)

Render va :
1. ✅ Installer les dépendances Python (backend)
2. ✅ Installer les dépendances Node (frontend)
3. ✅ Builder le frontend React
4. ✅ Démarrer les 2 services

Vous verrez des logs défiler. C'est normal !

---

## 🎉 ÉTAPE 6 : Récupérer vos URLs

Une fois terminé, vous aurez **2 URLs permanentes** :

```
Backend:  https://salescoach-backend.onrender.com
Frontend: https://salescoach-frontend.onrender.com
```

✅ **Partagez l'URL du Frontend** avec qui vous voulez !

---

## 🔧 Configuration du Frontend

Si le frontend ne se connecte pas au backend :

1. Allez dans **salescoach-frontend** sur Render
2. Onglet **"Environment"**
3. Vérifiez que `VITE_API_URL` pointe vers l'URL exacte du backend
4. Format : `https://salescoach-backend.onrender.com` (SANS slash à la fin)
5. Sauvegardez et redémarrez le service

---

## 📱 Tester l'application

1. Ouvrez l'URL frontend dans votre navigateur
2. Collez une transcription de vente
3. Cliquez "Analyser"
4. ✅ Ça marche !

---

## 🔄 Mettre à jour l'application

Quand vous modifiez le code :

```powershell
git add .
git commit -m "Description des changements"
git push
```

Render **redéploie automatiquement** ! 🚀

---

## 💡 Astuces

### Premier déploiement lent ?
- Le **premier déploiement** prend 5-10 minutes
- Les suivants sont **plus rapides** (2-3 min)

### Application "endormie" ?
- Render met les apps gratuites en **veille après 15 min d'inactivité**
- Premier chargement = **30 secondes** de réveil
- Ensuite = **instantané**

### Logs et debugging
- Dans Render Dashboard → Service → Onglet **"Logs"**
- Vous voyez tous les logs en temps réel

---

## ❓ Problèmes courants

### "Build failed"
→ Vérifiez que `render.yaml` est bien à la racine du projet

### "GEMINI_API_KEY not found"
→ Ajoutez la clé dans Environment Variables du backend

### Frontend ne charge pas
→ Vérifiez que `VITE_API_URL` pointe vers le backend

### "Service unavailable"
→ Attendez 30 secondes (réveil de l'app gratuite)

---

## 🎯 Résultat Final

✅ Application accessible **24/7** de n'importe où
✅ URL permanente **https://salescoach-frontend.onrender.com**
✅ HTTPS automatique (sécurisé)
✅ Mises à jour automatiques via Git
✅ **100% GRATUIT**

---

## 📞 Besoin d'aide ?

Si vous bloquez à une étape, je suis là pour vous aider ! 🚀
