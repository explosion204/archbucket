from archbucket.core.server import Server
import argparse
import json
import os
import socket
import sys
import threading

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', choices=['cmd', 'no-cmd'], default='no-cmd')
    
    return parser

def run_cmd(ip, port):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, int(port)))
            command = input('>')

            if command:
                if command.startswith('import module'):
                    path = command.split()[3]
                    if os.path.exists(path):
                        command = ' '.join(command.split()[:3])
                        with open(path, 'r') as f:
                            command += ' ' + f.read()

                if command.startswith('import api'):
                    path = command.split()[4]
                    if os.path.exists(path):
                        command = ' '.join(command.split()[:4])
                        with open(path, 'r') as f:
                            command += ' ' + f.read()

                sock.send(command.encode())
                sock.shutdown(socket.SHUT_WR)
                response = str()

                while True:
                    data = sock.recv(1024).decode()
                    if not data:
                        break
                    response += data

                response = json.loads(response[:-1])
                print(response['message'])

def main():
    args = init_parser().parse_args()
    (ip, port) = Server().configure_server()

    if args.mode == 'cmd':
        threading.Thread(target=Server().start_server()).start()
        run_cmd(ip, port)
    else:
        threading.Thread(target=Server().start_server()).start()
        while True:
            # waiting for KeyboardInterrupt
            pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        Server().stop_server()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)