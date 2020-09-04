class DefaultRequestRouter(object):
    def __init__(self, scripts_dict):
        self.scripts = scripts_dict

    def route(self, request):
        command = request.command
        
        try:
            self.scripts[command]().run(request)
        except KeyError:
            return
