import json
import redis
from time import strftime


# Consts
class Const:
    def __init__(self):
        super().__init__()
        # Bot token to interact with the Telegram API
        self.token = '' 
        # URL API Telegram
        self.api = f"https://api.telegram.org/bot{self.token}/"
        # WebHook to get updates in the bot
        self.webhook_url = f"local-net.ml/webhook{self.token}"
        # Database Redis
        self.r = redis.Redis(decode_responses=True)
        # Uids on bot administrators
        self.admins = ()
        # Colors for outputting data to the console
        self.red = '\033[31m'
        self.blue = '\033[36m'
        self.clear = '\033[0m'
        self.green = '\033[32m'
        self.line = '\033[42m'
        self.darkblue = '\033[34m'
        # Outputs to the console of the main inscriptions
        self.text = f'{self.line}                             Glucower Bot by frezX                             {self.clear}'
        self.start_text = f'Bot {self.green}STARTED{self.clear}'
        self.stop_text = f'Bot {self.red}STOPED{self.clear}'

    # Translation function
    def translate(self, key, lang="ua"):
        with open('translate/translate.json', 'r') as f:
            data = json.load(f)
        return data[lang][key]

    # Logging of main events and errors in the bot
    def logging(self, message, color=False):
        if not color:
            with open("log/log.txt", "a", encoding="utf-8") as file:
                file.write(f"[{strftime('%d.%m.%y|%X')}] {message}\n")
        print(f"{self.blue}INFO {self.darkblue}[{strftime('%X')}]:{self.clear} {message}")
