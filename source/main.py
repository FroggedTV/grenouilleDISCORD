import discord
import asyncio
import pytz
import time
import config
import logging
import logging.handlers
import sys

from probe import Probe
from database import Database
from alert import Alert

LOGGER = logging.getLogger(__name__)

token           = sys.argv[1]
api_key         = sys.argv[2]
client          = discord.Client()


def get_time():
    tz = pytz.timezone('Europe/Paris')
    paris_now = datetime.datetime.now(tz)
    return paris_now.strftime('%d-%m-%Y %H:%M:%S')

@client.event
async def on_ready():
    LOGGER.info("GrenouilleDISCORD is ready")


@client.event
async def on_message(message):
    try:
        pass
        #NO COMMANDS YET
    except Exception as e:
        LOGGER.error('Error in on_message: '+str(e))


def main():
    try:
        logging.basicConfig(level=config.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.handlers.RotatingFileHandler("grenouille-discord.log",
            maxBytes=10000000, backupCount=15)
        handler.setLevel(config.log_level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger('').addHandler(handler)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        database = Database()
        alert = Alert(client, database)
        probe = Probe(alert, config.api_url, config.refresh_time, api_key)
        probe.start()
        
        #client.run(token)

    except Exception as e:
        LOGGER.error('Error in main: '+str(e))
        
if __name__ == "__main__":
    main()
