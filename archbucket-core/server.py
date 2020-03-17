import threading
import socketserver
import socket
import json
import singleton3
import api.telegram.telegram_api as telegram_api
from core.bot import Bot
from queue import Queue
from importlib import import_module
from os.path import exists

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# request handler
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        recieved_data = str()
        try:
            while True:
                partial_data = self.request.recv(1024).decode()
                if not partial_data:
                    break
                recieved_data += partial_data
        except ConnectionResetError:
            # logging manipulations will be added
            return
        response = Server().execute_command(recieved_data)
        # notify client about request status
        if response:
            self.request.sendall(response.encode())

class Server(metaclass=singleton3.Singleton):
    def __init__(self):
        _instance = self
        self.server_configured = False
        self.server_started = False
        self.bot_running = False
        self.bot = Bot()
        self.init_commands()
        self.init_api_list()
        # configuring class
        with open('server.config') as file:
            config_dict = json.load(file)
        self.server_is_local = config_dict['is_local']
        self.port = int(config_dict['port'])
        self.pipelines_count = int(config_dict['pipelines_count'])
        self.api = self.api_list[config_dict['default_api']]

    def init_commands(self):
        self.commands = {
            'bot start': self.start_bot,
            'bot stop': self.stop_bot,
            'bot restart': self.restart_bot,
            'bot status': self.get_bot_status,
            'set pipelines': self.set_pipelines,
            'set api': self.set_api,
            'get modules': self.get_modules,
            'import module': self.import_module,
            'help': self.get_help
        }

    def init_api_list(self):
        self.api_list = {
            'telegram': telegram_api.TelegramAPI
        }

    def start_server(self):
        if self.server_configured:
            self.server_thread.start()
            print('[success]: Server started.')
            self.server_started = True
        else:
            print('[error]: Server has not been configured yet.')

    def configure_server(self):
        try:
            # getting internal ip of machine
            self.ip = socket.gethostbyname(socket.gethostname()) if not self.server_is_local else '0.0.0.0'
            # configuring server
            self.server = ThreadedTCPServer((self.ip, self.port), ThreadedTCPRequestHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
        except Exception:
            print('[error]: Cannot initialize server.')
            return
        print('[success]: Server configured.')
        self.server_configured = True

    def stop_server(self):
        if self.server_started:
            self.server.shutdown()
            self.server.server_close()
            print('[success]: Server stopped.')
        else:
            print('[error]: Cannot stop server. Is it running?')

    def execute_command(self, text):
        if text:
            # try:
            command_text = ' '.join(text.split()[:2])
            (prefix, message) = self.commands[command_text](text.partition(command_text)[2].lstrip())
            return f'[{prefix}]: {message}'
            # except Exception:
            #    return '[error]: Incorrect command.'

    def start_bot(self):
        try:
            if self.api and not self.bot_running:
                self.bot.set_api(self.api)
                for _ in range(self.pipelines_count):
                    self.bot.create_pipeline()
                self.bot.start_bot()
                self.bot_running = True
                return ('success', 'Bot is running.')
            else:
                return ('error', 'Bot is already running.')
        except Exception:
            return ('error', 'Cannot start bot.')

    def stop_bot(self):
        try:
            if self.bot_running:
                self.bot.stop_bot()
                self.bot_running = False
                return ('success', 'Bot stopped.')
            else:
                return ('error', 'Bot is not running now.')
        except Exception:
            return ('error', 'Cannot stop bot.')

    def restart_bot(self):
        try:
            if self.bot_running:
                self.bot.stop_bot()
                self.bot = Bot()
                self.bot.set_api(self.api)
                for _ in range(self.pipelines_count):
                    self.bot.create_pipeline()
                self.start_bot()
                return ('success', 'Bot restarted.')
            else:
                return ('error', 'Bot is not running now.')
        except Exception:
            return ('error', 'Cannot restart bot.')

    def set_pipelines(self, number):
        self.pipelines_count = int(number)
        return ('success', f'Pipelines count set to {number}. Restart to apply changes.') 

    def set_api(self, api_name):
        try:
            self.api = self.api_list[api_name]
            return ('success', f'API set to {api_name}')
        except KeyError:
            return ('error', 'Cannot set API. Are you sure its name is correct?')

    def get_bot_status(self):
        return ('info', 'Bot is running.') if self.bot_running else ('info', 'Bot is not running.')

    def get_modules(self):
        with open('core/modules/.modules') as file:
            validated_modules = json.load(file)
        repr_str = repr(validated_modules).replace('[', '')
        repr_str = repr_str.replace(']', '')
        repr_str = repr_str.replace(', ', ' ')
        return ('info', repr_str)

    def import_module(self, arg):
        module_name = arg.partition(' ')[0]
        source_code = arg.partition(' ')[2]
        (status, msg) = self.bot.request_router.validate(module_name, source_code)
        if status == False:
            return ('error', msg)
        else:
            return ('success', msg)

    def get_help(self):
        pass