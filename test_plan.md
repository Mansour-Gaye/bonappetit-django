# Plan de Test Manuel - Semaine 3

Ce document détaille les tests manuels effectués pour vérifier les fonctionnalités implémentées pour la Semaine 3 de l'application Bon Appétit (Comptes).

## 1. Finalisation de l’authentification

### 1.1. Déconnexion
- **Test 1.1.1: Lien de déconnexion visible et fonctionnel**
  - **Action:** Se connecter en tant que client ou gestionnaire.
  - **Attendu:** Le lien "Déconnexion" est visible dans la barre de navigation.
  - **Action:** Cliquer sur "Déconnexion".
  - **Attendu:** L'utilisateur est déconnecté et redirigé vers la page de connexion (`/comptes/login/`). Un message "Vous avez été déconnecté." s'affiche. Le lien "Déconnexion" n'est plus visible; les liens "Connexion" et "Inscription" le sont.

### 1.2. Gestion de session
- **Test 1.2.1: Expiration de session**
  - **Action:** Se connecter. Naviguer sur quelques pages. Laisser la session inactive pendant plus de 30 minutes (nécessite d'ajuster temporairement `SESSION_COOKIE_AGE` à une valeur plus courte, ex: `60` secondes, pour tester facilement, puis remettre à `30 * 60`).
  - **Attendu:** Après le délai, lors de la prochaine action nécessitant une authentification (ou rafraîchissement de page), l'utilisateur est redirigé vers la page de connexion.
  - **Note:** Le test réel avec 30 minutes est long; le principe est vérifié avec une durée courte.

- **Test 1.2.2: Réinitialisation de session à chaque requête**
  - **Action:** Se connecter. Effectuer des actions (cliquer sur des liens, naviguer) à intervalles réguliers inférieurs à la durée d'expiration de session (ex: toutes les 20 minutes si expiration à 30 min).
  - **Attendu:** La session ne doit pas expirer tant que l'utilisateur reste actif, grâce à `SESSION_SAVE_EVERY_REQUEST = True`.

## 2. Différenciation Client / Gestionnaire

### 2.1. Vérification des rôles et accès
- **Test 2.1.1: Accès client aux URLs gestionnaire**
  - **Action:** Se connecter en tant que client (non-gestionnaire). Tenter d'accéder manuellement aux URLs suivantes:
    - `/comptes/gestionnaire/dashboard/`
    - `/commandes/gestionnaire/toutes/`
    - `/commandes/gestionnaire/update_status/1/` (ou un ID de commande valide)
  - **Attendu:** L'utilisateur est redirigé vers la page de connexion (ou une page d'erreur 403 si `raise_exception=True` était utilisé avec `user_passes_test`, mais ici c'est `login_url`).

- **Test 2.1.2: Accès gestionnaire aux URLs gestionnaire**
  - **Action:** Se connecter en tant que gestionnaire. Accéder aux URLs ci-dessus.
  - **Attendu:** L'accès est autorisé, les pages correspondantes s'affichent.

### 2.2. Redirection post-login
- **Test 2.2.1: Redirection client après connexion**
  - **Action:** Se connecter avec un compte client.
  - **Attendu:** L'utilisateur est redirigé vers `/comptes/mon_compte/`.

- **Test 2.2.2: Redirection gestionnaire après connexion**
  - **Action:** Se connecter avec un compte gestionnaire.
  - **Attendu:** L'utilisateur est redirigé vers `/comptes/gestionnaire/dashboard/`.

- **Test 2.2.3: Redirection après inscription (nouveau client)**
  - **Action:** S'inscrire en tant que nouvel utilisateur (qui sera un client par défaut).
  - **Attendu:** L'utilisateur est automatiquement connecté et redirigé vers `/comptes/mon_compte/`.

### 2.3. Templates
- **Test 2.3.1: Affichage `mon_compte.html`**
  - **Action:** Se connecter en tant que client et naviguer vers `/comptes/mon_compte/`.
  - **Attendu:** La page "Mon Compte" s'affiche correctement avec les informations de base de l'utilisateur. Les sections "Historique des Commandes" et "Notifications" sont présentes (même si vides initialement).

- **Test 2.3.2: Affichage `gestionnaire/dashboard.html`**
  - **Action:** Se connecter en tant que gestionnaire et naviguer vers `/comptes/gestionnaire/dashboard/`.
  - **Attendu:** La page "Dashboard Gestionnaire" s'affiche correctement avec les placeholders pour statistiques et actions rapides. Le lien "Gérer les commandes" doit pointer vers `/commandes/gestionnaire/toutes/`.

## 3. Permissions personnalisées (Commandes)

- **Test 3.1.1: Accès client à la gestion des commandes (gestionnaire)**
  - **Action:** Se connecter en tant que client. Tenter d'accéder à `/commandes/gestionnaire/toutes/`.
  - **Attendu:** Accès refusé, redirection vers la page de connexion.

- **Test 3.1.2: Modification de statut par client**
  - **Action:** Se connecter en tant que client. Tenter d'effectuer une requête POST (par ex. avec un outil de développement ou un client API) pour modifier le statut d'une commande via l'URL `/commandes/gestionnaire/update_status/<id_commande>/`.
  - **Attendu:** Action refusée / redirection.

- **Test 3.1.3: Modification de statut par gestionnaire**
  - **Action:** Se connecter en tant que gestionnaire. Naviguer vers `/commandes/gestionnaire/toutes/`. Choisir une commande et modifier son statut en utilisant le formulaire fourni.
  - **Attendu:** Le statut de la commande est mis à jour dans la base de données et affiché correctement. Un message de succès s'affiche.

## 4. Notifications basiques

- **Test 4.1.1: Création de notification lors du changement de statut**
  - **Action:** Se connecter en tant que gestionnaire. Modifier le statut d'une commande appartenant à un client spécifique.
  - **Attendu:** Une nouvelle entrée est créée dans la table `Notification` de la base de données, associée à l'utilisateur client, avec un message pertinent.

- **Test 4.1.2: Affichage des notifications non lues**
  - **Action:** Se connecter en tant que client pour lequel une notification a été générée (cf. Test 4.1.1). Naviguer vers `/comptes/mon_compte/`.
  - **Attendu:** La section "Notifications" affiche le message de la notification non lue, avec l'heure de création.

- **Test 4.1.3: Aucune notification si pas de changement ou pour autre utilisateur**
  - **Action:** (Gestionnaire) Modifier le statut d'une commande. (Client A) Se connecter.
  - **Attendu:** Client A ne voit pas de notification si la commande appartenait à Client B.
  - **Action:** (Client B) Se connecter.
  - **Attendu:** Client B voit la notification. Si Client B n'a pas de notifications non lues, la section affiche "Vous n'avez aucune nouvelle notification."

## 5. Vérifications Générales

### 5.1. Hachage des mots de passe
- **Action:** Créer un nouvel utilisateur. Examiner l'entrée correspondante dans la table `comptes_customuser` de la base de données (colonne `password`).
- **Attendu:** Le mot de passe ne doit pas être en clair. Il doit être une longue chaîne de caractères hachée (ex: commençant par `pbkdf2_sha256$...`). (Ceci est un comportement par défaut de Django).

### 5.2. Redirection `comptes:home` / URL racine
- **Test 5.2.1: Accès à l'URL racine (non authentifié)**
  - **Action:** Ouvrir le site à l'URL racine (`/`) sans être connecté.
  - **Attendu:** Redirection vers la page de connexion (`/comptes/login/`).
- **Test 5.2.2: Accès à l'URL racine (client authentifié)**
  - **Action:** Se connecter en tant que client. Accéder à l'URL racine (`/`).
  - **Attendu:** Redirection vers `/comptes/mon_compte/`.
- **Test 5.2.3: Accès à l'URL racine (gestionnaire authentifié)**
  - **Action:** Se connecter en tant que gestionnaire. Accéder à l'URL racine (`/`).
  - **Attendu:** Redirection vers `/comptes/gestionnaire/dashboard/`.

---

Ces tests couvrent les principaux aspects des fonctionnalités implémentées. Des captures d'écran ou des notes spécifiques peuvent être ajoutées lors de l'exécution réelle des tests pour documenter les résultats.
