# 🔐 Changement de Mot de Passe Obligatoire - Guide Rapide

## 🎯 Nouvelle Fonctionnalité Ajoutée !

Lors de la **première connexion**, les utilisateurs sont maintenant **obligés de changer leur mot de passe**. C'est une excellente pratique de sécurité qui élimine les risques liés aux mots de passe par défaut.

---

## 🚀 Test Rapide (2 minutes)

### Étape 1 : Connexion initiale
```
1. Ouvrez http://localhost:8050
2. Connectez-vous avec : admin / admin123
```

### Étape 2 : Redirection automatique
```
➜ Vous êtes automatiquement redirigé vers /change-password
➜ Un message vous informe du changement obligatoire
➜ Impossible d'accéder au dashboard sans changer le mot de passe
```

### Étape 3 : Créer un nouveau mot de passe
```
Nouveau mot de passe : Admin2024!
Confirmer : Admin2024!

Cliquez sur "Changer le mot de passe"
```

### Étape 4 : Accès au dashboard
```
✅ Mot de passe changé avec succès
✅ Redirection vers le dashboard
✅ Vous pouvez maintenant naviguer librement
```

---

## 📋 Exigences du Mot de Passe

Votre nouveau mot de passe doit contenir :

| Critère | Exigence |
|---------|----------|
| 📏 **Longueur** | Minimum 8 caractères |
| 🔤 **Majuscule** | Au moins 1 lettre majuscule (A-Z) |
| 🔡 **Minuscule** | Au moins 1 lettre minuscule (a-z) |
| 🔢 **Chiffre** | Au moins 1 chiffre (0-9) |

### Exemples

| Mot de passe | Status | Raison |
|--------------|--------|--------|
| `admin` | ❌ Refusé | Trop court, pas de majuscule, pas de chiffre |
| `Admin123` | ❌ Refusé | Trop court (< 8 caractères) |
| `adminadmin` | ❌ Refusé | Pas de majuscule, pas de chiffre |
| `AdminAdmin` | ❌ Refusé | Pas de chiffre |
| `Admin2024` | ✅ Accepté | Respecte tous les critères |
| `Admin2024!` | ✅ Accepté | Fort avec caractère spécial |

---

## 🎨 Interface

### Page de changement de mot de passe

```
┌─────────────────────────────────────────────────────┐
│                       🔑                             │
│         Changement de mot de passe                   │
│    Vous devez changer votre mot de passe             │
│                                                       │
├─────────────────────────────────────────────────────┤
│  ⚠️ Changement obligatoire                           │
│  Vous utilisez un mot de passe par défaut           │
├─────────────────────────────────────────────────────┤
│  👤 Utilisateur : admin                              │
│                                                       │
│  Nouveau mot de passe                                │
│  [••••••••••••••]                                    │
│  ✓ Mot de passe fort                                 │
│                                                       │
│  Confirmer le mot de passe                           │
│  [••••••••••••••]                                    │
│                                                       │
│  Exigences du mot de passe:                          │
│  ✅ Au moins 8 caractères                            │
│  ✅ Au moins une majuscule                           │
│  ✅ Au moins une minuscule                           │
│  ✅ Au moins un chiffre                              │
│                                                       │
│  [  ✓ Changer le mot de passe  ]                    │
└─────────────────────────────────────────────────────┘
```

### Indicateur de force en temps réel

Pendant que vous tapez, l'indicateur change :

```
Mot de passe : test
🔴 ✗ Mot de passe faible

Mot de passe : testtest
🔴 ✗ Mot de passe faible

Mot de passe : Testtest
🟠 ⚠ Mot de passe moyen

Mot de passe : Testtest1
🟢 ✓ Mot de passe fort
```

---

## 📁 Fichiers Modifiés/Créés

### Nouveau fichier
- ✨ `dashboard/pages/change_password.py` - Page de changement de mot de passe

