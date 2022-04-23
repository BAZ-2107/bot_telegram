# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters # импорт объектов

class MoveHandlers:
   def __init__(self, updater, **kwargs): # передача бота и обработчиков
      self.kwargs = kwargs
      self.dispatcher = updater.dispatcher # диспетчер, в который добавляют обработчики

   def change_handlers(self, theme_name):
      for group in self.dispatcher.handlers:
         self.dispatcher.handlers[group].clear()
              
      self.addMainCommands()
      if theme_name == "Меню": self.addThemes()
      elif theme_name == "Геокодер": self.addGeocoderThemes()
      elif theme_name == "Википедик": self.addVikipediya()
      elif theme_name == "Геокодер-картинка": self.addGeocoderPicture()
      elif theme_name == "Геокодер-адресовик": self.addGeocoderAddress()

   def addMainCommands(self): # добавляет главные команды в обработчик
      self.dispatcher.add_handler(CommandHandler("start", self.kwargs['start']))
      self.dispatcher.add_handler(CommandHandler("help", self.kwargs['help']))

   def addFirst(self):
      self.dispatcher.add_handler(MessageHandler(Filters.text, self.kwargs['first_message']))

   def addThemes(self): # добавляет обработчики для тем
      self.dispatcher.add_handler(MessageHandler(Filters.text("Геокодер"), self.kwargs['geocoder']))
      self.dispatcher.add_handler(MessageHandler(Filters.text("Википедик"), self.kwargs['vikipediya']))

   def addGeocoderThemes(self): # добавляет обработчики для темы Геокодер
      self.dispatcher.add_handler(MessageHandler(Filters.text("В меню"), self.kwargs['start']))
      self.dispatcher.add_handler(MessageHandler(Filters.text("Адрес"), self.kwargs['geocoder_address']))
      self.dispatcher.add_handler(MessageHandler(Filters.text("Картинка"), self.kwargs['geocoder_picture']))

   def addVikipediya(self): # обработчики для Википедика
      self.dispatcher.add_handler(MessageHandler(Filters.text("В меню"), self.kwargs['start']))
      self.dispatcher.add_handler(MessageHandler(Filters.text, self.kwargs['vikipediya']))

   def addGeocoderPicture(self): # добавляет обработчик для темы Картинка(Геокодер)
      self.dispatcher.add_handler(MessageHandler(Filters.text("Назад"), self.kwargs['geocoder']))
      self.dispatcher.add_handler(MessageHandler(Filters.text, self.kwargs['geocoder_picture']))

   def addGeocoderAddress(self): # добавляет обработчик для темы Адрес(Геокодер)
      self.dispatcher.add_handler(MessageHandler(Filters.text("Назад"), self.kwargs['geocoder']))
      self.dispatcher.add_handler(MessageHandler(Filters.text, self.kwargs['geocoder_address']))