import threading
import socketserver
import socket
import json
import singleton3
import api.telegram.telegram_api as telegram_api
from core.bot import Bot
from queue import Queue
from importlib import import_module

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# request handler
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        response = Server().execute_command(data.decode())
        # notify client about request status
        self.request.sendall(response.encode())

class ServerRequestError(Exception):
    pass

class Server(metaclass=singleton3.Singleton):
    def __init__(self):
        _instance = self
        self.server_configured = False
        self.server_started = False
        self.bot_running = False
        self.bot = Bot()
        self.commands = {
            'bot start': self.start_bot,
            'bot stop': self.stop_bot,
            'bot restart': self.restart_bot,
            'pipelines set': self.set_pipelines,
            'api set': self.set_api
        }
        self.api_list = {
            'telegram': telegram_api.TelegramAPI
        }
        # configuring class
        with open('server.config') as file:
            config_dict = json.load(file)
        self.server_is_local = config_dict['is_local']
        self.port = config_dict['port']
        self.pipelines_count = config_dict['pipelines_count']
        self.api = self.api_list[config_dict['default_api']]

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
        command_text = ' '.join(text.split()[:2])
        args_list = text.split()[2:]
        try:
            return self.commands[command_text](*args_list)
        except Exception as ex:
            return f'[error]: {str(ex)}'

    def start_bot(self):
        try:
            if self.api and not self.bot_running:
                self.bot.set_api(self.api)
                for _ in range(self.pipelines_count):
                    self.bot.create_pipeline()
                self.bot.start_bot()
                self.bot_running = True
                return '[success]: Bot is running.'
        except Exception:
            raise ServerRequestError('Cannot start bot.')

    def stop_bot(self):
        try:
            if self.bot_running:
                self.bot.stop_bot()
                self.bot_running = False
                return '[success]: Bot stopped.'
        except Exception:
            raise ServerRequestError('Cannot stop bot.')

    def restart_bot(self):
        try:
            if self.bot_running:
                self.bot.stop_bot()
                self.bot = Bot()
                self.bot.set_api(self.api)
                for _ in range(self.pipelines_count):
                    self.bot.create_pipeline()
                self.start_bot()
                return '[success]: Bot restarted.'
        except Exception:
            raise ServerRequestError('Cannot restart bot.')

    def set_pipelines(self, number):
        self.pipelines_count = number
        return '[success]: Pipelines count set to {number}. Restart to apply changes.'

    def set_api(self, api_name):
        try:
            self.api = self.api_list[api_name]
            return f'[success]: API set to {api_name}'
        except KeyError:
            raise ServerRequestError('Cannot set API. Are you sure its name is correct?')