import os

import apiai
import json
from dotenv import load_dotenv
from telegram.ext import CommandHandler
from telegram.ext import Filters, MessageHandler
from telegram.ext import Updater
from google.api_core.exceptions import InvalidArgument

load_dotenv(verbose=True)

project_id = os.getenv('PROJECT_ID')
chat_id = os.getenv('CHAT_ID')


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Здравствуйте')


def echo(bot, update):
    update.message.reply_text(update.message.text)


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
    except InvalidArgument:
        raise
    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Fulfillment text:", response.query_result.fulfillment_text)

    bot.send_message(chat_id=chat_id, text=response.query_result.fulfillment_text)


def main():
    updater = Updater(os.getenv('BOT_TOKEN'))
    start_handler = CommandHandler('start', start)
    text_message_handler = MessageHandler(Filters.text, text_message)

    dp = updater.dispatcher
    dp.add_handler(start_handler)
    dp.add_handler(text_message_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
