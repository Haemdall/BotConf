import telebot
from telebot import types

token = ""                      # Токен бота
bot = telebot.TeleBot(token)
volunteersChannel = ""          # Канал волонтеров
speakerChannel = ""             # Канал канал спикеров
messVolunteers = ""             # Сообщение волонтерам
messSpeaker = ""                # Сообщение спикерам
rowNum = ""                     # Номер ряда
placeNum = ""                   # Номер места

# Клавиатуры для пользователя
keyboardStart = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardCancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardRedirect = types.InlineKeyboardMarkup()
keyboardGoIt = types.InlineKeyboardMarkup()

# Кнопки на клавиатурах
btnQuestion = types.KeyboardButton("📢 Задать вопрос спикеру")
btnOrder = types.KeyboardButton("🆘 Обратиться за помощью")
btnGoIt = types.KeyboardButton("🦾 Стать Айтишником")
btnCancel = types.KeyboardButton("🚫 Отменить")
btnGroup = types.InlineKeyboardButton(text="Чат с поддержкой", url="https://t.me/+uhdq9BVb9aowZjdi")
btnIt = types.InlineKeyboardButton(text="Наш сайт", url="https://clck.ru/32iXzF")

# Добавление кнопок на клавиатуры
keyboardStart.row(btnQuestion)
keyboardStart.row(btnOrder)
keyboardStart.row(btnGoIt)
keyboardCancel.add(btnCancel)
keyboardRedirect.add(btnGroup)
keyboardGoIt.add(btnIt)

@bot.message_handler(commands=['start'])
def start(message):
    """Реакция бота на /start и приветствие пользователя"""
    bot.send_message(message.from_user.id, "{0}, рад приветствовать Вас на конференции!🥳".format(message.from_user.first_name))
    bot.send_message(message.from_user.id, "Сделайте выбор с помощью кнопок внизу☺", reply_markup=keyboardStart)

@bot.message_handler(content_types=['text'])
def getMessages(message):
    """Реакция бота на текстовые сообщения пользователя"""
    global rowNum, placeNum # Добавляем глобальные переменные в функцию
    if message.text == "📢 Задать вопрос спикеру":
        bot.send_message(message.from_user.id, "Напишите мне свой вопрос и я отправлю его спикеру", reply_markup=keyboardCancel)
        bot.register_next_step_handler(message, sendQuestion) # Ждем ответ и уходим в функцию sendQuestion
    elif message.text == "🆘 Обратиться за помощью":
        bot.send_message(message.from_user.id, "Прошу вас перейти по ссылке ниже:", reply_markup=keyboardRedirect)
    #   bot.register_next_step_handler(message, getRow) при надобности раскоментить вместе с getRow и getPlace # Ждем ответ и уходим в функцию getRow
    elif message.text == "🦾 Стать Айтишником":
        bot.send_message(message.from_user.id, "Присоединяйся к нам!", reply_markup=keyboardGoIt)
    else:
        bot.send_message(message.from_user.id, "Извините, я Вас не понимаю... Воспользуйтесь кнопками", reply_markup=keyboardStart)

def sendQuestion(message):
    """Отправка сообщения в канал спикеров"""
    global messSpeaker # Добавляем глобальную переменную
    if message.text == "🚫 Отменить":
        """Если пользователь передумал отправлять сообщение в канал"""
        bot.send_message(message.from_user.id, "Дайте знать если еще что то понадобится", reply_markup=keyboardStart)
        bot.register_next_step_handler(message, getMessages)
    else:
        """Отправка и зануление переменных"""
        messSpeaker = message.text
        bot.send_message(speakerChannel, messSpeaker) # Отправка
        messSpeaker = ""
        bot.send_message(message.from_user.id, "Ваше сообщение отправлено спикеру", reply_markup=keyboardStart)
        bot.register_next_step_handler(message, getMessages)

'''
Выпилено из финального релиза в связи с отсутствием нумерации

def getRow(message):
    """Получаем ряд пользователя"""
    global rowNum
    rowNum = message.text
    try:
        """Проверка что пользователь ввел именно число"""
        rowNum = int(rowNum)
        bot.send_message(message.from_user.id, "Напишите номер Вашего места", reply_markup=keyboardCancel)
        bot.register_next_step_handler(message, getPlace) # Ждем ответ и переходим в функцию getPlace
    except Exception:
        """Обработка исключений и отмена ввода с возвратом в главное меню"""
        if message.text == "🚫 Отменить":
            rowNum = ""
            bot.send_message(message.from_user.id, "Дайте знать если еще что то понадобится", reply_markup=keyboardStart)
            bot.register_next_step_handler(message, getMessages) # Ждем ответа в функции getMessages
        else:
            bot.send_message(message.from_user.id, "Попробуйте еще раз, надо ввести число", reply_markup=keyboardCancel)
            bot.register_next_step_handler(message, getRow) # Рекурсим функцию



def getPlace(message):
    """Получение места пользователя, формирование сообщения в канал волонтеров и зануление переменных"""
    global rowNum, placeNum, messVolunteers # Добавляем глобальные
    placeNum = message.text
    try:
        """Проверка на то, что пользователь ввел в место число """
        placeNum = int(placeNum)
        messVolunteers = f"Гостю в ряду №{rowNum} место №{placeNum}\nтребуется помощь\nподойдите к нему"
        bot.send_message(volunteersChannel, messVolunteers) # отправка сообщения в канал волонтеров
        messVolunteers = ""
        rowNum = ""
        placeNum = ""
        bot.send_message(message.from_user.id, "Наш сотрудник подойдет к Вам, немного подождите☺", reply_markup=keyboardStart)
        bot.register_next_step_handler(message, getMessages)
    except Exception:
        """Обработка исключений"""
        if message.text == "🚫 Отменить":
            """Отмена операции"""
            rowNum = ""
            placeNum = ""
            messVolunteers = ""
            bot.send_message(message.from_user.id, "Дайте знать если еще что то понадобится", reply_markup=keyboardStart)
            bot.register_next_step_handler(message, getMessages) # Ждем сообщение и переходим в главное меню (функция getMessages)
        else:
            bot.send_message(message.from_user.id, "Попробуйте еще раз, надо ввести число", reply_markup=keyboardCancel)
            bot.register_next_step_handler(message, getPlace) # Рекурсим функцию
'''


"""Постоянно ожидаем сообщение пользователей"""
bot.polling(none_stop=True, interval=0)
