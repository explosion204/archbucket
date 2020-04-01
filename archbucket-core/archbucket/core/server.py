import threading
import socketserver
import socket
import json
import singleton3
import importlib
import os
from .bot import Bot
from . import manipulator
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
        self.api_dict = dict()
        self.load_api_instances()
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

    def init_commands(self):
        self.commands = {
            'bot start': self.start_bot,
            'bot stop': self.stop_bot,
            'bot restart': self.restart_bot,
            'bot status': self.get_bot_status,
            'set pipelines': self.set_pipelines,
            'get api_list': self.get_api_list,
            'set port': self.set_port,
            'get modules': self.get_modules,
            'import module': self.import_module,
            'remove module': self.remove_module,
            'enable module': self.enable_module,
            'disable module': self.disable_module,
            'import api': self.import_api,
            'remove api': self.remove_api,
            'enable api': self.enable_api,
            'disable api': self.disable_api,
            'shutdown': 'to implement',
            'run locally': self.run_locally,
            'run globally': self.run_globally,
            'server status': self.get_server_status,
            'help': self.get_help
        }

    def load_api_instances(self):
        with open(self.core_path + '/api/.api', 'r') as file:
            names = json.load(file)
        for (api_name, [class_name, enabled]) in names.items():
            if api_name not in self.api_dict.keys() and enabled:
                api_module = importlib.import_module(f'.{api_name}', 'archbucket.core.api')
                api_instance = eval(f'api_module.{class_name}()')
                self.api_dict[api_name] = api_instance

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
            if self.api_dict and not self.bot_running:
                # new instance of Bot class
                self.bot = Bot(self.pipelines_count, self.api_dict)
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

    def get_api_list(self):
        return ('info', f'{self.api_dict}')

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
        (status, msg) = manipulator.import_module(module_name, source_code)
        if status == False:
            return ('error', msg)
        else:
            return ('success', msg)

    def remove_module(self, module_name):
        (status, msg) = manipulator.remove_module(module_name)
        if status == False:
            return ('error', msg)
        else:
            return ('success', msg)

    def enable_module(self, module_name):
        (status, msg) = manipulator.enable_module(module_name)
        if status == False:
            return ('error', msg)
        else:
            return ('success', msg)

    def disable_module(self, module_name):
        (status, msg) = manipulator.disable_module(module_name)
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
        with open('server.config', 'w') as file:
            json.dump(config_dict, file)
        
    def restore_config(self):
        json_dict = {'is_local': True, 'port': 0, 'pipelines_count': 1, 'default_api': 'telegram_api'}
        with open('server.config', 'w') as file:
            json.dump(json_dict, file)

    def import_api(self, *args):
        api_name = args[0]
        class_name = args[1]
        source_code = ' '.join(args[2:])
        (status, msg) = manipulator.import_api(api_name, class_name, source_code)
        if status == False:
            return ('error', msg)
        else:
            return ('success', msg)
        pass

    def remove_api(self, api_name):
        (status, msg) = manipulator.remove_api(api_name)
        if status == False:
            return ('error', msg)
        else:
            return ('success', msg)

    def enable_api(self, api_name):
        (status, msg) = manipulator.enable_api(api_name)
        if status == False:
            return ('error', msg)
        else:
            return ('success', msg)

    def disable_api(self, api_name):
        (status, msg) = manipulator.disable_api(api_name)
        if status == False:
            return ('error', msg)
        else:
            return ('success', msg)

    def get_help(self):
        pass