import core

def run(request_args: list) -> str:
    if len(request_args) != 0:
        return ' '.join(request_args)
    else: 
        return 'error!'