import discord
import random

client = discord.Client()

emojis = [':smiley:', ':sunglasses:', ':thinking:', ':angry:', ':laughing:', ':heart:']
scores = {'user': 0, 'bot': 0}
current_emojis = emojis.copy()


def get_emoji(number):
    if number > len(current_emojis):
        number = number % len(current_emojis)
    return current_emojis[number - 1]


def get_emoji_value(emoji):
    return ord(emoji)


def play_round(number):
    user_emoji = get_emoji(number)
    bot_emoji = get_emoji(random.randint(1, len(current_emojis)))
    result = get_emoji_value(user_emoji) - get_emoji_value(bot_emoji)
    if result > 0:
        scores['user'] += 1
    elif result < 0:
        scores['bot'] += 1
    current_emojis.remove(user_emoji)
    current_emojis.remove(bot_emoji)
    random.shuffle(current_emojis)
    return user_emoji, bot_emoji


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.content.startswith('/play'):
        await message.channel.send('Starting a new game! To stop the game, type /stop')
        current_emojis = emojis.copy()
        scores['user'] = 0
        scores['bot'] = 0
        while current_emojis:
            try:
                user_number = await client.wait_for('message', timeout=10.0, check=lambda m: m.author == message.author)
                if user_number.content == '/stop':
                    current_emojis = []
                    scores['user'] = 0
                    scores['bot'] = 0
                    await message.channel.send('Game stopped! Scores have been reset.')
                else:
                    user_emoji, bot_emoji = play_round(int(user_number.content))
                    await message.channel.send(f'User: {user_emoji}\nBot: {bot_emoji}\nScores: {scores}')
            except asyncio.TimeoutError:
                await message.channel.send('Time\'s up! You didn\'t respond in time. Game over.')
                break
        if scores['user'] > scores['bot']:
            await message.channel.send('Congratulations! You won!')
        elif scores['user'] < scores['bot']:
            await message.channel.send('Sorry, you lost. Better luck next time.')
        else:
            await message.channel.send('It\'s a tie!')


client.run('BOT_TOKEN')