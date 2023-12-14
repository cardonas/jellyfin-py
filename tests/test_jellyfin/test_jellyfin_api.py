import responses
from jellyfin.jellyfin_api import JellyfinApi
from pytest import mark


class TestJellyfinApi:
    @responses.activate
    def test_get_json(self, api: JellyfinApi):
        """
        :param api: The JellyfinApi instance used for making the API request.
        :return: The items count in JSON format.

        This method sends a GET request to the '/Items/Counts' endpoint of the Jellyfin API using the provided JellyfinApi instance. It expects to receive a JSON response containing the counts
        * of different types of items (such as movies, series, episodes, artists, etc.) available in the Jellyfin library.

        The method sets up a mock response for the '/Items/Counts' endpoint with the expected JSON response. It then compares the returned items count with the expected JSON and asserts their
        * equality.

        Example usage:
            @responses.activate
            def test_get_json(self, api: JellyfinApi):
                expected_json = {
                    "MovieCount": 0,
                    "SeriesCount": 0,
                    "EpisodeCount": 0,
                    "ArtistCount": 0,
                    "ProgramCount": 0,
                    "TrailerCount": 0,
                    "SongCount": 0,
                    "AlbumCount": 0,
                    "MusicVideoCount": 0,
                    "BoxSetCount": 0,
                    "BookCount": 0,
                    "ItemCount": 0,
                }

                url = f"{api.jellyfin_request.base_url}/Items/Counts"
                responses.add(responses.GET, url, json=expected_json, status=200)

                assert api.get_items_count() == expected_json
        """
        # Define the expected json response
        expected_json = {
            "MovieCount": 0,
            "SeriesCount": 0,
            "EpisodeCount": 0,
            "ArtistCount": 0,
            "ProgramCount": 0,
            "TrailerCount": 0,
            "SongCount": 0,
            "AlbumCount": 0,
            "MusicVideoCount": 0,
            "BoxSetCount": 0,
            "BookCount": 0,
            "ItemCount": 0,
        }

        # Define the endpoint url
        url = f"{api.jellyfin_request.base_url}/Items/Counts"

        # Setup the mock for responding to the '/Items/Count' endpoint
        responses.add(responses.GET, url, json=expected_json, status=200)

        assert api.get_items_count() == expected_json

    @responses.activate
    @mark.parametrize(
        "server_response, expected_status",
        [("Jellyfin Server", "Running"), ("Something Else", "Not Running")],
    )
    def test_server_status(
        self, api: JellyfinApi, server_response: str, expected_status: str
    ):
        """
        Test the server status.

        :param api: The `JellyfinApi` object representing the Jellyfin API.
        :param server_response: The server response to be mocked.
        :param expected_status: The expected server status.

        :return: None
        """
        url = f"{api.jellyfin_request.base_url}/System/Ping"

        responses.add(responses.GET, url, json=server_response, status=200)
        assert api.get_server_status() == expected_status
