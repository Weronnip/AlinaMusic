import telebot
# # import random
# import os
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
    bot.send_message(message.chat.id, "Приветик😊, {0.first_name}!"
                                    " \n \nЕсли нужна помощь напиши /help"
                                    .format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['music'])
def listmusic(message):
    bth = types.InlineKeyboardMarkup(row_width=2)
    bt1 = types.InlineKeyboardButton("Added", callback_data="added")
    bt2 = types.InlineKeyboardButton("random", callback_data="rand")
    # bt3 = types.InlineKeyboardButton("close", callback_data="close")
    bth.add(bt1, bt2)
    # bth.add(bt3)
    bot.send_message(message.chat.id, "Выберите действие".format(message.from_user), reply_markup=bth)

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

        if call.message:
            if call.data == "added":
                bot.send_message(call.message.chat.id, 'Загрузите вашу песню...')

        if call.message:
            if call.data == "rand":
                bot.send_message(call.message.chat.id, 'Идет подборка песни, прошу подождите пожалуйста...')

    except Exception as e:
        print(repr(e))

bot.polling()