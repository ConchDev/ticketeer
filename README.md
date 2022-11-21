# Ticketeer
## A basic open-source Discord ticket bot made in Python

Ticketeer is a Discord ticket bot made with Pycord in Python. It uses Tortoise ORM and SQLite as a database, and Poetry as a package manager. While not exactly being for beginners, this open sourced project could help some people understand how to use Tortoise ORM and Pycord.

## To do:
- [ ] Create tickets:
- - [ ] Forum Private
- - [ ] Forum Public
- - [x] Text Private Thread
- - [x] Text Public Thread
- - [x] Text Private Channel
- - [ ] Text Public Channel
- [x] Record Ticket messages
- [ ] Close tickets
- - [ ] Process data on thread delete
- - [ ] Process data with close command
- - [ ] Create, format, and send ticket transcripts to a channel
- [ ] Config settings
- - [x] Ticket channel
- - [x] Ticket handler role
- - [x] Ticket type
- - [ ] Transcript channel
- - [ ] Automatically add ticket handlers to channel
- - [ ] Auto archive settings
- - [ ] Ticket channel category
- [ ] Ticket Categories
- - [ ] Create, Manage, and Delete ticket categories
- - [ ] Different handlers for category
- - [ ] Add tags to forum channel thread
- - [ ] Add tickets with categories to corresponding channel categories

## Setup

To run the bot, you'll need to clone this repository and install the packages with Poetry. If you don't have Poetry installed, you can get it [here](https://python-poetry.org/).

```
git clone https://github.com/ConchDev/ticketeer
cd ticketeer
poetry install
```

Then, clone `.env.example` as `.env`, and populate the environment variables to be specific to you.
```
cp .env.example .env
```

After all that, you can finally run the bot. 
You can run it in prod mode or in dev mode.
```
poetry run dev
poetry run prod
```
At the moment, they're basically the same, with differences in the logger.

## Changing the Database

Thanks to Tortoise, swapping out databases from the default SQLite is relatively easy.
All you need to do is add the Tortoise extra in `pyproject.toml` and swap around the config.

Here's an example with PostgreSQL:

pyproject.toml:
```toml
tortoise-orm = { extras = ["asyncpg"], version = "^0.19.2" }
```

ticketeer/objects/bot.py DB_CONFIG:
```py
DB_CONFIG = {
    "connections": {
        "ticketeer": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.getenv("HOST"),
                "port": os.getenv("PORT"),
                "user": os.getenv("USER"),
                "password": os.getenv("PASS"),
                "database": os.getenv("DB")
            },
        },
    },
    "apps": {
        "ticketeer": {
            "models": ["ticketeer.database.models", "aerich.models"],
            "default_connection": "ticketeer",
        }
    }
}
```

and just like that, the bot will now be configured to use PostgreSQL. If you need to use a different database, please take a look at the official [Tortoise ORM Documentation](https://tortoise.github.io/#pluggable-database-backends)