import requests


def send_message(chat_id, message):
    TOKEN = ""
    url = (
        "https://api.telegram.org/bot"
        + str(TOKEN)
        + "/sendMessage?chat_id="
        + str(chat_id)
        + "&text="
        + str(message)
    )
    requests.get(url)
