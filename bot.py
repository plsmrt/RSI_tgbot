import config
import telebot
from telebot import types  # кнопки
from string import Template

from db import SQLighter
from quiz import Quiz, Question

bot = telebot.TeleBot(config.token)
users = {}

scores = [5, 10]

questions = [Question('Как зовут текстового помощника Иннополиса?', 'Инна',
                      ['Инна', 'Полли', 'Айгюль']),
             Question('Сколько участников в чате “Котячий Иннополис”?', '490-510+',
                      ['370-390', '440-460', '490-510+']),
             Question('Кто из птиц не обитает в Иннополисе?', 'Длиннохвостая синица',
                      ['Коноплянка', 'Ласточка', 'Длиннохвостая синица']),
             Question('Сколько улиц в Иннополисе?', '5', ['4', '5', '6']),
             Question('Как зовут мэра Иннополиса?', 'Руслан',
                      ['Руслан', 'Рустем', 'Рустам']),
             Question('Как называются пространства Технопарка им. А.С. Попова?', 'Камень, трава, дерево',
                      ['Камень, ножницы, бумага', 'Камень, трава, дерево',
                       'Вода, Земля, Огонь, Воздух']),
             Question('Как зовут самую знаменитую собаку Иннополиса?', 'Нора',
                      ['Нора', 'Нода', 'Null']),
             Question('Как называется бар в Иннополисе?', '108',
                      ['108', '404', '8080']),
             Question('Кто из известных людей приезжал в Иннополис, чтобы поставить прививку от COVID-19?',
                      'Рыжий из Иванушек',
                      ['Барух Садогурский', 'Павел Финкельштейн', 'Рыжий из Иванушек'])
             ]
quiz = Quiz(questions)


class User:
    def __init__(self, chat_id, name, alias):
        self.chat_id = chat_id
        self.name = name
        self.alias = alias
        self.first_name = ''
        self.last_name = ''
        self.full_name = ''
        self.is_registered = False
        self.phone = ''
        self.email = ''
        self.cv_link = ''
        self.step = 0
        self.balance = 0
        self.tasks = [False, False, False]
        self.test_score = 0
        self.question_num = 0


def get_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_row1 = ['👩‍💻 Регистрация', '❓ Помощь']
    buttons_row2 = ['🎯 Прогресс', '🏆 Баланс очков']
    buttons_row3 = ['📄 Резюме', '💯 Тест']
    menu.add(*buttons_row1)
    menu.add(*buttons_row2)
    menu.add(*buttons_row3)
    return menu


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if len(users) > 0:
        if chat_id in users.keys():
            current_user = users[chat_id]
        else:
            current_user = False
    else:
        current_user = False

    keyboard = get_menu()

    # Проверка что пользователь уже есть в БД
    if current_user and current_user.is_registered:
        text = "Отлично, вы уже зарегистрированы. Для проверки прогресса нажмите кнопку: 🎯 Прогресс"
    else:
        text = "Для начала выполнения заданий необходима регистрация! " \
               + "Нажми кнопку в меню: 👩‍💻 Регистрация "
        name = message.from_user.first_name
        alias = message.from_user.username
        if not alias:
            alias = ''
        users[chat_id] = User(chat_id, name, alias)

    bot.send_message(message.chat.id, "Привет, "
                     + message.from_user.first_name
                     + "!\nЯ RCI бот 🤖 \n"
                     + "C моей помощью ты можешь выполнять задания и обменивать полученные баллы на призы!"
                     + "\n\n" + text, reply_markup=keyboard)


def finish_test(message):
    chat_id = message.chat.id
    user = users[chat_id]

    markup = get_menu()

    if user.test_score == 9:
        user.balance += 10
        update_test_progress_in_db(user)
        update_db_user_balance(user)
        finish_test_db(user)
        bot.send_message(config.chat_id, getUserData(user, 'Обновление данных пользователя'),
                         parse_mode="Markdown")
        bot.send_message(chat_id,
                         'Поздравляю! Вы правильно ответили на все вопросы! За это вы получаете ещё 10 баллов на '
                         'баланс! '
                         ' Теперь он составляет ' + str(user.balance) + ' баллов', reply_markup=markup)
    else:
        user.balance += 5
        update_db_user_balance(user)
        finish_test_db(user)
        bot.send_message(config.chat_id, getUserData(user, 'Обновление данных пользователя'),
                         parse_mode="Markdown")
        bot.send_message(chat_id,
                         'Поздравляю! Вы правильно ответили на ' + str(user.test_score) +
                         ' вопросов! За это вы получаете еще 5 баллов на баланс!'
                         ' Теперь он составляет ' + str(user.balance) + ' баллов',
                         reply_markup=markup)


def process_check_answer(message):
    user = users[message.chat.id]
    i = user.question_num
    q = questions[i]
    if message.text == q.correct:
        user.test_score += 1
    i += 1
    if i == len(quiz.questions):
        finish_test(message)
    else:
        user.question_num = i
        update_test_progress_in_db(user)
        quiz_ask(message)


