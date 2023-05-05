import discord
import pymorphy2

client = discord.Client()
morph = pymorphy2.MorphAnalyzer()


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = message.content.lower()
    words = text.split()
    result = []

    for word in words:
        parsed = morph.parse(word)[0]
        if parsed.tag.POS == 'NUMR':
            result.append(parsed.make_agree_with_number(1).word)
        elif parsed.tag.POS == 'NOUN':
            if parsed.tag.animacy == 'anim':
                agree = parsed.inflect({'nomn', 'sing'})
                result.append(agree.word)
            elif parsed.tag.animacy == 'inan':
                agree = parsed.inflect({'nomn', 'sing'})
                result.append(agree.word)
            else:
                result.append(word)
        else:
            result.append(word)

    response = ' '.join(result)
    await message.channel.send(response)


client.run('BOT_TOKEN')