import sys
import json
import socket

from importlib import reload
from service.src.db import Db
from service.src.logger import Log
from multiprocessing import Process
from dotenv import load_dotenv
from service.service_controller import ServiceController

class Server():

    def __init__(self):

        # List of service processes
        self.service_processes = {}
        # Database
        self.services = Db('./db/service.json').read()
        # Log property
        self.log = Log("Main Server")
        # Socket 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Socket listening ip and port
        self.socket.bind(('127.0.0.1', 5230))
        # Load env 
        load_dotenv()
        # Get port
        self.PORT = os.getenv('PORT')


    # Load and start service
    def load_service(self, service):
        
        # Check if service is a valid service
        if service not in self.services:

            self.log.error(f"No service {service} found in current services")
            return

        # Check if service is running
        if service in self.service_processes:

            if self.service_processes[service]["is_running"]:
                self.log.error(f"Try to run an already running service {service}")
                return

        self.log.important(f"Trying to load and start <{service}>")

        # Load service module
        new_service = getattr(__import__(f'service.{service}', fromlist=[self.services[service]['name']]), self.services[service]['name'])(service, self.services[service]['prefix'])

        # Set service config
        self.service_processes[service] = {
            "process" : Process(target = new_service.run),
            "module" : __import__(f'service.{service}'),
            "service" : new_service,
            "is_running" : True
        }

        # Start service process
        self.service_processes[service]['process'].start()

    # Reload service
    def reload_service(self, service):

        # Check if the service is valid
        if service not in self.services:

            self.log.error(f"No service {service} found in current services")
            return

        # Check if the service is running
        if service in self.service_processes:

            self.log.important(f"Try to reload service <{service}>")

            self.log.important(f"Terminating service <{service}>")

            # Stop service process
            self.terminate_service(service)

            # Delete service module
            self.log.important(f"Reloading service <{service}>")
            del self.service_processes[service]['module']

            # Load new service module and start service
            self.log.important(f"Restarting service <{service}>")
            self.load_service(service)

        else:
            self.log.error(f"Can't reload a unloaded service <{service}>")

    # Stop a service
    def terminate_service(self, service):

        # Check if service is valid
        if service not in self.services:

            self.log.error(f"No service {service} found in current services")
            return

        # Check if service is running
        if service in self.service_processes:

            if not self.service_processes[service]["is_running"]:
                self.log.error(f"Try to terminate an already terminated service {service}")
                return

            # Delete service module
            self.log.important(f"Trying to terminate <{service}>")
            del sys.modules[f'service.{service}']

            # Stop service process
            self.service_processes[service]['is_running'] = False
            self.service_processes[service]['process'].kill()

        else:
            self.log.error(f"Can't terminate a not running service {service}")

    # Refresh service database config
    def refresh_service(self):
        self.services = Db('./db/service.json').read()

    # Print service status
    def get_service_status(self):
        for service in self.service_processes:
            self.log.important(f"Service <{service}> is running : {self.service_processes[service]['is_running']}")

    # Main server
    def run(self):

        # Open socket
        self.socket.listen()
        conn, addr = self.socket.accept()

        # Get connection
        with conn:
            self.log.log(f'Connected by {addr}')
            while True:
                self.recv = conn.recv(1024)

                # Stop reciving data while recived nothing
                if not self.recv:
                    break

                # Parse recived data
                responds = json.loads(self.recv.decode('utf-8'))
                author = responds['author']
                content = responds['content']

                # Do operation
                self.log.important(f'operation {content} is commanded by {author}')
                self.oper(responds['content'])

    # Map command to Operation
    def oper(self, operation):
        try:
            operator = operation.split(' ')[0]
            try:
                service = operation.split(' ')[1]
            except:
                service = ''
            
            # Load command
            if operator == 'load':
                self.load_service(service)

            # Reload command
            if operator == 'reload':
                self.reload_service(service)

            # Terminate command
            if operator == 'terminate':
                self.terminate_service(service)

            # Refresh command
            if operator == 'refresh':
                self.refresh_service()

        except Exception as e:
            # Get service loading error
            self.log.error(f'operation {operation} failed by {e}')

    # Stop all running services
    def terminate_all(self):
        for service in self.service_processes:
            if self.service_processes[service]['is_running']:
                self.terminate_service(service)

if __name__ == "__main__":

    # Connect port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Check if port is used
        if s.connect_ex(('localhost', self.PORT)) == 0:
            print(f'Port {self.PORT} is already used')
            exit()

    # Get server
    server = Server()

    # Load service controller
    server.load_service('service_controller')

    # Run server
    while True:
        server.run()

    # While server end
    server.terminate_all()
