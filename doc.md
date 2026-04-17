# 📚 Documentation API BitSport

L'API BitSport est une plateforme de marché de prédiction (betting exchange) basée sur le Bitcoin (Satoshi). Elle permet aux utilisateurs de s'inscrire, de gérer leur portefeuille, de consulter les marchés disponibles et de placer des paris sur des événements.

## 🔑 Authentification
L'API utilise des **JSON Web Tokens (JWT)**.
Pour les requêtes protégées, vous devez inclure le header suivant :
`Authorization: Bearer <votre_access_token>`

---

## 👤 Gestion des Utilisateurs (Auth)

### 1. Inscription
Crée un nouveau compte utilisateur.
- **POST** `/api/auth/register`
- **Body (JSON) :**
```json
{
  "username": "monPseudo",
  "email": "user@example.com",
  "password": "monMotDePasse8"
}
```

### 2. Connexion
Obtient les tokens d'accès.
- **POST** `/api/auth/login`
- **Body (JSON) :**
```json
{
  "email": "user@example.com",
  "password": "monMotDePasse8"
}
```

---

## 📈 Marchés (Markets)

### 1. Liste des Marchés
- **GET** `/api/markets`
- **Query Params (Optionnel) :** `?status=active` (par défaut) ou `?status=resolved`
- **Réponse (200 OK) :**
```json
{
  "markets": [
    {
      "id": "match-123",
      "title": "Qui gagnera le match A vs B ?",
      "event_date": "2023-12-01",
      "option_a": "Équipe A",
      "option_b": "Équipe B",
      "price_a_sats": 1000,
      "price_b_sats": 1000,
      "votes_a": 1,
      "votes_b": 1,
      "resolved": false
    }
  ]
}
```
*Note : Le prix d'une part est dynamique et dépend du nombre de "votes" (parts achetées) sur chaque option. Par défaut, la cote est de 10 (Prix = Payout / 10). Plus une option reçoit de votes, plus son prix augmente et sa cote diminue.*

### 2. Création de Marché (Admin)
- **POST** `/api/markets`
- **Headers :** `Authorization: Bearer <admin_token>`
- **Body (JSON) :**
```json
{
  "id": "match-123",
  "title": "Titre",
  "event_date": "2023-12-01",
  "option_a": "Équipe A",
  "option_b": "Équipe B"
}
```
*Les prix sont initialisés automatiquement par le système.*

---

## 💰 Portefeuille (Wallet)

### 1. Consulter le Solde
- **GET** `/api/wallet/balance`
- **Headers :** `Authorization: Bearer <token>`

---

## 📑 Commandes et Paris (Orders)

### 1. Placer un Pari
- **POST** `/api/orders`
- **Headers :** `Authorization: Bearer <token>`
- **Body (JSON) :**
```json
{
  "marketId": "match-123",
  "outcomeIdx": 0,
  "shares": 5
}
```
*`outcomeIdx` : 0 pour Option A, 1 pour Option B.*

### 2. Historique des Commandes
- **GET** `/api/orders`
- **Query Params :** `?status=all`, `?status=open`, `?status=settled`

### 3. Vendre un Pari (Marché Secondaire)
Mettre en vente un pari ouvert à un prix fixe.
- **POST** `/api/orders/sell/<order_id>`
- **Headers :** `Authorization: Bearer <token>`
- **Body (JSON) :**
```json
{
  "salePriceSats": 15000
}
```

### 4. Acheter un Pari
Acheter un pari mis en vente par un autre utilisateur.
- **POST** `/api/orders/buy/<order_id>`
- **Headers :** `Authorization: Bearer <token>`

### 5. Liste du Marché Secondaire
Consulter tous les paris actuellement en vente.
- **GET** `/api/secondary-market`
- **Headers :** `Authorization: Bearer <token>`

---

## 💡 Notes pour l'implémentation Front-end

1.  **Prix Dynamiques :** Les prix sont basés sur le ratio des votes. 
    - Formule : `Prix_A = (Payout / 5) * (votes_A / (votes_A + votes_B))`.
    - La cote initiale est de 10 (Prix = 1000 si Payout = 10000).
2.  **Vente/Achat :** Les utilisateurs peuvent s'échanger des paris ouverts via le marché secondaire.
3.  **Gains :** Si le marché est résolu et que vous avez parié sur le gagnant, vous recevez `shares * PAYOUT_PER_SHARE_SATS`.
