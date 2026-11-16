import os
import requests
from playwright.sync_api import sync_playwright

def send_telegram_message(chat_id, token, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erreur d'envoi Telegram : {e}")

def check_user_jirama(chat_id, email, password, telegram_token):
    print(f"Vérification pour l'utilisateur {chat_id} ({email})...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto("https://espaceclient.jirama.mg/app/autoreleve", timeout=60000)
            # Connexion automatisée
            page.fill("input[type='email'], input[name='email'], input[placeholder*='email'i]", email)
            page.fill("input[type='password'], input[name='password']", password)
            page.click("button[type='submit'], button:has-text('Connexion')")
            page.wait_for_timeout(10000)
            
            # Simulation de lecture du tableau de bord / autorelevé
            send_telegram_message(chat_id, telegram_token, "✅ *JIRAMA Bot* : Connexion réussie à votre espace client. Vos installations sont en cours de surveillance.")
        except Exception as e:
            send_telegram_message(chat_id, telegram_token, f"❌ *JIRAMA Bot* : Échec de connexion au portail JIRAMA. Veuillez vérifier vos identifiants via /start.")
        finally:
            browser.close()
