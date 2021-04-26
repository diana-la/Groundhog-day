import telebot
import time
import random
from telebot.types import Message

import tok
from telebot import types

text_play = open('text_play.txt', encoding='utf-8')
lines = text_play.readlines()
bot = telebot.TeleBot(tok.token)
USERS = set()
isRunning = False
inventory = []
gold = 0
wordd = 0
count = 0
lucky = 0


@bot.message_handler(commands=['help'])
def help(message):
    help_text = open('help.txt', encoding='utf-8')
    bot.reply_to(message, help_text.readline())


@bot.message_handler(commands=['gold'])
def money(message):
    global gold
    bot.reply_to(message, f'В вашем мешке {gold} золотых')


@bot.message_handler(commands=['lucky'])
def luky(message):
    global lucky
    bot.reply_to(message, f'У вас {lucky} единиц удачи')


@bot.message_handler(commands=['start'])
def hi(message):
    global isRunning
    if not isRunning:
        bot.reply_to(message, "Доброго времени суток, {0.first_name}\nХотите пограть?".format(message.from_user,
                                                                                              bot.get_me()))


@bot.message_handler(content_types=['text'])
def echo(message):
    global wordd, gold, count

    used = []
    chat_id = message.chat.id
    text = message.text
    if wordd == 0:
        if text.lower() == 'да':
            msg = bot.send_message(chat_id, lines[0])
            get_dom(msg)
        else:
            bot.send_message(chat_id, "Если хочешь начать играть, напиши 'да'")


def get_dom(message):
    USERS.add(message.from_user.id)
    chat_id = message.chat.id
    for i in range(1, 4):
        time.sleep(2)
        bot.send_message(chat_id, lines[i])

    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="/1 Выйти на улицу", callback_data='a')
    keyboard.add(b1)
    b2 = types.InlineKeyboardButton(text="/2 Посмотреть в окно", callback_data='b')
    keyboard.add(b2)
    time.sleep(2)
    bot.send_message(message.chat.id, "Ладно, пора вставать",
                     reply_markup=keyboard)


def get_okno(message):
    chat_id = message.chat.id
    time.sleep(2)
    bot.send_message(chat_id, 'На улице было ветрено, но это не мешало соседским'
                              ' детям веселиться на площадке перед домом.')
    time.sleep(2)
    bot.send_message(chat_id, 'Вскоре мне надоело созерцать и я вышел на улицу.')
    time.sleep(2)
    msg = bot.send_message(chat_id, lines[6])
    get_ulitsa(msg)


def get_ulitsa(message):
    chat_id = message.chat.id
    for i in range(7, 8):
        time.sleep(2)
        bot.send_message(chat_id, lines[i])
    keyboard = types.InlineKeyboardMarkup()
    b3 = types.InlineKeyboardButton(text="/1 Пойти влево", callback_data='c')
    b4 = types.InlineKeyboardButton(text="/2 Пойти вправо", callback_data='d')
    keyboard.add(b3, b4)
    time.sleep(2)
    bot.send_message(chat_id, lines[9], reply_markup=keyboard)


