import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

NAME, CITY, WEATHER = range(3)

def start(update, context):
    update.message.reply_text('Привет! Как тебя зовут?')
    return NAME

def get_name(update, context):
    context.user_data['name'] = update.message.text
    update.message.reply_text('Отлично, {}. А в каком городе ты живешь?'.format(context.user_data['name']))
    return CITY

def get_city(update, context):
    context.user_data['city'] = update.message.text
    update.message.reply_text('Понятно. А какая погода в городе {}?'.format(context.user_data['city']))
    return WEATHER

def get_weather(update, context):
    context.user_data['weather'] = update.message.text
    update.message.reply_text('Спасибо за информацию, {}!'.format(context.user_data['name']))
    return ConversationHandler.END

def skip_city(update, context):
    update.message.reply_text('Хорошо, а какая погода у вас за окном?')
    return WEATHER

def cancel(update, context):
    update.message.reply_text('Жаль, что ты не захотел поделиться этой информацией. До свидания!')
    return ConversationHandler.END

def main():
    updater = Updater('6176384593:AAF1akigJOLjs6GHlu7cc65eloinb7gHEGw', use_context=True)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text, get_name)],
            CITY: [MessageHandler(Filters.text & ~Filters.command, get_city), CommandHandler('skip', skip_city)],
            WEATHER: [MessageHandler(Filters.text & ~Filters.command, get_weather)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    updater.dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()