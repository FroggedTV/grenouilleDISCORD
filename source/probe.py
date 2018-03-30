import logging
from threading import Thread
from time import sleep
import requests
import config
import asyncio
import config
import discord
import datetime

LOGGER = logging.getLogger(__name__)


async def send_message(client, channel, message):
    await client.send_message(channel, message)


class Probe(Thread):
    def __init__(self, database, api_handler):
        Thread.__init__(self)
        LOGGER.debug("Initializing Probe thread")
        self.database           = database
        self.api_handler        = api_handler
        self.client             = None
        self.refresh_time       = config.refresh_time
        self.channel            = None


    def get_admin(self, match):
        admin = None
        match_splitted = match.split("_")
        try:
            for div in config.team_tags:
                for tag in config.team_tags[div]:
                    if match_splitted[1] == tag or match_splitted[2] == tag:
                        admin = config.admins[div]
            if admin:
                return discord.utils.get(self.client.get_all_members(), server__name=config.server_name, id=admin)
            else:
                return None
        except Exception as e:
            LOGGER.error("Error in get_admin: "+str(e))
            return None


    def alert_consumer(self, game_id, name, status, bot, password, team1, team2):
        alert = None
        admin = self.get_admin(name)
        mention = ""
        if admin:
            mention = admin.mention
            
        if status == 'GameStatus.WAITING_FOR_PLAYERS' or status == 'GameStatus.CANCELLED':                
            alert = "La game `"+name+"` n° `"+str(game_id)+"`  (password `"+password+"`), hosted par l'ami `"+bot+"` vient de passer en statut `"+status+"` "+mention
        if not self.database.is_alert(game_id, status):
            self.database.insert_alert(game_id, status)
            async def task_send_message():
                await send_message(self.client, self.channel, alert)
            task = self.client.loop.create_task(task_send_message())

    def run(self):
        LOGGER.debug("Starting Probe...")
        while True:
            try:
                games = self.api_handler.get_games()
                for game in games:
                    if game['status'] == 'GameStatus.WAITING_FOR_PLAYERS' or game['status'] == 'GameStatus.CANCELLED':
                        self.alert_consumer(game['id'], game['name'], game['status'], game['bot'], game['password'], game['team1'], game['team2'])
            except Exception as e:
                LOGGER.error("Error in Probe.run: "+str(e))
            sleep(int(self.refresh_time))
