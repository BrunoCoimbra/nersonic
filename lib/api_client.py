from typing import Protocol
from requests import Response

from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7523 import PrivateKeyJWT

from lib.config_manager import ConfigManager


config = ConfigManager()


class ApiClient(Protocol):
    """
    Protocol for API client classes.
    """

    @property
    def connected(self) -> bool:
        """
        Checks if the client is connected to the API.
        """

    def connect(self) -> bool:
        """
        Connects to the API and fetches the access token.
        """

    def request(self, method, api, **kwargs) -> Response:
        """
        Makes a request to the API with the provided headers.

        Args:
            method (str): The HTTP method to use (GET, POST, etc.).
            api (str): The API endpoint to call.
            **kwargs: Additional parameters to include in the request.
        Returns:
            Response: The response from the API.
        """


class NerscApiClient(ApiClient):
    """
    NERSC API client class.
    """

    NERSC_API_URL = config.get("NERSC", "ApiUrl")
    NERSC_TOKEN_URL = config.get("NERSC", "TokenUrl")
    with open(config.get("NERSC", "ClientIdPath"), "r") as f:
        NERSC_CLIENT_ID = f.read().strip()
    with open(config.get("NERSC", "PrivateKeyPath"), "r") as f:
        NERSC_PRIVATE_KEY = f.read().strip()

    def __init__(
        self,
        api_url=NERSC_API_URL,
        token_url=NERSC_TOKEN_URL,
        client_id=NERSC_CLIENT_ID,
        private_key=NERSC_PRIVATE_KEY,
    ):
        self.session: OAuth2Session | None = None
        self.api_url = api_url
        self.token_url = token_url
        self.client_id = client_id
        self.private_key = private_key

    @property
    def connected(self) -> bool:
        return self.session is not None

    def connect(self) -> bool:
        try:
            self.session = OAuth2Session(
                self.client_id,
                self.private_key,
                PrivateKeyJWT(self.token_url),
                grant_type="client_credentials",
                token_endpoint=self.token_url,
            )
            self.session.token = self.session.fetch_token()
        except Exception as e:
            print(f"Error connecting to NERSC API: {e}")
        return self.connected

    def request(self, method, api, **kwargs) -> Response:
        if not self.connected:
            raise RuntimeError(
                "Not connected to NERSC API. Call connect() first.")

        url = f"{self.api_url}/{api.lstrip('/')}"
        return self.session.request(method=method, url=url, **kwargs)
