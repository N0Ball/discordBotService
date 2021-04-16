from abc import abstractmethod

try:
    from src.service import Service
except:
    from service.src.service import Service

class Test(Service):

    @abstractmethod
    def operation(self):

        super().operation()

        @self.client.command()
        async def say(ctx, msg=""):
            await ctx.send(f"{str(ctx.author)}, I say's hi to you!")