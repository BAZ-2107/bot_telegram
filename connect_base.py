from data import db_session # модуль для работы с БД
from data.users import User # модель ORM (информация о новом пользователе -> объект класса User -> запись в БД)

class Data:
    db_session.global_init("db/blogs.db") # Создание БД, если еще не создана
    db_sess = db_session.create_session() # подключение к БД

    def isUser(self, id_user): # проверка на нахождение пользователя в БД
        if id_user in [user.user_id for user in self.db_sess.query(User).all()]:
            return True
        return False

    def addUser(self, id_user): # добавление пользователя
        user = User(); user.user_id = id_user # создание объекта класса User
        self.db_sess.add(user); self.db_sess.commit() # добавление пользователя в БД

    def getLocation(self, id_user): # получение локации пользователя по его id
        return self.db_sess.query(User).filter(User.user_id == id_user).first().location

    def setLocation(self, id_user, location): # изменение локации пользователя
        user = self.db_sess.query(User).filter(User.user_id == id_user).first()
        user.location = location; self.db_sess.commit()