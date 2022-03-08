import abc
import socket
import socketserver

class Consumer(abc.ABC):

    def connect(self):
        pass

    def fetch(self):
        pass

class Producer(abc.ABC):

    def connect(self):
        pass

    def push(self):
        pass


class Connection(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._conn = None

    def connect(self):
        pass

    def send(self):
        pass

    def receive(self):
        pass

    def close(self):
        pass


class Broker(abc.ABC):

    def serve_forever(self):
        pass

class Timer(abc.ABC):

    def schedule(self):
        pass