import socket
from threading import Thread

class proxyToDNS(Thread):

    def __init__(self, host, port):
        super(proxyToDNS, self).__init__()
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((host, port))

    def run(self):
        while True:
            data = self.server
            if data:
                print("[{}] -> {}").format(self.port, data[:100].encode('hex'))
                self.server.sendall(data)
