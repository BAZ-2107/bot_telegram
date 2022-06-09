# -*- coding: utf-8 -*-
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove # импорт объектов

class Keyboards:
    main_keyboard = ReplyKeyboardMarkup([["Геокодер"], ["Википедик"]], one_time_keyboard=False) # Клавиатура меню
    geocoder_keyboard = ReplyKeyboardMarkup([["Картинка"], ["Адрес"], ["В меню"]], one_time_keyboard=False) # Клавиатура геокодера
    back_keyboard = ReplyKeyboardMarkup([["Назад"]], one_time_keyboard=False)
    vikipedia_keyboard = ReplyKeyboardMarkup([["В меню"]], one_time_keyboard=False)