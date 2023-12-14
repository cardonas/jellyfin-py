import json
import tempfile

from jellyfin.jellyfin_api import JellyfinApi
from Models.ConfigurationData import ConfigurationData
from pytest import fixture


@fixture
def config_data():
    return {
        "hostname": "test_hostname",
        "port": "8080",
        "api_key": "test_api_key"
    }

@fixture
def api(config_data):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as config_file:
        json.dump(config_data, config_file)
    return JellyfinApi(file_path=config_file.name)
