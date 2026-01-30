# 🌐 Guide : URL Permanente pour SalesCoach

## 🎯 Objectif

Avoir une URL fixe (ex: `salescoach.votresite.com`) accessible 24/7 par vos collègues.

---

## ✅ Solution Recommandée : Cloudflare Tunnel + Compte Gratuit

### Avantages :
- ✅ **Gratuit** à vie
- ✅ **URL permanente** qui ne change jamais
- ✅ **Européen** (RGPD compliant)
- ✅ **Sécurisé** (HTTPS automatique)
- ✅ **Pas de domaine requis** (utilise `*.trycloudflare.com`)

---

## 📋 Étapes Complètes

### 🔧 Étape 1 : Créer un compte Cloudflare (5 min)

1. Allez sur : https://dash.cloudflare.com/sign-up
2. Créez un compte **gratuit**
3. Confirmez votre email

### 🔧 Étape 2 : Configuration du tunnel (5 min)

**Lancez :** `3-Configuration-URL-Permanente.bat`

Le script va :
1. Vous connecter à Cloudflare (page web)
2. Créer un tunnel nommé (ex: "salescoach")
3. Vous donner une URL permanente

### 🔧 Étape 3 : Lancement (2 min)

**Option A - Pour usage quotidien :**

1. Lancez : `2-Demarrer-Application.bat` (backend + frontend)
2. Lancez : `4-Demarrer-Tunnel-Permanent.bat` (tunnel)

**Option B - Script combiné :**

Créez un fichier `Tout-Demarrer.bat` :
```batch
@echo off
cd /d "%~dp0"

echo Demarrage du backend...
cd backend
start "Backend" cmd /k "python -m uvicorn main:app --reload"
cd ..

timeout /t 5

echo Demarrage du frontend...
cd frontend
start "Frontend" cmd /k "npm run dev"
cd ..

timeout /t 5

echo Demarrage du tunnel permanent...
start "Tunnel" cmd /k "cloudflared.exe tunnel --config config.yml run"

echo.
echo Tout est lance !
pause
```

---

## 🎯 Résultat

### URL permanente :
```
https://salescoach.trycloudflare.com
```

### Caractéristiques :
- ✅ Ne change **jamais**
- ✅ Accessible **24/7** (tant que votre PC est allumé)
- ✅ Pas besoin de **domaine personnalisé**
- ✅ HTTPS **automatique**

---

## 🌟 Bonus : Avec votre propre domaine

Si vous avez un domaine (ex: `votreentreprise.com`) :

### Dans Cloudflare Dashboard :

1. Ajoutez votre domaine à Cloudflare
2. Dans la configuration du tunnel, changez :
   ```
   hostname: salescoach.votreentreprise.com
   ```
3. L'URL devient : `https://salescoach.votreentreprise.com`

---

## 🔒 Sécurité Avancée (Optionnel)

Pour restreindre l'accès à vos collègues uniquement :

1. Dans Cloudflare Dashboard → Access
2. Créez une politique d'accès :
   - Emails autorisés : `@votreentreprise.com`
   - Ou liste d'emails spécifiques

---

## 🆘 Dépannage

### "tunnel login failed"
→ Vérifiez que vous êtes connecté à internet
→ Essayez dans un autre navigateur

### "config.yml not found"
→ Relancez `3-Configuration-URL-Permanente.bat`

### "Connection refused"
→ Vérifiez que l'application est lancée (backend + frontend)

---

## 💡 Alternative : Déploiement Cloud

Si vous voulez que l'app tourne **sans votre PC** :

### Render.com (Gratuit)
- Backend Python : Gratuit 750h/mois
- Frontend : Gratuit illimité
- URL : `https://votreapp.onrender.com`

### Voir le guide : `GUIDE-DEPLOIEMENT-CLOUD.md`

---

## 📞 Résumé

| Critère | Cloudflare Tunnel | Déploiement Cloud |
|---------|------------------|-------------------|
| 💰 Coût | Gratuit | Gratuit (limité) |
| 🖥️ PC requis | Oui | Non |
| 🌐 URL | Permanente | Permanente |
| ⚡ Setup | 10 min | 30 min |
| 🔧 Maintenance | Faible | Aucune |

**Pour commencer : Cloudflare Tunnel**
**Pour production : Déploiement Cloud**
