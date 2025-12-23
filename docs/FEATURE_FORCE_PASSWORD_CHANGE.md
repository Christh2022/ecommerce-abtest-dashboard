# 🔐 Changement de Mot de Passe Obligatoire - Première Connexion

## ✅ Fonctionnalité Ajoutée

Le système d'authentification force maintenant les utilisateurs à changer leur mot de passe lors de la première connexion, une excellente pratique de sécurité !

---

## 🎯 Comment ça fonctionne

### Flux d'authentification avec changement de mot de passe

```
1. Utilisateur se connecte avec mot de passe par défaut
   ↓
2. Système détecte force_password_change = True
   ↓
3. Redirection automatique vers /change-password
   ↓
4. Utilisateur doit créer un nouveau mot de passe fort
   ↓
5. Validation des exigences de sécurité
   ↓
6. Mot de passe changé, force_password_change = False
   ↓
7. Redirection vers le dashboard
```

---

## 🆕 Nouveaux fichiers créés

### 1. Page de changement de mot de passe
**Fichier** : [dashboard/pages/change_password.py](dashboard/pages/change_password.py)

**Fonctionnalités** :
- ✅ Interface moderne et intuitive
- ✅ Validation en temps réel du mot de passe
- ✅ Indicateur de force du mot de passe
- ✅ Vérification des exigences (majuscule, minuscule, chiffre, longueur)
- ✅ Confirmation du mot de passe
- ✅ Impossibilité de contourner (si forcé)

---

## 🔧 Modifications apportées

### 1. Module d'authentification (`auth.py`)

#### Classe User
```python
class User(UserMixin):
    def __init__(self, id, username, email=None, role='user', force_password_change=False):
        # ...
        self.force_password_change = force_password_change  # NOUVEAU
```

#### Comptes par défaut
```python
default_users = {
    'admin': {
        # ...
        'force_password_change': True  # NOUVEAU - Force le changement
    },
    'user': {
        # ...
        'force_password_change': True  # NOUVEAU - Force le changement
    }
}
```

#### Nouvelle méthode
```python
def change_password(self, username, new_password):
    """Change user password and remove force_password_change flag"""
    # Change le mot de passe
    # Met force_password_change à False
    # Sauvegarde dans users.json
```

### 2. Middleware d'authentification (`app.py`)

```python
@server.before_request
def check_authentication():
    # Vérification authentification existante
    
    # NOUVEAU - Vérification changement de mot de passe obligatoire
    if current_user.is_authenticated and \
       hasattr(current_user, 'force_password_change') and \
       current_user.force_password_change and \
       not request.path.startswith('/change-password'):
        return redirect('/change-password')
```

### 3. Page de login (`login.py`)

Ajout d'une alerte informative :
```python
dbc.Alert([
    html.I(className="fas fa-info-circle me-2"),
    html.Strong("Première connexion : "),
    "Vous devrez changer votre mot de passe après la première connexion."
], color="info")
```

---

## 🛡️ Exigences de sécurité du mot de passe

Le nouveau mot de passe doit respecter :

1. ✅ **Longueur minimale** : Au moins 8 caractères
2. ✅ **Majuscule** : Au moins une lettre majuscule (A-Z)
3. ✅ **Minuscule** : Au moins une lettre minuscule (a-z)
4. ✅ **Chiffre** : Au moins un chiffre (0-9)

### Indicateur de force

- 🔴 **Faible** : Moins de 3 critères respectés
- 🟠 **Moyen** : 3 critères respectés
- 🟢 **Fort** : Tous les critères respectés

---

## 🎨 Interface de changement de mot de passe

### Éléments visuels

1. **Icône de clé** 🔑 en haut de page
2. **Alerte d'avertissement** (si forcé) pour informer l'utilisateur
3. **Indicateur de force du mot de passe** en temps réel
4. **Checklist visuelle** avec icônes :
   - ⚪ Critère non respecté
   - ✅ Critère respecté
5. **Messages d'erreur clairs** si problème
6. **Bouton de validation vert** pour confirmer
7. **Bouton annuler** (seulement si changement optionnel)

---

## 🚀 Test de la fonctionnalité

### Scénario 1 : Première connexion avec admin

