from multiprocessing import Queue, Process

from archbucket.components import DefaultRequestRouter
from .pipeline import Pipeline

class Bot(object):
    def __init__(self, api_dict, scripts_dict, pipelines_count):
        self.api_dict = api_dict
        self.request_router = DefaultRequestRouter(scripts_dict)
        self.request_queue, self.output_queue = Queue(), Queue()
        self.pipelines = list()

        for _ in range(pipelines_count):
            input_queue = Queue()
            new_pipeline = Pipeline(input_queue, self.output_queue, self.request_router)
            self.pipelines.append(new_pipeline)
            # start pipeline proccess
            Process(target=new_pipeline.start).start()

    def start(self):
        for api_name, api_class in self.api_dict.items():
            api_instance = api_class(self.request_queue)
            # transform dict of classes to dict of instances
            self.api_dict[api_name] = api_instance
            Process(target=api_instance.start).start()


        while True:
            request = self.request_queue.get()
            
            if request:
                min_pipeline = min(self.pipelines, key=lambda x: x.input_queue.qsize())
                min_pipeline.input_queue.put(request)

            request = self.output_queue.get()

            if request:
                self.api_dict[request.api_name].send_response(request)
                
