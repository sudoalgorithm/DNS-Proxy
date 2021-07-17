from threading import Thread
from clientToProxy import clientToProxy
from proxyToDNS import proxyToDNS

class Proxy(Thread):
    def __init__(self, from_host, to_host, port):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port

    def run(self):
        while True:
            self.c2p = clientToProxy(self.from_host, self.port)
            self.p2DNS = proxyToDNS(self.to_host, self.port)
            self.c2p.server = self.p2DNS.server
            self.p2DNS.server = self.c2p.servers
            self.c2p.start()
            self.p2DNS.start()

proxy = Proxy('0.0.0.0','8.8.8.8',53)
proxy.start()
