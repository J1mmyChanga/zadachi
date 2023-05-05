import discord
import asyncio
import datetime

TOKEN = "BOT_TOKEN"
CHANNEL_ID = "CHANNEL_ID"
TIME = "21:00"

client = discord.Client()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")

async def send_message():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    while not client.is_closed():
        now = datetime.datetime.now().strftime('%H:%M')
        if now == TIME:
            await channel.send("Время Х наступило!")
            await asyncio.sleep(60)

client.loop.create_task(send_message())
client.run(TOKEN)