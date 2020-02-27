import vk_api
import random

from google.api_core.exceptions import InvalidArgument
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import os

load_dotenv()

project_id = os.getenv('PROJECT_ID')
chat_id = os.getenv('CHAT_ID')


def dialog(event, vk_api):
    # vk_api.messages.send(
    #     user_id=event.user_id,
    #     message=event.text,
    #     random_id=random.randint(1, 1000)
    # )
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, random.randint(1, 1000))
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(
        text=event.text, language_code='ru')

    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Fulfillment text:", response.query_result.fulfillment_text)

    vk_api.messages.send(
        user_id=event.user_id,
        message=response.query_result.fulfillment_text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    vk_token = os.getenv('VK_GROUP_KEY')
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            dialog(event, vk_api)
