# 🔐 Système d'Authentification - Vue d'ensemble

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    CLIENT (Browser)                       │
└────────────────────┬─────────────────────────────────────┘
                     │
                     │ HTTP Request
                     ▼
┌──────────────────────────────────────────────────────────┐
│              DASH APPLICATION (app.py)                    │
│  ┌────────────────────────────────────────────────────┐  │
│  │    Flask Server + Flask-Login                      │  │
│  └────────────────────────────────────────────────────┘  │
│                     │                                     │
│                     │ Before Request                      │
│                     ▼                                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │    Authentication Middleware                       │  │
│  │  - Check if user is authenticated                  │  │
│  │  - Redirect to /login if not                       │  │
│  │  - Allow /login, /assets, /_dash                   │  │
│  └────────────────────────────────────────────────────┘  │
│                     │                                     │
│                     │ Authenticated?                      │
│        ┌────────────┴────────────┐                        │
│        │ NO                  YES │                        │
│        ▼                         ▼                        │
│  ┌─────────────┐      ┌──────────────────┐               │
│  │  /login     │      │  Dashboard Pages │               │
│  │  page       │      │  /traffic, etc.  │               │
│  └─────────────┘      └──────────────────┘               │
└──────────────────────────────────────────────────────────┘
                     │
                     │ User Data
                     ▼
┌──────────────────────────────────────────────────────────┐
│              AuthManager (auth.py)                        │
│  ┌────────────────────────────────────────────────────┐  │
│  │  - Load users from users.json                      │  │
│  │  - Verify passwords (hashed)                       │  │
│  │  - Manage sessions                                 │  │
│  │  - User CRUD operations                            │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
                     │
                     │ Read/Write
                     ▼
┌──────────────────────────────────────────────────────────┐
│                    users.json                             │
│  {                                                        │
│    "admin": {                                             │
│      "id": "1",                                           │
│      "username": "admin",                                 │
│      "password": "scrypt:32768...",                       │
│      "role": "admin"                                      │
│    }                                                      │
│  }                                                        │
└──────────────────────────────────────────────────────────┘
```

## Flux d'authentification

### 1. Connexion (Login Flow)

```
User                Browser               Server              AuthManager
  |                    |                    |                     |
  |   Visit /          |                    |                     |
  |------------------->|  GET /             |                     |
  |                    |------------------->|                     |
  |                    |                    | Check auth          |
  |                    |                    |-------------------->|
  |                    |                    |   Not authenticated |
  |                    |                    |<--------------------|
  |                    | Redirect /login    |                     |
  |                    |<-------------------|                     |
  |                    |                    |                     |
  |   Show login form  |                    |                     |
  |<-------------------|                    |                     |
  |                    |                    |                     |
  |   Enter creds      |                    |                     |
  |------------------->|                    |                     |
  |                    | POST /login        |                     |
  |                    |------------------->|                     |
  |                    |                    | Verify password     |
  |                    |                    |-------------------->|
  |                    |                    |   Valid credentials |
  |                    |                    |<--------------------|
  |                    |                    | Create session      |
  |                    |                    |-------------------->|
  |                    | Set-Cookie: session|                     |
  |                    |<-------------------|                     |
  |                    | Redirect /         |                     |
  |                    |<-------------------|                     |
  |                    |                    |                     |
  |   Show dashboard   |                    |                     |
  |<-------------------|                    |                     |
```

### 2. Navigation (Authenticated)

```
User                Browser               Server              AuthManager
  |                    |                    |                     |
  |   Click /traffic   |                    |                     |
  |------------------->|  GET /traffic      |                     |
  |                    |  Cookie: session   |                     |
  |                    |------------------->|                     |
  |                    |                    | Check session       |
  |                    |                    |-------------------->|
  |                    |                    |   Valid session     |
  |                    |                    |<--------------------|
  |                    | Show page          |                     |
  |                    |<-------------------|                     |
  |   View page        |                    |                     |
  |<-------------------|                    |                     |
```

### 3. Déconnexion (Logout Flow)

```
User                Browser               Server              AuthManager
  |                    |                    |                     |
  |   Click logout     |                    |                     |
  |------------------->|  GET /logout       |                     |
  |                    |  Cookie: session   |                     |
  |                    |------------------->|                     |
  |                    |                    | Destroy session     |
  |                    |                    |-------------------->|
  |                    |                    |   Session deleted   |
  |                    |                    |<--------------------|
  |                    | Clear cookie       |                     |
  |                    |<-------------------|                     |
  |                    | Redirect /login    |                     |
  |                    |<-------------------|                     |
  |   Show login       |                    |                     |
  |<-------------------|                    |                     |
