import requests
import json

def get_bot_nickname(uin):
    """
    获取机器人的昵称。

    通过请求 QQ 空间的 API 获取机器人的昵称。

    :param uin: 用户 ID。
    :return: 机器人的昵称。
    """
    url = f"http://users.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins={uin}"
    response = requests.get(url).text[len('portraitCallBack('):-1]
    response = json.loads(response)
    nickname = response[str(uin)][6]
    return nickname