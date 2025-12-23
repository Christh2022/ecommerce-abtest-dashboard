# Système d'Authentification - Guide de Démarrage Rapide

## ✅ Installation Complète

Le système d'authentification a été installé avec succès ! Voici ce qui a été ajouté :

### 📁 Nouveaux fichiers

1. **dashboard/auth.py** : Module de gestion d'authentification
2. **dashboard/pages/login.py** : Page de connexion
3. **dashboard/pages/logout.py** : Page de déconnexion
4. **dashboard/users.json.example** : Exemple de base utilisateurs
5. **dashboard/AUTH_README.md** : Documentation complète
6. **dashboard/generate_password_hash.py** : Utilitaire pour créer des hash
7. **dashboard/.env.example** : Exemple de configuration

### 🔄 Fichiers modifiés

1. **dashboard/app.py** : Ajout du middleware d'authentification
2. **dashboard/requirements.txt** : Ajout des dépendances d'authentification

---

## 🚀 Démarrage Rapide (3 étapes)

### 1. Installer les dépendances

```bash
cd dashboard
pip install -r requirements.txt
```

### 2. Lancer le dashboard

```bash
python app.py
```

### 3. Se connecter

- Ouvrez http://localhost:8050
- Vous serez redirigé vers la page de connexion
- Utilisez les identifiants par défaut :
  - **Admin** : `admin` / `admin123`
  - **User** : `user` / `user123`

---

## 🎯 Fonctionnalités

### ✨ Ce qui fonctionne

✅ **Protection complète** : Toutes les pages nécessitent une authentification  
✅ **Session persistante** : Option "Se souvenir de moi"  
✅ **Interface moderne** : Design cohérent avec le dashboard  
✅ **Sécurité** : Mots de passe hachés, sessions sécurisées  
✅ **Journalisation** : Tous les événements sont enregistrés  
✅ **Déconnexion** : Bouton dans la sidebar avec nom d'utilisateur

### 🔐 Sécurité

- Hachage des mots de passe avec `scrypt` (Werkzeug)
- Gestion des sessions avec Flask-Login
- Protection automatique contre les accès non autorisés
- Redirection vers login si non authentifié

---

## 📊 Test du système

1. **Accès non authentifié**

   ```
   http://localhost:8050/traffic → Redirige vers /login
   ```

2. **Connexion réussie**

   ```
   Login avec admin/admin123 → Accès au dashboard
   ```

3. **Navigation**

   ```
   Toutes les pages sont accessibles après connexion
   ```

4. **Déconnexion**
   ```
   Cliquez sur "Déconnexion" → Retour au login
   ```

---

## 👥 Gestion des utilisateurs

### Ajouter un nouvel utilisateur

**Méthode 1 : Via Python (recommandé)**

```python
from dashboard.auth import AuthManager
from dashboard.app import server

auth = AuthManager(server)
success = auth.add_user(
    username='john',
    password='secure_password_123',
    email='john@example.com',
    role='user'  # ou 'admin'
)
print("User added!" if success else "Error adding user")
```

**Méthode 2 : Générer un hash manuellement**

```bash
cd dashboard
python generate_password_hash.py
```

Puis ajoutez l'utilisateur dans `users.json` :

```json
{
  "john": {
    "id": "3",
    "username": "john",
    "password": "[HASH_GÉNÉRÉ]",
    "email": "john@example.com",
    "role": "user"
  }
}
```

---

## ⚙️ Configuration avancée

### Changer la clé secrète (IMPORTANT pour production)

1. Générez une clé sécurisée :

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

2. Créez un fichier `.env` :

```bash
cd dashboard
cp .env.example .env
```

3. Éditez `.env` et ajoutez votre clé :

```env
SECRET_KEY=votre_cle_generee_ici
```

### Modifier la durée de session

Dans `dashboard/auth.py`, ligne 36 :

```python
self.server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
```

Changez `hours=24` selon vos besoins.

---

## 🔍 Vérification

### Journaux d'authentification

Lors de l'exécution, vous verrez :

```
INFO - Successful login: admin
INFO - Request: GET / from 127.0.0.1 - User: admin
WARNING - Unauthorized access attempt to /traffic from 127.0.0.1
INFO - User logged out: admin
```

### Structure de users.json

```json
{
  "admin": {
    "id": "1",
    "username": "admin",
    "password": "scrypt:32768:8:1$...",
    "email": "admin@example.com",
    "role": "admin"
  }
}
```

---

## 🐛 Dépannage

### Problème : "ModuleNotFoundError: No module named 'flask_login'"

**Solution** :

```bash
pip install flask-login dash-auth
```

### Problème : "ImportError: cannot import name 'AuthManager'"

**Solution** : Vérifiez que `dashboard/auth.py` existe et est accessible

### Problème : Mot de passe refusé avec comptes par défaut

**Solution** : Supprimez `users.json` et relancez l'app pour régénérer

### Problème : Redirection infinie

**Solution** : Vérifiez que `/login` est bien exclu du middleware dans `app.py`

---

## 📚 Documentation complète

Pour plus de détails, consultez :

- [dashboard/AUTH_README.md](AUTH_README.md) : Documentation complète
- [dashboard/auth.py](auth.py) : Code source du module d'authentification

---

## 🎉 C'est prêt !

Votre dashboard est maintenant sécurisé avec un système d'authentification complet.

**Prochaines étapes recommandées** :

1. ✅ Testez la connexion avec les comptes par défaut
2. ✅ Changez la SECRET_KEY pour la production
3. ✅ Créez vos propres comptes utilisateurs
4. ✅ Supprimez ou désactivez les comptes de démonstration
5. ✅ Configurez HTTPS pour la production

---

**Besoin d'aide ?** Consultez [AUTH_README.md](AUTH_README.md) pour plus d'informations.
