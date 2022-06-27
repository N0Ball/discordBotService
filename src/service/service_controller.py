
from abc import abstractmethod

try:
    from src.db import Db
    from src.logger import Log
    from src.service import Service
except:
    from service.src.db import Db
    from service.src.logger import Log
    from service.src.service_client import ServiceClient

class ServiceController(ServiceClient):

    def __init__(self, name, prefix, debug = False, db = './db/service.json'):

        super().__init__(name, prefix, debug)

        # Get service config
        self.services = Db(db).read()
        self.db = db

    @abstractmethod
    def operation(self):

        super().operation()

        # Load service command
        @self.client.command()
        async def load(ctx, service=""):

            # Check if service is valid
            if service in self.services:

                # Load service by sending command to server
                self.log.important(f"{str(ctx.author)} is trying to load <{service}>")
                await ctx.send(f"loading {service}")
                self.send(f"load {service}", str(ctx.author))

            else:
                self.log.warning(f"{str(ctx.author)} is trying to load a non-existing service <{service}>")

        # Reload service command
        @self.client.command()
        async def reload(ctx, service=""):

            # Check if service is valid
            if service in self.services:

                # Reload service by sending command to server
                self.log.important(f"{str(ctx.author)} is trying to reload <{service}>")
                await ctx.send(f"reloading {service}")
                self.send(f"reload {service}", str(ctx.author))

            else:
                self.log.warning(f"{str(ctx.author)} is trying to reload a non-existing service <{service}>")

        # Stop service command
        @self.client.command()
        async def terminate(ctx, service=""):

            # Check if service is valid
            if service in self.services:

                # Terminate service by sending command to service
                self.log.important(f"{str(ctx.author)} is trying to terminate <{service}>")
                await ctx.send(f"terminating {service}")
                self.send(f"terminate {service}", str(ctx.author))

            else:
                self.log.warning(f"{str(ctx.author)} is trying to terminate a non-existing service <{service}>")

        # List all existing service
        @self.client.command()
        async def listservice(ctx):

            self.log.log(f"Replying to {str(ctx.author)} lists of all services")

            # Send all service in service config
            msg = '```\nAvailable Services:\n'
            for service in self.services:
                msg += f'\t{service}\n'
            msg += '```'
            await ctx.send(msg)

        # Refresh service config
        @self.client.command()
        async def refresh(ctx):

            # Also refresh server's service config
            self.send(f"refresh", str(ctx.author))
            self.services = Db(self.db).read()