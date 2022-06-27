from abc import abstractmethod
import requests

URL = 'https://docs.google.com/spreadsheets/d/13ZacBjfuDXAaa5FzxsvG1Rt_qnoiGjVVHQyvkC3_igk/export?exportFormat=csv'

try:
    from src.service import Service
except:
    from service.src.service import Service

class Order(Service):

    @abstractmethod
    def operation(self):

        self.BUDGET = 0
        self.MENU = {}
        self.ORDER = {}
        self.HEADER = None

        super().operation()


        async def whiteList(ctx):

            WHITELIST = [
                '大俠#7423',
                'Wama#3851',
                '№ 球球#6730'
            ]

            if str(ctx.author) not in WHITELIST:

                await ctx.send(f"{str(ctx.author)} you are not permitted to use this")
                return 0

            return 1

        @self.client.command()
        async def order(ctx, dish=""):

            author = str(ctx.author)

            if dish in self.MENU:

                self.ORDER.update({
                    author: dish
                })

                await ctx.send(f"{author} had ordered {dish}, you have to pay NT${self.MENU[dish] - self.BUDGET}")
                return

            await ctx.send(f"ERROR:\t{author} had ordered an unexisted dish")

        @self.client.command()
        async def list(ctx, cmd=""):

            if cmd == 'help':

                helpText = """```
help: display this text
order <dish name>: order an dish
list:
    menu: list current menu
    orders: list current orders
    itmes: list current item amount
    budget: list current budget
    myOrder: list your current orders
set:
    budget: set current budget
    clear: clear all settings
update:
    menu: update current menu at https://docs.google.com/spreadsheets/d/13ZacBjfuDXAaa5FzxsvG1Rt_qnoiGjVVHQyvkC3_igk/
                ```"""

                await ctx.send(helpText)
                return

            if cmd == 'myOrder':

                try:
                    await ctx.send(f"{str(ctx.author)} has order {self.ORDER[str(ctx.author)]}")
                except Exception:
                    await ctx.send(f"{str(ctx.author)} has no order")

                return
            
            if cmd == 'menu':

                orderText = f'```\n{"品項".ljust(10, "　")}\t價格\n'

                for dish in self.MENU:

                    orderText += f'{dish.ljust(10, "　")}\t{self.MENU[dish]}\n'

                orderText += '```'

                await ctx.send(f"{orderText}")
                return

            if cmd == 'orders':

                orderText = f'```\n{"姓名     ".ljust(10, "　")}\t{"品項".ljust(10, "　")}\t價格\n'
                price = 0

                for user in self.ORDER:

                    orderText += f'{user.ljust(10, "　")}\t{self.ORDER[user].ljust(10, "　")}\t{self.MENU[self.ORDER[user]] - self.BUDGET}\n'
                    price += self.MENU[self.ORDER[user]]

                orderText += '```'

                await ctx.send(f'{orderText}\nwith total of `{len(self.ORDER)}` orders with NT$`{price}`')
                return

            if cmd == 'items':

                orderText = f'```\n{"品項".ljust(10, "　")}\t數量\n'
                price = 0

                orders = self.MENU

                for item in orders:

                    orders[item] = 0

                for user in self.ORDER:

                    orders[self.ORDER[user]] += 1

                for item in orders:

                    orderText += f'{item.ljust(10, "　")}\t{orders[item]}\n'

                orderText += '```'

                await ctx.send(f'{orderText}\nwith total of `{len(self.ORDER)}` orders with NT$`{price}`\n')
                return


            if cmd == 'budget':

                await ctx.send(f'Current budget is {self.BUDGET}')
                return

            await ctx.send(f"no such command {cmd}")

        @self.client.command()
        async def update(ctx, cmd=""):

            check = await whiteList(ctx)

            if not check:
                return

            if cmd == 'menu':

                orders = requests.get(URL, allow_redirects=True)
                orders.encoding = 'utf-8'

                self.HEADER = orders.text.split('\r\n')[0].split(',')
                orders = orders.text.split('\r\n')[1:]

                for order in orders:

                    try:
                        item, price = order.split(',')
                        self.MENU.update({
                            item: int(price)
                        })

                    except Exception as e:
                        await ctx.send(f"ERROR: something is wrong with {item = }, {price = }\nmessage: {e}\n")

                await ctx.send(f"Menu has updated")
                return

            await ctx.send(f"update has no command: {cmd}")

        @self.client.command()
        async def set(ctx, cmd="", config=""):

            check = await whiteList(ctx)

            if not check:
                return

            if cmd == 'budget':
            
                try:
                    self.BUDGET = int(config)
                except ValueError:
                    await ctx.send(f"You should send a number for price instead of {config}")
                    return

                await ctx.send(f"{ctx.author} set the price to {self.BUDGET}")
                return

            if cmd == 'clear':

                self.BUDGET = 0
                self.MENU = {}
                self.ORDER = {}
                self.HEADER = None

                await ctx.send(f"{ctx.author} had clear the settings")
                return

            await ctx.send(f"no such command {cmd}")
            