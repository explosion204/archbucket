from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters
import api.telegram.telegram_config as config
from api.abstract_api import AbstractAPI
from bot_interface import BotInterface
from core import Request
from time import sleep

class TelegramAPI(AbstractAPI):
    def __init__(self, bot_interface):
        self.bot = Bot(token=config.TOKEN)
        self.bot_interface = bot_interface
        self.updater = Updater(token=config.TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.__listen))
        self.delay = 0.3 # 300 ms
    
    def start(self):
        self.updater.start_polling()

    def __listen(self, update, context):
        if update.effective_message.text:
            text_request = str(update.effective_message.text).split()
            request = Request(id=update.effective_chat.id, request_type='text', command=text_request[0], args=text_request[1:])
            self.bot_interface.push_request(request)
            sleep(self.delay)

    def send_response(self, request: Request):
        self.bot.send_message(chat_id=request.id, text=request.response)