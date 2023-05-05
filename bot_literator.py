from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

POEM_TEXT = """
Что мне твое вечернее звездопаденье,
Если в них нет той, которой мил я был?
"""

current_line = 0


def start(update, context):
    global current_line
    current_line = 0
    update.message.reply_text(POEM_TEXT.strip().split("\n")[current_line])


def handle_text(update, context):
    global current_line
    user_input = update.message.text.strip()
    poem_lines = POEM_TEXT.strip().split("\n")
    if user_input.lower() == poem_lines[current_line + 1].lower():
        current_line += 1
        if current_line == len(poem_lines) - 1:
            update.message.reply_text("Отлично! Вы прошли стихотворение! Хотите повторить?")
            current_line = 0
        else:
            update.message.reply_text(poem_lines[current_line])
    else:
        update.message.reply_text("Нет, не так. Вот правильный ответ:")
        update.message.reply_text(poem_lines[current_line + 1])


def suphler(update, context):
    poem_lines = POEM_TEXT.strip().split("\n")
    update.message.reply_text("Правильный ответ:")
    update.message.reply_text(poem_lines[current_line + 1])


def stop(update, context):
    update.message.reply_text("До свидания!")
    updater.stop()


if __name__ == "__main__":
    updater = Updater("6176384593:AAF1akigJOLjs6GHlu7cc65eloinb7gHEGw", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("suphler", suphler))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(MessageHandler(Filters.text, handle_text))
    # Запускаем бота
    updater.start_polling()
    updater.idle()