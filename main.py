import os
import telebot
from telebot import types
from yandex_music import Client
from configureted.token_bot import token_bot
from configureted.token_bot import yandex_token

bot = telebot.TeleBot(token_bot)
client = Client().init()
# onclient = Client(yandex_token).init()

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

type_to_name = {
    'track': 'трек',
    'artist': 'исполнитель',
    'album': 'альбом',
    'playlist': 'плейлист',
    'video': 'видео',
    'user': 'пользователь',
    'podcast': 'подкаст',
    'podcast_episode': 'эпизод подкаста',
}

@bot.message_handler(commands=['search'])
def post(message):
    chat = message.chat.id

    type_to_name = {
        'track': 'трек',
        'artist': 'исполнитель',
        'album': 'альбом',
        'playlist': 'плейлист',
        'video': 'видео',
        'user': 'пользователь',
        'podcast': 'подкаст',
        'podcast_episode': 'эпизод подкаста',
    }

    def send_search_request_and_print_result(query):
        search_result = client.search(query)

        text = [f'Результаты по запросу "{query}":', '']

        best_result_text = ''
        if search_result.best:
            type_ = search_result.best.type
            best = search_result.best.result

            text.append(bot.send_message(chat, f'❗️Лучший результат: {type_to_name.get(type_)}'))

            if type_ in ['track', 'podcast_episode']:
                artists = ''
                if best.artists:
                    artists = ' - ' + ', '.join(artist.name for artist in best.artists)
                best_result_text = best.title + artists
            elif type_ == 'artist':
                best_result_text = best.name
            elif type_ in ['album', 'podcast']:
                best_result_text = best.title
            elif type_ == 'playlist':
                best_result_text = best.title
            elif type_ == 'video':
                best_result_text = f'{best.title} {best.text}'

            text.append(bot.send_message(chat, f'Содержимое лучшего результата: {best_result_text}\n'))

        if search_result.artists:
            text.append(bot.send_message(chat, f'Исполнителей: {search_result.artists.total}'))
        if search_result.albums:
            text.append(bot.send_message(chat, f'Альбомов: {search_result.albums.total}'))
        if search_result.tracks:
            text.append(bot.send_message(chat, f'Треков: {search_result.tracks.total}'))
        if search_result.playlists:
            text.append(bot.send_message(chat, f'Плейлистов: {search_result.playlists.total}'))
        if search_result.videos:
            text.append(bot.send_message(chat, f'Видео: {search_result.videos.total}'))

    if message.text == '__main__':
        while True:
            input_query = bot.reply_to(message, 'Введите поисковой запрос: ')
            bot.register_next_step_handler(message, send_search_request_and_print_result)
    else:
        bot.send_message(chat, "Баг! перезагрузите код, и не пишите \n/playlist и /search !!")
        bot.register_next_step_handler(message, post)


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

@bot.message_handler(commands=['playlist'])
def playlist(messages):
    chat = messages.chat.id
    if messages.text == "playlist":
        bot.reply_to(chat, "Команда в разработке прощу прощения ")
        bot.register_next_step_handler(messages, playlist)
    else:
        bot.send_message(chat, "Баг! перезагрузите код, и не пишите \n/playlist и /search !!")
        bot.register_next_step_handler(messages, playlist)

@bot.message_handler(commands=['help'])
def help(message):
    c = message.chat.id
    inline_markup = types.InlineKeyboardMarkup(row_width=2)
    imp1 = types.InlineKeyboardButton("Команды🖋", callback_data='commands')
    imp2 = types.InlineKeyboardButton("FAQ📚", callback_data='faq')
    imp3 = types.InlineKeyboardButton("developer👨‍💻", callback_data='dev')
    inline_markup.add(imp1, imp2)
    inline_markup.add(imp3)
    bot.send_message(c, "Вы вызвали команду помощи".format(message.from_user), reply_markup=inline_markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        if call.message:
            if call.data == "commands":
                bot.send_message(call.message.chat.id, "Команды:\n \n"
                                                       "* /search - поиск песни по запросу\n \n"
                                                       "* /chart - Лучшие песни по мнению Яндекс Музыки\n \n"
                                                       "* /playlist - Сборник лучших песен по мнению, пользователей\n\n"
                                                       "* /help - Помощь в случай, не понятных ституаций с ботом ")

        if  call.message:
            if call.data == "faq":
                mep = types.InlineKeyboardMarkup(row_width=1)
                mp1 = types.InlineKeyboardButton("Цель бота", callback_data='bots')
                mep.add(mp1)
                bot.send_message(call.message.chat.id, "FAQ - ответ на вопросы", reply_markup=mep)

        if call.message:
            if call.data == "bots":
                bot.send_message(call.message.chat.id, "Цель бота, дарить бесплатную музыку:)")

        if call.message:
            if call.data == "dev":
                bot.send_message(call.message.chat.id, "Связь с разработчиком: \n \n telegram: @weronnip \n \n "
                                                       "vk: @weronnip")

    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True, interval=0)