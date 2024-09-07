import requests


def send_message(chat_id, message):
    TOKEN = ""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)
