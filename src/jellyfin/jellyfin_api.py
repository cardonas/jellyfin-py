from pathlib import Path
from typing import Any
from typing import Optional

import requests.auth
from jellyfin.configuration import Configuration
from Models.ConfigurationData import ConfigurationData
from requests.exceptions import ConnectTimeout


class JellyFinApiError(Exception):
    pass


class JellyfinApi:
    """
    This class is a subclass of the `requests.Session` class and is used to send HTTP requests with a base URL.

    Attributes:
        base_url (str): The base URL to be used for all requests.

    Methods:
        request:
            Sends an HTTP request with the specified method and URL.

            Parameters:
                method (str): The HTTP method to be used for the request (e.g., 'GET', 'POST', 'PUT', 'DELETE').
                url (str): The URL to which the request should be sent.
                *args: Additional positional arguments to be passed to the `request` method of the parent class.
                **kwargs: Additional keyword arguments to be passed to the `request` method of the parent class.

            Returns:
                requests.Response: The response object returned by the `request` method of the parent class.
    """

    class BaseUrlSession(requests.Session):
        """
        This class is a subclass of the `requests.Session` class and is used to send HTTP requests with a base URL.

        Attributes:
            base_url (str): The base URL to be used for all requests.

        Methods:
            request:
                Sends an HTTP request with the specified method and URL.

                Parameters:
                    method (str): The HTTP method to be used for the request (e.g., 'GET', 'POST', 'PUT', 'DELETE').
                    url (str): The URL to which the request should be sent.
                    *args: Additional positional arguments to be passed to the `request` method of the parent class.
                    **kwargs: Additional keyword arguments to be passed to the `request` method of the parent class.

                Returns:
                    requests.Response: The response object returned by the `request` method of the parent class.
        """

        base_url: Optional[str] = None

        def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:  # type: ignore
            return super().request(method, self.base_url + url, **kwargs)  # type: ignore

    def __init__(self, *, file_path: Path | str):
        """
        Initialize the class instance.

        :param file_path: The path to the configuration file.
                          It can be either a `Path` object or a string representing the file path.
        """
        self.config: ConfigurationData = Configuration(
            file_path=file_path
        ).load_configuration()
        self.jellyfin_request = self.BaseUrlSession()
        self.jellyfin_request.base_url = (
            f"http://{self.config.hostname}:{self.config.port}"
        )
        self.jellyfin_request.headers.update(
            {"X-Emby-Token": self.config.api_key, "Content-Type": "application/json"}
        )

    def get_items_count(self) -> dict[Any, Any]:
        """
        Return a dictionary with the count of items in Jellyfin.

        :return: A dictionary containing the count of items in Jellyfin.
        :rtype: dict[Any, Any]
        :raises JellyFinApiError: If an error occurs while fetching the item count.
        :raises ConnectTimeout: If the connection times out.
        """
        try:
            response = self.jellyfin_request.get("/Items/Counts")
            return response.json()
        except ConnectTimeout as ct:
            raise JellyFinApiError("Connection timed out", ct)

    def get_server_status(self) -> str:
        """
        Gets the status of the Jellyfin server.

        :return: A string indicating the server status. Possible values are "Not Running" and "Running".
        """
        status = "Not Running"
        response = self.jellyfin_request.get("/System/Ping")
        result = response.content.decode()
        if result == '"Jellyfin Server"':
            status = "Running"
        return status


if __name__ == "__main__":
    try:
        api = JellyfinApi(file_path="mock_json.json")
        print(api.get_items_count())
    except JellyFinApiError as je:
        print(je)
