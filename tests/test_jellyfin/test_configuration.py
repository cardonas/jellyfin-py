import builtins
import json

import pytest
from jellyfin.configuration import Configuration


class TestConfiguration:
    @pytest.fixture
    def mock_file(self):
        return {"apiKey": "test_api_key"}

    @pytest.fixture
    def config(self):
        return Configuration(file_path="does_not_matter")

    def test_load_configuration(self, monkeypatch, mocker, config, mock_file):
        mock_open = mocker.mock_open(read_data=json.dumps(mock_file))
        monkeypatch.setattr(builtins, "open", mock_open)

        result = config.load_configuration()
        assert result.api_key == mock_file["apiKey"]