def get_right(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    b3 = types.InlineKeyboardButton(text="/1 Зайти", callback_data='come_in')
    b4 = types.InlineKeyboardButton(text="/2 Пойти дальше", callback_data='go_further')
    keyboard.add(b3, b4)
    time.sleep(2)
    bot.send_message(chat_id, lines[130], reply_markup=keyboard)


def fortune_teller(message):
    chat_id = message.chat.id
    for i in range(132, 139):
        time.sleep(2)
        bot.send_message(chat_id, lines[i])
    keyboard = types.InlineKeyboardMarkup()
    b3 = types.InlineKeyboardButton(text="/1 Да", callback_data='yes')
    b4 = types.InlineKeyboardButton(text="/2 Нет", callback_data='no')
    keyboard.add(b3, b4)
    time.sleep(2)
    bot.send_message(chat_id, lines[140], reply_markup=keyboard)


def get_go_further(message):
    global lucky
    chat_id = message.chat.id
    prediction = ['-Ваш день сегодня будет наполнен удачей', '-Сегодня вас ждёт огорчение',
                  '-Внимательнее смотрите по сторонам',
                  '-Не перетруждайте себя работой.Это может плохо закончиться',
                  '-Ваш день сегодня будет наполнен неудачей',
                  '-Глубоко скрытые конфликты и противоречия могут неожиданно всплыть на поверхность',
                  '-Чем дольше вы будете обдумывать ситуацию, тем меньше шансов, что найдёте правильное решение'
                  ' в короткое время',
                  '-Вы не замечаете того, что очевидно для окружающих. Постарайтесь не совершить ошибок',
                  '-Если вы проанализируете ситуацию, то увидите простой путь достижения желаймого']
    pr = random.choice(prediction)

    if pr == 'Ваш день сегодня будет наполнен удачей':
        lucky += 10
    elif pr == 'Ваш день сегодня будет наполнен неудачей':
        lucky -= 10
    time.sleep(2)
    bot.send_message(chat_id, pr)
    time.sleep(2)
    bot.send_message(chat_id, 'Довольно странное предсказание...')
    time.sleep(2)
    msg = bot.send_message(chat_id, 'Я вышел на улицу')
    get_choice_r(msg)


def shop(message):
    global gold, lucky
    chat_id = message.chat.id
    if lucky >= 10:
        time.sleep(2)
        bot.send_message(chat_id, lines[160])
        time.sleep(2)
        bot.send_message(chat_id, lines[161])
        gold += 100
        time.sleep(2)
        bot.send_message(chat_id, 'Сегодня удача на вашей стороне. Вы нашли мешочек, в  котором 100 золотых')
    for i in range(172, 179):
        time.sleep(2)
        bot.send_message(chat_id, lines[i])
    msg = bot.send_message(chat_id, lines[179])
    shop_choice(msg)


def shop_choice(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    b3 = types.InlineKeyboardButton(text="/1 Пожелтевший свёрток", callback_data='map')
    b4 = types.InlineKeyboardButton(text="/2 Баночка зелья удачи", callback_data='bank')
    b5 = types.InlineKeyboardButton(text="/3 Веточка жар-цвета", callback_data='stick')
    b6 = types.InlineKeyboardButton(text="/4 Покинуть магазин", callback_data='leave')
    keyboard.add(b3, b4, b5, b6)
    time.sleep(2)
    bot.send_message(chat_id, lines[180], reply_markup=keyboard)


def map(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, '-Если хотите проветить свою удачу, то покупайте')
    keyboard = types.InlineKeyboardMarkup()
    b3 = types.InlineKeyboardButton(text="/1 Купить", callback_data='buy_m')
    b4 = types.InlineKeyboardButton(text="/2 Отказаться", callback_data='renouncement_m')
    keyboard.add(b3, b4)
    time.sleep(2)
    bot.send_message(chat_id, '-Отдам всего лишь за 100 золотых', reply_markup=keyboard)


def bank(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    b3 = types.InlineKeyboardButton(text="/1 Купить", callback_data='buy_b')
    b4 = types.InlineKeyboardButton(text="/2 Отказаться", callback_data='renouncement_b')
    keyboard.add(b3, b4)
    time.sleep(2)
    bot.send_message(chat_id, '-Отдам всего лишь за 50 золотых', reply_markup=keyboard)


def get_left(message):
    global gold
    order = ['музыка', 'картины']  # добавить слова и арифметику
    ord = random.choice(order)
    chat_id = message.chat.id
    time.sleep(2)
    bot.send_message(chat_id, lines[15])

    if ord == 'картины':
        keyboard = types.InlineKeyboardMarkup()
        b3 = types.InlineKeyboardButton(text="/1 Легко", callback_data='easy_p')
        b4 = types.InlineKeyboardButton(text="/2 Сложно", callback_data='hard_p')
        keyboard.add(b3, b4)
        time.sleep(2)
        bot.send_message(chat_id, 'Выберите уровень сложности', reply_markup=keyboard)

    if ord == 'музыка':
        keyboard = types.InlineKeyboardMarkup()
        b3 = types.InlineKeyboardButton(text="/1 Легко", callback_data='easy')
        b4 = types.InlineKeyboardButton(text="/2 Сложно", callback_data='hard')
        keyboard.add(b3, b4)
        time.sleep(2)
        bot.send_message(chat_id, 'Выберите уровень сложности', reply_markup=keyboard)


def gildia_choise(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    b3 = types.InlineKeyboardButton(text="/1 Взять ещё задание", callback_data='task')
    b4 = types.InlineKeyboardButton(text="/2 Выйти", callback_data='exit')
    keyboard.add(b3, b4)
    time.sleep(2)
    bot.send_message(chat_id, 'Выполнить ещё задание или уйти?', reply_markup=keyboard)


def get_choice_r(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    b2 = types.InlineKeyboardButton(text="/1 Домой", callback_data='home_r')
    b3 = types.InlineKeyboardButton(text="/2 Влево", callback_data='left_r')
    b4 = types.InlineKeyboardButton(text="/3 Вправо", callback_data='right_r')
    keyboard.add(b2, b3, b4)
    time.sleep(2)
    bot.send_message(chat_id, 'Пожалуй, пойду...', reply_markup=keyboard)


def get_choise_g(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    b2 = types.InlineKeyboardButton(text="/1 Домой", callback_data='home_r')
    b3 = types.InlineKeyboardButton(text="/2 Вправо", callback_data='right_g')
    keyboard.add(b2, b3)
    time.sleep(2)
    bot.send_message(chat_id, 'Пожалуй, пойду...', reply_markup=keyboard)


def get_choice_s(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    b2 = types.InlineKeyboardButton(text="/1 Домой", callback_data='home_r')
    b3 = types.InlineKeyboardButton(text="/2 Влево", callback_data='left_s')
    keyboard.add(b2, b3)
    time.sleep(2)
    bot.send_message(chat_id, 'Пожалуй, пойду...', reply_markup=keyboard)


def get_home(message):
    chat_id = message.chat.id
    time.sleep(2)
    bot.send_message(chat_id, lines[169])
    time.sleep(2)
    msg = bot.send_message(chat_id, lines[170])
    get_dom(msg)


def picture_easy(message):
    chat_id = message.chat.id
    name = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg']
    random_picture = random.choice(name)
    if random_picture == '1.jpg':
        image = open('1.jpg', 'rb')
        bot.send_sticker(chat_id, image)
        keyboard = types.InlineKeyboardMarkup()
        b4 = types.InlineKeyboardButton(text="/1 Эдвард Мунк", callback_data='false')
        b5 = types.InlineKeyboardButton(text="/2 Казимир Северинович Малевич", callback_data='false')
        b6 = types.InlineKeyboardButton(text="/3 Леонардо да Винчи", callback_data='false')
        b7 = types.InlineKeyboardButton(text="/4 Винсент ван Гог", callback_data='right')
        b8 = types.InlineKeyboardButton(text="/5 Иван Иванович Шишкин", callback_data='false')
        keyboard.add(b4, b5, b6, b7, b8)
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)
    elif random_picture == '2.jpg':
        image = open('2.jpg', 'rb')
        bot.send_sticker(chat_id, image)
        keyboard = types.InlineKeyboardMarkup()
        b4 = types.InlineKeyboardButton(text="/1 Эдвард Мунк", callback_data='false')
        b5 = types.InlineKeyboardButton(text="/2 Казимир Северинович Малевич", callback_data='false')
        b6 = types.InlineKeyboardButton(text="/3 Леонардо да Винчи", callback_data='right')
        b7 = types.InlineKeyboardButton(text="/4 Винсент ван Гог", callback_data='false')
        b8 = types.InlineKeyboardButton(text="/5 Иван Иванович Шишкин", callback_data='false')
        keyboard.add(b4, b5, b6, b7, b8)
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)
    elif random_picture == '3.jpg':
        image = open('3.jpg', 'rb')
        bot.send_sticker(chat_id, image)
        keyboard = types.InlineKeyboardMarkup()
        b4 = types.InlineKeyboardButton(text="/1 Эдвард Мунк", callback_data='false')
        b5 = types.InlineKeyboardButton(text="/2 Казимир Северинович Малевич", callback_data='right')
        b6 = types.InlineKeyboardButton(text="/3 Леонардо да Винчи", callback_data='false')
        b7 = types.InlineKeyboardButton(text="/4 Винсент ван Гог", callback_data='false')
        b8 = types.InlineKeyboardButton(text="/5 Иван Иванович Шишкин", callback_data='false')
        keyboard.add(b4, b5, b6, b7, b8)
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)
    elif random_picture == '4.jpg':
        image = open('4.jpg', 'rb')
        bot.send_sticker(chat_id, image)
        keyboard = types.InlineKeyboardMarkup()
        b4 = types.InlineKeyboardButton(text="/1 Эдвард Мунк", callback_data='false')
        b5 = types.InlineKeyboardButton(text="/2 Казимир Северинович Малевич", callback_data='false')
        b6 = types.InlineKeyboardButton(text="/3 Леонардо да Винчи", callback_data='false')
        b7 = types.InlineKeyboardButton(text="/4 Винсент ван Гог", callback_data='false')
        b8 = types.InlineKeyboardButton(text="/5 Иван Иванович Шишкин", callback_data='right')
        keyboard.add(b4, b5, b6, b7, b8)
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)
    elif random_picture == '5.jpg':
        image = open('5.jpg', 'rb')
        bot.send_sticker(chat_id, image)
        keyboard = types.InlineKeyboardMarkup()
        b4 = types.InlineKeyboardButton(text="/1 Эдвард Мунк", callback_data='right')
        b5 = types.InlineKeyboardButton(text="/2 Казимир Северинович Малевич", callback_data='false')
        b6 = types.InlineKeyboardButton(text="/3 Леонардо да Винчи", callback_data='false')
        b7 = types.InlineKeyboardButton(text="/4 Винсент ван Гог", callback_data='false')
        b8 = types.InlineKeyboardButton(text="/5 Иван Иванович Шишкин", callback_data='false')
        keyboard.add(b4, b5, b6, b7, b8)
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)


def picture_hard(message):
    chat_id = message.chat.id
    name = ['мане.jpg', 'моне.jpg', 'дали.jpg']
    random_picture = random.choice(name)
    if random_picture == 'мане.jpg':
        image = open('мане.jpg', 'rb')
        bot.send_sticker(chat_id, image)
        keyboard = types.InlineKeyboardMarkup()
        b4 = types.InlineKeyboardButton(text="/1 Рене Магритт", callback_data='false_h')
        b5 = types.InlineKeyboardButton(text="/2 Сальвадор Дали", callback_data='false_h')
        b6 = types.InlineKeyboardButton(text="/3 Клод Моне", callback_data='false_h')
        b7 = types.InlineKeyboardButton(text="/4 Эдуард Мане", callback_data='right_h')
        keyboard.add(b4, b5, b6, b7, )
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)
    elif random_picture == 'моне.jpg':
        image = open('моне.jpg', 'rb')
        bot.send_sticker(chat_id, image)
        keyboard = types.InlineKeyboardMarkup()
        b4 = types.InlineKeyboardButton(text="/1 Рене Магритт", callback_data='false_h')
        b5 = types.InlineKeyboardButton(text="/2 Сальвадор Дали", callback_data='false_h')
        b6 = types.InlineKeyboardButton(text="/3 Клод Моне", callback_data='right_h')
        b7 = types.InlineKeyboardButton(text="/4 Эдуард Мане", callback_data='false_h')
        keyboard.add(b4, b5, b6, b7, )
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)
    elif random_picture == 'дали.jpg':
        image = open('дали.jpg', 'rb')
        bot.send_sticker(chat_id, image)
        keyboard = types.InlineKeyboardMarkup()
        b4 = types.InlineKeyboardButton(text="/1 Рене Магритт", callback_data='false_h')
        b5 = types.InlineKeyboardButton(text="/2 Сальвадор Дали", callback_data='right_h')
        b6 = types.InlineKeyboardButton(text="/3 Клод Моне", callback_data='false_h')
        b7 = types.InlineKeyboardButton(text="/4 Эдуард Мане", callback_data='false_h')
        keyboard.add(b4, b5, b6, b7, )
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)


