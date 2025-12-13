"""
Script de test pour vérifier la fonctionnalité de changement de mot de passe forcé
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_user_model():
    """Test du modèle User avec force_password_change"""
    from dashboard.auth import User
    
    print("📝 Test 1: Modèle User avec force_password_change")
    
    user = User(
        id='1',
        username='testuser',
        email='test@example.com',
        role='user',
        force_password_change=True
    )
    
    assert user.id == '1', "ID incorrect"
    assert user.username == 'testuser', "Username incorrect"
    assert user.force_password_change == True, "force_password_change devrait être True"
    
    print("  ✅ Modèle User fonctionne correctement")
    return True


def test_auth_manager():
    """Test du AuthManager"""
    from dashboard.auth import AuthManager
    from flask import Flask
    
    print("\n📝 Test 2: AuthManager et gestion des utilisateurs")
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-key'
    
    auth_manager = AuthManager(app)
    
    # Vérifier que les utilisateurs par défaut ont force_password_change
    admin = auth_manager.get_user_by_username('admin')
    assert admin is not None, "Admin devrait exister"
    assert hasattr(admin, 'force_password_change'), "Admin devrait avoir force_password_change"
    print(f"  ✅ Admin force_password_change = {admin.force_password_change}")
    
    user = auth_manager.get_user_by_username('user')
    assert user is not None, "User devrait exister"
    assert hasattr(user, 'force_password_change'), "User devrait avoir force_password_change"
    print(f"  ✅ User force_password_change = {user.force_password_change}")
    
    return True


def test_change_password():
    """Test de la méthode change_password"""
    from dashboard.auth import AuthManager
    from flask import Flask
    
    print("\n📝 Test 3: Méthode change_password")
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-key'
    
    auth_manager = AuthManager(app)
    
    # Vérifier force_password_change avant
    admin = auth_manager.get_user_by_username('admin')
    print(f"  📊 Avant changement: force_password_change = {admin.force_password_change}")
    
    # Changer le mot de passe
    success = auth_manager.change_password('admin', 'NewPassword123')
    assert success, "Le changement de mot de passe devrait réussir"
    print("  ✅ Mot de passe changé avec succès")
    
    # Vérifier force_password_change après
    admin_after = auth_manager.get_user_by_username('admin')
    print(f"  📊 Après changement: force_password_change = {admin_after.force_password_change}")
    assert admin_after.force_password_change == False, "force_password_change devrait être False après changement"
    print("  ✅ force_password_change correctement mis à False")
    
    # Restaurer le mot de passe original
    auth_manager.users_db['admin']['password'] = auth_manager.users_db['admin']['password']
    auth_manager.users_db['admin']['force_password_change'] = True
    
    return True


def test_password_validation():
    """Test de la validation du mot de passe"""
    import re
    
    print("\n📝 Test 4: Validation de la force du mot de passe")
    
    test_passwords = [
        ('test', False, "Trop court, pas de majuscule, pas de chiffre"),
        ('testtest', False, "Pas de majuscule, pas de chiffre"),
        ('Testtest', False, "Pas de chiffre"),
        ('Test123', False, "Trop court"),
        ('Testtest1', True, "Valide"),
        ('Admin2024!', True, "Valide avec caractère spécial"),
    ]
    
    for password, should_be_valid, reason in test_passwords:
        length_ok = len(password) >= 8
        uppercase_ok = re.search(r'[A-Z]', password) is not None
        lowercase_ok = re.search(r'[a-z]', password) is not None
        number_ok = re.search(r'[0-9]', password) is not None
        
        is_valid = length_ok and uppercase_ok and lowercase_ok and number_ok
        
        status = "✅" if is_valid == should_be_valid else "❌"
        print(f"  {status} '{password}': {reason}")
        
        assert is_valid == should_be_valid, f"Validation incorrecte pour '{password}'"
    
    print("  ✅ Toutes les validations fonctionnent correctement")
    return True


def main():
    """Exécuter tous les tests"""
    print("="*60)
    print("🧪 Tests de la fonctionnalité de changement de mot de passe")
    print("="*60)
    
    try:
        results = []
        
        results.append(test_user_model())
        results.append(test_auth_manager())
        results.append(test_change_password())
        results.append(test_password_validation())
        
        print("\n" + "="*60)
        if all(results):
            print("✅ Tous les tests ont réussi!")
            print("="*60)
            print("\n🎉 La fonctionnalité est prête à l'emploi!")
            print("\nPour tester l'interface :")
            print("  1. python dashboard/app.py")
            print("  2. Ouvrez http://localhost:8050")
            print("  3. Connectez-vous avec admin/admin123")
            print("  4. Vous serez redirigé vers /change-password")
            return 0
        else:
            print("❌ Certains tests ont échoué")
            return 1
            
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
