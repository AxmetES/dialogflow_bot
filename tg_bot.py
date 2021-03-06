import os
from dotenv import load_dotenv
from telegram.ext import CommandHandler
from telegram.ext import Filters, MessageHandler
from telegram.ext import Updater
import logging
from dialog_tool import detect_intent

load_dotenv()

logger = logging.getLogger('dialogflow_bot_logger')

updater = Updater(os.getenv('BOT_TOKEN'))
project_id = os.getenv('PROJECT_ID')
log_chat_id = os.getenv('CHAT_ID')


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Здравствуйте')


def send_message(bot, update):
    chat_id = f'tg_{update.message.chat_id}'
    text = update.message.text
    intent = detect_intent(project_id, chat_id, text)
    bot.send_message(chat_id=update.message.chat_id, text=intent.query_result.fulfillment_text)


class BotLoggerHandler(logging.Handler):
    """ Handler
    Handler for processing logs and send it to user
    """

    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.chat_id, text=log_entry)


def main():
    start_handler = CommandHandler('start', start)
    text_message_handler = MessageHandler(Filters.text, send_message)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    handler = BotLoggerHandler(bot=updater.bot, chat_id=log_chat_id)
    logger.addHandler(handler)

    dp = updater.dispatcher
    dp.add_handler(start_handler)
    dp.add_handler(text_message_handler)
    updater.start_polling()
    logger.info('bot started')
    updater.idle()


if __name__ == '__main__':
    main()
