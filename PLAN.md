# 🗳️ Planification : Pool Élections Québec 2026

## 1. Objectifs du Projet
*   **Networking :** Créer un point de contact interactif et ludique pour un cercle restreint de contacts (collègues, amis, connaissances stratégiques).
*   **Engagement :** Fournir une plateforme de compétition amicale basée sur les données réelles (projections Qc125) et les résultats finaux officiels.
*   **Simplicité & Transparence :** Gestion des "points" et de l'argent virtuel pour éviter les complexités légales/techniques des paiements en ligne.

## 2. Architecture Technique
*   **Frontend :** Next.js 14 (App Router) - pour la performance et le SEO.
*   **Design :** Tailwind CSS - pour un UI moderne et responsive (mobile-first).
*   **Backend & DB :** Supabase (PostgreSQL) - pour l'authentification, le stockage des données et le temps réel (Realtime).
*   **Logic :** PostgreSQL Functions (RPC) - pour calculer les scores et les parts du pot de manière centralisée et sécurisée.

## 3. Schéma de la Base de Données

### Table: `profiles`
*   `id` (uuid, PK) : Référence vers `auth.users`.
*   `username` (text) : Nom d'affichage.
*   `avatar_url` (text) : Lien vers l'image de profil (Supabase Storage).
*   `bio` (text) : Petite description pour le networking.
*   `user_type` (enum) : `human`, `bot` (ton expert), `system` (Qc125).
*   `is_eligible_for_pot` (boolean) : Définit si l'utilisateur participe au partage de l'argent.

### Table: `ridings` (Les 125 circonscriptions)
*   `id` (text, PK) : Identifiant unique (ex: `jean-talon`).
*   `name` (text) : Nom complet.
*   `region` (text) : Région administrative.
*   `qc125_url` (text) : Lien direct vers la page de la circonscription.
*   `current_projection` (text) : ID du parti projeté gagnant par Qc125.
*   `last_election_result` (text) : ID du parti gagnant en 2022 (pour contexte).
*   `final_result` (text) : ID du parti gagnant réel.

### Table: `predictions`
*   `user_id` (uuid, FK) : Référence au profil.
*   `riding_id` (text, FK) : Référence à la circonscription.
*   `party_id` (text) : Parti choisi (PQ, CAQ, PLQ, QS, PCQ, IND).
*   `updated_at` (timestamp) : Pour suivre les changements.

### Table: `wildcards` (Paris spéciaux)
*   `id` (uuid, PK) : Identifiant unique.
*   `question` (text) : La question posée.
*   `options` (jsonb) : Liste des choix possibles.
*   `correct_answer` (text) : La réponse finale.
*   `points_value` (int) : Nombre de points attribués.
*   `status` (enum) : `open`, `locked`, `resolved`.

### Table: `forum_messages`
*   `id` (uuid, PK).
*   `user_id` (uuid, FK).
*   `content` (text).
*   `created_at` (timestamp).

## 4. Logique de Scoring & "Le Pot"
*   **Points :**
    *   1 point par circonscription correctement devinée.
    *   X points par "Wildcard" réussi.
*   **Le Pot (Système Proportionnel) :**
    *   Le pot total est virtuel (ex: 10$ x nombre de participants humains).
    *   La part de chacun est calculée ainsi : `(Points de l'utilisateur / Somme totale des points du groupe éligible) * Pot Total`.
    *   Les utilisateurs de type `bot` et `system` apparaissent au classement mais ne sont pas inclus dans le calcul du partage du pot.

## 5. Fonctionnalités Clés
*   **Modification Libre :** Les utilisateurs peuvent modifier leurs prédictions jusqu'à une date de verrouillage (ex: 24h avant l'élection).
*   **Contexte Historique :** Affichage des résultats antérieurs (2022) sur l'écran de prédiction par circonscription pour aider à la décision.
*   **Visibilité :** Les prédictions des autres sont masquées jusqu'à la date de verrouillage pour éviter le "copy-pasting", puis rendues publiques.
*   **Forum Live :** Un chat interactif pour discuter des derniers sondages.
*   **Leaderboard Dynamique :** Un classement basé sur les projections actuelles de Qc125 pour voir qui "gagnerait si l'élection avait lieu aujourd'hui".

## 6. Roadmap
1.  **Setup :** Initialisation Next.js et configuration Supabase.
2.  **DB & Auth :** Création des tables, des RLS (Row Level Security) et de l'interface de login.
3.  **Moteur de Vote :** UI pour les 125 circonscriptions et enregistrement des prédictions.
4.  **Social & Scoring :** Création du forum, de la page profil et calcul automatique des scores.
5.  **Polissage & Bots :** Ajout des Wildcards, création du Bot Expert et intégration des données Qc125.
