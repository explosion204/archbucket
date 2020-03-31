import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from archbucket.core.bot import Bot, Request

class VkAPI:
    def __init__(self):
        TOKEN = 'c7a2fef41a79db46cfe2178e0d9d0de37b93b300c10bd2337cf7c4ecb2a0b1851fed333c58023713e6f77'
        self.vk = vk_api.VkApi(token=TOKEN)
        self.longpoll = VkLongPoll(self.vk)
        self.is_running = False
    
    def start(self, core_bot):
        self.core_bot = core_bot
        self.is_running = True
        while self.is_running:
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        text_request = event.text.split()
                        request = Request('vk_api', id=event.user_id, request_type='text', command=text_request[0], args=text_request[1:])
                        self.core_bot.push_request(request)

    def stop(self):
        self.is_running = False

    def send_response(self, request: Request):
        if request.request_type == 'text' and request.response:
            self.vk.method('messages.send', {'user_id': request.id, 'random_id': random.randint(0, 10000), 'message': request.response})