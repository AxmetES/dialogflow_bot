from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters, MessageHandler
from dotenv import load_dotenv
import os
import apiai, json


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Здравствуйте')


def echo(bot, update):
    update.message.reply_text(update.message.text)


# def detect_intent_texts(project_id, session_id, texts, language_code):
#     """Returns the result of detect intent with texts as inputs.
#
#     Using the same `session_id` between requests allows continuation
#     of the conversation."""
#     import dialogflow_v2 as dialogflow
#     session_client = dialogflow.SessionsClient()
#
#     session = session_client.session_path(project_id, session_id)
#     print('Session path: {}\n'.format(session))
#
#     for text in texts:
#         text_input = dialogflow.types.TextInput(
#             text=text, language_code=language_code)
#
#         query_input = dialogflow.types.QueryInput(text=text_input)
#
#         response = session_client.detect_intent(
#             session=session, query_input=query_input)
#
#         print('=' * 20)
#         print('Query text: {}'.format(response.query_result.query_text))
#         print('Detected intent: {} (confidence: {})\n'.format(
#             response.query_result.intent.display_name,
#             response.query_result.intent_detection_confidence))
#         print('Fulfillment text: {}\n'.format(
#             response.query_result.fulfillment_text))


def text_message(bot, update):
    response = 'Got youre message: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)

    # request = apiai.ApiAI(os.getenv('DIALOG_TOKEN')).text_request()
    # request.lang = 'ru'
    # request.session_id = update.message.chat_id
    # request.query = update.message.text
    # response_json = json.load(request.getresponse().read().decode('utf-8'))
    # response = response_json['result']['fulfillment']['speech']
    # if response:
    #     bot.send_message(chat_id=update.message.chat_id, text=response)
    # else:
    #     bot.send_message(chat_id=update.message.chat_id, text="I don't understand")


def main():
    load_dotenv(verbose=True)
    project_id = os.getenv('PROJECT_ID')
    chat_id = os.getenv('CHAT_ID')

    updater = Updater(os.getenv('BOT_TOKEN'))

    start_handler = CommandHandler('start', start)
    text_message_handler = MessageHandler(Filters.text, text_message)

    dp = updater.dispatcher
    dp.add_handler(start_handler)
    dp.add_handler(text_message_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
