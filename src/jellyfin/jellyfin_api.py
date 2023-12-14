import requests.auth

from Models.ConfigurationData import ConfigurationData


class Jellyfin:
    jellyfin_request = None

    def __init__(self, config: ConfigurationData):
        self.jellyfin_request = requests.Session()
        self.jellyfin_request.headers.update({'Authorization': config.api_key})