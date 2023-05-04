import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
import datetime as dt

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение {update.message.text}')


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def tell_time(update, context):
    await update.message.reply_html(
        rf"Текущее время - {dt.datetime.now().time().strftime('%H:%M:%S')}",
    )


async def tell_date(update, context):
    await update.message.reply_html(
        rf"Сегодняшняя дата - {dt.datetime.now().date().strftime('%d.%m.%y')}",
    )


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update, context):
    chat_id = update.effective_message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    timer = int(context.args[0]) if len(context.args) > 0 else 5
    context.job_queue.run_once(task, timer, chat_id=chat_id, name=str(chat_id), data=timer)

    text = f'Вернусь через {timer} с.!'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text)


async def task(context):
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! Время вышло!')


async def unset(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


def main():
    application = Application.builder().token('6176384593:AAF1akigJOLjs6GHlu7cc65eloinb7gHEGw').build()

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time", tell_time))
    application.add_handler(CommandHandler("date", tell_date))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))

    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()