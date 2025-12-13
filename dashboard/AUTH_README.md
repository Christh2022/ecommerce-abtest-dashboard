# Système d'Authentification - Dashboard E-Commerce

## 📋 Vue d'ensemble

Le dashboard E-Commerce dispose maintenant d'un système d'authentification complet basé sur Flask-Login. Tous les utilisateurs doivent se connecter avant d'accéder aux pages du dashboard.

## 🔐 Caractéristiques

- **Authentification par session** : Utilise Flask-Login pour gérer les sessions utilisateurs
- **Protection des routes** : Toutes les pages du dashboard nécessitent une authentification
- **Gestion des mots de passe** : Hachage sécurisé avec Werkzeug
- **Option "Se souvenir de moi"** : Session persistante disponible
- **Interface de connexion moderne** : Design cohérent avec le thème du dashboard
- **Journalisation** : Tous les événements d'authentification sont enregistrés

## 👥 Comptes par défaut

Le système inclut deux comptes de démonstration :

### Compte Administrateur

- **Nom d'utilisateur** : `admin`
- **Mot de passe** : `admin123`
- **Rôle** : Administrateur
- **Email** : admin@example.com

### Compte Utilisateur

- **Nom d'utilisateur** : `user`
- **Mot de passe** : `user123`
- **Rôle** : Utilisateur
- **Email** : user@example.com

## 🚀 Utilisation

### Connexion

1. Accédez au dashboard : `http://localhost:8050`
2. Vous serez automatiquement redirigé vers `/login`
3. Entrez vos identifiants
4. Cochez "Se souvenir de moi" pour une session persistante (24h)
5. Cliquez sur "Se connecter"

### Déconnexion

- Cliquez sur le bouton "Déconnexion" dans la barre latérale
- Ou accédez à `/logout`

## 🔧 Configuration

### Variables d'environnement

Créez un fichier `.env` dans le dossier `dashboard/` :

```bash
# Clé secrète pour les sessions (CHANGEZ EN PRODUCTION!)
SECRET_KEY=votre-cle-secrete-super-longue-et-aleatoire

# Durée de session (en secondes)
SESSION_LIFETIME=86400  # 24 heures par défaut
```

### Ajouter des utilisateurs

Les utilisateurs sont stockés dans `dashboard/users.json`. Pour ajouter un nouvel utilisateur :

1. **Via Python** (recommandé) :

```python
from dashboard.auth import AuthManager
from dashboard.app import server

auth = AuthManager(server)
auth.add_user(
    username='nouvel_utilisateur',
    password='mot_de_passe',
    email='email@example.com',
    role='user'  # ou 'admin'
)
```

2. **Manuellement** : Éditez `users.json` (nécessite le hachage du mot de passe) :

```python
from werkzeug.security import generate_password_hash
print(generate_password_hash('votre_mot_de_passe'))
```

## 📁 Structure des fichiers

```
dashboard/
├── app.py                    # Application principale avec middleware d'auth
├── auth.py                   # Module de gestion d'authentification
├── users.json                # Base de données des utilisateurs (créé auto)
├── users.json.example        # Exemple de structure
├── requirements.txt          # Dépendances (inclut flask-login, dash-auth)
└── pages/
    ├── login.py              # Page de connexion
    ├── logout.py             # Page de déconnexion
    └── ...                   # Autres pages (protégées)
```

## 🛡️ Sécurité

### Bonnes pratiques implémentées

- ✅ Mots de passe hachés avec `scrypt` (via Werkzeug)
- ✅ Sessions sécurisées avec clé secrète
- ✅ Protection CSRF automatique (Flask)
- ✅ Journalisation des tentatives de connexion
- ✅ Redirection automatique si non authentifié

### Recommandations pour la production

1. **Changez la clé secrète** :

   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

   Utilisez cette valeur pour `SECRET_KEY`

2. **Utilisez HTTPS** : Déployez derrière un reverse proxy SSL (nginx, Apache)

3. **Base de données** : Remplacez `users.json` par une vraie base de données (PostgreSQL, MySQL)

4. **Limiter les tentatives** : Ajoutez un rate limiting sur les connexions

5. **MFA** : Envisagez l'authentification à deux facteurs pour les comptes admin

## 🔄 Migration depuis l'ancienne version

Si vous utilisez une ancienne version du dashboard sans authentification :

1. Installez les nouvelles dépendances :

   ```bash
   cd dashboard
   pip install -r requirements.txt
   ```

2. Le fichier `users.json` sera créé automatiquement au premier lancement

3. Relancez l'application :
   ```bash
   python app.py
   ```

## 🧪 Tests

Pour tester l'authentification :

```bash
# Lancez le dashboard
python dashboard/app.py

# Dans un navigateur
# 1. Accédez à http://localhost:8050
# 2. Essayez d'accéder directement à http://localhost:8050/traffic (redirigé vers login)
# 3. Connectez-vous avec admin/admin123
# 4. Vérifiez que vous pouvez accéder aux pages
# 5. Déconnectez-vous et vérifiez la redirection
```

## 📝 Journaux

Les événements d'authentification sont enregistrés :

```
INFO - Successful login: admin
WARNING - Failed login attempt: wronguser
WARNING - Unauthorized access attempt to /traffic from 127.0.0.1
INFO - User logged out: admin
```

## 🆘 Dépannage

### "ImportError: cannot import name 'AuthManager'"

Solution : Assurez-vous que `auth.py` existe dans le dossier `dashboard/`

### "Redirection infinie entre / et /login"

Solution : Vérifiez que le middleware `check_authentication` dans `app.py` est correctement configuré

### "Session expirée trop rapidement"

Solution : Augmentez `PERMANENT_SESSION_LIFETIME` dans la configuration

### "Impossible de se connecter avec les identifiants par défaut"

Solution : Supprimez `users.json` et relancez l'application pour régénérer les comptes

## 🔮 Améliorations futures

- [ ] Interface d'administration des utilisateurs
- [ ] Authentification OAuth2 (Google, GitHub, etc.)
- [ ] Authentification à deux facteurs (2FA)
- [ ] Rôles et permissions granulaires
- [ ] Historique des connexions
- [ ] Récupération de mot de passe par email
- [ ] Politique de mot de passe fort

## 📞 Support

Pour toute question ou problème :

1. Consultez les logs de l'application
2. Vérifiez la documentation
3. Créez une issue sur le dépôt GitHub
