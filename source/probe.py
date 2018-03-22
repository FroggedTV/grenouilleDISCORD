import logging
from threading import Thread
from time import sleep
import requests
import config
import asyncio
import config
import discord

LOGGER = logging.getLogger(__name__)

async def send_message(client, channel, message):
    await client.send_message(channel, message)


class Probe(Thread):
    def __init__(self, api_key, database):
        Thread.__init__(self)
        LOGGER.debug("Initializing Probe thread")
        self.api_key            = api_key
        self.database           = database
        self.host               = config.api_url
        self.refresh_time       = config.refresh_time
        self.game_list_limit    = config.game_list_limit
        self.game_list_offset   = config.game_list_offset
        self.client             = None
        self.channel            = None
        self.loop               = asyncio.new_event_loop()

    def get_list(self):
        r = requests.get(self.host + '/api/game/list',
            headers= {
                'API_KEY': self.api_key
            },
            json={
                'fields': ['name', 'status', 'bot'],
                'limit': self.game_list_limit,
                'offset': self.game_list_offset
            }
        )
        content = r.json()
        games = content['payload']['games']
        return games

    def alert_consumer(self, game_id, status):
        if not self.database.is_alert(game_id, status):
            LOGGER.debug("ALERT FOR GAME "+str(game_id)+" : "+status)

            async def test():
                await send_message(self.client, self.channel, "ALERT FOR GAME "+str(game_id)+" : "+status)

            self.loop.run_until_complete(test())

            self.database.insert_alert(game_id, status)

    def run(self):
        try:
            LOGGER.debug("Starting Probe...")
            while True:
                games = self.get_list()
                for game in games:
                    if game['status'] == 'GameStatus.WAITING_FOR_PLAYERS' or game['status'] == 'GameStatus.CANCELLED':
                        self.alert_consumer(game['id'], game['status'])
                sleep(int(self.refresh_time))
        except Exception as e:
            LOGGER.error("Error in Probe.run: "+str(e))
