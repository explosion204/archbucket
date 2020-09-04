class Pipeline(object):
    def __init__(self, input_queue, output_queue, request_router):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.request_router = request_router

    def start(self):
        while True:
            request = self.input_queue.get()
            self.request_router.route(request)
            self.output_queue.put(request)

            