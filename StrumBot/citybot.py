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
    global cities_list, used_cities, active_char
    used_cities = []
    first_name = update['message']['chat']['first_name']
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Привет, {first_name}, начнем игру в "Города"!',
        # reply_markup=button
    )
    with open('.\StrumBot\cities_clean.txt', mode='r', encoding='utf-8') as file:
        cities_list = sorted(list(set([city.strip().lower() for city in file.readlines()])))
    
    # cities_round(update, context, cities_list)
    chosen_city = choice(cities_list)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Первый город: {chosen_city.capitalize()}'
    )
    used_cities.append(chosen_city)
    active_char = active_letter(chosen_city)
    cities_list.remove(chosen_city)

def active_letter(city):
    """
    Функция определяет последнюю (активную) букву
    """
    prohibited_letters = ['ь', 'ы', 'ъ']
    last_letter = city[-1]
    if last_letter in prohibited_letters:
        last_letter = city[-2]
    return last_letter.lower()

def cities_player_round(update: Update, context: CallbackContext):
    # chosen_city = choice(cities_list)
    # context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text=f'Первый город: {chosen_city}'
    # )
    global cities_list, used_cities, active_char
    message = None
    player_city: str = update['message']['text'].lower()
    if player_city in used_cities:
        message = 'Такой город уже назывался. Конец игры!'
    if not player_city.startswith(active_char):
        message = f'Вы нарушили правила! Конец игры!. Выш город {player_city}, а текущая буква - {active_char}'
    if message:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Сыграем еще!'
        )
        wake_up(update, context)

    used_cities.append(player_city)
    if player_city in cities_list:
        cities_list.remove(player_city)
    active_char = active_letter(player_city)
    cities_comp_round(update, context)


def cities_comp_round(update: Update, context: CallbackContext):
    global cities_list, used_cities, active_char
    for city in cities_list:
        if city.startswith(active_char):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'Мой город: {city.capitalize()}'
            )
            cities_list.remove(city)
            used_cities.append(city)
            active_char = active_letter(city)
            break


def main():
    # global button
    # button = ReplyKeyboardMarkup([['Time', 'Пёсики'],['Котики!', 'Города']],
    #                              resize_keyboard=True)
    load_dotenv()
    updater = Updater(token=os.getenv('TOKEN'))
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    # updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Города'), cities))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(r''), cities_player_round))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
