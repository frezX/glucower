import requests

from modules import bot
from modules import const

# API with Telegram
class Api(bot.Bot, const.Const):
    # Function for processing messages from users
    async def message_handler(self, updates):
        data = await self.get_data(updates)
        user_id = data["user_id"]
        try:
            lang = self.r.get(f"user:{user_id}:lang")
            if lang == None:
                lang = "ru"
        except:
            lang = "ru"
        try:
            text = data["text"]
            await self.new_msg(user_id, text)
            if text.startswith("/"):
                command = text.split(" ")[0][1:]
                text = await self.commands(user_id, command, text, lang)
            else:
                text = self.translate('onlyCommand', lang)
        except:
            return
        await self.send_message(user_id, text)

    # Function for obtaining structured data
    async def get_data(self, updates):
        message = updates["message"]
        messageFrom = message["from"]
        messageChat = message["chat"]
        data = {"user_id": messageFrom["id"], "is_bot": messageFrom["is_bot"], 
                "first_name": messageFrom["first_name"], "username": messageFrom["username"], 
                "language_code": messageFrom["language_code"], "chat_id": messageChat["id"],
                "type": messageChat["type"]
        }
        types = ["from", "chat"]
        for type in message:
            if type not in types:
                if type != "caption":
                    data[type] = message[type]
                else:
                    data["text"] = message[type]
        return data

    # Function for sending messages to the user
    async def send_message(self, chat_id, text):
        data = requests.post(self.api + "sendMessage", {'chat_id': chat_id ,'text': text}).json()
        message_id = data["result"]["message_id"]
        return message_id

    # Function for changing messages
    async def edit_message(self, chat_id, message_id, text):
        data = requests.post(self.api + "editMessageText", {'chat_id': chat_id ,'text': text, "message_id": message_id}).json()
        message_id = data["result"]["message_id"]
        return message_id

    # Function for sending photos to the user
    async def send_photo(self, chat_id, name):
        photo = {'photo': open(name, 'rb')}
        requests.post(self.api + "sendPhoto", {"chat_id": chat_id}, files=photo)

    # Function for set Webhook
    async def set_webhook(self):
        url = f'{self.api}setWebhook?url={self.webhook_url}'
        data = requests.post(url).json()
        if data["ok"]:
            color = self.green
        else:
            color = self.red
        text = f'Webhook: {color}{data["description"]}{self.clear}'
        self.logging(text, True)

    # Function for logging new messages in the bot
    async def new_msg(self, user_id, text):
        self.logging(f"New message from user: {user_id}: {text}")


