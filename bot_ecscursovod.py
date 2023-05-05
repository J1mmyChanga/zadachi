import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

FIRST, SECOND, THIRD, FOURTH, EXIT = range(5)

keyboard_main = [['Зал 1'], ['Зал 2'], ['Зал 3'], ['Зал 4']]
keyboard_exit = [['Выход']]

texts = {
    'Зал 1': 'В данном зале представлено...',
    'Зал 2': 'В данном зале представлено...',
    'Зал 3': 'В данном зале представлено...',
    'Зал 4': 'В данном зале представлено...',
}

def start(update, context):
    reply_markup = ReplyKeyboardMarkup(keyboard_main, resize_keyboard=True)
    update.message.reply_text('Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!', reply_markup=reply_markup)
    return FIRST

def exit(update, context):
    reply_markup = ReplyKeyboardMarkup(keyboard_exit, resize_keyboard=True)
    update.message.reply_text('Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!', reply_markup=reply_markup)
    return EXIT

def button(update, context):
    query = update.callback_query
    choice = query.data
    if choice == 'Зал 1':
        query.edit_message_text(text=texts[choice])
        reply_markup = ReplyKeyboardMarkup(keyboard_main, resize_keyboard=True)
        context.user_data['last_choice'] = choice
        return SECOND
    elif choice == 'Зал 2':
        query.edit_message_text(text=texts[choice])
        reply_markup = ReplyKeyboardMarkup(keyboard_main, resize_keyboard=True)
        context.user_data['last_choice'] = choice
        return THIRD
    elif choice == 'Зал 3':
        query.edit_message_text(text=texts[choice])
        reply_markup = ReplyKeyboardMarkup(keyboard_main, resize_keyboard=True)
        context.user_data['last_choice'] = choice
        return FOURTH
    elif choice == 'Зал 4':
        query.edit_message_text(text=texts[choice])
        reply_markup = ReplyKeyboardMarkup(keyboard_exit, resize_keyboard=True)
        context.user_data['last_choice'] = choice
        return EXIT
    elif choice == 'Выход':
        query.edit_message_text(text='Спасибо, что посетили наш музей!', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END