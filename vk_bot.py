import vk_api
import random
import logging
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiError
from dotenv import load_dotenv
import os
import dialogflow_v2 as dialogflow

load_dotenv()

logger = logging.getLogger('dialogflow_bot_logger.vk_bot_mod')


def dialog(event, vk_api):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, random.randint(1, 1000))
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(
        text=event.text, language_code='ru')

    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except Exception:
        logger.debug('error in dialog flow response')

    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )
    else:
        pass


class BotLoggerHandler(logging.Handler):
    """ Handler
    Handler for processing logs and send it to user
    """

    def __init__(self, bot, chat_id, random_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id
        self.random = random_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.messages.send(
            user_id=event.user_id,
            message=log_entry,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    project_id = os.getenv('PROJECT_ID')
    chat_id = os.getenv('CHAT_ID')
    vk_token = os.getenv('VK_GROUP_KEY')

    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    handler = BotLoggerHandler(bot=vk_api, chat_id=chat_id, random_id=random.randint(1, 1000))
    logger.addHandler(handler)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                dialog(event, vk_api)
            except Exception:
                logger.debug('vk api error')
