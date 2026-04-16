# Rapport d'Incohérence BitSport

Ce document liste les différences entre la structure initiale du front-end et les spécifications de l'API.

## 1. Authentification
- **Problème** : Le front-end n'avait aucune interface pour la connexion ou l'inscription.
- **Solution** : Ajout d'une section d'authentification (Login/Register) pour obtenir le token JWT nécessaire aux requêtes.

## 2. Formatage des données (Naming)
- **Problème** : Le front-end utilisait du camelCase (`optionA`, `priceA_sats`, `winnerIdx`) pour les objets marchés, tandis que l'API renvoie du snake_case (`option_a`, `price_a_sats`, `winner_idx`).
- **Solution** : Adaptation des fonctions de rendu pour utiliser les clés renvoyées par l'API.

## 3. Persistance
- **Problème** : Le front-end utilisait `localStorage` pour simuler une base de données.
- **Solution** : Remplacement des appels `localStorage` par des appels `fetch()` vers les points de terminaison de l'API.

## 4. Droits d'accès (Admin)
- **Problème** : L'interface de résolution de marché était accessible à tous les utilisateurs.
- **Solution** : Masquage des options d'administration si l'utilisateur n'est pas identifié comme `isAdmin` par l'API.
