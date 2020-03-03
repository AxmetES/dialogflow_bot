## Google "Dialogflow" and telegram bot and vk bot

Project to integration google api dialogflow in telegram bot and vk bot
via `python-telegram-bot` and `vk-api` modules.

## Getting Started

- Via `python-telegram-bot` and `vk-api` modules created simple echo bot on [telegram](https://web.telegram.org/#/login) messenger, and [vkontakte](https://vk.com/)
social network.
- Create Group in VK and use vk api to get secret key [vk API](https://vk.com/dev/bots_docs).
- Fulfill all necessary conditions on [google cloud](https://cloud.google.com/dialogflow/docs/quick/api) and create [dialogflow agent](https://cloud.google.com/dialogflow/docs/quick/api).
- Get all necessary api key and fill `.env` file.
```python
BOT_TOKEN="your telegram bot token"
PROJECT_ID="your google cloud project identification"
CHAT_ID="your chat ID"
DIALOG_TOKEN="dialog flow agent token"
export GOOGLE_APPLICATION_CREDENTIALS ="your credentials JSON file"
VK_GROUP_KEY="vk api secret key"
```

## Running

Running from command line:
```shell script
python tg_bot.py 
```
to start telegram bot.

```shell script
python vk_bot.py 
```
to start vkontakte bot.

#### Training dialog flow agent to new phrases in code

Dialog flow agent training by json file. Script load training phrases from jason file and create new intents, 
also intents can be created in [dialog flow side](https://dialogflow.com/).
```python
     with open('questions.json', 'r') as file:
        intents = json.load(file)
```
to start:
```shell script
python training.py
```
## License

You may copy, distribute and modify the software.