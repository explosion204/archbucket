from queue import Queue
import core

# import random
# import time

class Pipeline:
    def __init__(self, bot_api):
        self.request_queue = Queue()
        self.count = 0
        self.busy = False
        self.bot_api = bot_api
        # test
        # self.test_id = random.randint(0, 100)

    def start(self):
        while True:
            if not self.request_queue.empty():
                # test
                # print(self.test_id, '\n')
                # time.sleep(2)
                self.count -= 1
                self.busy = True
                request = self.request_queue.get()
                core.call(request)
                self.bot_api.send_response(request)
                self.busy = False

    def push_request(self, request):
        self.request_queue.put(request)
        self.count += 1