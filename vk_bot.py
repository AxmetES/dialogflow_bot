import vk_api
import random
import logging
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from dotenv import load_dotenv
import os
import dialogflow_v2 as dialogflow
from tg_bot import BotLoggerHandler
from tg_bot import updater

load_dotenv()

logger = logging.getLogger(__name__)


def get_response(project_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, get_random_id())

    text_input = dialogflow.types.TextInput(
        text=event.text, language_code='ru')
    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except Exception as message:
        logger.debug(message)
    return response


def get_dialog(event, vk_api):
    response = get_response(project_id)
    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
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
    handler = BotLoggerHandler(bot=updater.bot, chat_id=chat_id)
    logger.addHandler(handler)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                get_dialog(event, vk_api)
            except Exception as message:
                logger.debug(message)
