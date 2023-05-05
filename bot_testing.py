import json
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

with open('questions.json') as f:
    questions = json.load(f)['test']

random.shuffle(questions)

score = 0

in_progress = False


def start(update, context):
    global in_progress, score
    if in_progress:
        update.message.reply_text('Тест уже начат. Введите ответ на предыдущий вопрос.')
    else:
        in_progress = True
        score = 0
        context.user_data['question_idx'] = 0
        update.message.reply_text(questions[0]['question'])


def stop(update, context):
    global in_progress
    if in_progress:
        in_progress = False
        update.message.reply_text('Тест прерван.')
    else:
        update.message.reply_text('Тест не был начат.')


def answer(update, context):
    global in_progress, score
    if not in_progress:
        update.message.reply_text('Тест не начат. Наберите /start, чтобы начать тест.')
        return

    user_answer = update.message.text.strip()

    correct_answer = questions[context.user_data['question_idx']]['response']
    if user_answer == correct_answer:
        score += 1
    else:
        update.message.reply_text(f'Неправильно. Правильный ответ: {correct_answer}')

    if context.user_data['question_idx'] < len(questions) - 1:
        context.user_data['question_idx'] += 1
        update.message.reply_text(questions[context.user_data['question_idx']]['question'])
    else:
        in_progress = False
        update.message.reply_text(f'Тест окончен. Правильных ответов: {score}.')
        update.message.reply_text('Введите /start, чтобы начать тест заново.')


def main():
    updater = Updater('6176384593:AAF1akigJOLjs6GHlu7cc65eloinb7gHEGw', use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('stop', stop))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, answer, run_async=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()