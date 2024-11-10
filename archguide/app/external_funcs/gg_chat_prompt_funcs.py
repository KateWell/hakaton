import json

import requests

from config import get_ggchat_settings


def get_ggchat_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    payload = 'scope=GIGACHAT_API_PERS'
    sets = get_ggchat_settings()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': f"{sets["RqUID"]}",
        'Authorization': f'Basic {sets["AuthorizationKey"]}'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify='chain.pem')
    return json.loads(response.text)["access_token"]

def do_prompt(address: str) -> str:
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": f"По адресу {address} расположено здание, составь краткую историческую справку о нём."
            }
        ],
        "stream": False,
        "repetition_penalty": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_ggchat_token()}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify='chain.pem')
    print(response.text)
    return json.loads(response.text)["choices"][0]["message"]["content"]