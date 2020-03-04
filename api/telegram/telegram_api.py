import telegram
import telegram.ext as ext
import api.telegram.telegram_config as config
from api.abstract_api import AbstractAPI
from bot_interface import BotInterface
import core

class TelegramAPI(AbstractAPI):
    def __init__(self, bot_interface):
        self.bot = telegram.Bot(token=config.TOKEN)
        self.bot_interface = bot_interface
        self.updater = ext.Updater(token=config.TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(ext.MessageHandler(ext.Filters.text, self.__listen))
    
    def start(self):
        self.updater.start_polling()

    def __listen(self, update, context):
        if update.effective_message.text:
            text_request = str(update.effective_message.text).split()
            request = core.Request(id=update.effective_chat.id, request_type='text', command=text_request[0], args=text_request[1:])
        self.bot_interface.push_request(request)
        # test
        # for _ in range(100):
        #     test_request = core.Request(id = 465986607, request_type='text', command='echo', args=['spam'])
        #     self.bot_interface.push_request(test_request)

    def send_response(self, request: core.Request):
        self.bot.send_message(chat_id=request.id, text=request.response)