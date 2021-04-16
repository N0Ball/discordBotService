import time

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[1;34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class Log():
    
    def __init__(self, name):
        self.name = name

    def log(self, msg):
        print("[+] " + time.ctime(time.time())[:-4] + self.name + style.WHITE + " LOG:\t" + msg + style.RESET)

    def important(self, msg):
        print("[+] " + time.ctime(time.time())[:-4] + self.name + style.CYAN + " LOG:\t" + msg + style.RESET)

    def error(self, msg):
        print("[+] " + time.ctime(time.time())[:-4] + self.name + style.RED + " ERROR:\t" + msg + style.RESET)

    def warning(self, msg):
        print("[+] " + time.ctime(time.time())[:-4] + self.name + style.GREEN + " ALERT:\t" + msg + style.RESET)


if __name__ == '__main__':
    test = Log("test")
    test.log("Logging test")
    test.important("Important logging test")
    test.error("Error test")
    test.warning("ALERT test")