1. Démarrez le dashboard :
   ```bash
   cd dashboard
   python app.py
   ```

2. Ouvrez http://localhost:8050

3. Connectez-vous avec :
   - Username: `admin`
   - Password: `admin123`

4. **Résultat attendu** : 
   - ✅ Connexion réussie
   - ✅ Redirection automatique vers `/change-password`
   - ✅ Message indiquant le changement obligatoire

5. Essayez d'accéder à une autre page (ex: `/traffic`) :
   - ✅ Redirection vers `/change-password`
   - ✅ Impossible de contourner

6. Changez le mot de passe :
   - Entrez : `Admin2024!` (respecte tous les critères)
   - Confirmez : `Admin2024!`
   - Cliquez sur "Changer le mot de passe"

7. **Résultat attendu** :
   - ✅ Message de succès
   - ✅ Redirection vers `/`
   - ✅ Accès libre au dashboard

8. Déconnectez-vous et reconnectez-vous avec le nouveau mot de passe :
   - Username: `admin`
   - Password: `Admin2024!`
   - ✅ Pas de redirection vers change-password

---

### Scénario 2 : Mot de passe faible

1. Lors du changement, essayez : `test`
   - ❌ Trop court (< 8 caractères)
   - ❌ Pas de majuscule
   - ❌ Pas de chiffre
   - 🔴 Indicateur : "Mot de passe faible"

2. Essayez : `testtest`
   - ❌ Pas de majuscule
   - ❌ Pas de chiffre
   - 🔴 Indicateur : "Mot de passe faible"

3. Essayez : `Testtest`
   - ✅ Longueur OK
   - ✅ Majuscule OK
   - ✅ Minuscule OK
   - ❌ Pas de chiffre
   - 🟠 Indicateur : "Mot de passe moyen"

4. Essayez : `Testtest1`
   - ✅ Tous les critères
   - 🟢 Indicateur : "Mot de passe fort"
   - ✅ Peut être sauvegardé

---

### Scénario 3 : Mots de passe ne correspondent pas

1. Nouveau mot de passe : `Admin2024!`
2. Confirmation : `Admin2024`
3. Cliquez sur "Changer le mot de passe"
4. **Résultat** :
   - ❌ Erreur : "Les mots de passe ne correspondent pas"
   - 🔴 Alert rouge affichée

---

## 📊 Structure des données

### Fichier users.json

```json
{
  "admin": {
    "id": "1",
    "username": "admin",
    "password": "scrypt:32768:8:1$...",
    "email": "admin@example.com",
    "role": "admin",
    "force_password_change": true    ← NOUVEAU champ
  },
  "john": {
    "id": "3",
    "username": "john",
    "password": "scrypt:32768:8:1$...",
    "email": "john@example.com",
    "role": "user",
    "force_password_change": false   ← False après changement
  }
}
```

---

## 🔐 Sécurité

### Améliorations apportées

1. ✅ **Mots de passe forts obligatoires**
   - Validation stricte côté serveur
   - Feedback visuel temps réel

2. ✅ **Impossible de contourner**
   - Middleware vérifie à chaque requête
   - Seules exceptions : /login, /logout, /change-password

3. ✅ **Comptes par défaut sécurisés**
   - Force le changement dès la première connexion
   - Élimine les mots de passe par défaut

4. ✅ **Journalisation**
   - Tous les changements sont enregistrés
   - Traçabilité complète

---

## 🎓 Pour les développeurs

### Ajouter un utilisateur avec changement forcé

```python
from dashboard.auth import AuthManager
from dashboard.app import server

auth = AuthManager(server)

# Utilisateur devra changer son mot de passe
auth.users_db['newuser'] = {
    'id': '4',
    'username': 'newuser',
    'password': generate_password_hash('TempPass123'),
    'email': 'newuser@example.com',
    'role': 'user',
    'force_password_change': True  # Force le changement
}

# Sauvegarder
import json
with open('dashboard/users.json', 'w') as f:
    json.dump(auth.users_db, f, indent=2)
```

### Désactiver le changement forcé pour un utilisateur

