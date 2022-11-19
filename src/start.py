from objects import Bot, StartupType


if __name__ == "__main__":
    bot = Bot(StartupType.dev)
    bot.run()