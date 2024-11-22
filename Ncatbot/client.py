# client.py
from .message import GroupMessage,PrivateMessage

class BotClient:
    """
    一个客户端类，用于处理不同类型的消息和请求。
    """

    def __init__(self):
        """
        初始化 BotClient 实例。

        创建消息处理器、消息发送处理器、请求处理器和通知处理器的字典。
        """
        self.message_handlers = {
            'group': [],
            'private': []
        }
        self.message_sent_handlers = {
            'group': [],
            'private': []
        }
        self.request_handlers = {
            'friend': [],
            'group': []
        }
        self.notice_handlers = []

    async def message_handle(self, message):
        """
        处理接收到的消息。

        根据消息类型调用相应的处理器。
        """
        message_type = message.get('message_type')
        for handler in self.message_handlers.get(message_type, []):
            # 如果订阅了group，则message=GroupMessage(message)，否则为PrivateMessage(message)
            message = GroupMessage(message) if message_type == 'group' else PrivateMessage(message)
            await handler(message)

    async def message_sent_handle(self, message):
        """
        处理发送的消息。

        根据消息类型调用相应的处理器。
        """
        message_type = message.get('message_type')
        for handler in self.message_sent_handlers.get(message_type, []):
            message = GroupMessage(message) if message_type == 'group' else PrivateMessage(message)
            await handler(message)

    """
    TODO:等待处理，还不能使用
    """
    async def request_handle(self, message):
        """
        处理请求。

        根据请求类型调用相应的处理器。
        """
        request_type = message.get('request_type')
        for handler in self.request_handlers.get(request_type, []):
            await handler(message)

    async def notice_handle(self, message):
        """
        处理通知。

        调用所有的通知处理器。
        """
        for handler in self.notice_handlers:
            await handler(message)

    def register_handler(self, handlers_dict, types, func):
        """
        注册处理器。

        将函数注册到指定类型的处理器列表中。
        """
        if not isinstance(types, list):
            types = [types]
        for t in types:
            handlers_dict[t].append(func)

    def message(self, types):
        """
        装饰器，用于注册消息处理器。

        :param types: 消息类型列表。
        :return: 注册的处理器函数。
        """
        def decorator(func):
            self.register_handler(self.message_handlers, types, func)
            return func
        return decorator

    def message_sent(self, types):
        """
        装饰器，用于注册消息发送处理器。

        :param types: 消息类型列表。
        :return: 注册的处理器函数。
        """
        def decorator(func):
            self.register_handler(self.message_sent_handlers, types, func)
            return func
        return decorator

    def request(self, types):
        """
        装饰器，用于注册请求处理器。

        :param types: 请求类型列表。
        :return: 注册的处理器函数。
        """
        def decorator(func):
            self.register_handler(self.request_handlers, types, func)
            return func
        return decorator

    def notice(self, func):
        """
        装饰器，用于注册通知处理器。

        :param func: 处理器函数。
        :return: 注册的处理器函数。
        """
        self.notice_handlers.append(func)
        return func