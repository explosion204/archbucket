from queue import Queue

class Pipeline:
    def __init__(self, bot):
        self.request_queue = Queue()
        self.count = 0
        self.busy = False
        self.bot = bot

    def start(self):
        while True:
            if self.request_queue.qsize() != 0:
                self.count -= 1
                self.busy = True
                request = self.request_queue.get()
                self.bot.request_router.route(request)
                self.bot.send_response(request)
                self.busy = False

    def push_request(self, request):
        self.request_queue.put(request)
        self.count += 1