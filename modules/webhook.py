from aiohttp import web
from modules import api

# Webhook
class Webhook(api.Api):
    # Function for receiving updates in the bot
    async def webhook(self, request):
        updates = await request.json()
        try:
            await self.message_handler(updates)
        except:
            pass
        return web.Response(text="Glucower Bot by frezX")

    # Web server deployment feature
    async def web(self):
        app = web.Application()
        app.add_routes([web.post(f"/webhook{self.token}", Webhook().webhook)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 80)
        await site.start()