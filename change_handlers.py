from telegram.ext import Updater, MessageHandler, CommandHandler, Filters # импорт объектов

class MoveHandlers:
    '''main_commands = [CommandHandler("start", start), CommandHandler("help", help)]
    geocoder_handlers = [MessageHandler("Геокодер", geocoder), MessageHandler("Переводчик", translater)]'''
    

    def __init__(self, updater, **kwargs): # передача бота и обработчиков
        self.kwargs = kwargs
        self.dispatcher = updater.dispatcher # диспетчер, в который добавляют обработчики

    def change_handlers(self, theme_name):
        self.dispatcher.clear()
        self.addMainCommands()
        if theme_name == "Меню": self.addThemes()
        elif theme_name == "Геокодер": self.addGeocoderThemes()
        elif theme_name == "Геокодер": self.addTranslaterThemes()

    def addMainCommands(self): # добавляет главные команды в обработчик
        self.dispatcher.add_handler(CommandHandler("start", self.kwargs['start']))
        self.dispatcher.add_handler(CommandHandler("help", self.kwargs['help']))

    def addThemes(self): # добавляет обработчики для тем
        self.dispatcher.add_handler(MessageHandler("Геокодер", self.kwargs['geocoder']))
        self.dispatcher.add_handler(MessageHandler("Переводчик", self.kwargs['translater']))

    def addGeocoderThemes(self): # добавляет обработчики для тем
        self.dispatcher.add_handler(MessageHandler("Координаты", self.kwargs['coords']))
        self.dispatcher.add_handler(MessageHandler("Картинка", self.kwargs['picture']))