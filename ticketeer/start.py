from ticketeer.objects import Bot, StartupType


def start():
    bot = Bot(StartupType.prod)
    bot.run()

def dev():
    bot = Bot(StartupType.dev)
    bot.run()

if __name__ == "__main__":
    dev()
