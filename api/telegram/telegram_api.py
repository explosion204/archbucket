import telegram
import telegram.ext as ext
import api.telegram.telegram_config as config
import controlunit
import core

class TelegramAPI:
    def __init__(self, control_unit):
        self.bot = telegram.Bot(token=config.TOKEN)
        self.control_unit = control_unit
        self.updater = ext.Updater(token=config.TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(ext.MessageHandler(ext.Filters.text, self.__listen))
    
    def start(self):
        self.updater.start_polling()

    def __listen(self, update, context):
        if update.effective_message.text:
            text_request = str(update.effective_message.text).split()
            request = core.Request(id=update.effective_chat.id, request_type='text', command=text_request[0], args=text_request[1:])
        self.control_unit.push_request(request)

    def send_response(self, request: core.Request):
        self.bot.send_message(chat_id=request.id, text=request.response)