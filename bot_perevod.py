import discord
import requests
import json

client = discord.Client()

translate_url = "https://translate.yandex.net/api/v1.5/tr.json/translate"

direction = 'en-ru'

def translate_text(text, direction):
    params = {
        'key': 'YOUR_API_KEY_HERE',
        'text': text,
        'lang': direction
    }
    response = requests.get(translate_url, params=params)
    result = json.loads(response.text)
    return result['text'][0]

async def handle_command(message):
    if message.content == '/help_bot':
        await message.channel.send('Commands:\n/set_lang - Set translation direction (default: en-ru)\n/text - Translate text')
    elif message.content.startswith('/set_lang'):
        global direction
        direction = message.content.split()[1]
        await message.channel.send(f'Translation direction set to {direction}')
    elif message.content.startswith('/text'):
        text_to_translate = message.content.split(maxsplit=1)[1]
        translated_text = translate_text(text_to_translate, direction)
        await message.channel.send(f'Translated text: {translated_text}')

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('/'):
        await handle_command(message)

client.run('BOT_TOKEN')