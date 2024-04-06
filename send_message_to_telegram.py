import requests
from data.get_credentials import Credentials


def send_telegram_message(text: str):
    token = Credentials().kp_tools
    channel_id = Credentials().admin

    url = "https://api.telegram.org/bot"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })

    if r.status_code != 200:
        raise Exception("post_text error")


if __name__ == '__main__':
    send_telegram_message('test message')
