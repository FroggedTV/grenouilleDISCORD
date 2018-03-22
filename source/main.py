import discord
import asyncio
import time
import config
import logging
import logging.handlers
import sys
from time import sleep
from threading import Thread

from probe import Probe
from database import Database

LOGGER = logging.getLogger(__name__)

token           = sys.argv[1]
api_key         = sys.argv[2]
client          = discord.Client()
probe           = None
channel         = None


@client.event
async def on_ready():
    try:
        global channel
        while not channel:
            LOGGER.debug("Waiting to get channel from discord...")
            channel = discord.utils.get(client.get_all_channels(), server__name=config.server_name, name=config.report_channel)
            sleep(1)
        probe.channel = channel
        probe.client = client
        probe.start()
        LOGGER.info("GrenouilleDISCORD is ready!")
    except Exception as e:
        LOGGER.error('Error in on_ready: '+str(e))


@client.event
async def on_message(message):
    try:
        pass
    except Exception as e:
        LOGGER.error('Error in on_message: '+str(e))


def main():
    try:
        logging.basicConfig(level=config.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.handlers.RotatingFileHandler("grenouille-discord.log", maxBytes=10000000, backupCount=15)
        handler.setLevel(config.log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger('').addHandler(handler)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("discord").setLevel(logging.WARNING)
        logging.getLogger("websockets").setLevel(logging.WARNING)

        database = Database()
        global probe
        probe = Probe(api_key, database)
        client.run(token)

    except Exception as e:
        LOGGER.error('Error in main: '+str(e))

if __name__ == "__main__":
    main()
