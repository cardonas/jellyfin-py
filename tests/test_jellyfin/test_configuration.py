import builtins
import json

from jellyfin.configuration import Configuration
from pytest import fixture


class TestConfiguration:
    @fixture
    def mock_file(self):
        return {
            "apiKey": "test_api_key",
            "hostname": "test_hostname",
            "port": "test_port",
        }

    @fixture
    def config(self):
        return Configuration(file_path="does_not_matter")

    def test_load_configuration(self, monkeypatch, mocker, config, mock_file):
        mock_open = mocker.mock_open(read_data=json.dumps(mock_file))
        monkeypatch.setattr(builtins, "open", mock_open)

        result = config.load_configuration()
        assert result.api_key == mock_file["apiKey"]
