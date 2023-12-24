import os
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
    print('Someone was here', update, '!!!', context)

def mytime(update: Update, context: CallbackContext):
    current_time = datetime.now()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Текущее время {current_time}!',
        reply_markup=button
    )


def orientation(update: Update, context: CallbackContext):
    choices = ['Гетеро', 'Гомо', 'Би', 'Что-то непонятное', 'Я люблю струмера!']
    result = choice(choices)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Ваша ориентация, {result}!',
        reply_markup=button
    )


def condensed_milk(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Мммм, печенька',
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
    button = ReplyKeyboardMarkup([['Time', 'Сгущенка'],['Orientation', 'Города']])
    load_dotenv()
    updater = Updater(token=os.getenv('TOKEN'))
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Time'), mytime))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Orientation'), orientation))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Сгущенка'), condensed_milk))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Города'), cities))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
