import requests
import streamlit as st

class TelegramService:
    def __init__(self):
        self.token = st.secrets["TELEGRAM_TOKEN"]
        self.chat_id = st.secrets["TELEGRAM_CHAT_ID"]

    def send(self, message: str):
        url = f"https://telegram.org{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            response = requests.post(url, json=payload, timeout=20)
            return response.status_code == 200
        except Exception:
            return False

telegram = TelegramService()
