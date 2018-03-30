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
from api_handler import ApiHandler

LOGGER = logging.getLogger(__name__)

token           = sys.argv[1]
api_key         = sys.argv[2]
client          = discord.Client()
probe           = None
api_handler     = ApiHandler(api_key)


@client.event
async def on_ready():
    try:
        channel = None
        while not channel:
            LOGGER.debug("Waiting to get channel from discord...")
            channel = discord.utils.get(client.get_all_channels(), server__name=config.server_name, id=config.report_channel_id)
            sleep(1)
        
        probe.channel = channel
        probe.client = client
        probe.start()
        LOGGER.info("GrenouilleDISCORD is ready!")
    except Exception as e:
        LOGGER.error('Error in on_ready: '+str(e))


@client.event
async def on_message(message):
    if not message.channel.id == config.report_channel_id:
        pass
    elif message.content == '!now':
        try:
            games = api_handler.get_current_games()
            if len(games) == 0:
                await client.send_message(message.channel, 'Nada, rien')
            else:
                for game in games:
                    await client.send_message(message.channel, game)

        except Exception as e:
            LOGGER.error('Error in on_message in condition !now: '+str(e))

    elif message.content.startswith('!status'):
        content = message.content.split(' ')
        if len(content) == 2:
            game_id = content[1]
            try:
                game_status = api_handler.get_status(int(game_id))
                await client.send_message(message.channel, game_status)
            except Exception as e:
                LOGGER.error('Error in on_message in condition !status: '+str(e))
                await client.send_message(message.channel, "Existe pas, > Oups!")
        else:
            await client.send_message(message.channel, 'Utilisation de !status: !status 250')


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
        probe = Probe(database, api_handler)
        probe.daemon = True
        client.run(token)

    except Exception as e:
        LOGGER.error('Error in main: '+str(e))

if __name__ == "__main__":
    main()
