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
- **Réponse (201 Created) :**
```json
{
  "userId": "uuid",
  "username": "monPseudo",
  "createdAt": "2023-10-27T..."
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
- **Réponse (200 OK) :**
```json
{
  "token": "eyJhbG...",
  "refreshToken": "eyJhbG...",
  "userId": "uuid",
  "username": "monPseudo",
  "isAdmin": false,
  "expiresIn": 86400
}
```

### 3. Rafraîchir le Token
- **POST** `/api/auth/refresh`
- **Body (JSON) :** `{"refreshToken": "votre_refresh_token"}`
- **Réponse (200 OK) :** `{"token": "nouveau_token"}`

### 4. Profil Utilisateur
- **GET** `/api/auth/me`
- **Headers :** `Authorization: Bearer <token>`
- **Réponse (200 OK) :**
```json
{
  "id": "uuid",
  "username": "monPseudo",
  "email": "user@example.com",
  "balance_sats": 100000,
  "is_admin_user": false,
  "date_joined": "2023-10-27T..."
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
      "id": "uuid",
      "title": "Qui gagnera le match A vs B ?",
      "event_date": "2023-12-01T20:00:00Z",
      "option_a": "Équipe A",
      "option_b": "Équipe B",
      "price_a_sats": 60000,
      "price_b_sats": 40000,
      "resolved": false
    }
  ]
}
```
*Note : Le prix d'une part est toujours entre 0 et 100 000 sats. Si vous gagnez, chaque part vous rapporte 100 000 sats.*

### 2. Détails d'un Marché
- **GET** `/api/markets/<market_id>`
- **Réponse (200 OK) :** (Objet marché individuel)

---

## 💰 Portefeuille (Wallet)

### 1. Consulter le Solde
- **GET** `/api/wallet/balance`
- **Headers :** `Authorization: Bearer <token>`
- **Réponse (200 OK) :**
```json
{
  "balanceSats": 100000,
  "balanceBTC": "0.00100000"
}
```

### 2. Dépôt (Mode Demo/Debug)
- **POST** `/api/wallet/deposit`
- **Headers :** `Authorization: Bearer <token>`
- **Body (JSON) :** `{"amountSats": 50000}`
- **Réponse (200 OK) :** `{ "balanceSats": 150000, "balanceBTC": "0.00150000" }`

### 3. Retrait
- **POST** `/api/wallet/withdraw`
- **Headers :** `Authorization: Bearer <token>`
- **Body (JSON) :** 
```json
{
  "address": "bc1q...",
  "amountSats": 10000
}
```
- **Réponse (200 OK) :** `{ "txid": "uuid", "address": "bc1q...", "amountSats": 10000, "remainingBalanceSats": 140000 }`

---

## 📑 Commandes et Paris (Orders)

### 1. Placer un Pari
- **POST** `/api/orders`
- **Headers :** `Authorization: Bearer <token>`
- **Body (JSON) :**
```json
{
  "marketId": "uuid-du-marché",
  "outcomeIdx": 0,
  "shares": 5
}
```
*`outcomeIdx` : 0 pour Option A, 1 pour Option B.*

- **Réponse (201 Created) :**
```json
{
  "orderId": "uuid",
  "marketId": "uuid",
  "outcomeIdx": 0,
  "shares": 5,
  "pricePaidPerShare_sats": 60000,
  "totalCostSats": 300000,
  "newBalanceSats": 700000,
  "createdAt": "2023-10-27T..."
}
```

### 2. Historique des Commandes
- **GET** `/api/orders`
- **Query Params :** `?status=all` ou `?status=open` (par défaut) ou `?status=settled`
- **Headers :** `Authorization: Bearer <token>`
- **Réponse (200 OK) :**
```json
{
  "orders": [
    {
      "orderId": "uuid",
      "marketId": "uuid",
      "outcomeIdx": 0,
      "shares": 5,
      "pricePaidPerShare_sats": 60000,
      "totalCostSats": 300000,
      "status": "open",
      "createdAt": "2023-10-27T...",
      "settledAt": null
    }
  ]
}
```

### 3. Positions Actuelles (Paris en cours)
- **GET** `/api/positions`
- **Headers :** `Authorization: Bearer <token>`
- **Réponse (200 OK) :**
```json
{
  "positions": [
    {
      "marketId": "uuid",
      "marketTitle": "Match A vs B",
      "outcomeName": "Équipe A",
      "shares": 5,
      "investedSats": 300000,
      "potentialPayoutSats": 500000,
      "potentialProfitSats": 200000,
      "status": "open"
    }
  ]
}
```

---

## 🛠️ Outils de Développement (Demo)

### Réinitialiser le compte Demo
Supprime vos paris en cours et remet votre solde à la valeur initiale définie dans la configuration.
- **POST** `/api/demo/reset`
- **Headers :** `Authorization: Bearer <token>`
- **Réponse (200 OK) :** `{"message": "Demo reset successful", "newBalanceSats": 1000000}`

---

## 💡 Notes pour l'implémentation Front-end

1.  **Gestion des Erreurs :** En cas d'erreur (400, 401, 403, etc.), l'API renvoie généralement un objet avec une clé `"error"` ou les noms des champs en faute.
2.  **Calcul des Gains :** 
    - Coût d'achat = `shares * price_at_purchase`.
    - Gain si victoire = `shares * 100,000 sats`.
    - Profit net = `Gain - Coût`.
3.  **Mise à jour des prix :** Les prix (`price_a_sats` / `price_b_sats`) sont dynamiques. Il est conseillé de rafraîchir les données du marché avant de soumettre une commande.
4.  **Throttling :** La création de paris (`POST /api/orders`) est limitée à 10 par minute par utilisateur pour éviter les abus.
5.  **Admin :** Les actions de création de marchés (`POST /api/markets`) et de résolution (`POST /api/markets/<id>/resolve`) nécessitent que l'utilisateur ait l'attribut `is_admin_user` à `true`.
