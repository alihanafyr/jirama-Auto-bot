import os
import time
import requests
import schedule
from database import init_db, get_all_users, save_user
from bot_engine import check_user_jirama, send_telegram_message

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

def process_daily_checks():
    print("Exécution de la vérification quotidienne pour tous les utilisateurs...")
    users = get_all_users()
    for chat_id, email, password in users:
        check_user_jirama(chat_id, email, password, TELEGRAM_TOKEN)

def poll_telegram_updates():
    if not TELEGRAM_TOKEN:
        print("Erreur : TELEGRAM_BOT_TOKEN n'est pas défini !")
        return
    
    offset = 0
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    
    while True:
        try:
            response = requests.get(url, params={"offset": offset, "timeout": 30})
            data = response.json()
            if data.get("ok"):
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    message = update.get("message", {})
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text", "").strip()
                    
                    if not chat_id or not text:
                        continue
                    
                    if text.startswith("/start"):
                        send_telegram_message(chat_id, TELEGRAM_TOKEN, 
                            "👋 Bienvenue sur le bot JIRAMA public !

Pour lier votre compte, envoyez vos identifiants sous ce format :
`/login votre_email@domain.mg votre_mot_de_passe`")
                    
                    elif text.startswith("/login"):
                        parts = text.split(" ")
                        if len(parts) >= 3:
                            email = parts[1]
                            password = parts[2]
                            save_user(chat_id, email, password)
                            send_telegram_message(chat_id, TELEGRAM_TOKEN, "🔒 Vos identifiants ont été enregistrés avec succès. Le bot va surveiller vos factures et autorelevés !")
                            # Test immédiat
                            check_user_jirama(chat_id, email, password, TELEGRAM_TOKEN)
                        else:
                            send_telegram_message(chat_id, TELEGRAM_TOKEN, "⚠️ Format incorrect. Utilisez : `/login email mot_de_passe`")
                            
                    elif text.startswith("/etat"):
                        send_telegram_message(chat_id, TELEGRAM_TOKEN, "📊 Vérification de vos données en cours...")
        except Exception as e:
            print(f"Erreur de polling Telegram : {e}")
        time.sleep(2)

def main():
    print("Démarrage du service JIRAMA Bot Public...")
    init_db()
    
    # Planification quotidienne à 07:00
    schedule.every().day.at("07:00").do(process_daily_checks)
    
    # Lancement du polling Telegram en arrière-plan ou boucle
    import threading
    t = threading.Thread(target=poll_telegram_updates, daemon=True)
    t.start()
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
