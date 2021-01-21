import vk_api, random
import sqlite3
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# Импортируем токен из файла
from toks import main_token

# Подключаем токен
vk_session = vk_api.VkApi (token = main_token)


# Работа с сообщениями
longpoll = VkLongPoll(vk_session)

# Авторизуемся как сообщество
vk = vk_session.get_api()

# Работа с базой данных
conn = sqlite3.connect("dab.db")
c = conn.cursor()

list_of_users = []

# Метод для генерации пароля. Для ближайшей игры не нужен
#def generate_user_password(user_id):
#    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
#    for n in range(1):
#        password = ''
#        for i in range(8):
#            password += random.choice(chars)
#        return password

# Клавиатура 1
keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Регистрация команды', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Переименовать команду', color=VkKeyboardColor.NEGATIVE)
keyboard.add_line()
keyboard.add_button('FAQ', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('О команде Молодёжки ОНФ', color=VkKeyboardColor.NEGATIVE)


# Методки для отправки сообщения ботом пользователю в вк (Всё работает)
def write_message (user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, "random_id": get_random_id(), 'keyboard': keyboard.get_keyboard()})

# Проверка в бд id пользователя (Всё работает)
def check_if_user(user_id):
    c.execute("SELECT user_id FROM dat WHERE user_id = %d" % user_id)
    result = c.fetchone()
    if result is None:
        return False
    return True

# Проверка в бд названия команды (Всё работает)
def check_if_team(user_id):
    c.execute("SELECT team FROM dat WHERE user_id = %d" % user_id)
    result = c.fetchone()
    if result is None:
        return False
    return True

# Обновление названия команды в бд названия команды (Всё не работает)
def update(user_id, team):
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_id = event.user_id
            message = event.text
            per = (user_id, message)
            print(user_id)
            print(message)
            print(per)
            if check_if_user(user_id) and check_if_team(user_id):
                list_of_users.append(user_id)
                print(user_id)
                print(message)
                print(per)
                write_message(user_id, per)
                write_message(user_id, "Ваша команда успешно зарегистрирована!")
                game_step_one()
            elif not (check_if_user(user_id) and check_if_team(user_id)):
                print(user_id)
                print(message)
                print(per)
                write_message(user_id, per)
                write_message(user_id, "Ваша команда не зарегистрирована. Зарегистрируйтесь)")
            break


# Регистрация нового пользователя и команды (Всё работает)
def register_new_user_and_team(per):
    c.execute('''INSERT INTO dat(user_id, team) VALUES(?, ?)''', per)
    conn.commit()

# Метод для регистрации (high) Для ближайшей игры не нужен
#def register():
#    for event in longpoll.listen():
#        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
#            user_id = event.user_id
#            message = event.text
#            if check_if_exists(user_id) == False:
#                pas = generate_user_password(user_id)
#                write_message(user_id, "Твоя команда зарегистрирована! Пароль для входа: "+pas)
#            else:
#                user_id = event.user_id
#                write_message(user_id, "Такая команда уже зарегистрирована! Попробуй другое название(")

# Метод для входа (high) Для ближайшей игры не нужен
#def login():
#    for event in longpoll.listen():
#        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
#            user_id = event.user_id
#            message = event.text
#            write_message(user_id, "Введи свой пароль")
#        continue
#        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
#            user_id = event.user_id
#            message = event.text
#            if check_if_exists(message) and check_if_exists(message1) == True:
#                write_message(user_id, "Команда успешна авторизирована")
#            else:
#                write_message(user_id, "Произошла ошибка, проверь правильность данных")

# Метод для регистрации
def register():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_id = event.user_id
            message = event.text
            per = (user_id, message)
            print(user_id)
            print(message)
            print(per)
            if not (check_if_user(user_id) and check_if_team(user_id)):
                register_new_user_and_team(per)
                list_of_users.append(user_id)
                print(user_id)
                print(message)
                print(per)
                write_message(user_id, per)
                write_message(user_id, "Ваша команда успешно зарегистрирована!")
                game_step_one()
            elif (check_if_user(user_id) and check_if_team(user_id)):
                print(user_id)
                print(message)
                print(per)
                write_message(user_id, per)
                write_message(user_id, "Ваша команда не успешно зарегистрирована!")
            break


# Первый этап игры
def game_step_one():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_id = event.user_id
            message = event.text
            team = message
            if message == "Регистрация команды":
                write_message(user_id, "Введите название команды")
                register()
            elif message == "Переименовать команду":
                write_message(user_id, "Введите новое название команды")
                update(user_id, team)
            elif message == "FAQ":
                write_message(user_id, "БЛАБАЛАЛЛАБАЛЛА")
            elif message == "О команде Молодёжки ОНФ":
                write_message(user_id, "БЛАБЛАБАЛБЛАЛАЛА")
            elif message == "КОД" and user_id == 150252444:
                game_step_two()
                for user in list_of_users:
                    write_message(user, "Игра началась")
            else:
                write_message(user_id, "Я вас не понимаю, напишите ещё раз)")

def z1(user_id,message):
    if message == "Код1":
        write_message(user_id, "Истина")
    elif message != "Код1":
            write_message(user_id, "Ошибка")
            write_message(user_id, "Ложь")

def z2(user_id,message):
    if message == "Код3":
        write_message(user_id, "Истина")
    elif message != "Код3":
            write_message(user_id, "Ошибка")
            write_message(user_id, "Ложь")

# Процесс игры
def game_step_two():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            user_id = event.user_id
            message = event.text
            z1(user_id, message)
            print(list_of_users)
            continue
            z2(user_id, message)





def game_step_three():
    pass

game_step_one()