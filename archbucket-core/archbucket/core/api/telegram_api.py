import telegram
from telegram.ext import Updater, MessageHandler, Filters
from archbucket.core.bot import Bot, Request
from time import sleep

class TelegramAPI:
    def __init__(self):
        self.auth_token = '1048894024:AAGJOo6YwcKzQgHBz_JkwHxKbE5EelZtfhI'
        self.bot = telegram.Bot(token=self.auth_token)
        self.updater = Updater(token=self.auth_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.listen))
        self.dispatcher.add_handler(MessageHandler(Filters.photo, self.listen))
        self.delay = 0.3 # 300 ms
    
    def start(self, core_bot):
        self.core_bot = core_bot
        self.updater.start_polling()
        
    def stop(self):
        self.updater.stop()

    def send_response(self, request: Request):
        if request.request_type == 'text' and not request.response == '':
            self.bot.send_message(chat_id=request.id, text=request.response)

    def listen(self, update, context):
        message = update.effective_message
        if message.text != None:
            text_request = str(message.text).split()
            request = Request('telegram_api', id=update.effective_chat.id, request_type='text', command=text_request[0], args=text_request[1:])
            self.core_bot.push_request(request)
            sleep(self.delay)
        if message.caption and len(message.photo) != 0:
            print('photo with caption')