import os
import requests
from random import choice
from datetime import datetime

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update


def wake_up(update: Update, context: CallbackContext):
    first_name = update['message']['chat']['first_name']
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Привет, {first_name}!',
        reply_markup=button
    )

def mytime(update: Update, context: CallbackContext):
    current_time = datetime.now()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Текущее время {current_time}!',
        reply_markup=button
    )


# def orientation(update: Update, context: CallbackContext):
#     choices = ['Гетеро', 'Гомо', 'Би', 'Что-то непонятное', 'Я люблю струмера!']
#     result = choice(choices)
#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text=f'Ваша ориентация, {result}!',
#         reply_markup=button
#     )


def get_new_dog_image():
    URL_DOG = os.getenv('URL_DOG')
    response = requests.get(URL_DOG).json()
    random_cat = response[0].get('url')
    return random_cat

def get_new_dog(update: Update, context: CallbackContext):
    context.bot.send_photo(
        update.effective_chat.id,
        get_new_dog_image(),
        reply_markup=button
    )


def get_new_cat_image():
    URL_CAT = os.getenv('URL_CAT')
    response = requests.get(URL_CAT).json()
    random_cat = response[0].get('url')
    return random_cat

def get_new_cat(update: Update, context: CallbackContext):
    context.bot.send_photo(
        update.effective_chat.id,
        get_new_cat_image(),
        reply_markup=button
    )

def cities_round(update: Update, context: CallbackContext, cities_list: list):
    chosen_city = choice(cities_list)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Первый город: {chosen_city}'
    )

def cities(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Привет, начнем игру в "Города"'
    )
    with open('.\StrumBot\cities_clean.txt', mode='r', encoding='utf-8') as file:
        cities_list = sorted(list(set([city.strip() for city in file.readlines()])))
    
    cities_round(update, context, cities_list)


def main():
    global button
    button = ReplyKeyboardMarkup([['Time', 'Пёсики'],['Котики!', 'Города']],
                                 resize_keyboard=True)
    load_dotenv()
    updater = Updater(token=os.getenv('TOKEN'))
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Time'), mytime))
    # updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Orientation'), orientation))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Города'), cities))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Котики'), get_new_cat))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Пёсики'), get_new_dog))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
