import sys
import time
import asyncio
import threading

from modules import api
from modules import const

# Basic loops in the bot
class BotLoop(api.Api, const.Const):
    # Function for constant monitoring of data changes and their updating in the message (Works every 5 seconds)
    async def monitoring_loop(self):
        while True:
            try:
                uid = 1
                try:
                    count = int(self.r.get(f"list:uid:count"))
                except:
                    count = 0
                while uid <= count:
                    userID = self.r.get(f"uids:{uid}:userID")
                    monitoring = self.r.get(f"user:{userID}:monitoring")
                    if monitoring == "1":
                        msg_id = self.r.get(f"user:{userID}:msg_id")
                        login = self.r.get(f"user:{userID}:login")
                        if login != None:
                            date = self.r.get(f"user:{userID}:date")
                            if date == None:
                                date = 0
                            try:
                                lang = self.r.get(f"user:{userID}:lang")
                                text, minute = await self.mon(login, lang, True)
                                if int(minute) != int(date):
                                    self.r.set(f"user:{userID}:date", minute)
                                    await self.edit_message(userID, msg_id, text)
                            except:
                                continue
                    uid += 1
                await asyncio.sleep(7)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                self.logging(f"{e}\t{exc_type} {exc_obj} {exc_tb.tb_lineno}" )

    # Function for monitoring the level of glucose according to the norms set by the user (Works every 3 minutes)
    async def valid_loop(self):
        while True:
            try:
                uid = 1
                try:
                    count = int(self.r.get(f"list:uid:count"))
                except:
                    count = 0
                while uid <= count:
                    userID = self.r.get(f"uids:{uid}:userID")
                    monitoring = self.r.get(f"user:{userID}:monitoring")
                    min_glucose = self.r.get(f"user:{userID}:min")
                    max_glucose = self.r.get(f"user:{userID}:max")
                    if monitoring == "1":
                        login = self.r.get(f"user:{userID}:login")
                        if login != None:
                            wait = int(self.r.get(f"user:{userID}:wait"))
                            if int(time.time()) > wait:
                                lang = self.r.get(f"user:{userID}:lang")
                                try:
                                    text, sgv = await self.mon(login, lang, False, True)
                                    if float(min_glucose) > float(sgv) or float(sgv) > float(max_glucose):
                                        text = f"🆘{self.translate('glucoseNotNormal', lang)}🆘\n{text}\n\n" \
                                               f"/wait - {self.translate('waitCommand', lang)}"
                                        await self.send_message(userID, text)
                                except:
                                    continue
                    uid += 1
                await asyncio.sleep(3*60)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                self.logging(f"{e}\t{exc_type} {exc_obj} {exc_tb.tb_lineno}" )
