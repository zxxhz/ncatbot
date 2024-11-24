import asyncio
import websockets
import json
import time

from .client import BotClient  # 注意首字母大写
from .utils import get_bot_nickname

class BotWebSocket:
    """
    一个 WebSocket 客户端类，用于与机器人服务器进行通信。
    """

    def __init__(self, url):
        """
        初始化 BotWebSocket 实例。

        :param url: WebSocket 服务器的 URL。
        """
        self.url = url
        self.client = BotClient()

    async def on_message(self, ws, message):
        """
        处理接收到的消息。

        根据消息类型调用相应的处理器。
        """
        message = json.loads(message)

        event = message.get('post_type')
        TIME = message.get('time')
        time_tuple = time.localtime(TIME)
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
        bot_id = message.get('self_id')

        if event == "meta_event":
            print(f"ncatbot({formatted_time})| 机器人 [{get_bot_nickname()}] 成功上线!")

        elif event == "message":
            await self.client.message_handle(message)  # 使用 self.client 调用方法

        elif event == "message_sent":
            await self.client.message_sent_handle(message)  # 使用 self.client 调用方法

        elif event == "request":
            await self.client.request_handle(message)  # 使用 self.client 调用方法

        elif event == "notice":
            await self.client.notice_handle(message)  # 使用 self.client 调用方法

    async def on_error(self, ws, error):
        """
        处理错误。
        """
        print(error)

    async def on_close(self, ws, close_status_code, close_msg):
        """
        处理连接关闭。
        """
        print("### closed ###")

    async def on_open(self, ws):
        """
        处理连接打开。
        """
        print("### connection success ###")

    async def ws_run(self):
        """
        运行 WebSocket 客户端。

        创建并启动 WebSocket 客户端。
        """
        uri = f"{self.url}"
        async with websockets.connect(uri) as websocket:
            await self.on_open(websocket)
            while True:
                try:
                    message = await websocket.recv()
                    await self.on_message(websocket, message)
                except websockets.ConnectionClosed:
                    break



