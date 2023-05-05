import discord
import requests

API_KEY = 'API_KEY'

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'help_bot':
        response = 'Привет! Я могу сообщать текущую погоду и прогноз на несколько дней. Для получения текущей погоды используйте команду "current", а для прогноза на несколько дней - "forecast {количество дней}". Чтобы задать место для прогноза, используйте команду "place {название города}"'
        await message.channel.send(response)

    elif message.content.startswith('place'):
        location = message.content.split(' ')[1]
        url = f'https://api.weather.yandex.ru/v2/forecast?&lang=ru_RU&limit=1&hours=false&geoid=&lat=&lon=&extra=false&{location}=true'
        headers = {'X-Yandex-API-Key': API_KEY}
        response = requests.get(url, headers=headers).json()
        city = response['geo_object']['locality']['name']
        await message.channel.send(f'Место прогноза установлено на {city}')

    elif message.content == 'current':
        url = f'https://api.weather.yandex.ru/v2/forecast?&lang=ru_RU&limit=1&hours=false&geoid=&lat=&lon=&extra=false'
        headers = {'X-Yandex-API-Key': API_KEY}
        response = requests.get(url, headers=headers).json()
        fact = response['fact']
        temp = fact['temp']
        pressure = fact['pressure_mm']
        humidity = fact['humidity']
        wind_dir = fact['wind_dir']
        wind_speed = fact['wind_speed']
        await message.channel.send(f'Температура: {temp} градусов Цельсия\nДавление: {pressure} мм.рт.ст.\nВлажность: {humidity}%\nНаправление ветра: {wind_dir}\nСкорость ветра: {wind_speed} м/с')

client.loop.create_task(on_message())
client.run()