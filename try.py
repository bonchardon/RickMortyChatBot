import requests
from telegram import Bot

# bot = Bot(token='6475998403:AAHHPMW8HWxz1zwL5diBbPeaLKGCs2fUE5k')
url = f'https://api.telegram.org/bot6475998403:AAHHPMW8HWxz1zwL5diBbPeaLKGCs2fUE5k/getMe'
response = requests.get(url)
data = response.json()
print(data)
chat_id = data['result']['id']
print(chat_id)