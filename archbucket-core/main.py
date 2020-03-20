import json
import atexit
from os.path import exists
from server import Server

def exit_handler():
    Server().stop_server()

def main():
    # config set up
    if not exists('server.config'):
        json_dict = {'is_local': True, 'port': 0, 'pipelines_count': 1, 'default_api': 'telegram'}
        with open('server.config', 'w') as file:
            json.dump(json_dict, file)
    # set up server
    atexit.register(exit_handler)
    Server().configure_server()
    Server().start_server()

if __name__ == '__main__':
    main()