```

## Composants clés

### 1. AuthManager (auth.py)

- **Responsabilité** : Gestion des utilisateurs et authentification
- **Méthodes principales** :
  - `authenticate_user()` : Vérifier les identifiants
  - `get_user_by_id()` : Charger un utilisateur depuis la session
  - `add_user()` : Ajouter un nouvel utilisateur
  - `verify_password()` : Vérifier un mot de passe haché

### 2. Middleware (app.py)

- **check_authentication()** :
  - Exécuté avant chaque requête
  - Redirige vers /login si non authentifié
  - Permet l'accès aux ressources publiques

### 3. Pages

- **login.py** : Interface de connexion
- **logout.py** : Déconnexion et redirection
- **Autres pages** : Protégées automatiquement

### 4. User Model

```python
class User(UserMixin):
    def __init__(self, id, username, email, role):
        self.id = id              # Identifiant unique
        self.username = username  # Nom d'utilisateur
        self.email = email        # Email (optionnel)
        self.role = role          # 'admin' ou 'user'
```

## Sécurité

### Hachage des mots de passe

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Création d'un hash
hashed = generate_password_hash('password123')
# Output: 'scrypt:32768:8:1$...'

# Vérification
is_valid = check_password_hash(hashed, 'password123')
# Output: True
```

### Session management

- **Durée** : 24 heures par défaut
- **Stockage** : Cookie sécurisé
- **Clé secrète** : SECRET_KEY dans .env

## Configuration

### Variables d'environnement (.env)

```env
SECRET_KEY=your-super-secret-key-here
SESSION_LIFETIME_HOURS=24
DEBUG=False
```

### Structure users.json

```json
{
  "username": {
    "id": "unique_id",
    "username": "username",
    "password": "scrypt:hash...",
    "email": "user@email.com",
    "role": "user|admin"
  }
}
```

## Routes protégées

### Publiques (pas d'authentification requise)

- `/login` - Page de connexion
- `/assets/*` - Fichiers statiques
- `/_dash/*` - Ressources Dash internes

### Protégées (authentification requise)

- `/` - Accueil
- `/traffic` - Trafic
- `/behavior` - Comportement
- `/conversions` - Conversions
- `/products` - Produits
- `/funnel` - Funnel
- `/cohorts` - Cohorts
- `/ab-testing/*` - Tests A/B
- `/methodology` - Méthodologie
- `/about` - À propos
- `/logout` - Déconnexion

## Journalisation

### Types d'événements logués

```python
# Connexion réussie
INFO - Successful login: admin

# Tentative échouée
WARNING - Failed login attempt: wronguser

# Accès non autorisé
WARNING - Unauthorized access attempt to /traffic from 127.0.0.1

# Déconnexion
INFO - User logged out: admin

# Requêtes
INFO - Request: GET /traffic from 127.0.0.1 - User: admin
```

## Améliorations futures possibles

1. **Base de données** : Remplacer users.json par PostgreSQL/MySQL
2. **OAuth2** : Intégration Google/GitHub
3. **2FA** : Authentification à deux facteurs
4. **Rate limiting** : Limitation des tentatives de connexion
5. **Audit log** : Historique complet des actions
6. **Permissions** : Contrôle d'accès granulaire par page
7. **API tokens** : Authentification par token pour API
8. **Password reset** : Récupération de mot de passe par email

## Tests

### Test manuel

```bash
# 1. Démarrer le dashboard
python dashboard/app.py

# 2. Tester l'accès non authentifié
curl -I http://localhost:8050/traffic
# Expected: 302 Redirect to /login

# 3. Tester la page de login
curl http://localhost:8050/login
# Expected: 200 OK with login form

# 4. Connexion (avec session)
# Utiliser le navigateur ou un outil comme Postman
```

### Test automatisé (exemple)

```python
import requests

session = requests.Session()

# Test 1: Accès sans auth -> redirect
response = session.get('http://localhost:8050/traffic')
assert response.history[0].status_code == 302

# Test 2: Login
response = session.post('http://localhost:8050/login', data={
    'username': 'admin',
    'password': 'admin123'
})
assert response.status_code == 200

# Test 3: Accès avec auth -> success
response = session.get('http://localhost:8050/traffic')
assert response.status_code == 200
```
