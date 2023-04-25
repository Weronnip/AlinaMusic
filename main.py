import os
import telebot
from telebot import types
from yandex_music import Client
from configureted.token_bot import token_bot
from configureted.token_bot import yandex_token

bot = telebot.TeleBot(token_bot)
client = Client().init()

@bot.message_handler(commands=['start'])
def start(message):
    chat = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    mp1 = types.KeyboardButton('/search')
    mp2 = types.KeyboardButton('/chart')
    mp3 = types.KeyboardButton('/playlist')
    mp4 = types.KeyboardButton('/help')
    markup.add(mp1, mp2, mp3)
    markup.add(mp4)
    bot.send_message(chat, "Приветик😄! Я музыкальный бот Алина\n \n "
                           "Если нужна помощь то пиши - /help".format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['chart'])
def charts(message):
    chat = message.chat.id

    CHART_ID = 'world'
    TOKEN = os.environ.get(yandex_token)

    client = Client(TOKEN).init()
    chart = client.chart(CHART_ID).chart

    text = [f'🏆 {chart.title}', chart.description, '', 'Треки:']

    for track_short in chart.tracks:
        track, chart = track_short.track, track_short.chart
        artists = ''
        if track.artists:
            artists = ' - ' + ', '.join(artist.name for artist in track.artists)

        track_text = f'{track.title}{artists}'

        if chart.progress == 'down':
            track_text = '🔻 ' + track_text
        elif chart.progress == 'up':
            track_text = '🔺 ' + track_text
        elif chart.progress == 'new':
            track_text = '🆕 ' + track_text
        elif chart.position == 1:
            track_text = '👑 ' + track_text

        track_text = f'{chart.position} {track_text}'
        text.append(track_text)

        msg = bot.send_message(chat, f"{track_text}")
        bot.register_next_step_handler(msg, track)

bot.polling(none_stop=True, interval=0)