# -*- coding: utf-8 -*-
from telegram.ext import Updater
import requests
import wikipedia
wikipedia.set_lang("ru")

from connect_base import Data
from change_handlers import MoveHandlers
from keyboard import Keyboards

def start(update, context): # функция перезапуска бота
    chat_id = update.message.chat_id # id пользователя
    data.setLocation(chat_id, 'Меню')
    handlers.change_handlers("Меню") # добавление обработчиков для тем    
    if not data.isUser(chat_id):
        data.addUser(chat_id)
        message_text = f'Здравствуйте, "{update.message.chat.first_name}"! Вы находитесь в главном меню'
    else:
        message_text = "Вы в меню"
    update.message.reply_text(message_text, reply_markup=keyboards.main_keyboard) # сообщение пользователю

def help(update, context):
    update.message.reply_text(open("data\instruction.txt", encoding='utf-8').read())

def geocoder(update, context):
    data.setLocation(update.message.chat_id, "Геокодер")
    handlers.change_handlers("Геокодер") # добавление обработчиков для тем
    update.message.reply_text('''Вы в геокодере. Здесь есть 2 функции:
1. Для отображения участка карты введите слово "Картинка", затем вводите координаты в формате: широта, долгота, затем вводите масштаб(1-17)
2. Для отображения адреса через координаты введите слово "Адрес", затем координаты в формате: широта, долгота''', reply_markup=keyboards.geocoder_keyboard)

def first_message(update, context): # когда программа заускается в первый раз, пользователь мог находиться уже в какой-то теме. Для перемещение его туда и создана эта функция
    handlers.change_handlers(data.getLocation(update.message.chat_id)) # добавление обработчиков для тем
    update.message.reply_text("Извините, я был выключен. Можете еще раз повторить?")

def geocoder_picture(update, context): # функция для отображения карты по заданным параметрам
    if data.getLocation(update.message.chat_id) != "Геокодер-картинка":
        data.setLocation(update.message.chat_id, "Геокодер-картинка")
        handlers.change_handlers("Геокодер-картинка")     
        update.message.reply_text("Введите координаты в формате: широта, долгота, затем введите масштаб (от 1 до 17)", reply_markup=keyboards.back_keyboard)
    else: # пользователь вводит что-то
        try:
            message = update.message.text.split()
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={float(message[1])},{float(message[0])}&z={int(message[-1])}&l=sat,skl&size=450,450"
            context.bot.send_photo(update.message.chat_id, map_request)
        except Exception:
            update.message.reply_text("Входные данные некорректны")

def geocoder_address(update, context): # функция для показа адреса объекта по заданным координатам
    if data.getLocation(update.message.chat_id) != "Геокодер-адресовик":
        data.setLocation(update.message.chat_id, "Геокодер-адресовик")
        handlers.change_handlers("Геокодер-адресовик")     
        update.message.reply_text("Введите координаты в формате: широта, долгота", reply_markup=keyboards.back_keyboard)
    else:
        try:
            message = update.message.text.split()
            apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
            geocoder_request = f"https://geocode-maps.yandex.ru/1.x/?apikey={apikey}&geocode={','.join(elem for elem in message[::-1])}&format=json"
            update.message.reply_text(requests.get(geocoder_request).json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"])
        except Exception:
            update.message.reply_text("Входные данные некорректны")

def vikipediya(update, context): # функция взаимодействия с википедией
    if data.getLocation(update.message.chat_id) != "Википедик":
        data.setLocation(update.message.chat_id, "Википедик")
        handlers.change_handlers("Википедик")     
        update.message.reply_text("Введите ваш запрос", reply_markup=keyboards.vikipedia_keyboard)
    else:
        message = update.message.text
        try:
            update.message.reply_text(wikipedia.summary(message))
        except Exception:
            update.message.reply_text(f'По запросу "{message}" ничего не найдено')


if __name__ == '__main__': # запуск программы
    TOKEN = "5193422398:AAFde7LeP50xSgtzBE33QWD3ctg9nDSkth0" # токен бота
    data = Data() # создание объекта для взаимодействия с БД
    keyboards = Keyboards() # создание объекта с клавиатурами
    updater = Updater(token=TOKEN, use_context=True) # создание объекта, осуществляющего связь между ботом и пользователем
    handlers = MoveHandlers(updater, start=start, help=help, geocoder=geocoder, first_message=first_message, 
                            geocoder_picture=geocoder_picture, geocoder_address=geocoder_address, vikipediya=vikipediya)
    handlers.addMainCommands()
    handlers.addFirst()
    updater.start_polling() # начало работы объекта
    updater.idle() # прекращение работы объекта