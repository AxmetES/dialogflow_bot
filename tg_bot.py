import os
from dotenv import load_dotenv
from telegram.ext import CommandHandler
from telegram.ext import Filters, MessageHandler
from telegram.ext import Updater
from google.api_core.exceptions import InvalidArgument
import logging

load_dotenv()

logger = logging.getLogger('dialogflow_bot_logger.tg_bot_mod')

project_id = os.getenv('PROJECT_ID')
chat_id = os.getenv('CHAT_ID')


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Здравствуйте')


def text_message(bot, update):
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, chat_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(
        text=update.message.text, language_code='ru')

    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument as message:
        logger.debug(f'{message}')

    bot.send_message(chat_id=chat_id, text=response.query_result.fulfillment_text)


class BotLoggerHandler(logging.Handler):
    # send message to user
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.chat_id, text=log_entry)


def main():
    updater = Updater(os.getenv('BOT_TOKEN'))
    start_handler = CommandHandler('start', start)
    text_message_handler = MessageHandler(Filters.text, text_message)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    handler = BotLoggerHandler(bot=updater.bot, chat_id=chat_id)
    logger.addHandler(handler)

    dp = updater.dispatcher
    dp.add_handler(start_handler)
    dp.add_handler(text_message_handler)
    updater.start_polling()
    logger.debug('bot is started')

    updater.idle()


if __name__ == '__main__':
    main()
