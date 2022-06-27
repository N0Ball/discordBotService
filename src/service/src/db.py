import json

class Db:
    
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path) as json_file:
            res = json.load(json_file)

        return res

    def write(self, data):
        with open(self.path, 'w') as json_file:
            json.dump(data, json_file)

