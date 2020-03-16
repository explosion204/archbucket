import telegram
from telegram.ext import Updater, MessageHandler, Filters
import api.telegram.telegram_config as config
from api.abstract_api import AbstractAPI
from core.bot import Bot
from core.request_router import Request
from time import sleep

class TelegramAPI(AbstractAPI):
    def __init__(self, core_bot):
        self.bot = telegram.Bot(token=config.TOKEN)
        self.core_bot = core_bot
        self.updater = Updater(token=config.TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.listen))
        self.dispatcher.add_handler(MessageHandler(Filters.photo, self.listen))
        self.delay = 0.3 # 300 ms
    
    def start(self):
        self.updater.start_polling()
        
    def stop(self):
        self.updater.stop()

    def listen(self, update, context):
        message = update.effective_message
        if message.text != None:
            text_request = str(message.text).split()
            request = Request(id=update.effective_chat.id, request_type='text', command=text_request[0], args=text_request[1:])
            self.core_bot.push_request(request)
            sleep(self.delay)
        if message.caption and len(message.photo) != 0:
            print('photo with caption')

    def send_response(self, request: Request):
        if request.request_type == 'text' and not request.response == '':
            self.bot.send_message(chat_id=request.id, text=request.response)