import vk_api
import random
import logging
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from dotenv import load_dotenv
import os
from tg_bot import BotLoggerHandler
from tg_bot import updater
from tg_bot import log_chat_id
from dialog_tool import detect_intent

load_dotenv()

logger = logging.getLogger('dialogflow_bot_logger')


def send_message(vk_api, project_id, text, user_id):
    chat_id = f'vk_{user_id}'
    intent = detect_intent(project_id, chat_id, text)
    if not intent.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=user_id,
            message=intent.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    project_id = os.getenv('PROJECT_ID')
    vk_token = os.getenv('VK_GROUP_KEY')

    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    handler = BotLoggerHandler(bot=updater.bot, chat_id=log_chat_id)
    logger.addHandler(handler)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text
            user_id = event.user_id
            try:
                send_message(vk_api, project_id, text, user_id)
            except Exception as message:
                logger.debug(message)
