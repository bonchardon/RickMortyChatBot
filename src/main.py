from typing import Final

import time
import random
from os import environ
from dotenv import load_dotenv

from requests import get
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from telegram import Bot
from aiogram import Bot, types
from telegram import Update
from itertools import chain
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes, filters
from telegram.ext import Updater, CommandHandler, CallbackContext

import aiogram
import schedule
import threading

load_dotenv()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.chat_id)
    bot = Bot(token=environ.get('TOKEN'))
    async def scrap():
        response = get('https://simpsonsua.tv/rickandmorty-sezon-7/')
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            a_discr = soup.find_all('div', class_='descr')
            links = [a['href'] for a in soup.find_all('a', href=lambda href: href and href.startswith(
                'https://simpsonsua.tv/rickandmorty-sezon-7/'))]
            exp = []
            for i in a_discr:
                title = i.text
                exp.append(title)

            combined_lines = []
            for i in range(0, len(exp), 2):
                if i + 1 < len(exp):
                    combined_lines.append(exp[i] + " " + exp[i + 1])
            my_dict = dict(zip(combined_lines, links))
            return my_dict

        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")

    async def random_ep():
        urls = [
            'https://simpsonsua.tv/rickandmorty-sezon-1/',
            'https://simpsonsua.tv/rickandmorty-sezon-2/',
            'https://simpsonsua.tv/rickandmorty-sezon-3/',
            'https://simpsonsua.tv/rickandmorty-sezon-4/',
            'https://simpsonsua.tv/rickandmorty-sezon-5/',
            'https://simpsonsua.tv/rickandmorty-sezon-6/'
        ]

        all_links = []

        for url in urls:
            response = get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                links = [a['href'] for a in soup.find_all('a', href=lambda href: href and href.startswith(
                    'https://simpsonsua.tv/rickandmorty-sezon-'))]
                all_links.append(links)
            else:
                print("Not today, honey!")

        clear_list = list(chain(*all_links))
        random_episode = random.choice(clear_list)
        return random_episode
    scrap = await scrap()
    random_result = await random_ep()

    """
        here we choose needed episode and send it to our start command.
    """

    last_key = list(scrap)[-1]
    last_value = scrap[last_key]
    while True:
        if len(scrap) > 8:
            resp = f'There is a new episode already! GO AHEAD AND WATCH IT! ' \
                   f'Here is a link: {last_value}'

            await update.message.reply_text(str(resp))

        else:
            resp_2 = f'Not yet, soon! ' \
                     f'However, here is a link to one of the previous episodes: {random_result}'
            await update.message.reply_text(str(resp_2))

        time.sleep(10)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('You are more than capable of solving your own shit. Go ahead!')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What do you want now?')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    BOT_USERNAME = str(Bot(token=environ.get('BOT_USERNAME')))

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = 'HERE 1'
        else:
            return
    else:
        return
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


async def send_telegram_message(message):
    bot = Bot(token=environ.get('TOKEN'))
    await bot.send_message(chat_id=6475998403, text=message)


if __name__ == "__main__":

    print('Starting bot...')

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print('Polling...')
    app.run_polling(poll_interval=5)

    # pkill -f main.py
    # check the processes: ps aux | grep main.py

    # schedule_thread = threading.Thread(target=job)
    # print('Threading...')
    # schedule_thread.start()
    # print('Threading 2...')
    #
    # from aiogram import executor
    #
    # executor.start_polling(dp, skip_updates=True)
