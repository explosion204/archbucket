from .request_router import RequestRouter, Request
from .pipeline import Pipeline
from threading import Thread
import ast
import re
import os
import json
import importlib
import inspect

class Bot:
    def __init__(self, pipelines_count, api_dict):
        self.pipelines = list()
        for _ in range(pipelines_count):
            # setting pipelines
            new_pipeline = Pipeline(self)
            self.pipelines.append(new_pipeline)
            pipeline_thread = Thread(target=new_pipeline.start)
            pipeline_thread.start()
        # setting up request router
        self.request_router = RequestRouter()
        # loading api classes
        self.api_path = os.path.join(os.path.dirname(__file__), 'api')
        self.api_dict = api_dict
        # with open(self.api_path + '/.api') as file:
        #     names = json.load(file)
        # for (api_name, [class_name, enabled]) in names.items():
        #     if enabled:
        #         api_module = importlib.import_module(f'.{api_name}', 'archbucket.core.api')
        #         api_instance = eval(f'api_module.{class_name}()')
        #         self.api_dict[api_name] = api_instance
        # busy flag
        self.busy = False

    def push_request(self, request):
        while True:
            if not self.busy:
                self._find_pipeline(request)
                break

    def _find_pipeline(self, request):
        self.busy = True
        free_pipelines = [item for item in self.pipelines]
        min_pipeline = min(free_pipelines, key=lambda item: item.count)
        min_pipeline.push_request(request)
        self.busy = False

    def start_bot(self):
        for api_instance in self.api_dict.values():
            try:
                api_thread = Thread(target=api_instance.start, args=(self, ))
                api_thread.start()
            except Exception:
                pass

    def stop_bot(self):
        for api_instance in self.api_dict.values():
            try:
                api_instance.stop()
            except Exception:
                pass

    def send_response(self, request: Request):
        self.api_dict[request.api_name].send_response(request)

    def import_api(self, api_name, class_name, source_code) -> (bool, str):
        try:
             ast.parse(source_code)
        except SyntaxError:
            return (False, 'Syntax error.')
        if not re.search(r'\tdef __init__\(self\):', source_code):
            return (False, "API class must have '__init__' member function which takes one argument (including 'self')")
        if not re.search(r'\tdef start\(self, [^\s\n]+\):', source_code):
            return (False, "API class must have 'start' member function which takes two arguments (including 'self')")
        if not re.search(r'\tdef stop\(self\):', source_code):
            return (False, "API class must have 'stop' member function which takes one argument (including 'self')")
        if not re.search(r'\tdef send_response\(self, [^\s\n]+\):', source_code):
            return (False, "API class must have 'send_response' member function whick takes two arguments (including 'self')")
        with open(self.api_path + '/.api', 'r') as file:
            apis_dict = json.load(file)
            apis_dict[f'{api_name}'] = [class_name, 'disabled']
        with open(self.api_path + '/.api', 'w') as file:
            json.dump(apis_dict, file)
        with open(self.api_path + f'/{api_name}.py', 'w') as file:
            file.write(source_code)
        return (True, f'API class {api_name} successfully imported.')