def quiz_ask(message):
    update_db()
    cid = message.chat.id
    user = users[cid]
    i = user.question_num
    q = questions[i]
    answers = q.answers

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text=answers[0])
    keyboard.add(button_1)
    button_2 = answers[1]
    keyboard.add(button_2)
    button_3 = answers[2]
    keyboard.add(button_3)

    bot.send_message(cid, str(i+1) + "." + q.text, reply_markup=keyboard)
    bot.register_next_step_handler(message, process_check_answer)


def process_user_test(message):
    cid = message.chat.id
    if message.text == 'Нет я не готов(а) пройти тест':
        bot.send_message(cid, 'Хорошо, но если передумаете - возвращайтесь)', reply_markup=get_menu())
    if message.text == 'Да я готов(а) пройти тест':
        bot.send_message(cid, 'Отлично! Приступим)')
        quiz_ask(message)


def user_test(message):
    update_db()
    cid = message.chat.id
    user = users[cid]

    if user and user.is_registered:
        if user.tasks[2]:
            bot.send_message(cid, "Вы уже выполнили это задание!")
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons_row = ['Нет я не готов(а) пройти тест', 'Да я готов(а) пройти тест']
            keyboard.add(*buttons_row)
            bot.send_message(cid, 'Ответь на несколько вопросов про Иннополис и получи подарки🦾)' +
                             '\nТы готов(а)?', reply_markup=keyboard)

            bot.register_next_step_handler(message, process_user_test)
    else:
        bot.send_message(cid, "Вы не зарегистрированы. Нажми кнопку в меню: 👩‍💻 Регистрация ")


@bot.message_handler(content_types=["text"])
def click_button(message):
    if message.text == '👩‍💻 Регистрация':
        user_registration(message)
    elif message.text == '❓ Помощь':
        help_user(message)
    elif message.text == '🎯 Прогресс':
        user_status(message)
    elif message.text == '🏆 Баланс очков':
        user_balance(message)
    elif message.text == '📄 Резюме':
        user_cv(message)
    elif message.text == '💯 Тест':
        user_test(message)


def help_user(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     'Для продолжения выберите пункт меню. Если Вам нужна помощь, пожалуйста обратитесь в поддержку: ' + config.helpdesk)


def user_status(message):
    update_db()
    chat_id = message.chat.id
    user = users[chat_id]
    if user and user.is_registered:
        status = 'Прогресс: \n Регистрация '
        if user.tasks[0]:
            status += "✅"
        else:
            status += "❌"
        status += "\n Резюме "
        if user.tasks[1]:
            status += "✅"
        else:
            status += "❌"
        status += "\n Тест "
        if user.tasks[2]:
            status += "✅"
        else:
            status += "❌"
        bot.send_message(chat_id, status)
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы. Нажми кнопку в меню: 👩‍💻 Регистрация ")


def user_balance(message):
    chat_id = message.chat.id
    user = users[chat_id]
    if user and user.is_registered:
        update_db()
        bot.send_message(chat_id, "Текущий баланс: " + str(user.balance) + " баллов ✨✨✨")
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы. Нажми кнопку в меню: 👩‍💻 Регистрация ")


def user_cv(message):
    chat_id = message.chat.id
    user = users[chat_id]
    if user and user.is_registered:
        if user.tasks[1]:
            bot.send_message(chat_id, "Вы уже выполнили это задание!")
        else:
            # удалить старую клавиатуру
            markup = types.ReplyKeyboardRemove(selective=False)
            msg = bot.send_message(chat_id, "Введите ссылку на ваше резюме, либо аккаунт linkedin, или vk",
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, process_cv_step)
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы. Нажми кнопку в меню: 👩‍💻 Регистрация ")


def user_registration(message):
    try:
        chat_id = message.chat.id
        if users[chat_id] and users[chat_id].is_registered:
            bot.send_message(chat_id, 'Вы уже зарегистрированы')
        else:
            # удалить старую клавиатуру
            markup = types.ReplyKeyboardRemove(selective=False)

            msg = bot.send_message(chat_id, 'Введите Ваше имя', reply_markup=markup)
            bot.register_next_step_handler(msg, process_first_name_step)

    except Exception as e:
        print(e)
        bot.reply_to(message, 'Произошла непредвиденная ошибка пожалуйста напишите в поддержку: ' + config.helpdesk)


def process_first_name_step(message):
    if message.text == '/start':
        send_welcome(message)
    else:
        try:
            chat_id = message.chat.id
            user = users[chat_id]
            user.first_name = message.text

            msg = bot.send_message(chat_id, 'Введите Вашу фамилию')
            bot.register_next_step_handler(msg, process_last_name_step)

        except Exception as e:
            print(e)
            bot.reply_to(message, 'Произошла непредвиденная ошибка пожалуйста напишите в поддержку: ' + config.helpdesk)


