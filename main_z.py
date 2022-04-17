# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackContext, Filters # импорт объектов
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove # импорт объектов
import requests

from data import db_session # модуль для работы с БД
from data.users import User # модель ORM (информация о новом пользователе -> объект класса User -> запись в БД)


'''Функции-обработчики'''
def start(update, context): # обработчик команды "start"
    for handler in handlers.action_handlers: updater.dispatcher.add_handler(handler)
    chat_id = update.message.chat_id # id пользователя
    if not data.userExists(chat_id): # если пользователя нет в БД
        user = User(); user.user_id, user.name = update.message.chat.id, update.message.chat.first_name # создание объекта User(через этот класс записывается пользователь в БД)
        data.db_sess.add(user); data.db_sess.commit() # добавление пользователя в БД
        data.users[chat_id] = {} # добавление в data в словарь users id пользователя
        update.message.reply_text("Здравствуйте, бот к вашим услугам. Я умею выполнять некоторые вещи", reply_markup=data.main_keyboard)
    else: update.message.reply_text("Если вам нужна помощь, воспользуйтесь командой /help")

def help(update, context): # обработчик команды "help"
    update.message.reply_text(f'''    Здравствуйте, "{update.message.chat.first_name}"!
Общение с ботом выглядит примерно таким образом:
Пользователь выбирает какое-то действие и начинает на его тему общаться с ботом.
Для того чтобы выйти из темы, пользователь должен набрать фразу "В меню". С остальным проблем возникнуть не должно''')
    
def translater(update, context):
    pass

def in_menu(update, context):
    updater.dispatcher.handlers.clear()
    for handler in handlers.action_handlers: updater.dispatcher.add_handler(handler)
    update.message.reply_text("Вы в меню. В клавиатуре вы можете выбрать область взаимодействия с ботом", reply_markup=data.main_keyboard)

def geocoder(update, context):
    #удаление текущих обработчиков и установка обработчиков для геокодера
    updater.dispatcher.handlers.clear()
    for handler in handlers.geocoder_handlers: updater.dispatcher.add_handler(handler)
    update.message.reply_text("Здравствуйте, с вами геокодер!", reply_markup=data.geocoder_keyboard) # пользователь впервые в теме

def translater(update, context):
    pass


class Decorater(Updater): # класс, обрабатывающий ввод пользователя
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for handler in handlers.command_handlers: self.dispatcher.add_handler(handler) # добавление обработчиков комманд help и start
        

class Handlers: # класс, содержащий обработчики
    command_handlers =  [CommandHandler("start", start),  CommandHandler("help", help)] # массив с обработчиками комманд help и start
    action_handlers = [MessageHandler(Filters.text("Переводчик"), translater),  MessageHandler(Filters.text("Геокодер"), geocoder)] # массив с обработчиками тем бота
    geocoder_handlers = [MessageHandler(Filters.text("В меню"), in_menu)] # массив с обработчиками бота-геокодера
    

class Geocoder:
    def showPicture(self, update, context):
        pass


class Data: # взаимодействие с БД и хранение данных
    db_session.global_init("db/blogs.db") # Создание БД, если еще не создана
    db_sess = db_session.create_session() # подключение к БД

    users = dict([(user.user_id, {}) for user in db_sess.query(User).all()]) # словарь с данными о пользователях. Ключ - id  пользователя
    commands = ["start", "help"] # массив с названием команды и его обработчиком
    actions = ["Геокодер", "Переводчик"] # массив с названием темы и ее обработчика
    for_geocoder = ["В меню"] # массив возможностей бота в теме Геокодер

    main_keyboard = ReplyKeyboardMarkup([[elem] for elem in actions], one_time_keyboard=False) # Клавиатура меню
    geocoder_keyboard = ReplyKeyboardMarkup([[elem] for elem in for_geocoder], one_time_keyboard=False) # Клавиатура геокодера

    def in_geocoder(self):
        pass
    
    def addUser(self, user_id, name): # метод добавления пользователя в БД и массив users
        user = User(); user.user_id = user_id; user.name = name # создание объекта User(через этот класс записывается пользователь в БД)
        self.db_sess.add(user); self.db_sess.commit() # добавление данных пользователя в БД
        self.users[user_id] = {} # добавление данных пользователя в словарь users

    def getUser(self, user_id): # метод возвращает данные пользователя по id
        return self.users[user_id]

    def userExists(self, user_id): # метод возвращает True, если пользователь с таким id уже есть в БД, или False
        return user_id in self.users


if __name__ == '__main__': # запуск программы
    data = Data() # объект для взаимодействия с БД
    handlers = Handlers() # объект, содержащий массивы команд
    TOKEN = "5193422398:AAFde7LeP50xSgtzBE33QWD3ctg9nDSkth0" # токен бота
    updater = Decorater(token=TOKEN, use_context=True) # создание объекта, осуществляющего связь между ботом и пользователем
    updater.start_polling() # начало работы объекта
    updater.idle() # прекращение работы объекта