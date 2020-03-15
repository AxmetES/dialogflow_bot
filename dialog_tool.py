import logging
import dialogflow_v2 as dialogflow

logger = logging.getLogger('dialogflow_bot_logger.dialog_tool_model')


def detect_intent(project_id, chat_id, text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, chat_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code='ru')
    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        intent = session_client.detect_intent(session=session, query_input=query_input)
    except:
        logger.debug('Dialog flow error, check project_id')
    return intent
