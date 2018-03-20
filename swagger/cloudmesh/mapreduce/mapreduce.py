import json

from flask import request
import connexion

def do_map():
    data = json.loads(request.data)
    output = [(w, 1) for w in data['words'].split(' ')]
    return json.dumps(output)
    
def do_reduce():
    data = json.loads(request.data)
    
    output = {}
    
    for word in data['words'].split(' '):
        if word in output:
            output[word] += 1
        else:
            output[word] = 1
            
    return json.dumps(output)
