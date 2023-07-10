import threading
import sqlite3

class UserMapper:
    """
    Паттерн DATA MAPPER
    Слой преобразования данных
    """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def find_by_id(self, id_user):
        self.cursor = connection.cursor()
        statement = "SELECT id, name, status FROM users WHERE id=?"
        self.cursor.execute(statement, (id_user,))
        result = self.cursor.fetchone()
        if result:
            id, name, status = result
            user = UserFactory.create_user(status, data=(id, name, status))  # "воссоздание" объекта класса
            return user
        else:
            f'record with id={id_user} not found'

    def find_by_name(self, user_name):
        self.cursor = connection.cursor()
        statement = "SELECT id, name, status FROM users WHERE name=?"
        self.cursor.execute(statement, (user_name,))
        result = self.cursor.fetchone()
        if result:
            print(*result)  # возврат кортеж значений
            id, name, status = result
            user = UserFactory.create_user(status, data=(id, name, status))  # "воссоздание" объекта класса
            return user
        else:
            f'record with id={user_name} not found'

    def find_child(self, parent_id):  # ищем child в таблице parenthood по id родителя (parent)
        statement = "SELECT parenthood_id, child, child_id, parent_id FROM parenthood WHERE parent_id=?"
        self.cursor.execute(statement, (parent_id,))
        return [child for child in self.cursor.execute(statement, (parent_id,))]

    def insert(self, user):
        statement = "INSERT INTO users (name, status) VALUES (?, ?)"
        self.cursor.execute(statement, (user.name, user.status))
        try:
            self.connection.commit()
        except Exception as e:
            raise e

    def add_child(self, user, parent_id):
        print('start adding child into table parenthood...params == ', 'name: ', user.name, 'id: ', user.id, 'par_id: ', parent_id)
        statement = "INSERT INTO parenthood (child, child_id, parent_id) values(?, ?, ?)"
        self.cursor.execute(statement, (user.name, user.id, parent_id))
        try:
            self.connection.commit()
            print('...finish')
        except Exception as e:
            raise e

    def update(self, user):
        statement = "UPDATE users SET name=?, status=? WHERE id=?"
        self.cursor.execute(statement, (user.name, user.status, user.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise e

    def delete(self, user):
        statement = "DELETE FROM users WHERE id=?"
        self.cursor.execute(statement, (user.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise e

    def delete_parenthood(self, row_id):
        statement = "DELETE FROM parenthood WHERE parenthood_id=?"
        self.cursor.execute(statement, (row_id,))
        try:
            self.connection.commit()
            print('запись удалена')
        except Exception as e:
            raise e

    def get_users(self):
        statement = "SELECT * FROM users"
        return [user for user in self.cursor.execute(statement)]  # возвращаем список кортежей всех пользователей

    def get_parenthood(self):
        self.cursor = connection.cursor()
        statement = "SELECT * FROM parenthood"
        return [user for user in self.cursor.execute(statement)]

    def users_category(self, category):  # поиск пользователей по категориям - учителя, родители, дети
        statement = "SELECT * FROM users"
        result = []
        for user in self.cursor.execute(statement):
            name, kind, id = user
            if category == kind:
                that_user = UserFactory.create_user(kind, data=(id, name, kind))
                result.append(that_user)
        return result


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def insert_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


connection = sqlite3.connect('main_db.sqlite')

class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, User):
            print('from MapperRegistry', obj)
            return UserMapper(connection)

class UserFactory:
    @staticmethod
    def create_user(user_type, data):
        users = {
            'teacher': Teacher,
            'parent': Parent,
            'child': Child
        }
        return users[user_type](*data)


class DomainObject:
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class User(DomainObject):
    # count = 1

    def __init__(self, id, name, status):
        self.id = id
        self.name = name
        self.status = status

    # def __str__(self):
    #     return self.name


class Teacher(User):
    pass


class Parent(User):

    def __init__(self, id, name, status):
        super().__init__(id, name, status)
        self.id = id
        self.name = name
        self.status = status
        self.childs = []

    def add_child(self, child):
        self.childs.append(child)

    def get_childs(self):
        return self.childs


class Child(User):
    pass