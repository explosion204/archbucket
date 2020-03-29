from .request_router import RequestRouter, Request
from .pipeline import Pipeline
from threading import Thread
import ast
import re
import os
import json

class Bot:
    def __init__(self):
        self.pipelines = list()
        self.request_router = RequestRouter()
        self.apis_path = os.path.join(os.path.dirname(__file__), 'apis')

    def push_request(self, request):
        free_pipelines = [item for item in self.pipelines]
        min_pipeline = min(free_pipelines, key=lambda item: item.count)
        min_pipeline.push_request(request)

    def create_pipeline(self):
        new_pipeline = Pipeline(self)
        self.pipelines.append(new_pipeline)
        pipeline_thread = Thread(target=new_pipeline.start)
        pipeline_thread.start()

    def start_bot(self, bot_api):
        self.bot_api = bot_api
        try:
            self.bot_api.start(self)
        except Exception:
            pass

    def stop_bot(self):
        try:
            self.bot_api.stop()
        except Exception:
            pass

    def send_response(self, request: Request):
        self.bot_api.send_response(request)

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
        with open(self.apis_path + '/.api', 'r') as file:
            apis_dict = json.load(file)
            apis_dict[f'{api_name}'] = [class_name, 'disabled']
        with open(self.apis_path + '/.api', 'w') as file:
            json.dump(apis_dict, file)
        with open(self.apis_path + f'/{api_name}.py', 'w') as file:
            file.write(source_code)
        return (True, f'API class {api_name} successfully imported.')
