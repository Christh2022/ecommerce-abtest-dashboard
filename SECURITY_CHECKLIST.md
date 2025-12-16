# 📋 Checklist Sécurité pour Collaborateurs

**Avant chaque Pull Request, assurez-vous d'avoir complété cette checklist** ✅

---

## 🎯 Tests Obligatoires (5 minutes)

### 1. Tests de Sécurité Automatisés

```bash
# Windows
lancer_tests_securite.bat

# Linux/Mac
./lancer_tests_securite.sh
```

**✅ Résultat attendu** : 41/41 attaques testées avec succès

---

### 2. Test de Rate Limiting (optionnel mais recommandé)

```bash
python test_rate_limit.py
```

**✅ Résultat attendu** : > 90% de requêtes bloquées

---

## 🔍 Vérifications Manuelles (2 minutes)

### 3. Aucun Secret Committé

```bash
# Vérifier qu'aucun secret n'est dans le code
git diff --cached | grep -iE "password|secret|token|api_key|private_key"
```

**✅ Résultat attendu** : Aucune sortie (pas de secret trouvé)

---

### 4. Debug Mode Désactivé

```bash
docker exec ecommerce-dashboard python -c "from dashboard.app import app; print('Debug:', app.debug)"
```

**✅ Résultat attendu** : `Debug: False`

---

### 5. En-têtes de Sécurité Présents

```bash
curl -I http://localhost:8050/ | grep -E "X-Frame-Options|Content-Security-Policy"
```

**✅ Résultat attendu** : Les deux en-têtes doivent être présents

---

## 📝 Documentation

### 6. Modifications Documentées

- [ ] README.md mis à jour (si nécessaire)
- [ ] CHANGELOG.md contient vos modifications (si projet mature)
- [ ] Code commenté (si logique complexe)
- [ ] Tests unitaires ajoutés (si nouvelles fonctionnalités)

---

## 🤝 Collaboration

### 7. Code Review

- [ ] Branche à jour avec `main` (`git rebase main`)
- [ ] Pas de conflit Git
- [ ] Commits clairs et atomiques
- [ ] Pull Request créée avec description détaillée

---

## 🚨 En Cas d'Échec

Si un test échoue, **NE PAS créer de Pull Request** avant correction !

**Actions à prendre** :
1. Analyser les logs d'erreur
2. Corriger le problème
3. Re-tester localement
4. Demander de l'aide si nécessaire (#security Slack)

---

## 📚 Ressources

- [Guide Sécurité Complet](SECURITY_GUIDE_COLLABORATORS.md) - 500+ lignes de documentation
- [Rapport Protection DDoS](docs/DDOS_PROTECTION_REPORT.md) - Architecture et tests
- [README.md](README.md) - Guide de démarrage général
- [SECURITY.md](SECURITY.md) - Politique de sécurité du projet

---

## ✅ Validation Finale

**Avant de cliquer sur "Create Pull Request"** :

- [ ] ✅ Tous les tests passent
- [ ] ✅ Aucun secret committé
- [ ] ✅ Debug mode désactivé
- [ ] ✅ En-têtes de sécurité OK
- [ ] ✅ Documentation à jour
- [ ] ✅ Branche à jour avec main
- [ ] ✅ Description PR claire et complète

---

**Merci de contribuer à la sécurité du projet ! 🛡️**

En cas de question : security@example.com ou #security sur Slack
