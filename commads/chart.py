import os
import telebot
from yandex_music import Client
from configureted.token_bot import token_bot
from configureted.token_bot import yandex_token

bot = telebot.TeleBot(token_bot)

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

    print('\n'.join(text))