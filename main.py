import os
import asyncio

from modules import webhook
from modules.botLoop import BotLoop

class Main(webhook.Webhook):
    async def start(self):
        print(self.text)
        await self.set_webhook()
        await self.web()
        self.logging(self.start_text, True)

    async def stop(self):
        self.logging(self.stop_text, True)


if __name__ == "__main__":
    os.system("clear")
    os.system("stty -echo")
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(Main().start())
        monitoring_loop = loop.create_task(BotLoop().monitoring_loop())
        valid_loop = loop.create_task(BotLoop().valid_loop())
        loop.run_until_complete(monitoring_loop)
        loop.run_until_complete(valid_loop)
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(Main().stop())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        os.system("stty echo")
