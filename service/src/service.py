import os
import asyncio

from abc import abstractmethod
from time import sleep
from dotenv import load_dotenv
from discord.ext import commands
from multiprocessing import Process, Manager

try:
    from service.src.logger import Log
except:
    from src.logger import Log

class Service:

    def __init__(self, name, prefix,  debug = False):

        # Load .env's token
        load_dotenv()
        # Command name
        self.name = name
        # Get discord
        self.client = commands.Bot(prefix)
        # Command prefix
        self.prefix = prefix
        # Discord token
        self.TOKEN = os.getenv('DISCORD_TOKEN')
        # Debug use
        self.debug = debug
        # Logger
        self.log = Log(self.name)

    @abstractmethod
    def operation(self):

        # Execute while bot is ready
        @self.client.event
        async def on_ready():
            self.log.important(f'{self.client.user.name}\'s {self.name} service has connected to Discord!')

        # Kill service's event loop (only works in debug mode)
        @self.client.command()
        async def kill(ctx):
            if self.debug:

                # Kill service
                self.log.important("Trying to kill " + self.name + " by " + str(ctx.author))
                exit(0)

        # Echo test for service (only works in debug mode)
        @self.client.command()
        async def echo(ctx, msg=""):
            if self.debug:

                # Echo test
                self.log.log("Echo message " + msg + " to " + str(ctx.author))
                await ctx.send(msg)

        # Restart service (only works in debug mode)
        @self.client.command()
        async def restart(ctx):
            if self.debug:

                self.log.important("Service stopping by " + str(ctx.author))
                await self.Stop()

        # Close all restart error
        if not self.debug:
            @restart.error
            async def restart_handler(ctx, error):
                pass

    # Kill event loop
    async def Stop(self):
        self.log.important("Service has gone down")
        await self.client.logout()

    # Start event loop
    def Start(self):

        self.log.important(f"Try starting service with prefix:{self.prefix}")
        self.operation()

        try:
            self.log.important("Event loop is starting")
            # Start event loop with discord token
            self.client.run(self.TOKEN)
        except KeyboardInterrupt:
            exit(0)
        except:
            self.log.important("Event loop died, trying to kill process")

    # Main service
    def run(self):
        self.Start()