```python
# Si vous voulez permettre à un utilisateur de garder son mot de passe
auth.users_db['admin']['force_password_change'] = False

# Sauvegarder
import json
with open('dashboard/users.json', 'w') as f:
    json.dump(auth.users_db, f, indent=2)
```

---

## 🔄 Migration depuis l'ancienne version

Si vous avez déjà des utilisateurs sans le champ `force_password_change` :

### Option 1 : Automatique (recommandé)

Le système gère automatiquement les utilisateurs existants :
- Si `force_password_change` n'existe pas → considéré comme `False`
- L'utilisateur peut se connecter normalement

### Option 2 : Forcer tous les utilisateurs existants

```python
import json

# Charger users.json
with open('dashboard/users.json', 'r') as f:
    users = json.load(f)

# Ajouter force_password_change pour tous
for username in users:
    if 'force_password_change' not in users[username]:
        users[username]['force_password_change'] = True

# Sauvegarder
with open('dashboard/users.json', 'w') as f:
    json.dump(users, f, indent=2)

print("✅ Tous les utilisateurs devront changer leur mot de passe")
```

---

## 📝 Journaux (Logs)

### Exemples de logs

```bash
# Redirection vers changement de mot de passe
INFO - Redirecting admin to change password

# Changement réussi
INFO - Password changed successfully for user: admin

# Tentative échouée
ERROR - Failed to change password for user: admin

# Accès à la page de changement
INFO - Request: GET /change-password from 127.0.0.1 - User: admin
```

---

## 🆘 Dépannage

### Problème : Boucle infinie vers /change-password

**Cause** : Le mot de passe n'a pas été changé correctement dans users.json

**Solution** :
```python
import json

# Forcer force_password_change à False
with open('dashboard/users.json', 'r') as f:
    users = json.load(f)

users['admin']['force_password_change'] = False

with open('dashboard/users.json', 'w') as f:
    json.dump(users, f, indent=2)
```

---

### Problème : Impossible de changer le mot de passe

**Cause** : Permissions d'écriture sur users.json

**Solution** :
```bash
# Windows
attrib -r dashboard\users.json

# Linux/Mac
chmod 644 dashboard/users.json
```

---

### Problème : L'indicateur de force ne s'affiche pas

**Cause** : JavaScript ou callback non chargé

**Solution** : 
- Videz le cache du navigateur (Ctrl+F5)
- Vérifiez les logs pour erreurs JavaScript

---

## ✨ Améliorations futures possibles

- [ ] Politique de renouvellement régulier (ex: tous les 90 jours)
- [ ] Historique des anciens mots de passe (éviter réutilisation)
- [ ] Envoi d'email de confirmation après changement
- [ ] Option "Afficher le mot de passe" avec icône œil
- [ ] Générateur de mot de passe fort
- [ ] Score de force plus détaillé (avec caractères spéciaux)
- [ ] Authentification à deux facteurs (2FA)

---

## 🎉 Résumé

### Ce qui a été ajouté

1. ✅ Page de changement de mot de passe (`change_password.py`)
2. ✅ Champ `force_password_change` dans le modèle User
3. ✅ Méthode `change_password()` dans AuthManager
4. ✅ Middleware de redirection automatique
5. ✅ Validation de force du mot de passe
6. ✅ Interface utilisateur moderne et claire
7. ✅ Exigences de sécurité strictes
8. ✅ Journalisation des changements

### Bénéfices sécurité

- 🛡️ Élimine les mots de passe par défaut
- 🛡️ Force des mots de passe forts
- 🛡️ Impossible à contourner
- 🛡️ Traçabilité complète
- 🛡️ Conformité aux bonnes pratiques

---

## 🚀 Pour commencer

1. **Aucune installation supplémentaire nécessaire** (même dépendances)

2. **Lancez le dashboard** :
   ```bash
   cd dashboard
   python app.py
   ```

3. **Connectez-vous** avec `admin` / `admin123`

4. **Suivez les instructions** pour changer votre mot de passe

5. **Profitez du dashboard sécurisé** ! 🎊

---

**Créé le** : 13 décembre 2025  
**Fonctionnalité** : Changement de mot de passe obligatoire  
**Status** : ✅ Prêt à l'emploi  
**Sécurité** : 🛡️ Renforcée
