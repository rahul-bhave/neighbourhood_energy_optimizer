import threading, time
class BaseAgent(threading.Thread):
    def __init__(self, name, bus):
        super().__init__(daemon=True)
        self.name = name
        self.bus = bus
        self.bus.register(self.name)
    def send(self, env):
        self.bus.send(env)
    def recv(self, timeout=0.5):
        return self.bus.recv(self.name, timeout)
