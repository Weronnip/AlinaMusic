import telebot
from telebot import types
from configureted.token_bot import token_bot
from yandex_music import Client

bot = telebot.TeleBot(token_bot)
client = Client().init()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    mk1 = types.KeyboardButton('/search')
    mk2 = types.KeyboardButton('лучшие')
    mk3 = types.KeyboardButton('плейлист')
    mk4 = types.KeyboardButton('музыка')
    markup.add(mk1, mk2)
    markup.add(mk3, mk4)
    bot.send_message(message.chat.id, "Приветик😊, {0.first_name}!"
                                    " \n \nЕсли нужна помощь напиши /help"
                                    .format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['search'])
def post(message):
    chat = message.chat.id

    input_query = bot.send_message(chat, 'Введите поисковой запрос: ')
    bot.register_next_step_handler(input_query, send_search_request_and_print_result)
def send_search_request_and_print_result(query):
    search_result = client.search(query)

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

    text = [f'Результаты по запросу "{query}":', '']

    best_result_text = ''
    if search_result.best:
        type_ = search_result.best.type
        best = search_result.best.result

        text.append(f'❗️Лучший результат: {type_to_name.get(type_)}')

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

        text.append(f'Содержимое лучшего результата: {best_result_text}\n')

    if search_result.artists:
        text.append(f'Исполнителей: {search_result.artists.total}')
    if search_result.albums:
        text.append(f'Альбомов: {search_result.albums.total}')
    if search_result.tracks:
        text.append(f'Треков: {search_result.tracks.total}')
    if search_result.playlists:
        text.append(f'Плейлистов: {search_result.playlists.total}')
    if search_result.videos:
        text.append(f'Видео: {search_result.videos.total}')

    if __name__ == '__main__':
            while True:
                pass

bot.polling(none_stop=True, interval=0)