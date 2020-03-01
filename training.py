import os
import json
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument, FailedPrecondition
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger('dialogflow_bot_logger')


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)
    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])
    try:
        response = intents_client.create_intent(parent, intent)
    except InvalidArgument as message:
        logger.debug(f'{message}')
    else:
        logger.debug('Intent created: {}'.format(response))


def train_agent(project_id):
    import dialogflow_v2beta1
    client = dialogflow_v2beta1.AgentsClient()
    parent = client.project_path(project_id)
    client.train_agent(parent)


def main():
    project_id = os.getenv('PROJECT_ID')

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)

    with open('questions.json', 'r') as file:
        intents = json.load(file)

    for intent in intents:
        display_name = intent
        intent_body = intents[f'{display_name}']
        training_phrases_parts = intent_body['questions']
        message_texts = {intent_body['answer']}

        create_intent(project_id, display_name, training_phrases_parts,
                      message_texts)

    train_agent(project_id)


if __name__ == '__main__':
    main()
