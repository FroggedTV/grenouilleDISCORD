import logging
from time import sleep
import discord
import config

LOGGER = logging.getLogger(__name__)

class Alert(object):
    def __init__(self, client, database):
        LOGGER.debug("Initializing Alert object")
        self.client = client
        self.database = database
        self.admins = {}
        self.report_channel = discord.utils.get(self.client.get_all_channels(),
            server__name=config.server_name, id=config.report_channel)
        self.get_discord_users()

    def get_discord_users(self):
        for admin in config.admins:
            self.admins[admin] = discord.utils.get(self.client.get_all_members(),
            server__name=config.server_name, id=config.admins[admin])
            LOGGER.debug(self.admins)

    def alert_consumer(self, game_id, status):
        if not self.database.is_alert(game_id, status):
            self.send_alert(game_id, status)

    def send_alert(self, game_id, status):
        LOGGER.debug("ALERT FOR GAME "+str(game_id)+" : "+status)
        self.database.insert_alert(game_id, status)
