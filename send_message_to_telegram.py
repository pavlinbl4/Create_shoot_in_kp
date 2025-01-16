import requests
from data.get_credentials import Credentials

def send_telegram_message(text: str):
    token = Credentials().kp_tools
    channel_id = Credentials().admin

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    r = requests.post(url, data={
        "chat_id": channel_id,
        "text": text
    })

    if r.status_code != 200:
        raise Exception(f"post_text error: {r.status_code} - {r.text}")

if __name__ == '__main__':
    send_telegram_message('test message')
