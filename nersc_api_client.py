import requests

from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7523 import PrivateKeyJWT


DEFAULT_API_URL = "https://api.nersc.gov/api/v1.2"
DEFAULT_TOKEN_URL = "https://oidc.nersc.gov/c2id/token"
with open("./creds/clientid.txt", "r") as f:
    DEFAULT_CLIENT_ID = f.read().strip()
with open("./creds/priv_key.pem", "r") as f:
    DEFAULT_PRIVATE_KEY = f.read().strip()


class NERSCApiClient:
    def __init__(
        self,
        api_url=DEFAULT_API_URL,
        token_url=DEFAULT_TOKEN_URL,
        client_id=DEFAULT_CLIENT_ID,
        private_key=DEFAULT_PRIVATE_KEY,
    ):
        self.session: OAuth2Session | None = None
        self.api_url = api_url
        self.token_url = token_url
        self.client_id = client_id
        self.private_key = private_key

    @property
    def connected(self) -> bool:
        """
        Checks if the client is connected to the NERSC API.
        """

        return self.session is not None

    def connect(self) -> bool:
        """
        Connects to the NERSC API and fetches the access token.
        """

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

    def request(self, method, api, **params) -> requests.Response:
        """
        Makes a request to the NERSC API with the provided headers.
        """

        if not self.connected:
            raise RuntimeError(
                "Not connected to NERSC API. Call connect() first.")

        url = f"{self.api_url}/{api}"
        if params:
            url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
        return self.session.request(method=method, url=url)

    def get(self, api, **params) -> requests.Response:
        """
        Makes a GET request to the NERSC API with the provided headers.
        """

        return self.request("GET", api, **params)

    def post(self, api, **params) -> requests.Response:
        """
        Makes a POST request to the NERSC API with the provided headers.
        """

        return self.request("POST", api, **params)
