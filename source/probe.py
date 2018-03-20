import logging
from threading import Thread
from time import sleep
import requests
import config

LOGGER = logging.getLogger(__name__)

class Probe(Thread):
    def __init__(self,alert, host, refresh_time, api_key):
        Thread.__init__(self)
        LOGGER.debug("Initializing Probe thread")
        self.alert = alert
        self.host = host
        self.refresh_time = refresh_time
        self.api_key = api_key

    def get_list(self):
        r = requests.get(self.host + '/api/game/list',
            headers= {
                'API_KEY': self.api_key
            },
            json={
                'fields': ['name', 'status', 'bot'],
                'limit': config.game_list_limit,
                'offset': config.game_list_offset
                }
            )
        content = r.json()
        games = content['payload']['games']
        return games

    def run(self):
        try:
            LOGGER.debug("Starting Probe loop")
            while True:
                games = self.get_list()
                for game in games:
                    if game['status'] == 'GameStatus.WAITING_FOR_PLAYERS' or game['status'] == 'GameStatus.CANCELLED':
                        self.alert.alert_consumer(game['id'], game['status'])
                sleep(int(self.refresh_time))
        except Exception as e:
            LOGGER.error("Error in Probe.run: "+str(e))
