# -*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove # импорт объектов
import requests
from connect_base import Data
from change_handlers import MoveHandlers

def start(update, context):
    update.message.reply_text("Здравствуйте, бот к вашим услугам. Я умею выполнять некоторые вещи")

def help(update, context):
    update.message.reply_text("Здравствуйте, бот к вашим услугам. Я умею выполнять некоторые вещи")


if __name__ == '__main__': # запуск программы
    TOKEN = "5193422398:AAFde7LeP50xSgtzBE33QWD3ctg9nDSkth0" # токен бота
    updater = Updater(token=TOKEN, use_context=True) # создание объекта, осуществляющего связь между ботом и пользователем
    handlers = MoveHandlers(updater, start=start, help=help)
    handlers.addMainCommands()
    updater.start_polling() # начало работы объекта
    updater.idle() # прекращение работы объекта