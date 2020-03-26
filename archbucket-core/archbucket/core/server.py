import threading
import socketserver
import socket
import json
import singleton3
import importlib
import os
from .bot import Bot
from urllib.request import urlopen
from urllib.error import URLError
from requests import get

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
        # path to file with api list
        self.core_path = os.path.dirname(__file__)
        self.init_commands()
        self.init_api_list()
        # default config
        if not os.path.exists(self.core_path + '/server.config'):
            config_dict = {'is_local': True, 'port': 0, 'pipelines_count': 1, 'default_api': 'telegram'}
            with open('server.config', 'w') as file:
                json.dump(config_dict, file)
        # configuring class
        with open(self.core_path + '/server.config') as file:
            config_dict = json.load(file)
        self.server_is_local = config_dict['is_local']
        self.port = int(config_dict['port'])
        self.pipelines_count = int(config_dict['pipelines_count'])
        self.api_name = config_dict['default_api']

    def init_commands(self):
        self.commands = {
            'bot start': self.start_bot,
            'bot stop': self.stop_bot,
            'bot restart': self.restart_bot,
            'bot status': self.get_bot_status,
            'set pipelines': self.set_pipelines,
            'set api': self.set_api,
            'get api': self.get_api,
            'set port': self.set_port,
            'get modules': self.get_modules,
            'import module': self.import_module,
            'remove module': self.remove_module,
            'enable module': self.enable_module,
            'disable module': self.disable_module,
            'import api': 'to implement',
            'remove api': 'to implement',
            'get apis': 'to implement',
            'shutdown': 'to implement',
            'run locally': self.run_locally,
            'run globally': self.run_globally,
            'server status': self.get_server_status,
            'help': self.get_help
        }

    def init_api_list(self):
        with open(self.core_path + '/api/.api', 'r') as file:
            self.api_list = json.load(file)

    def start_server(self):
        if self.server_configured:
            self.server_thread.start()
            ip = get('https://api.ipify.org').text if not self.server_is_local and self.check_connection() else self.server.server_address[0]
            # local case: print internal ip; nonlocal case: print external ip (router)
            print(f'[success]: Server started with address: {ip}:{self.server.server_address[1]}')
            self.server_started = True
        else:
            print('[error]: Server has not been configured yet.')

    def configure_server(self):
        try:
            ip = socket.gethostbyname(socket.gethostname())
            # local case: pick any free port
            port = 0 if self.server_is_local else self.port
            # configuring server
            self.server = ThreadedTCPServer((ip, port), ThreadedTCPRequestHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
        except Exception:
            print('[error]: Cannot initialize server.')
            return
        print('[success]: Server configured.')
        self.server_configured = True

    def check_connection(self):
        try:
            urlopen('http://216.58.192.142', timeout = 1)
            return True
        except URLError: 
            return False

    def stop_server(self):
        if self.server_started:
            self.server.shutdown()
            self.server.server_close()
            print('[success]: Server stopped. Config changes saved.')
        else:
            print('[error]: Cannot stop server. Is it running?')

    def execute_command(self, text):
        if text:
            try:
                command_text = ' '.join(text.split()[:2])
                args_list = text.split(' ')[2:]
                (prefix, message) = self.commands[command_text](*args_list)
                return f'[{prefix}]: {message}'
            except Exception:
                return '[error]: Incorrect command.'

    def start_bot(self):
        try:
            if self.api_name and not self.bot_running:
                # new instance of Bot class
                self.bot = Bot()
                # retrieve class name and token from API list
                (class_name, auth_token, api_type) = self.api_list[self.api_name]
                # importing API class
                api_module = importlib.import_module(f'.{self.api_name}', 'archbucket.core.api')
                # new instance of API with auth token passed
                api_instance = eval(f'api_module.{class_name}("{auth_token}")')
                # setting proccessing pipelines
                for _ in range(self.pipelines_count):
                    self.bot.create_pipeline()
                # pass API instance to start function
                self.bot.start_bot(api_instance)
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
                self.stop_bot()
                self.start_bot()
                return ('success', 'Bot restarted.')
            else:
                return ('error', 'Bot is not running now.')
        except Exception:
            return ('error', 'Cannot restart bot.')

    def set_pipelines(self, number):
        if int(number) > 0:
            self.pipelines_count = int(number)
            self.save_config()
            return ('success', f'Pipelines count set to {number}. Restart to apply changes.') 
        else:
            return ('error', 'Number of pipelines cannot be less then 1')

    def set_api(self, api_name):
        if api_name in self.api_list.keys():
            self.api_name = api_name
            return ('success', f'API set to {api_name}')
        else:
            return ('error', 'Cannot set API. Are you sure its name is correct?')

    def get_api(self):
        return ('info', f'{self.api_name}')

    def set_port(self, port):
        if port > 65535:
            return ('error', 'Invalid port value.')
        else:
            self.port = port
            return ('success', 'Port set successfully. Restart server to apply changes.')

    def get_bot_status(self):
        return ('info', 'Bot is running.') if self.bot_running else ('info', 'Bot is not running.')

    def get_modules(self):
        with open(self.core_path + '/modules/.modules') as file:
            validated_modules = json.load(file)
        return ('info', repr(validated_modules))

    def import_module(self, *args):
        module_name = args[0]
        source_code = ' '.join(args[1:])
        (status, msg) = self.bot.request_router.import_module(module_name, source_code)
        if status == False:
            return ('error', msg)
        else:
            return ('success', msg)

    def remove_module(self, module_name):
        (status, msg) = self.bot.request_router.remove_module(module_name)
        if status == False:
            return ('error', msg)
        else:
            return ('success', msg)

    def enable_module(self, module_name):
        (status, msg) = self.bot.request_router.enable_module(module_name)
        if status == False:
            return ('error', msg)
        else:
            return ('success', msg)

    def disable_module(self, module_name):
        (status, msg) = self.bot.request_router.disable_module(module_name)
        if status == False:
            return ('error', msg)
        else:
            return ('success', msg)

    def run_locally(self):
        if not self.server_is_local:
            self.server_is_local = True
            return ('success', 'Server switched to local running. Restart to apply changes.')
        else:
            return ('error', 'Server is already running locally.')

    def run_globally(self):
        if self.server_is_local:
            self.server_is_local = False
            return ('success', 'Server switched to global running. Restart to apply changes.')
        else:
            return ('error', 'Server is already running globally.')

    def get_server_status(self):
        if self.server_is_local:
            return ('info', 'Server is running locally.')
        else:
            return ('info', 'Server is running globally.')

    def save_config(self):
        with open(self.core_path + '/server.config', 'r') as file:
            config_dict = json.load(file)
        config_dict['is_local'] = self.server_is_local
        config_dict['port'] = self.port
        config_dict['pipelines_count'] = self.pipelines_count
        config_dict['default_api'] = self.api_name
        with open('server.config', 'w') as file:
            json.dump(config_dict, file)
        
    def restore_config(self):
        json_dict = {'is_local': True, 'port': 0, 'pipelines_count': 1, 'default_api': 'telegram_api'}
        with open('server.config', 'w') as file:
            json.dump(json_dict, file)


    def get_help(self):
        pass