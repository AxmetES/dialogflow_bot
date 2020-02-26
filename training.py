import os

from google.api_core.exceptions import InvalidArgument
from dotenv import load_dotenv

load_dotenv()


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""
    import dialogflow_v2 as dialogflow
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
        print(f'{message}')
    else:
        print('Intent created: {}'.format(response))
        # TODO: Initialize `intent`:


def train_agent(project_id):
    # , retry = google.api_core.gapic_v1.method.DEFAULT, timeout = google.api_core.gapic_v1.method.DEFAULT,
    # metadata = None
    import dialogflow_v2beta1
    client = dialogflow_v2beta1.AgentsClient()
    parent = client.project_path(project_id)
    response = client.train_agent(parent)
    print(response)


def main():
    project_id = os.getenv('PROJECT_ID')
    display_name = "Устройство на работу"
    training_phrases_parts = [
        "Как устроиться к вам на работу?",
        "Как устроиться к вам?",
        "Как работать у вас?",
        "Хочу работать у вас",
        "Возможно-ли устроиться к вам?",
        "Можно-ли мне поработать у вас?",
        "Хочу работать редактором у вас"
    ]
    message_texts = {'''Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com 
    мини-эссе о себе и прикрепите ваше портфолио.'''}

    create_intent(project_id, display_name, training_phrases_parts,
                  message_texts)
    train_agent(project_id)


if __name__ == '__main__':
    main()
