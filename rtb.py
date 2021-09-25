import telebot
import random

API_TOKEN = '1995585766:AAH_dHrjciIo7fWd9LfBdwE2tZFuRkPrUwQ'
bot = telebot.TeleBot(API_TOKEN)
cids = []
prizes = []

for i in range(60):
    prizes.append('Блокнот МТС')
for i in range(25):
    prizes.append('Блокнот Hh.ru')
for i in range(90):
    prizes.append('Бутылка X5 Group')
for i in range(6):
    prizes.append('Блокнот РХБ')

@bot.message_handler(commands=['start'])
def send_start(message):
    cid = message.chat.id
    bot.send_message(cid, 'Рад видеть тебя здесь! Это бот-рулетка, с помощью которого ты сможешь выиграть спец. приз! Для регистрации нпиши /reg в чат')

@bot.message_handler(commands=['spin'])
def send_start(message):
    cid = message.chat.id
    if cid in cids and cid not in usedcids and len(prizes) > 0:
        num = random.randrange(0, len(prizes))
        prize = prizes[num]
        bot.send_message(cid, 'Поздравляю! ВЫ выиграли ' + prize + ' подойдите к стенду SEZ, чтобы забрать ваш приз!')
        usedcids.append(cid)
        prizes.pop(num)
    elif cid in usedcids:
        bot.send_message(cid, 'Вы уже использовали свой шанс. Если вы еще не забрали приз на стенде SEZ, пройдите к волонтеру за помощью)')
    elif cid not in cids:
        bot.send_message(cid, 'Вы еще не зарегистрированы, для начала напишите /reg в чат')
    else:
        bot.send_message(cid, 'Мне очень жаль,но все призы были разыграны(')

@bot.message_handler(commands=['list'])
def send_start(message):
    cid = message.chat.id
    try:
        bot.send_message(cid, *prizes)
    except Exception:
        bot.send_message(cid, 'None')
bot.polling()
usedcids = []

@bot.message_handler(commands=['start'])
def send_start(message):
    cid = message.chat.id
    bot.send_message(cid, 'Рад видеть тебя здесь! Это бот-рулетка, с помощью которого ты сможешь выиграть спец. приз! Для регистрации нпиши /reg в чат')

@bot.message_handler(commands=['reg'])
def send_start(message):
    cid = message.chat.id
    if cid in cids:
        bot.send_message(cid, 'Вы уже зарегистрированы! ')
    else:
        bot.send_message(cid, 'Теперь вы зарегистрированы в боте-рулетке! Напишите в чат /spin, чтобы выиграть приз)')
        cids.append(cid)

@bot.message_handler(commands=['spin'])
def send_start(message):
    cid = message.chat.id
    if cid in cids and cid not in usedcids and len(prizes) > 0:
        num = random.randrange(0, len(prizes))
        prize = prizes[num]
        bot.send_message(cid, 'Поздравляю! ВЫ выиграли ' + prize + ' подойтие к стенду, чтобы забрать ваш приз!')
        usedcids.append(cid)
        prizes.pop(num)
    elif cid in usedcids:
        bot.send_message(cid, 'Вы уже использовали свой шанс. Если вы еще не забрали приз на стенде, пройдите к волонтеру за помощью)')
    elif cid not in cids:
        bot.send_message(cid, 'Вы еще не зарегистрированы, для начала напишите /reg в чат')
    else:
        bot.send_message(cid, 'Мне очень жаль,но все призы были разыграны(')

bot.polling()