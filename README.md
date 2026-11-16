# JIRAMA Bot Public (Multi-utilisateurs)

Ce bot Telegram permet à chaque utilisateur de surveiller son espace client JIRAMA de manière automatisée et sécurisée.

## Installation et Hébergement (ex: Render / Railway)
1. Créez un service de type **Background Worker** à partir de ce dépôt.
2. Définissez les variables d'environnement globales :
   - `TELEGRAM_BOT_TOKEN` : Le token de votre bot Telegram (fourni par @BotFather).
3. Le bot stocke les configurations de chaque utilisateur dans une base de données SQLite locale (`data/users.db`).

## Commandes Telegram pour les utilisateurs :
- `/start` : S'enregistrer et lier son compte JIRAMA en toute sécurité.
- `/etat` : Obtenir le résumé instantané des installations et factures.
- `/fait [N° installation]` : Valider un autorelevé pour stopper les rappels.
