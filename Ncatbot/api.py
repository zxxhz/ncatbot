
from .http import BotHttp, Route

class BotAPI:
    def __init__(self):
        self._http = BotHttp()

    async def post_group_message(self,
                                 group_id: str,
                                 at: str = None,
                                 text: str = None,
                                 image: str = None,
                                 face: str = None,
                                 jsoner: str = None,
                                 recode: str = None,
                                 video: str = None,
                                 reply: str = None,
                                 music: str = None,
                                 dic: bool = False,
                                 rps: bool = False,
                                 ):
        payload = locals()
        payload.pop("self", None)
        route = Route("/send_group_msg")
        headers = {
           'Content-Type': 'application/json'
        }
        response_text = await self._http.send_group_request(route, payload, headers, "POST")
        return response_text

    async def post_private_message(self,
                                   user_id: str,
                                   text: str = None,
                                   image: str = None,
                                   face: str = None,
                                   jsoner: str = None,
                                   recode: str = None,
                                   video: str = None,
                                   reply: str = None,
                                   music: str = None,
                                   dic: bool = False,
                                   rps: bool = False
                                    ):
        payload = locals()
        payload.pop("self", None)
        route = Route("/send_private_msg")
        headers = {
           'Content-Type': 'application/json'
        }
        response_text = await self._http.send_private_request(route, payload, headers, "POST")
        return response_text




