import json
from os.path import exists
from .server import Server

def main():
    # set up server
    Server().configure_server()
    Server().start_server()

if __name__ == '__main__':
    main()