### Fichiers modifiés
- ✏️ `dashboard/auth.py` - Ajout de `force_password_change` et méthode `change_password()`
- ✏️ `dashboard/app.py` - Middleware de redirection
- ✏️ `dashboard/pages/login.py` - Alerte informative

---

## 🔧 Pour les Administrateurs

### Réinitialiser un utilisateur

Si vous voulez forcer un utilisateur à changer son mot de passe :

```python
import json

# Charger users.json
with open('dashboard/users.json', 'r') as f:
    users = json.load(f)

# Forcer le changement pour un utilisateur
users['john']['force_password_change'] = True

# Sauvegarder
with open('dashboard/users.json', 'w') as f:
    json.dump(users, f, indent=2)
```

### Créer un utilisateur avec changement forcé

```python
from dashboard.auth import AuthManager
from werkzeug.security import generate_password_hash

auth = AuthManager(server)
auth.users_db['newuser'] = {
    'id': '4',
    'username': 'newuser',
    'password': generate_password_hash('TempPass123'),
    'email': 'newuser@example.com',
    'role': 'user',
    'force_password_change': True  # ← Force le changement
}
```

---

## 🛡️ Sécurité

### Pourquoi cette fonctionnalité ?

1. ✅ **Élimine les mots de passe par défaut**
   - Les comptes admin/admin123 ne peuvent plus être utilisés longtemps
   
2. ✅ **Force des mots de passe forts**
   - Validation stricte : majuscule, minuscule, chiffre, longueur
   
3. ✅ **Impossible à contourner**
   - Redirection automatique à chaque requête
   - Seule exception : page de changement elle-même
   
4. ✅ **Conformité aux standards**
   - Respecte les recommandations OWASP
   - Pratique courante dans les applications professionnelles

---

## 🔍 Vérification

### Checklist après mise en œuvre

- [ ] Connexion avec admin/admin123 fonctionne
- [ ] Redirection automatique vers /change-password
- [ ] Impossible d'accéder à /traffic sans changer le mot de passe
- [ ] Validation des exigences fonctionne (essayez "test" → refusé)
- [ ] Indicateur de force s'affiche en temps réel
- [ ] Changement de mot de passe réussit avec "Admin2024!"
- [ ] Redirection vers / après changement
- [ ] Reconnexion avec nouveau mot de passe fonctionne
- [ ] Pas de redirection vers /change-password après changement

---

## 🆘 Problèmes Courants

### "Je suis bloqué en boucle sur /change-password"

**Solution** : Éditez manuellement `users.json` :
```json
{
  "admin": {
    "force_password_change": false
  }
}
```

### "Mon mot de passe est refusé"

**Vérifiez** :
- ✅ Au moins 8 caractères
- ✅ Au moins 1 majuscule
- ✅ Au moins 1 minuscule  
- ✅ Au moins 1 chiffre

### "L'indicateur de force ne s'affiche pas"

**Solution** : Videz le cache du navigateur (Ctrl+F5)

---

## 📚 Documentation Complète

Pour plus de détails, consultez :
- 📖 [FEATURE_FORCE_PASSWORD_CHANGE.md](FEATURE_FORCE_PASSWORD_CHANGE.md) - Documentation complète
- 📖 [AUTH_README.md](../dashboard/AUTH_README.md) - Système d'authentification
- 📖 [AUTHENTICATION_SETUP.md](AUTHENTICATION_SETUP.md) - Guide de configuration

---

## ✅ Résumé

### Avant
```
1. Login : admin / admin123
2. ➜ Accès direct au dashboard
3. ⚠️ Mot de passe par défaut non changé
```

### Maintenant
```
1. Login : admin / admin123
2. ➜ Redirection vers /change-password
3. Changement obligatoire : Admin2024!
4. ➜ Accès au dashboard
5. ✅ Mot de passe sécurisé
```

---

**🎉 Votre dashboard est maintenant plus sécurisé !**

Pour tester immédiatement :
```bash
cd dashboard && python app.py
```
Puis connectez-vous avec `admin` / `admin123` 🚀
