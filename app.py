import logging
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters

TOKEN = '372828093:AAFIgqIHvneYjO-4PIrN8RF3mP9fzkB88-Q'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def newevent_handler(bot, update):
    update.message.reply_text('welcome MESSAGE')

def timetable_handler(bot, update):
    update.message.reply_text('Your time table:\n 10:00-11:20 - Уроки')

def help_handler(bot, update):
    update.message.reply_text('Help message should me here :(')


def textmessage_handler(bot, update):
    update.message.reply_text("Sorry, I'm just a reminder bot")


def error_handler(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("newevent", newevent_handler))
        dp.add_handler(CommandHandler("timetable", timetable_handler))
        
        # dp.add_handler(CommandHandler("start", start))
        # dp.add_handler(CommandHandler("help", help))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, textmessage_handler))

        # log all errors
        dp.add_error_handler(error_handler)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()