# 🇪🇺 Partager SalesCoach avec vos collègues

## Solution : Cloudflare Tunnel (Européen, Gratuit, Sécurisé)

---

## 📋 Étapes rapides

### 1️⃣ Installation (une seule fois)

Double-cliquez sur : **`installer-cloudflare.ps1`**

Cela télécharge automatiquement Cloudflare Tunnel (~50 MB).

---

### 2️⃣ Lancement avec partage

Double-cliquez sur : **`Lancer-Partage.bat`**

Cela lance :
- ✅ L'application SalesCoach (backend + frontend)
- ✅ Le tunnel Cloudflare qui crée une URL publique

---

### 3️⃣ Partager l'URL

Une fenêtre s'ouvre avec un message comme :

```
+--------------------------------------------------------------------------------------------+
|  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):
|  https://random-name-1234.trycloudflare.com
+--------------------------------------------------------------------------------------------+
```

**Copiez cette URL et envoyez-la à vos collègues !**

---

## ✅ Avantages Cloudflare

| Critère | Cloudflare Tunnel |
|---------|------------------|
| 🇪🇺 **Européen** | ✅ Serveurs en Europe, RGPD compliant |
| 💰 **Coût** | ✅ 100% gratuit, pas de limite |
| 🔒 **Sécurité** | ✅ Chiffrement SSL automatique |
| 🚀 **Performance** | ✅ CDN Cloudflare (très rapide) |
| ⏰ **Durée** | ⚠️ Temporaire (expire à la fermeture) |
| 🌍 **Accès** | ✅ Depuis n'importe où dans le monde |

---

## ⚠️ Important

- **Laissez les fenêtres ouvertes** : Ne fermez ni la fenêtre de l'app, ni celle de Cloudflare
- **Votre PC doit rester allumé** : L'application tourne sur votre machine
- **URL temporaire** : Chaque lancement génère une nouvelle URL
- **Pas de compte requis** : Cloudflare Tunnel fonctionne sans inscription

---

## 🔧 Alternative : Cloudflare avec compte (URL permanente)

Si vous voulez une URL fixe qui ne change jamais :

1. Créez un compte sur https://dash.cloudflare.com/
2. Suivez ce guide : https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-local-tunnel/
3. Vous aurez une URL permanente comme `salescoach.votredomaine.com`

---

## 📞 Support

Si ça ne fonctionne pas :
- Vérifiez que votre pare-feu/antivirus n'est pas trop strict
- Essayez de relancer l'application
- Vérifiez que les ports 8000 et 5173 ne sont pas utilisés par une autre app
