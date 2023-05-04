import logging, time
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from random import randint

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/dice', '/timer']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

reply_keyboard_dice = [['/hexagon_dice', '/two_hexagon_dices'],
                       ['/hexahedron_dice', '/go_back']]
markup_dice = ReplyKeyboardMarkup(reply_keyboard_dice, one_time_keyboard=False)

reply_keyboard_timer = [['/set_timer_seconds 5', '/set_timer_seconds 60'],
                        ['/set_timer_seconds 300', '/go_back']]
markup_timer = ReplyKeyboardMarkup(reply_keyboard_timer, one_time_keyboard=False)

reply_keyboard_close = [['/close']]
markup_close = ReplyKeyboardMarkup(reply_keyboard_close, one_time_keyboard=True)


async def start(update, context):
    await update.message.reply_text(
        "Я бот-помощник для игр.",
        reply_markup=markup
    )


async def dice(update, context):
    await update.message.reply_text(
        "Бросить кости",
        reply_markup=markup_dice
    )


async def hexagon_dice(update, context):
    await update.message.reply_text(
        f"После броска шестигранного кубика вам выпало - {randint(1, 6)}"
    )


async def two_hexagon_dices(update, context):
    await update.message.reply_text(
        f"После броска двух шестигранных кубиков вам выпало - {randint(1, 6)} и {randint(1, 6)}"
    )


async def hexahedron_dice(update, context):
    await update.message.reply_text(
        f"После броска двадцатигранного кубика вам выпало - {randint(1, 20)}"
    )


async def go_back(update, context):
    await update.message.reply_text(
        "Вы вернулись назад",
        reply_markup=markup
    )


async def timer(update, context):
    await update.message.reply_text(
        "Засечь время",
        reply_markup=markup_timer
    )


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


TIMER = None


async def set_timer_seconds(update, context):
    global TIMER
    chat_id = update.effective_message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    TIMER = int(context.args[0]) if len(context.args) > 0 else 5
    context.job_queue.run_once(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)

    text = f'Засек {TIMER} с' if len(context.args) > 0 and int(context.args[0]) < 60 else f'Засек {TIMER // 60} мин'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text,
                                              reply_markup=markup_close)


async def task(context):
    text = f'{TIMER} c' if int(TIMER) < 60 else f'{TIMER // 60} мин'
    await context.bot.send_message(context.job.chat_id, text=f'{text} истекло',
                                   reply_markup=markup_timer)


async def close(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text,
                                    reply_markup=markup_timer)


def main():
    application = Application.builder().token('6176384593:AAF1akigJOLjs6GHlu7cc65eloinb7gHEGw').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("hexagon_dice", hexagon_dice))
    application.add_handler(CommandHandler("two_hexagon_dices", two_hexagon_dices))
    application.add_handler(CommandHandler("hexahedron_dice", hexahedron_dice))
    application.add_handler(CommandHandler("go_back", go_back))
    application.add_handler(CommandHandler("timer", timer))
    application.add_handler(CommandHandler("set_timer_seconds", set_timer_seconds))
    application.add_handler(CommandHandler("close", close))
    application.run_polling()


if __name__ == '__main__':
    main()
