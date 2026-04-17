# 🚀 Documentation des Nouvelles Fonctionnalités API BitSport

Cette documentation détaille les mises à jour majeures concernant le système de cotation dynamique et le marché secondaire des paris.

---

## 📈 1. Système de Cotation Dynamique (Votes)

Le prix des parts n'est plus fixe. Il évolue en temps réel selon la loi de l'offre et de la demande, représentée ici par des "votes" (chaque part achetée équivaut à un vote).

### ⚙️ Logique métier
- **Cote par défaut** : Fixée à **10**. 
- **Prix initial** : `PAYOUT_PER_SHARE_SATS / 10`. Si le payout est de 10 000 sats, le prix de départ est de 1 000 sats.
- **Mécanisme de variation** : 
    - Plus une option reçoit de votes, plus son **pourcentage** augmente.
    - Lorsque le pourcentage d'une option augmente, son **prix augmente** et sa **cote diminue**.
    - À l'inverse, l'option avec moins de votes voit son prix diminuer et sa cote augmenter.

### 🧮 Formule de calcul
`Prix_Option = (Payout / 5) * (Votes_Option / Total_Votes)`
*Le facteur `/ 5` permet d'obtenir une cote de 10 quand les votes sont à 50/50.*

---

## 🤝 2. Marché Secondaire (Peer-to-Peer)

Les utilisateurs peuvent désormais revendre leurs paris en cours à d'autres utilisateurs.

### 💰 Vendre un pari
- **Endpoint** : `POST /api/orders/sell/<order_id>`
- **Action** : L'utilisateur fixe un prix (`salePriceSats`). L'ordre est marqué comme `is_on_sale`.
- **Condition** : Seuls les ordres ouverts (`status: 'open'`) peuvent être vendus.

### 🛒 Acheter un pari
- **Endpoint** : `POST /api/orders/buy/<order_id>`
- **Action** : Une tierce personne achète l'ordre. 
- **Transfert** : 
    1. Le montant `sale_price_sats` est débité de l'acheteur.
    2. Le montant est crédité au vendeur.
    3. La propriété de l'ordre (`user_id`) est transférée à l'acheteur.

---

## 🛠️ 3. Nouveaux Endpoints & Changements

### Marchés
- **`GET /api/markets`** : Affiche désormais les champs `votes_a` et `votes_b`.
- **`POST /api/markets` (Admin)** : Ne nécessite plus `price_a_sats` ni `price_b_sats`. Le système les initialise automatiquement à la valeur par défaut.

### Ordres & Positions
- **`GET /api/secondary-market`** : Liste tous les ordres actuellement en vente par d'autres utilisateurs.
- **`POST /api/orders`** : Lors d'un achat, le système incrémente automatiquement les votes du marché correspondant et recalcule les prix pour tous les futurs acheteurs.

---

## 💡 Exemple de Flux de Prix
1. **Création** : 1 vote pour A, 1 vote pour B. Prix A = 1000, Prix B = 1000 (Cote 10).
2. **Action** : Un utilisateur achète 8 parts de A.
3. **Mise à jour** : Votes A = 9, Votes B = 1.
4. **Résultat** : 
   - Prix A = (10000 / 5) * (9 / 10) = **1800 sats** (La cote de A tombe à ~5.5).
   - Prix B = (10000 / 5) * (1 / 10) = **200 sats** (La cote de B monte à 50).

---
*Note : Cette documentation complète les spécifications de base de `doc.md`.*
