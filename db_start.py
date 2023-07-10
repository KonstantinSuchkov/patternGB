# подключаем SQLite
import sqlite3


# открываем файл с базой данных
def start_bd():

    base = sqlite3.connect('main_db.sqlite')

    # создаём таблицу
    with base:
        # получаем количество таблиц с нужным нам именем
        data = base.execute("select count(*) from sqlite_master where type='table' and name='users'")
        for row in data:
            # если таких таблиц нет
            if row[0] == 0:
                print('starting create table - users')
                # создаём таблицу для пользователей
                with base:
                    base.execute("""
                                    CREATE TABLE users (
                                        name VARCHAR(40),
                                        status VARCHAR(40),
                                       id INTEGER PRIMARY KEY
                                    );
                                """)
                # подготавливаем множественный запрос
                sql = 'INSERT INTO users (name, status) values(?, ?)'
                # указываем данные для запроса
                data = [
                    ('Мама Варвары', 'parent'),
                    ('Папа Амелии', 'parent'),
                    ('Тестовый родитель 3', 'parent'),
                    ('Амелия', 'child'),
                    ('Варвара', 'child'),
                    ('Teacher 1', 'teacher'),
                    ('Teacher 2', 'teacher')
                ]

                # добавляем с помощью множественного запроса все данные сразу
                with base:
                    base.executemany(sql, data)
            else:
                print('users just created')
# выводим содержимое таблицы с пользователями на экран
# with base:
#     data = base.execute("SELECT * FROM users")
#     for row in data:
#         print(row)

    with base:
        # получаем количество таблиц с нужным нам именем — orders
        data = base.execute("select count(*) from sqlite_master where type='table' and name='parenthood'")
        for row in data:
            # если таких таблиц нет
            if row[0] == 0:
                # создаём таблицу для родителей
                print('starting create table - parenthood')
                with base:
                    sql_parenthood = """CREATE TABLE parenthood (
                            parenthood_id INTEGER PRIMARY KEY,
                            child VARCHAR,
                            child_id INTEGER,
                            parent_id INTEGER,
                            FOREIGN KEY (child) REFERENCES users(name),
                            FOREIGN KEY (child_id) REFERENCES users(id),
                            FOREIGN KEY (parent_id) REFERENCES users(id)
                        );"""
                    base.execute(sql_parenthood)

                # подготавливаем  запрос
                sql = 'INSERT INTO parenthood (child, child_id, parent_id) values(?, ?, ?)'
                # указываем данные для запроса
                data = [
                    ('Амелия', 4, 2),
                    ('Варвара', 5, 1)
                ]
                # добавляем запись в таблицу
                with base:
                    base.executemany(sql, data)

            else:
                print('parenthood table just created')
# выводим содержимое таблицы на экран
# with base:
#     data = base.execute("SELECT * FROM parenthood")
#     for row in data:
#         print(row)