def process_last_name_step(message):
    try:
        chat_id = message.chat.id
        user = users[chat_id]
        user.last_name = message.text
        user.full_name = user.last_name + ' ' + user.first_name

        msg = bot.send_message(chat_id, 'Введите Ваш номер телефона')
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        print(e)
        bot.reply_to(message, 'Произошла непредвиденная ошибка пожалуйста напишите в поддержку: ' + config.helpdesk)


def process_phone_step(message):
    try:
        int(message.text)

        chat_id = message.chat.id
        user = users[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Введите Ваш email')
        bot.register_next_step_handler(msg, process_email_step)

    except Exception as e:
        print(e)
        msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите номер телефона.')
        bot.register_next_step_handler(msg, process_phone_step)


def process_cv_step(message):
    try:
        chat_id = message.chat.id
        user = users[chat_id]
        user.cv_link = message.text
        user.tasks[1] = True
        user.balance += scores[0]

        update_db_user_cv(user)
        bot.send_message(config.chat_id, getUserData(user, 'Обновление данных пользователя'),
                         parse_mode="Markdown")

        bot.send_message(message.chat.id, "Задание выполнено! ✨\nВы получете +" + str(scores[0]) + " баллов",
                         reply_markup=get_menu())

    except Exception as e:
        print(e)
        bot.reply_to(message, 'Произошла непредвиденная ошибка! Пожалуйста, напишите в поддержку: ' + config.helpdesk)


def process_email_step(message):
    try:
        chat_id = message.chat.id
        user = users[chat_id]
        user.email = message.text
        user.is_registered = True
        user.tasks[0] = True
        user.step = 1

        add_new_user_to_db(user)

        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, 'Спасибо =) Регистрация пройдена!', message.from_user.first_name),
                         parse_mode="Markdown")
        # отправить в группу
        bot.send_message(config.chat_id, getRegData(user, 'Новая регистрация в боте', bot.get_me().username),
                         parse_mode="Markdown")

        menu_step(message)

    except Exception as e:
        print(e)
        msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите email.'
                           + '\nЕсли нужна помощь, пожалуйста, напишите в поддержку: ' + config.helpdesk)
        bot.register_next_step_handler(msg, process_email_step)


def menu_step(message):
    keyboard = get_menu()
    bot.send_message(message.chat.id, "Вам доступны задания: \n📄 Резюме (" + str(scores[0]) \
                     + " баллов)\n💯 Тест (Макс = " + str(scores[1]) + " баллов)", reply_markup=keyboard)


# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template(
        '$title *$name* \n#*$alias* \n ФИО: *$fullname* \n Телефон: *$phone* \n Email: *$email* \n Telegram: @*$alias*')

    if user.alias == '':
        alias = user.name
    else:
        alias = user.alias

    return t.substitute({
        'title': title,
        'name': name,
        'fullname': user.full_name,
        'phone': user.phone,
        'email': user.email,
        'alias': alias
    })


def getUserData(user, title):
    t = Template(
        '$title \n#*$alias* \n ФИО: *$fullname* \n Телефон: *$phone* \n Email: *$email* \n Telegram: @*$alias* '
        '\n Резюме: *$cv* \n Баллы: *$score*')

    if user.alias == '':
        alias = user.name
    else:
        alias = user.alias

    return t.substitute({
        'title': title,
        'fullname': user.full_name,
        'phone': user.phone,
        'email': user.email,
        'alias': alias,
        'cv': user.cv_link,
        'score': user.balance
    })


def update_users_from(db):
    rows = db.find_all()
    for row in rows:
        user = User(*row[:3])
        user.first_name = row[3]
        user.last_name = row[4]
        user.is_registered = row[5]
        user.tasks = [user.is_registered, row[6], row[7]]
        user.phone = row[8]
        user.email = row[9]
        user.cv_link = row[10]
        user.balance = row[11]
        user.question_num = row[12]
        user.test_score = row[13]
        users[user.chat_id] = user


def update_db():
    db = SQLighter(config.database_name)
    update_users_from(db)
    db.close()


def add_new_user_to_db(user):
    db = SQLighter(config.database_name)
    db.add_user(cid=user.chat_id,
                name=user.name,
                first_name=user.first_name,
                last_name=user.last_name,
                alias=user.alias,
                phone=user.phone,
                email=user.email
                )
    db.close()


def update_db_user_cv(user):
    db = SQLighter(config.database_name)
    db.update_user_cv(user.chat_id, user.cv_link)
    db.update_user_cv_add(user.chat_id)
    db.update_user_balance(user.chat_id, user.balance)
    db.close()


def finish_test_db(user):
    db = SQLighter(config.database_name)
    db.update_user_finish_test(user.chat_id)
    db.close()


def update_db_user_balance(user):
    db = SQLighter(config.database_name)
    db.update_user_balance(user.chat_id, user.balance)
    db.close()


def update_test_progress_in_db(user):
    db = SQLighter(config.database_name)
    db.update_user_test_num(user.chat_id, user.question_num)
    db.update_user_test_score(user.chat_id, user.test_score)
    db.close()


def main():
    db = SQLighter(config.database_name)
    db.init_db()
    update_users_from(db)
    db.close()
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
