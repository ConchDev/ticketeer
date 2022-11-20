# Ticketeer
## A basic open-source Discord ticket bot made in Python

Ticketeer is a Discord ticket bot made with Pycord in Python. It uses Tortoise ORM and SQLite as a database, and Poetry as a package manager. While not exactly being for beginners, this open sourced project could help some people understand how to use Tortoise ORM and Pycord.

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

