import os
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.environ.get("TOKEN")
translator_api_key = os.environ.get("TRANSLATOR_API_KEY")
translator_endpoint = "https://api.cognitive.microsofttranslator.com/translate"
supported_languages = {
    "en": "English",
    "ru": "Russian"
}


def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    context.chat_data[user_id] = {"src_lang": None, "dst_lang": None}
    keyboard = [[InlineKeyboardButton(supported_languages[lang_code], callback_data=lang_code)]
                for lang_code in supported_languages]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose source language:", reply_markup=reply_markup)


def choose_source_language(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    src_lang = query.data
    context.chat_data[user_id]["src_lang"] = src_lang
    keyboard = [[InlineKeyboardButton(supported_languages[lang_code], callback_data=lang_code)]
                for lang_code in supported_languages if lang_code != src_lang]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Choose destination language:", reply_markup=reply_markup)


def choose_destination_language(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    dst_lang = query.data
    context.chat_data[user_id]["dst_lang"] = dst_lang
    query.edit_message_text(text="Enter text to translate:")


def translate_text(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    src_lang = context.chat_data[user_id]["src_lang"]
    dst_lang = context.chat_data[user_id]["dst_lang"]
    text = update.message.text
    headers = {
        "Ocp-Apim-Subscription-Key": translator_api_key,
        "Content-Type": "application/json"
    }
    params = {
        "api-version": "3.0",
        "from": src_lang,
        "to": dst_lang
    }
    body = [{
        "text": text
    }]
    response = requests.post(translator_endpoint, headers=headers, params=params, json=body)
    if response.status_code == 200:
        translation = response.json()[0]["translations"][0]["text"]
        update.message.reply_text(translation)
    else:
        update.message.reply_text("An error occurred while translating the text.")


def error_handler(update: Update, context: CallbackContext) -> None:
    error_message = f"Update {update} caused error {context.error}"
    update.message.reply_text("An error occurred while processing your request.")
    context.bot.send_message(chat_id=123456789, text=error_message)


if __name__ == "__main__":
    updater = Updater('6176384593:AAF1akigJOLjs6GHlu7cc65eloinb7gHEGw', use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start, pass_chat_data=True))
    dispatcher.add_handler(CallbackQueryHandler(choose_source_language, pattern="^(en|ru)$", pass_chat_data=True))
    dispatcher.add_handler(CallbackQueryHandler(choose_destination_language, pattern="^(en|ru)$", pass_chat_data=True))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_text, pass_chat_data=True))