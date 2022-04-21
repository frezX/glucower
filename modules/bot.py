import sys
import time
import matplotlib.pyplot as plt

from modules import botFunc


# The main functions of the bot
class Bot(botFunc.BotFunc):
    # Function for processing commands
    async def commands(self, userID, command, msg, lang):
        try:
            user = self.r.get(f"user:{userID}:userID")
            if user:
                if command == "start":
                    text = self.translate('alreadyRegistered', lang)
                elif command == "help":
                    text = await self.help(lang)
                elif command == "login":
                    text = await self.login(userID, msg, lang)
                elif command == "delete":
                    text = await self.delete(userID, lang)
                elif command == "profile":
                    text = await self.profile(userID, lang)
                elif command == "monitoring":
                    text, monit = await self.monitoring(userID, lang)
                    message_id = await self.send_message(userID, text)
                    if monit:
                        login = self.r.get(f"user:{userID}:login")
                        text = await self.mon(login, lang, userID=userID)
                        msg_id = message_id + 1
                        self.r.set(f"user:{userID}:msg_id", msg_id)
                        await self.send_message(userID, text)
                    return ""
                elif command in ["min", "max"]:
                    text = await self.set_glucose_level(userID, command, msg, lang)
                elif command == "graph":
                    await self.graph(userID, msg, lang)
                    return ""
                elif command == "wait":
                    text = await self.wait(userID, msg, lang)
                elif command == "lang":
                    text = await self.setLang(userID, msg, lang)
                else:
                    text = f"{self.translate('dontKnowCommand', lang)}\n/help - {self.translate('commands', lang).lower()}"
            else:
                if command == "start":
                    text = await self.start(userID, lang)
                else:
                    text = f"{self.translate('notRegistered', lang)}\n" \
                           f"/start - {self.translate('startCommand', lang)}"
            return text
        except Exception as e:
            if userID in self.admins:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                return f"{e}\t{exc_tb.tb_lineno}"
            return ""

    # Function for registering users and saving them in the DB
    async def start(self, userID, lang):
        try:
            uid = int(self.r.get(f"list:uid:count"))
        except:
            uid = 1
        self.r.set(f"uids:{uid}:userID", userID)
        self.r.set(f"user:{userID}:uid", uid)
        self.r.set(f"user:{userID}:userID", userID)
        self.r.set(f"user:{userID}:date_reg", time.strftime("%d.%m.%y %X"))
        self.r.set(f"user:{userID}:time_reg", int(time.time()))
        self.r.set(f"user:{userID}:role", "User")
        self.r.set(f"user:{userID}:monitoring", 0)
        self.r.set(f"user:{userID}:min", 4.0)
        self.r.set(f"user:{userID}:max", 9.0)
        self.r.set(f"user:{userID}:color", "2079b6")
        self.r.set(f"user:{userID}:wait", 0)
        self.r.set(f"user:{userID}:lang", "ua")
        self.logging(f"New user: {userID} User count: {uid}")
        uid += 1
        self.r.set(f"list:uid:count", uid)
        text = f"{self.translate('greeting', lang)}\n" \
               f"{self.translate('enterCommand', lang)}  /login [login]"
        return text

    # Function for displaying basic information and all available commands
    async def help(self, lang):
        text = f"{self.translate('help', lang)}\n\n" \
               f"{self.translate('commands', lang)}:\n" \
               f"/login - {self.translate('loginCommand', lang)}\n" \
               f"/delete - {self.translate('deleteCommand', lang)}\n" \
               f"/profile - {self.translate('profileCommand', lang)}\n" \
               f"/monitoring - {self.translate('monitoringCommand', lang)}\n" \
               f"/min - {self.translate('minCommand', lang)}\n" \
               f"/max - {self.translate('maxCommand', lang)}\n" \
               f"/graph - {self.translate('graphCommand', lang)}\n" \
               f"/wait - {self.translate('waitCommand', lang)}\n" \
               f"/lang - {self.translate('langCommand', lang)}\n\n" \
               f"{self.translate('endHelp', lang)}"
        return text

    # Function for obtaining a login to interact with NightScout
    async def login(self, userID, msg, lang):
        try:
            value = msg.split(" ")[1]
            try:
                temp = await self.mon(value, lang, temp=True)
                if temp:
                    self.r.set(f"user:{userID}:login", value)
                    text = f"{self.translate('yourLogin', lang)}: {value}\n" \
                           f"{self.translate('yourUrl', lang)}: {value}.herokuapp.com\n\n" \
                           f"{self.translate('startMonitoring', lang)}:\n/monitoring - {self.translate('monitoringCommand', lang)}"
                else:
                    text = self.translate('loginNotPubliclyAvailable', lang)
            except:
                text = self.translate('loginNotPubliclyAvailable', lang)
        except:
            text = self.translate('enterCorrectlyCommand', lang) + "\n/login [login]"
        return text

    # Login deletion function
    async def delete(self, userID, lang):
        login = self.r.get(f"user:{userID}:login")
        if login:
            self.r.delete(f"user:{userID}:login")
            self.r.set(f"user:{userID}:monitoring", 0)
            text = self.translate('deleteLogin', lang)
        else:
            text = f"{self.translate('dontLogin', lang)}:\n/login [login] - {self.translate('loginCommand', lang)}"
        return text

    # Function for get basic user information
    async def profile(self, userID, lang):
        data = self.r.get(f"user:{userID}:date_reg")
        login = self.r.get(f"user:{userID}:login")
        monitoring = self.r.get(f"user:{userID}:monitoring")
        min_glucose = self.r.get(f"user:{userID}:min")
        max_glucose = self.r.get(f"user:{userID}:max")
        if monitoring == "1":
            monitoring = f"{self.translate('on', lang)} ✅"
        else:
            monitoring = f"{self.translate('off', lang)} ❌"
        if login:
            text = f"Login: {login}\n" \
                   f"URL: {login}.herokuapp.com\n"
        else:
            text = f"Login: {self.translate('none', lang)}\n"
        text += f"{self.translate('monitoringProfile', lang)}: {monitoring}\n" \
                f"{self.translate('minGlucose', lang)}: {min_glucose}\n" \
                f"{self.translate('maxGlucose', lang)}: {max_glucose}\n" \
                f"{self.translate('regProfile', lang)}: {data}"
        return text

    # Function to enable and disable monitoring
    async def monitoring(self, userID, lang):
        monitoring = self.r.get(f"user:{userID}:monitoring")
        text = self.translate('monitoringProfile', lang)
        if monitoring == "1":
            self.r.set(f"user:{userID}:monitoring", 0)
            text += f" {self.translate('off', lang)} ❌"
            monit = False
        else:
            login = self.r.get(f"user:{userID}:login")
            if login:
                self.r.set(f"user:{userID}:monitoring", 1)
                text += f" {self.translate('on', lang)} ✅"
                monit = True
            else:
                return self.translate('enterLogin', lang), False
        return text, monit

    # Function for setting normal limits for glucose
    async def set_glucose_level(self, userID, command, msg, lang):
        try:
            value = float(msg.split(" ")[1])
            self.r.set(f"user:{userID}:{command}", value)
            text = await self.get_glucose_level(userID, lang)
        except:
            text = f"{self.translate('enterCorrectlyCommand', lang)}\n" \
                   f"/{command} [value]"
        return text

    # Function for getting normal limits for glucose
    async def get_glucose_level(self, userID, lang):
        min_glucose = self.r.get(f"user:{userID}:min")
        max_glucose = self.r.get(f"user:{userID}:max")
        text = f"{self.translate('monitoringText', lang)}\n\n" \
               f"{self.translate('minGlucose', lang)}: {min_glucose}\n" \
               f"{self.translate('maxGlucose', lang)}: {max_glucose}"
        return text

    # Function to obtain a graph of changes in blood glucose levels
    async def graph(self, userID, msg, lang):
        login = self.r.get(f"user:{userID}:login")
        try:
            count = int(msg.split(" ")[1])
        except Exception:
            count = 100
        if count > 200:
            count = 200
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for i in range(1, 15):
            color = "gray"
            if i in [4, 9]:
                color = "red"
            elif i == 8:
                color = "orange"
            plt.plot([0, count+1], [i, i], c=color)
        bgs = self.get_graph(login, count)
        y = [float(bg['sgv']) for bg in bgs[::-1]]
        plt.scatter(range(1, len(y)+1), y, c = '#2079b6', marker = '.', zorder=999)
        sgv = bgs[0]['sgv']
        drc = self.replace(bgs[0]["direction"])
        ax.set_xlabel(f"{self.translate('glucoseNow', lang)}: {sgv}{drc}")
        ax.set_title('Glucower Bot')
        ax.set_xticks([])
        ax.set_yticks([i for i in range(1, 15)])
        ax.set_ylabel(self.translate('glucoseLevel', lang))
        ax.set(facecolor='black')
        imgName = f'graph-{userID}.png'
        plt.savefig("img/" + imgName, bbox_inches='tight')
        await self.send_photo(userID, f'img/{imgName}')

    # Alarm delay function
    async def wait(self, userID, msg, lang):
        try:
            minute = int(msg.split(" ")[1])
            if minute < 1:
                minute = 1
        except Exception:
            minute = 10
        self.r.set(f"user:{userID}:wait", int(time.time()) + minute * 60)
        text = f"{self.translate('waitTime', lang)} {minute} {self.format(minute, lang)}"
        return text

    # Function for changing the output language
    async def setLang(self, userID, msg, lang):
        try:
            newLang = msg.split(" ")[1]
            if newLang in ["ru", "ua", "en"]:
                self.r.set(f"user:{userID}:lang", newLang)
                text = f"{self.translate('newLang', newLang)} {self.translate('lang', newLang)} {self.translate('langBot', newLang)}"
            else:
                text = self.translate('notLang', lang)
        except Exception:
            text = f"{self.translate('enterCorrectlyCommand', lang)}\n" \
                   f"/lang [lang] - {self.translate('langCommand', lang)}"
        return text
