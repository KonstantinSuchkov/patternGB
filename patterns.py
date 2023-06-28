from copy import deepcopy


class Kindergarden:
    def __init__(self):
        self.users = {
            'teacher': ['Bairta Petrovna'],
            'parent': ['Papa', 'Mama'],
            'child': ['Amelia', 'Varvara']
        }
        self.groups = []

    def add_user(self, kind, name):
        new_user = UserFactory.create_user(kind, name)
        print(type(new_user))  # проверка что создался объект нужного класса (parent, child, teacher)
        self.users[kind].append(new_user)
        return new_user

    def add_group(self, kind, data):
        new_group = GroupFactory.create_group(kind, data)
        print(type(new_group))  # проверка что создался объект нужного класса (fullday, start)
        self.groups.append(new_group)
        return new_group

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
    def __init__(self, name):
        self.name = name

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
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Teacher(User):
    pass


class Parent(User):
    pass


class Child(User):
    pass
