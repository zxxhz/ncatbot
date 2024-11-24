# _*_ coding:utf-8 _*_
import os
import aiohttp

from .utils import markdown_to_image_beautified


class Base:
    def __init__(self, port_or_http: (int, str)):
        self.headers = {'Content-Type': 'application/json'}
        self.url = port_or_http if str(port_or_http).startswith('http') else f'http://localhost:{port_or_http}'

    async def get(self, *args, **kwargs):
        async with aiohttp.ClientSession(self.url, headers=self.headers) as session:
            async with session.get(*args, **kwargs) as response:
                return await response.json()

    async def post(self, *args, **kwargs):
        async with aiohttp.ClientSession(self.url, headers=self.headers) as session:
            async with session.post(*args, **kwargs) as response:
                return await response.json()



class Api(Base):
    def __init__(self, port_or_http: (int, str)):
        super().__init__(port_or_http)

    async def get_login_info(self):
        """
        获取登录信息
        :return: 登录信息
        """
        return await self.post("/get_login_info")

    async def get_group_info(self, group_id: (int, str)):
        """
        获取群信息
        :param group_id: 群号码
        :return: 群信息
        """
        data = {
            "group_id": group_id
        }
        return await self.post("/get_login_info", json=data)

    async def get_group_member_info(self, group_id: (int, str), user_id: (int, str)):
        """
        获取群成员信息
        :param group_id: 群号码
        :param user_id: 群成员QQ号
        :return: 群成员信息
        """
        data = {
            "group_id": group_id,
            "user_id": user_id
        }
        return await self.post("/get_group_member_info", json=data)

    async def set_qq_profile(self, nickname: str = None, personal_note: str = None, sex: str = None):
        """
        设置账号信息
        :param nickname: 昵称
        :param personal_note: 个性签名
        :param sex: 性别
        """
        data = {
            "nickname": nickname,
            "personal_note": personal_note,
            "sex": sex
        }
        return await self.post("/set_qq_profile", json=data)

    async def set_qq_avatar(self, file: str):
        """
        设置头像
        :param file: 路径或链接
        """
        data = {
            "file": file
        }
        return await self.post("/set_qq_avatar", json=data)

    async def set_self_longnick(self, long_nick: str):
        """
        设置个性签名
        :param long_nick: 内容
        """
        data = {
            "longNick": long_nick
        }
        return await self.post("/set_self_longnick", json=data)

    async def send_like(self, user_id: str, times: int):
        """
        设置个性签名
        :param user_id: QQ号
        :param times: 点赞次数
        """
        data = {
            "user_id": user_id,
            "times": times
        }
        return await self.post("/send_like", json=data)


