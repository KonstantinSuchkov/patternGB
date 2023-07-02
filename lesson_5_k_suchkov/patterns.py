from abc import ABCMeta, abstractmethod
from copy import deepcopy


class Kindergarden:
    def __init__(self):
        self.users = {
            'teacher': [],
            'parent': [],
            'child': []
        }
        self.groups = []
        self.lessons = []

    def add_user(self, kind, name):
        new_user = UserFactory.create_user(kind, name)
        self.users[kind].append(new_user)
        return new_user

    def add_group(self, kind, data):
        new_group = GroupFactory.create_group(kind, data)
        self.groups.append(new_group)
        return new_group

    # добавление тестовых данных - группы и пользователи
    def create_test_data(self):
        self.add_group('fullday', 'Ягодки')
        self.add_group('start', 'Ромашка')
        self.add_user('teacher', 'Зинаида Сергеевна')
        self.add_user('teacher', 'Анна Александровна')
        self.add_user('parent', 'Папа')
        self.add_user('parent', 'Мама')
        self.add_user('child', 'Амелия')
        self.add_user('child', 'Варвара')

        minor_1 = MinorLesson('Рисуем ежика')
        minor_2 = MinorLesson('Рисуем зайчика')
        main_1 = MainLesson('Рисование')
        main_1.append(minor_1)
        main_1.append(minor_2)

        main_2 = MainLesson('Арифметика')
        minor_3 = MinorLesson('Основы сложения')
        minor_4 = MinorLesson('Основы вычитания')
        main_2.append(minor_3)
        main_2.append(minor_4)

        self.lessons.append(main_1)
        self.lessons.append(main_2)

    @staticmethod
    def group_response(group):
        if isinstance(group, FulldayGroup):
            return 'группа полного дня'
        elif isinstance(group, StartGroup):
            return 'подготовительная группа'
        else:
            return 'дефолтная тестовая группа'

    @staticmethod
    def say_hello():
        print('Hello!!!')
        return 'Hello!'


class GroupPrototype:
    def copy_group(self):
        print('start copy')
        return deepcopy(self)


class Group(GroupPrototype):
    count = 1

    def __init__(self, name):
        self.name = name
        self.id = Group.count
        Group.count += 1

    # def __str__(self):
    #     return self.name


class FulldayGroup(Group):
    pass


class StartGroup(Group):
    pass


class GroupFactory:
    @staticmethod
    def create_group(group_type, data):
        groups = {
            'fullday': FulldayGroup,
            'start': StartGroup,
        }
        return groups[group_type](data)


class UserFactory:
    @staticmethod
    def create_user(user_type, name):
        users = {
            'teacher': Teacher,
            'parent': Parent,
            'child': Child
        }
        return users[user_type](name)


class User:
    count = 1

    def __init__(self, name):
        self.name = name
        self.id = User.count
        User.count += 1

    def __str__(self):
        return self.name


class Teacher(User):
    pass


class Parent(User):
    pass


class Child(User):
    pass


class Lesson(metaclass=ABCMeta):
    @abstractmethod
    def operation(self):
        pass


class MinorLesson(Lesson):
    def __init__(self, name):
        self.name = name

    def operation(self, lesson):
        return f'{lesson}/{self.name}'


class MainLesson(Lesson):
    def __init__(self, lesson):
        self._child = []
        self.lesson = lesson

    def operation(self):
        result = []
        for child in self._child:
            if child.operation(self.lesson) is None:
                pass
            else:
                result.append(child.operation(self.lesson))
        return result

    def append(self, component):
        self._child.append(component)

    def remove(self, component):
        self._child.append(component)