def get_music_sound(message):
    music = ['1.ogg', '2.wav', '3.wav']
    random_mus = random.choice(music)
    if random_mus == '1.ogg':
        audio = open(random_mus, 'rb')
        bot.send_audio(message.chat.id, audio)
        keyboard = types.InlineKeyboardMarkup()
        b5 = types.InlineKeyboardButton(text="/1 Кот", callback_data='cat1')
        b6 = types.InlineKeyboardButton(text="/2 Собака", callback_data='dog1')
        b7 = types.InlineKeyboardButton(text="/3 Корова", callback_data='cow1')
        b8 = types.InlineKeyboardButton(text="/4 Конь", callback_data='horse1')
        keyboard.add(b5, b6, b7, b8)
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)

    elif random_mus == '2.wav':
        audio = open(random_mus, 'rb')
        bot.send_audio(message.chat.id, audio)
        keyboard = types.InlineKeyboardMarkup()
        b5 = types.InlineKeyboardButton(text="/1 Кот", callback_data='cat2')
        b6 = types.InlineKeyboardButton(text="/2 Собака", callback_data='dog2')
        b7 = types.InlineKeyboardButton(text="/3 Корова", callback_data='cow2')
        b8 = types.InlineKeyboardButton(text="/4 Конь", callback_data='horse2')
        keyboard.add(b5, b6, b7, b8)
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)

    elif random_mus == '3.wav':
        audio = open(random_mus, 'rb')
        bot.send_audio(message.chat.id, audio)
        keyboard = types.InlineKeyboardMarkup()
        b5 = types.InlineKeyboardButton(text="/1 Кот", callback_data='cat3')
        b6 = types.InlineKeyboardButton(text="/2 Собака", callback_data='dog3')
        b7 = types.InlineKeyboardButton(text="/3 Корова", callback_data='cow3')
        b8 = types.InlineKeyboardButton(text="/4 Конь", callback_data='horse3')
        keyboard.add(b5, b6, b7, b8)
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)


