from archbucket.components import AbstractScript

class EchoScript(AbstractScript):
    class Meta:
        name = 'echo'
        
    def run(self, request):
        if len(request.args) != 0:
            request.response =  ' '.join(request.args)
        else: 
            request.response = 'error'