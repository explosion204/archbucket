import re

print('ArchBucket | Control App.')
print('Specify IP-address of ArchBucket server app or leave it empty if it is running localy:')
ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
while True:
    ip = input()
    if not ip:
        ip = 'localhost'
        port = '8000'
        break
    if not re.match(ip_pattern, ip):
        print('[error] Incorrect IP-address form. Try again: ')
    else:
        break

if ip != 'localhost':
    print('Specify port to connect to ArchBucket server app.')
    port_pattern = r"^/d{5}$"
    while True:
        port = input()
        if not re.match(port_pattern, int(port)):
            print('[error] Incorrect port form. Try again: ')
        else:
            break

import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(port)))
except Exception:
    print('[error] Connection refused. Check if provided IP-address and port are available.')
    import sys
    sys.exit()
s.close()
print('[success] Connected to server. Now you can type commands.')
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        connection = sock.connect((ip, int(port)))
        command = input('>')
        if command:
            sock.send(command.encode())
            print(sock.recv(1024).decode())