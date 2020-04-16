import json
from os.path import exists
import re
import socket
import sys

IP_PATTERN = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
PORT_PATTERN = r"^\d{1,5}$"

print('ArchBucket | Control App.')
print('Specify IP-address of ArchBucket server app or leave it empty if it is running on this machine:')

while True:
    ip = input()
    if not ip:
        ip = socket.gethostbyname(socket.gethostname())
        break
    if not re.match(IP_PATTERN, ip):
        print('[error]: Incorrect IP-address form. Try again: ')
    else:
        break

print('Specify port to connect to ArchBucket server app.')
while True:
    port = input()
    if not re.match(PORT_PATTERN, port):
        print('[error]: Incorrect port form. Try again: ')
    else:
        break

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(port)))
except Exception:
    print('[error]: Connection refused. Check if provided IP-address and port are available.')
    sys.exit(0)
s.close()

print('[success]: Connected to server. Now you can type commands.')
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            connection = sock.connect((ip, int(port)))
        except ConnectionRefusedError:
            print('[error]: Connection closed. Server is not available now.')
            sys.exit(0)
        command = input('>')

        if command:
            if command.startswith('import module'):
                path = command.split()[3]
                if exists(path):
                    command = ' '.join(command.split()[:3])
                    with open(path, 'r') as f:
                        command += ' ' + f.read()

            try:
                sock.send(command.encode())
                sock.shutdown(socket.SHUT_WR)
                response = str()

                while True:
                    data = sock.recv(1024).decode()
                    if not data:
                        break
                    response += data
                    
                response = json.loads(response[:-1])
                if response['status'] == True:
                    print('[success]: ', end='')
                else:
                    print('[error]: ', end='')

                print(response['message'])

            except ConnectionResetError:
                print('[error]: Connection closed. Server is not available now.')
                sys.exit(0)