def get_music(message):
    music = ['Чайковский.mp3', 'Чайковский2.mp3', 'Корсоков.mp3', 'Вивальди.mp3']
    random_mus = random.choice(music)
    if random_mus == 'Чайковский.mp3':
        audio = open(random_mus, 'rb')
        bot.send_audio(message.chat.id, audio)
        keyboard = types.InlineKeyboardMarkup()
        b9 = types.InlineKeyboardButton(text="/1 Римский-Корсаков Н.А.", callback_data='aut1')
        b10 = types.InlineKeyboardButton(text="/2 Чайковский П.И.", callback_data='aut2')
        b11 = types.InlineKeyboardButton(text="/3 Бах И.С.", callback_data='aut3')
        b12 = types.InlineKeyboardButton(text="/4 Вивальди А.", callback_data='aut4')
        keyboard.add(b9, b10, b11, b12)
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)

    elif random_mus == 'Чайковский2.mp3':
        audio = open(random_mus, 'rb')
        bot.send_audio(message.chat.id, audio)
        keyboard = types.InlineKeyboardMarkup()
        b9 = types.InlineKeyboardButton(text="/1 Римский-Корсаков Н.А.", callback_data='aut5')
        b10 = types.InlineKeyboardButton(text="/2 Чайковский П.И.", callback_data='aut6')
        b11 = types.InlineKeyboardButton(text="/3 Бах И.С.", callback_data='aut7')
        b12 = types.InlineKeyboardButton(text="/4 Вивальди А.", callback_data='aut8')
        keyboard.add(b9, b10, b11, b12)
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)

    elif random_mus == 'Корсоков.mp3':
        audio = open(random_mus, 'rb')
        bot.send_audio(message.chat.id, audio)
        keyboard = types.InlineKeyboardMarkup()
        b9 = types.InlineKeyboardButton(text="/1 Римский-Корсаков Н.А.", callback_data='aut9')
        b10 = types.InlineKeyboardButton(text="/2 Чайковский П.И.", callback_data='aut10')
        b11 = types.InlineKeyboardButton(text="/3 Бах И.С.", callback_data='aut11')
        b12 = types.InlineKeyboardButton(text="/4 Вивальди А.", callback_data='aut12')
        keyboard.add(b9, b10, b11, b12)
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)

    elif random_mus == 'Вивальди.mp3':
        audio = open(random_mus, 'rb')
        bot.send_audio(message.chat.id, audio)
        keyboard = types.InlineKeyboardMarkup()
        b9 = types.InlineKeyboardButton(text="/1 Римский-Корсаков Н.А.", callback_data='aut13')
        b10 = types.InlineKeyboardButton(text="/2 Чайковский П.И.", callback_data='aut14')
        b11 = types.InlineKeyboardButton(text="/3 Бах И.С.", callback_data='aut15')
        b12 = types.InlineKeyboardButton(text="/4 Вивальди А.", callback_data='aut16')
        keyboard.add(b9, b10, b11, b12)
        time.sleep(2)
        bot.send_message(message.chat.id, 'Это...', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global gold, lucky, inventory
    if call.data == 'a':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, lines[6])
        time.sleep(2)
        get_ulitsa(msg)
    elif call.data == 'b':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Я медленно встал с постели и подошёл к окну.')
        time.sleep(2)
        get_okno(msg)

    elif call.data == 'c':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Когда я прошёл немного влево, то увидел давно знакомую гильдию.')
        time.sleep(2)
        get_left(msg)
    elif call.data == 'd':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, lines[129])
        time.sleep(2)
        get_right(msg)
    elif call.data == 'easy':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, lines[21])
        get_music_sound(msg)
    elif call.data == 'hard':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, lines[22])
        time.sleep(2)
        get_music(msg)

    elif call.data == 'easy_p':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Определите автора картины')
        picture_easy(msg)
    elif call.data == 'hard_p':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Определите автора картины')
        picture_hard(msg)
    elif call.data == 'cat1':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Молодец!Держи 25 золотых!')
        gold = +25
        gildia_choise(msg)
    elif call.data == 'dog1':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'cow1':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'horse1':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'cat2':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'dog2':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Молодец!Держи 25 золотых!')
        gold = +25
        gildia_choise(msg)
    elif call.data == 'cow2':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'horse2':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'cat3':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'dog3':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'cow3':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Молодец!Держи 25 золотых!')
        gold += 25
        gildia_choise(msg)
    elif call.data == 'horse3':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)

    elif call.data == 'aut1':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'aut2':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Молодец!Держи 50 золотых!')
        gold += 50
        gildia_choise(msg)
    elif call.data == 'aut3':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'aut4':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'aut5':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'aut6':
        time.sleep(2)
        gold += 50
        msg = bot.send_message(call.message.chat.id, 'Молодец!Держи 50 золотых!')
        gildia_choise(msg)
    elif call.data == 'aut7':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'aut8':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'aut9':
        time.sleep(2)
        gold += 50
        msg = bot.send_message(call.message.chat.id, 'Молодец!Держи 50 золотых!')
        gildia_choise(msg)
    elif call.data == 'aut10':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'aut11':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'aut12':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'aut13':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'aut14':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'aut15':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'aut16':
        time.sleep(2)
        gold += 50
        msg = bot.send_message(call.message.chat.id, 'Молодец!Держи 50 золотых!')
        gildia_choise(msg)
    elif call.data == 'come_in':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, lines[131])
        fortune_teller(msg)
    elif call.data == 'go_further':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Он показался мне слишком странным и я решил туда не заходить')
        get_choice_r(msg)
    elif call.data == 'false':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'right':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Молодец!Держи 25 золотых!')
        gold += 25
        gildia_choise(msg)
    elif call.data == 'false_h':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Увы, но нет :(')
        gildia_choise(msg)
    elif call.data == 'right_h':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Молодец!Держи 50 золотых!')
        gold += 50
        gildia_choise(msg)
    elif call.data == 'yes':
        time.sleep(2)
        chat_id = call.message.chat.id
        msg = bot.send_message(chat_id, 'Я хоть и не верю в предсказания, но мне интересно...')
        time.sleep(2)
        get_go_further(msg)

    elif call.data == 'no':
        time.sleep(2)
        bot.send_message(call.message.chat.id, 'Не люблю я предсказания....')
        msg = bot.send_message(call.message.chat.id, 'Я вышел из шатра')
        time.sleep(2)
        get_choice_r(msg)
    elif call.data == 'home_r':
        msg = bot.send_message(call.message.chat.id, lines[168])
        time.sleep(2)
        get_home(msg)
    elif call.data == 'left_r':

        msg = bot.send_message(call.message.chat.id, 'Пожалуй, пойду влево')
        time.sleep(2)
        get_left(msg)
    elif call.data == 'right_r':
        msg = bot.send_message(call.message.chat.id, 'Пожалуй, пойду вправо')
        time.sleep(2)
        shop(msg)
    elif call.data == 'map':
        msg = bot.send_message(call.message.chat.id, '-Это старинная карта')
        time.sleep(2)
        map(msg)
    elif call.data == 'bank':
        msg = bot.send_message(call.message.chat.id, '-Если вы невезучи, то купив зелье вы это быстро исправите')
        time.sleep(2)
        bank(msg)
    elif call.data == 'stick':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, '-Увы, но без рецепта я не могу вам её продать')
        shop_choice(msg)
    elif call.data == 'leave':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Я решил покинуть магазин')
        get_choice_s(msg)
    elif call.data == 'left_s':
        time.sleep(2)
        msg = bot.send_message(call.message.chat.id, 'Я пришёл обратно к шатру, но его уже не было но месте ')
        get_choice_r(msg)
    elif call.data == 'buy_m':
        if gold >= 100:
            msg = bot.send_message(call.message.chat.id, '*Карта куплена')
            gold -= 100
            inventory.append('map')
            time.sleep(2)
            shop_choice(msg)
        elif gold == 0:
            time.sleep(2)
            bot.send_message(call.message.chat.id, 'Я достал свой мешочек с деньгами и увидел там'
                                                   ' лишь немного серебряников')
            time.sleep(2)
            msg = bot.send_message(call.message.chat.id, 'Я не буду покупать этот предмет')
            shop_choice(msg)
        else:
            time.sleep(2)
            bot.send_message(call.message.chat.id, f'Я достал свой мешочек с деньгами и увидел там {gold} золотых')
            time.sleep(2)
            msg = bot.send_message(call.message.chat.id, 'Я не буду покупать этот предмет')
            shop_choice(msg)
    elif call.data == 'renouncement_m':
        msg = bot.send_message(call.message.chat.id, 'Я не буду покупать этот предмет')
        shop_choice(msg)
    elif call.data == 'buy_b':
        if gold >= 50:
            gold -= 50
            lucky += 50
            msg = bot.send_message(call.message.chat.id,
                                   f'*Удача увеличена на 50 единиц. Ваша удача равна {lucky} единицам ')
            time.sleep(2)
            shop_choice(msg)
        elif gold == 0:
            time.sleep(2)
            bot.send_message(call.message.chat.id, 'Я достал свой мешочек с деньгами и увидел там'
                                                   ' лишь немного серебряников')
            time.sleep(2)
            msg = bot.send_message(call.message.chat.id, 'Я не буду покупать этот предмет')
            shop_choice(msg)
        else:
            time.sleep(2)
            bot.send_message(call.message.chat.id, f'Я достал свой мешочек с деньгами и увидел там {gold} золотых')
            time.sleep(2)
            msg = bot.send_message(call.message.chat.id, 'Я не буду покупать этот предмет')
            shop_choice(msg)
    elif call.data == 'renouncement_b':
        msg = bot.send_message(call.message.chat.id, 'Я не буду покупать этот предмет')
        shop_choice(msg)
    elif call.data == 'right_g':
        msg = bot.send_message(call.message.chat.id, 'Пожалуй, пойду вправо')
        time.sleep(2)
        shop(msg)
    elif call.data == 'exit':
        msg = bot.send_message(call.message.chat.id, 'Я устал выполнять задания и вышел из гильдии. ')
        time.sleep(2)
        get_choise_g(msg)
    elif call.data == 'task':
        msg = bot.send_message(call.message.chat.id, 'Пожалуй, выполню ещё задание')
        time.sleep(2)
        get_left(msg)


bot.polling(none_stop=True)
