import asyncio

from Ncatbot.websockNB import BotWebSocket
from Ncatbot.message import GroupMessage
bot_websocket = BotWebSocket("ws://localhost:3001")
bot_client = bot_websocket.client

@bot_client.message(['group'])
async def reply_group(message: GroupMessage):
    print(message)
    if message.raw_message == "你好":
        await message.reply(markdown = """## 案例\n你是谁？\n\n```python\nprint("hi")\n```""")

asyncio.run(bot_websocket.ws_run())