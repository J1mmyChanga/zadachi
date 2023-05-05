import discord
import requests
import json

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print('Ready to show cute cats and dogs!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'кот' in message.content.lower():
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        data = json.loads(response.text)
        url = data[0]['url']
        await message.channel.send(file=discord.File(requests.get(url, stream=True).raw, "cat.png"))

    if 'собак' in message.content.lower():
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = json.loads(response.text)
        url = data['message']
        await message.channel.send(file=discord.File(requests.get(url, stream=True).raw, "dog.png"))

client.run('BOT_TOKEN')