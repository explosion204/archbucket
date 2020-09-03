from multiprocessing import Queue, Process

from archbucket.core.request_router import DefaultRequestRouter
from archbucket.core.pipeline import Pipeline

class Bot(object):
    def __init__(self, api_dict, modules_list, pipelines_count, request_queue):
        self.api_dict = api_dict
        self.request_router = DefaultRequestRouter(modules_list)
        self.request_queue = request_queue
        self.output_queue = Queue()
        self.pipelines = list()
        self.busy = False

        for _ in range(pipelines_count):
            input_queue = Queue()
            new_pipeline = Pipeline(input_queue, output_queue)
            self.pipelines.append(new_pipeline)
            # start pipeline proccess
            Process(target=new_pipeline.start).start()

    def start(self):
        while True:
            request = self.request_queue.get()
            
            if request:
                min_pipeline = min(self.pipelines, key=lambda x: x.qsize())
                min_pipeline.input_queue.put(request)

            request = self.output_queue.get()

            if request:
                self.api_dict[request.api_name].send_response(request)
                