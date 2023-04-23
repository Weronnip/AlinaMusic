import telebot
# import random
from telebot import types
from configureted.token_bot import token_bot

bot = telebot.TeleBot(token_bot)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    mk1 = types.KeyboardButton('/search')
    mk2 = types.KeyboardButton('/best')
    mk3 = types.KeyboardButton('/playlist')
    mk4 = types.KeyboardButton('/music')
    markup.add(mk1, mk2)
    markup.add(mk3, mk4)
    bot.send_message(message.chat.id, "Приветик😊, {0.first_name}! \n \nЕсли нужна помощь напиши /help".format(message.from_user), reply_markup=markup )

@bot.message_handler(commands=['search'])
def search(message):
    bot.send_message(message.chat.id, "Введите название песни")

@bot.message_handler(commands=['help'])
def help(message):
    inlmp = types.InlineKeyboardMarkup(row_width=2)
    im1 = types.InlineKeyboardButton("Seacrh", callback_data="seacrh")
    im2 = types.InlineKeyboardButton("Best", callback_data="best")
    im3 = types.InlineKeyboardButton("Playlist", callback_data="playlist")
    im4 = types.InlineKeyboardButton("music", callback_data="addmusic")
    inlmp.add(im1, im2)
    inlmp.add(im3, im4)
    bot.send_message(message.chat.id, "Вы открыли меню помощи".format(message.from_user), reply_markup=inlmp)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        if call.message:
            if call.data == "seacrh":
                bot.send_message(call.message.chat.id, '/seacrh - ищет песни по запросу в своей базе данных')
        if call.message:
            if call.data == "best":
                bot.send_message(call.message.chat.id, '/best - подборка лучших треков за неделю')
        if call.message:
            if call.data == "playlist":
                bot.send_message(call.message.chat.id, '/playlist - Список песен в котором\n '
                                                       'находятся более двадцати различных песен.\n'
                                                       '\n'
                                                       'Так же вы моежете создать свой плей-лист,\n '
                                                       'для других пользователей')
        if call.message:
            if call.data == "addmusic":
                bot.send_message(call.message.chat.id, '/music - команда позволяет подбирать рандомный трек.\n'
                                                       'Так же вы можете загрузить свой трек')
    except Exception as e:
        print(repr(e))

bot.polling()