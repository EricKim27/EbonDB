import db
import socket
import pickle
from getpass4 import getpass
import security

class Client:
    def get_selfip(self):
        import requests
        response = requests.get('https://httpbin.org/ip')
        if response.status_code == 200:
            data = response.json()
            return data['origin']
        else:
            return None
    def __init__(self):
        self.ipaddr = self.get_selfip()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def runclient(self, serverip, port, username, password):
        pw_to_send = security.hash_pw(password)
        self.conn.connect((serverip, port))
        self.conn.sendall(f"{username},{pw_to_send}".encode('utf-8'))
        ifauth = self.conn.recv(1024).decode('utf-8')
        if ifauth == "Authenticated":
            flag = ' '
            resnum = 0
            while True:
                request = input("(" + username + ")[" + str(resnum) + "]>")
                req_to_send = pickle.dumps([username, request, flag])
                self.conn.send(req_to_send)
                data = b""
                while True:
                    result = self.conn.recv(1024)
                    if result == "EOR".encode('utf-8'):
                        break
                    data += result
                result_list = pickle.loads(data)
                if len(result_list) == 3:
                    print(result_list[0])
                    flag = result_list[1]
                    resnum = result_list[2]
                elif len(result_list) == 2:
                    if result_list[0] == "exit":
                        print("successfully disconnected from server.")
                        break
                    else:
                        print("Server sent a wrong result. Contact Developer at github.")
                        continue
                else:
                    if not result:
                        print("server disconnected unexpectedly")
                        break
                    else:
                        print("Server sent a wrong request. Contact Developer at github.")
            return 0
        else:
            print("Failed to authenticate")
            return 1

import sys

port = 50075
serverinfo = sys.argv[1].split('@')
password = getpass("Password: ")
clint = Client()
ret = clint.runclient(serverinfo[1], port, serverinfo[0], password)
if ret > 0:
    print("completed with errors")
else:
    print("successfully completed")