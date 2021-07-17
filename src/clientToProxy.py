import socket
from threading import Thread

class clientToProxy(Thread):

    def __init__(self, port, host):
        super(clientToProxy, self).__init__()
        self.server = None
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        #waiting for a connection
        self.client, addr = sock.accept()

    def run(self):
        while True:
            data = self.client.recv()
            if data:
                print("[{}] -> {}").format(self.port, data[:100].encode('hex'))
                self.server.sendall(data)