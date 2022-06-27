import os
import json
import socket

from dotenv import load_dotenv

try:
    from service import Service
except:
    from service.src.service import Service

class ServiceClient(Service):

    def __init__(self, name, prefix, debug = False):
        
        super().__init__(name, prefix)

        # Set port and ip
        self.PORT = os.getenv('PORT')
        self.HOST = '127.0.0.1'

    # Send message to server
    def send(self, msg, author = 'NAN'):

        # Set socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # Connect
            s.connect((self.HOST, int(self.PORT)))

            # Set message
            forward_message = {
                "name" : self.name,
                "content" : msg,
                "author" : author
            }

            # Send message
            s.sendall(json.dumps(forward_message).encode('utf-8'))
