файл run_api.py - запуск фреймворка c использованием декоратора @app.route

Стартовая страница:
http://127.0.0.1:8080
На http://127.0.0.1:8080/examples весь функционал: списки юзеров, групп, уроков, переходы на формы создания и личные страницы
Проект - сайт детского садика.
Есть группы - полного дня и подготовительные.
Есть пользователи - преподаватели, родители, дети.

Добавлено:
Преподаватели могут добавлять/удалять детей в(из) группы. При этом срабатывает оповещение (применен Шаблонный метод):
send_sms: ---sms---, Ягодки, У нас новый ученик: Варвара
send_mail: ---email---, Ягодки, У нас новый ученик: Варвара

Только Родители(parent) могут создать пользователя ребенок(child). При создании идет привязка ребенка к создавшему родителю.
Для преподавателя отображаются списки детей, групп + форма включения/удаления ученика в группу.
Для родителя отображается дети только этого родителя + форма регистрации нового ребенка.
Для ученика отображается информация о ребенке, группа в которой он состоит.