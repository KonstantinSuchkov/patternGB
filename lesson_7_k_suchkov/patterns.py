from abc import ABCMeta, abstractmethod
from copy import deepcopy

from arch_patterns import UserFactory, Teacher, Parent


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

    def get_user(self, id):
        for key, value in self.users.items():
            for user in value:
                if str(user.id) == id:
                    kind = key
                    res = [user.id, kind, user.name, user]
                    return res
        return None

    @staticmethod
    def check_user_class(user):
        if isinstance(user, Teacher):
            return 'учитель'
        elif isinstance(user, Parent):
            return 'родитель'
        else:
            return 'ребенок'

    def check_pupil(self, user):
        try:
            for group in self.groups:
                if user in group.pupils:
                    return group
        except:
            return 'Не состоит в группе'

    def add_group(self, kind, data):
        new_group = GroupFactory.create_group(kind, data)
        self.groups.append(new_group)
        return new_group

    def get_group(self, id):
        for group in self.groups:
            if str(group.id) == id:
                return group

    # добавление тестовых данных - группы и пользователи
    def create_test_data(self):
        self.add_group('fullday', 'Ягодки')
        self.add_group('start', 'Ромашка')
        # self.add_user('teacher', 'Зинаида Сергеевна')
        # self.add_user('teacher', 'Анна Александровна')
        # self.add_user('parent', 'Папа Варвары')
        # self.add_user('parent', 'Мама Амелии')
        # self.add_user('child', 'Амелия')
        # self.add_user('child', 'Варвара')
        # self.get_user('3')[3].add_child(self.get_user('6')[3])
        # self.get_user('4')[3].add_child(self.get_user('5')[3])
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
        self.pupils = []  # ученики группы

    # def __str__(self):
    #     return self.name

    def add_pupil(self, child):
        self.pupils.append(child)

    def del_pupil(self, child):
        self.pupils.remove(child)


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
        self._minor_lesson = []
        self.lesson = lesson

    def operation(self):
        result = []
        for child in self._minor_lesson:
            if child.operation(self.lesson) is None:
                pass
            else:
                result.append(child.operation(self.lesson))
        return result

    def append(self, component):
        self._minor_lesson.append(component)

    def remove(self, component):
        self._minor_lesson.append(component)
