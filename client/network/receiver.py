import threading

class Receiver(threading.Thread):
    def __init__(self, app):
        super().__init__(daemon=True)
        self.app = app
        self.running = True

    def run(self):
        while self.running:
            pass

    def stop(self):
        self.running = False