import config
import logging
import requests

LOGGER = logging.getLogger(__name__)


class ApiHandler(object):
    def __init__(self, api_key):
        LOGGER.debug("Initializing ApiHandler object")
        self.api_key            = api_key
        self.host               = config.api_url
        self.game_list_limit    = config.game_list_limit
        self.game_list_offset   = config.game_list_offset

    def get_games(self):
        r = requests.get(self.host + '/api/game/list',
            headers= {
                'API_KEY': self.api_key
            },
            json={
                'fields': ['name', 'status', 'bot', 'password', 'team1', 'team2'],
                'limit': self.game_list_limit,
                'offset': self.game_list_offset
            }
        )
        content = r.json()
        games = content['payload']['games']
        return games

    def get_status(self, game_id):
        r = requests.get(self.host + '/api/game/details',
            headers= {
                'API_KEY': self.api_key
            },
            json={
                'id': game_id
            }
        )
        content = r.json()
        return content['payload']['status']

    def get_current_games(self):
        games = self.get_games()
        res = []
        for game in games:
            if not game['status'] == 'GameStatus.CANCELLED' and not game['status'] == 'GameStatus.COMPLETED':
                res.append("`"+game['name']+"` (ID `"+str(game['id'])+"`) est host par l'ami `"+game['bot']+"` avec le statut `"+game['status']+"`")
        return res


