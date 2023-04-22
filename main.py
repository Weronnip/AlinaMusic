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
    mk4 = types.KeyboardButton('/added music')
    markup.add(mk1, mk2)
    markup.add(mk3, mk4)
    bot.send_message(message.chat.id, "Приветик😊, {0.first_name}!".format(message.from_user), reply_markup=markup )

bot.polling(none_stop=True, interval=0)