class BotAPI(Api):
    def __init__(self, port_or_http: (int, str), max_ids: int = 100):
        super().__init__(port_or_http=port_or_http)
        self.messages = []  # 存储消息体
        self.message_ids = []  # 存储消息id
        self.max_ids = max_ids  # 最大保留已发送消息的消息id数量

    def add_id(self, mid):
        self.message_ids.append(mid)
        if len(self.message_ids) >= self.max_ids:
            self.message_ids = self.message_ids[-self.max_ids:]

    async def send_group_msg(self, group_id: (int, str), clear_message: bool = True):
        """
        发送群聊消息
        :param group_id: 群号
        :param clear_message: 是否清空消息缓存
        :return: 群聊消息请求类
        """
        message_id = None
        for message in self.messages.copy():
            if message['type'] == 'reply':
                message_id = message['data']['id']
        if self.messages:
            if message_id:
                data = {
                    "group_id": group_id,
                    'message_id': message_id,
                    "message": self.messages.copy()
                }
            else:
                data = {
                    "group_id": group_id,
                    "message": self.messages.copy()
                }
            if clear_message:
                self.clear()
            result = await self.post("/send_group_msg", json=data)
            if result['data']:
                self.add_id(result['data']['message_id'])
            else:
                print(result)
        return self

    async def send_private_msg(self, user_id: (int, str), clear_message: bool = True):
        """
        发送私聊消息（自动去除@信息）
        :param user_id: QQ号
        :param clear_message: 是否清空消息缓存
        :return: 私聊消息请求类
        """
        for message in self.messages.copy():
            if message['type'] == 'at':
                self.messages.remove(message)
        if self.messages:
            data = {
                "user_id": user_id,
                "message": self.messages.copy()
            }
            if clear_message:
                self.clear()
            result = await self.post("/send_private_msg", json=data)
            if result['data']:
                self.add_id(result['data']['message_id'])
            else:
                print(result)
        return self

    def add_text(self, text: str):
        """
        纯文本
        :param text: 文本
        """
        self.messages.append({
            "type": "text",
            "data": {
                "text": text
            }
        })
        return self

    def add_face(self, face_id: (int, str)):
        """
        QQ表情
        :param face_id: QQ表情编号
            表情编号参考（系统表情）：https://bot.q.qq.com/wiki/develop/api-v2/openapi/emoji/model.html#Emoji%20%E5%88%97%E8%A1%A8
        """
        self.messages.append({
            "type": "face",
            "data": {
                "id": str(face_id),
            }
        })
        return self

    def add_media(self, media_type: str, media_path: str):
        """
        添加媒体资源（复用函数）
        :param media_type: 媒体资源类型
        :param media_path: 媒体资源地址（可以是网络地址）
        """
        if media_path.startswith('http'):
            self.messages.append({
                "type": media_type,
                "data": {
                    "file": media_path
                }
            })
        elif os.path.isfile(media_path):
            abspath = os.path.abspath(os.path.join(os.getcwd(), media_path)).replace('\\', '\\\\')
            self.messages.append({
                "type": media_type,
                "data": {
                    "file": f"file:///{abspath}"
                }
            })
        return self

    def add_image(self, image: str):
        """
        图片
        :param image: 图片地址
        """
        self.add_media('image', image)
        return self

    def add_record(self, record: str):
        """
        语音
        :param record: 语音地址
        """
        self.add_media('record', record)
        return self

    def add_video(self, video: str):
        """
        视频
        :param video: 视频地址
        """
        self.add_media('video', video)
        return self

    def add_at(self, target: (int, str) = 'all'):
        """
        @某人
        :param target: QQ表情编号
        """
        self.messages.append({
            "type": "at",
            "data": {
                "qq": str(target),
            }
        })
        self.add_text(' ')  # 自动隔开@信息
        return self

    def rps(self):
        """
        超级表情——猜拳（将清空所有消息列表）
        """
        self.messages = [{
            "type": "rps"
        }]
        return self

    def dice(self):
        """
        超级表情——骰子（将清空所有消息列表）
        """
        self.messages = [{
            "type": "dice"
        }]
        return self

    def music(self, music_type: str = 'custom', **kwargs):
        """
        音乐分享（将清空所有消息列表）
        :param music_type: qq / 163 / kugou / migu / kuwo / custom
        :param kwargs: qq / 163 / kugou / migu / kuwo：{id} | custom：{type, url, audio, title, image(选), singer(选)}
        """
        self.messages = [{
            "type": "music",
            "data": {
                "type": music_type,
                **kwargs
            }
        }]
        return self

    def add_reply(self, message_id: (int, str)):
        """
        回复消息（建议放在第一个消息参数位置）
        :param message_id: 消息id号
        """
        self.messages.append({
            "type": "reply",
            "data": {
                "id": str(message_id),
            }
        })
        return self

    def add_json(self, data: (int, str)):
        """
        回复消息（建议放在第一个消息参数位置）
        :param data: 消息id号
        """
        self.messages.append({
            "type": "json",
            "data": {
                "data": data,
            }
        })
        return self

    def add_file(self, file: str):
        """
        文件
        :param file: 文件地址
        """
        self.add_media('file', file)
        return self

    def add_markdown(self, markdown: str):
        """
        markdown美化图片
        :param markdown: 消息id号
        """
        self.add_media('image', markdown_to_image_beautified(markdown))
        return self

    def get(self):
        return self.messages

    def clear(self):
        self.messages = []
        return self
