import requests
from requests import Session
import secrets_1
from pprint import pprint as pp

class CMC:
    """
    A class for interacting with the CoinMarketCap API.

    Attributes:
    - apiurl (str): The base URL for the CoinMarketCap API.
    - headers (dict): A dictionary containing headers for API requests, including the API token.
    - session (requests.Session): A session object used to make HTTP requests to the CoinMarketCap API.
    """

    def __init__(self, token):
        """
        Initializes the CMC object with the provided API token.

        Args:
        - token (str): The API token for accessing the CoinMarketCap API.
        """
        self.apiurl = 'https://pro-api.coinmarketcap.com/'
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': token}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getAllCoins(self):
        """
        Retrieves information about all available cryptocurrencies from the CoinMarketCap API.

        Returns:
        - filtered_data (list): A list of dictionaries containing information about cryptocurrencies.
                               Each dictionary represents a cryptocurrency and includes the following keys:
                                 - 'id': Unique identifier for the cryptocurrency.
                                 - 'rank': Ranking of the cryptocurrency.
                                 - 'name': Name of the cryptocurrency.
                                 - 'symbol': Symbol of the cryptocurrency.
                                 - 'slug': Slug of the cryptocurrency.
                                 - 'is_active': Indicator of whether the cryptocurrency is active.
                                 - 'first_historical_data': Date and time of the first historical data.
                                 - 'last_historical_data': Date and time of the last historical data.
                                 - 'platform': Platform information for the cryptocurrency.
        """
        url = self.apiurl + 'v1/cryptocurrency/map'
        parameters = {'limit': 50}  # Limit of 50 records 
        r = self.session.get(url, params=parameters)
        data = r.json()['data']

        # Ensuring JSON Structure
        filtered_data = [
            entry for entry in data if all(
                key in entry for key in [
                    'id', 'rank', 'name', 'symbol', 'slug', 'is_active',
                    'first_historical_data', 'last_historical_data', 'platform'
                ]
            )
        ]

        return filtered_data

