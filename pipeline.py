from queue import Queue
import core

class Pipeline:
    def __init__(self, bot_api):
        self.request_queue = Queue()
        self.count = 0
        self.busy = False
        self.bot_api = bot_api

    def start(self):
        while True:
            if not self.request_queue.empty():
                self.count -= 1
                self.busy = True
                request = self.request_queue.get()
                core.call(request)
                self.bot_api.send_response(request)
                self.busy = False

    def push_request(self, request):
        self.request_queue.put(request)
        self.count += 1