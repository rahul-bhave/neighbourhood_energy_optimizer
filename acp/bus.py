import uuid, time
from queue import Queue, Empty
class MessageBus:
    def __init__(self):
        self.queues = {}
    def register(self, name):
        self.queues.setdefault(name, Queue())
    def send(self, envelope):
        dst = envelope.get('to')
        if dst not in self.queues:
            raise KeyError(f'No such agent registered: {dst}')
        self.queues[dst].put(envelope)
    def recv(self, name, timeout=0.1):
        q = self.queues.get(name)
        if q is None:
            raise KeyError(f'Agent not registered: {name}')
        try:
            return q.get(timeout=timeout)
        except Empty:
            return None
