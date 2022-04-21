import sys
import time
import json
import requests


# Functions for bot operation
class BotFunc:
    # Function for obtaining data from sensors using NightScout
    async def mon(self, login, lang, date=False, sgvs=False, userID=None, temp=False):
        try:
            try:
                response = json.loads(requests.get(f"https://{login}.herokuapp.com/pebble").text)
                data = response["bgs"][0]
            except:
                if temp:
                    return False
                return 
            sgv = data["sgv"]
            delta = data["bgdelta"]
            drc = self.replace(data["direction"])
            times = data["datetime"]
            minute = int((time.time() - (times / 1000))/60)
            text = f"{sgv} {drc}\n"
            if float(delta) > 0:
               text += f"+{delta} mmol/L\n"
            else:
               text += f"{delta} mmol/L\n"
            if minute == 0:
                text += self.translate('now', lang)
            else:
                text += f"{minute} {self.format(minute, lang)} {self.translate('ago', lang)}"
            if sgvs:
                return text, sgv
            elif date:
                return text, minute
            else:
                if userID != None:
                    self.r.set(f"user:{userID}:date", minute)
                return text
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"Mon: {e}\t{exc_tb.tb_lineno}")
    
    # Function to obtain data for glucose graphs
    def get_graph(self, login, count):
        bgs =  json.loads(requests.get(f"https://{login}.herokuapp.com/pebble?count={count}").text)["bgs"]
        return bgs

    # Arrow tilt change function
    def replace(self, drc):
        drc = drc.replace('None', '⇼')
        drc = drc.replace('DoubleUp', '⇈︎')
        drc = drc.replace('TripleUp', '⤊')
        drc = drc.replace('SingleUp', '↑')
        drc = drc.replace('FortyFiveUp', '↗️')
        drc = drc.replace('Flat', '→')
        drc = drc.replace('FortyFiveDown', '↘️')
        drc = drc.replace('SingleDown', '↓')
        drc = drc.replace('DoubleDown', '⇊')
        drc = drc.replace('TripleDown', '⤋')
        drc = drc.replace('NOT COMPUTABLE', '-')
        drc = drc.replace('RATE OUT OF RANGE', '⇕')
        return drc

    # Time formatting function
    def format(self, minute, lang):
        if minute % 10 == 1 and minute != 11:
            text = self.translate('minute1', lang)
        elif minute % 10 in [2,3,4] and minute not in [12,13,14]:
            text = self.translate('minute2', lang)
        else:
            text = self.translate('minute3', lang)
        return text