import config
import telebot
from telebot import types  # кнопки
from string import Template

from db import init_db, add_user

bot = telebot.TeleBot(config.token)

users = {}


class Member:
    def __init__(self, chat_id, name, alias):
        self.chat_id = chat_id
        self.name = name
        self.first_name = ''
        self.last_name = ''
        self.alias = alias
        self.is_registered = False
        self.full_name = ''
        self.phone = ''
        self.email = ''
        self.cv_link = ''
        self.step = 0
        self.balance = 0


# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_row1 = ['👩‍💻 Регистрация', '❓ Помощь']
    buttons_row2 = ['🎯 Прогресс', '🏆 Баланс очков']
    buttons_row3 = ['📄 Резюме', '💯 Тест']
    keyboard.add(*buttons_row1)
    keyboard.add(*buttons_row2)
    keyboard.add(*buttons_row3)

    # TODO проверка что пользователь уже есть в БД

    bot.send_message(message.chat.id, "Привет, "
                     + message.from_user.first_name
                     + "!\nЯ RCI бот 🤖 \n"
                     + "C моей помощью ты можешь выполнять задания и обменивать полученные баллы на призы!"
                     + "\n\nДля начала выполнения заданий необходима регистрация! "
                     + "Нажми кнопку в меню: 👩‍💻 Регистрация ", reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def send_help(message):
    cid = message.chat.id
    if message.text == '👩‍💻 Регистрация':
        user_reg(message)
        balance = 0
    if message.text == '💯 Тест':
        bot.send_message(cid, 'Ответь на 10 вопросы про Иннополис и получи подарки🦾)' +
                         '\nТы готов(а)?')
        markup = types.ReplyKeyboardRemove(selective=False)
        buttons_row = ['Нет я не готов(а) пройти тест', 'Да я готов(а) пройти тест']
        markup.add(*buttons_row)
    if message.text == 'Нет я не готов(а) пройти тест':
        bot.send_message(cid, 'Хорошо, но если передумаете - возвращайтесь)')
    if message.text == 'Да я готов(а) пройти тест':
        ans = 0
        bot.send_message(cid, 'Отлично! Приступим)')
        bot.send_message(cid, '1. Как зовут текстового помощника Иннополиса?')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons_row1 = ['Инна', 'Полли']
        buttons_row2 = ['Айгюль']
        keyboard.add(*buttons_row1)
        keyboard.add(*buttons_row2)
    if message.text == 'Инна' or message.text == 'Полли' or message.text == 'Айгюль':
        if message.text == 'Инна':
            ans += 1
        bot.send_message(cid, '2. Сколько участников в чате “Котячий Иннополис”? ')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons_row1 = ['370-390', '440-460']
        buttons_row2 = ['490-510+']
        keyboard.add(*buttons_row1)
        keyboard.add(*buttons_row2)
    if message.text == '370-390' or message.text == '440-460' or message.text == '490-510+':
        if message.text == '490-510+':
            ans += 1
        bot.send_message(cid, '3. Кто из птиц не обитает в Иннополисе?')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons_row1 = ['Коноплянка', 'Ласточка']
        buttons_row2 = ['Длиннохвостая синица']
        keyboard.add(*buttons_row1)
        keyboard.add(*buttons_row2)
    if message.text == 'Коноплянка' or message.text == 'Ласточка' or message.text == 'Длиннохвостая синица':
        if message.text == 'Длиннохвостая синица':
            ans += 1
        bot.send_message(cid, '2. Сколько участников в чате “Котячий Иннополис”? ')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons_row1 = ['370-390', '440-460']
        buttons_row2 = ['490-510+']
        keyboard.add(*buttons_row1)
        keyboard.add(*buttons_row2)
    if message.text == '370-390' or message.text == '440-460' or message.text == '490-510+':
        if message.text == '490-510+':
            ans += 1
        bot.send_message(cid, 'Сколько улиц в Иннополисе?')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons_row1 = ['4', '5']
        buttons_row2 = ['6']
        keyboard.add(*buttons_row1)
        keyboard.add(*buttons_row2)
    if message.text == '4' or message.text == '5' or message.text == '6':
        if message.text == '5':
            ans += 1
        bot.send_message(cid, '5. Как зовут мэра Иннополиса?')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons_row1 = ['Руслан', 'Рустем']
        buttons_row2 = ['Рустам']
        keyboard.add(*buttons_row1)
        keyboard.add(*buttons_row2)
    if message.text == 'Руслан' or message.text == 'Рустем' or message.text == 'Рустам':
        if message.text == 'Руслан':
            ans += 1
        bot.send_message(cid, '6. Как называются пространства Технопарка им. А.С. Попова?')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons_row1 = ['Камень, ножницы, бумага', 'Камень, трава, дерево']
        buttons_row2 = ['Вода, Земля, Огонь, Воздух']
        keyboard.add(*buttons_row1)
        keyboard.add(*buttons_row2)
    if message.text == 'Камень, ножницы, бумага' or message.text == 'Камень, трава, дерево' or message.text == 'Вода, Земля, Огонь, Воздух':
        if message.text == 'Камень, трава, дерево':
            ans += 1
        bot.send_message(cid, '7. Как зовут самую знаменитую собаку Иннополиса?')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons_row1 = ['Нора', 'Нода']
        buttons_row2 = ['Null']
        keyboard.add(*buttons_row1)
        keyboard.add(*buttons_row2)
    if message.text == 'Нора' or message.text == 'Нода' or message.text == 'Null':
        if message.text == 'Нора':
            ans += 1
        bot.send_message(cid, '9. Как называется бар в Иннополисе?')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons_row1 = ['108', '404']
        buttons_row2 = ['8080']
        keyboard.add(*buttons_row1)
        keyboard.add(*buttons_row2)
        if ans == 9:
            balance += 10
            bot.send_message('Поздравляю! Вы правильно ответили на все вопросы! За это вы получаете ещё 10 баллов на баланс!'
                             ' Теперь он составляет '+ balance + ' баллов')
        else:
            balance += 5
            bot.send_message('Поздравляю! Вы правильно ответили на ' + ans + ' вопросов! За это вы получаете еще 5 баллов на баланс!'
                             ' Теперь он составляет ' + balance + ' баллов')

@bot.message_handler(commands=['help'])
def send_about(message):
    bot.send_message(message.chat.id, "Инфо")


# /reg
@bot.message_handler(commands=["registration"])
def user_reg(message):
    try:
        chat_id = message.chat.id
        name = message.from_user.first_name
        alias = message.from_user.username
        if not alias:
            alias = ''
        users[chat_id] = Member(chat_id, name, alias)

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Введите Ваше имя', reply_markup=markup)
        bot.register_next_step_handler(msg, process_last_name_step)

    except Exception as e:
        print(e)
        bot.reply_to(message, 'Произошла непредвиденная ошибка пожалуйста напишите в поддержку')


def process_last_name_step(message):
    try:
        chat_id = message.chat.id
        user = users[chat_id]
        user.first_name = message.text

        msg = bot.send_message(chat_id, 'Введите Вашу фамилию')
        bot.register_next_step_handler(msg, process_full_name_step)

    except Exception as e:
        print(e)
        bot.reply_to(message, 'Произошла непредвиденная ошибка пожалуйста напишите в поддержку')


def process_full_name_step(message):
    try:
        chat_id = message.chat.id
        user = users[chat_id]
        user.last_name = message.text

        msg = bot.send_message(chat_id, 'Ваш номер телефона')
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        print(e)
        bot.reply_to(message, 'Произошла непредвиденная ошибка пожалуйста напишите в поддержку')


def process_phone_step(message):
    try:
        int(message.text)

        chat_id = message.chat.id
        user = users[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Введите email')
        bot.register_next_step_handler(msg, process_email_step)

    except Exception as e:
        print(e)
        msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите номер телефона.')
        bot.register_next_step_handler(msg, process_phone_step)


def process_email_step(message):
    try:
        chat_id = message.chat.id
        user = users[chat_id]
        user.email = message.text
        user.is_registered = True

        add_user(cid=user.chat_id,
                 first_name=user.first_name,
                 last_name=user.last_name,
                 alias=user.alias,
                 phone=user.phone,
                 email=user.email
                 )

        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, 'Спасибо =) Регистрация пройдена!', message.from_user.first_name),
                         parse_mode="Markdown")
        # отправить в группу
        bot.send_message(config.chat_id, getRegData(user, 'Новая регистрация в боте', bot.get_me().username),
                         parse_mode="Markdown")

    except Exception as e:
        print(e)
        msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите email.')
        bot.register_next_step_handler(msg, process_phone_step)


# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template(
        '$title *$name* \n ФИО: *$fullname* \n Телефон: *$phone* \n Email: *$email* \n Telegram: @*$alias* #*$alias*')

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


# произвольный текст
@bot.message_handler(content_types=["text"])
def send_help(message):
    bot.send_message(message.chat.id, 'Помощь')


# произвольное фото
@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    bot.send_message(message.chat.id, 'Напишите текст')


def main():
    init_db()
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
