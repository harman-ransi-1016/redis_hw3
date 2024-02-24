import yaml
import redis
import json
import CMC_api
import pandas as pd

class RedisUploader:
    """
    A class for uploading data to a Redis database.

    Attributes:
    - config_file (str): The path to the YAML configuration file containing Redis configurations.
    - redis_config (dict): A dictionary containing Redis configuration parameters.
    - redis_client (redis.Redis): The Redis client used for interacting with the Redis database.
    """

    def __init__(self, config_file='config.yaml'):
        """
        Initializes the RedisUploader object.

        Args:
        - config_file (str): The path to the YAML configuration file containing Redis configurations.
        """
        self.mysql_config = None
        self.redis_config = None
        self.load_config(config_file)
        self.redis_client = redis.Redis(
            host=self.redis_config['host'],
            port=self.redis_config['port'],
            db=self.redis_config['db'],
            password=self.redis_config.get('password', None) 
        )

    def load_config(self, config_file):
        """
        Loads MySQL and Redis configurations from the specified YAML configuration file.

        Args:
        - config_file (str): The path to the YAML configuration file.
        """
        with open(config_file, 'r') as file:
            config_data = yaml.safe_load(file)
            self.redis_config = config_data['redis']

    def upload_to_redis(self, data):
        """
        Uploads data to Redis.

        Args:
        - data (dict or list): A dictionary or a list containing the data to be uploaded to Redis.
                               Keys represent Redis keys and values represent corresponding values.

        Returns:
        - bool: True if the upload is successful, False otherwise.
        """
        try:
            if isinstance(data, dict):
                for key, value in data.items():
                    self.redis_client.set(key, json.dumps(value))
            elif isinstance(data, list):
                for idx, entry in enumerate(data):
                    self.redis_client.set(str(idx), json.dumps(entry))
            else:
                raise TypeError("Data must be a dictionary or a list.")

            return True
        except Exception as e:
            print(f"Error uploading data to Redis: {e}")
            return False
        
    def print_redis_data(self):
        """
        Prints data from Redis. Visual to see if data went through correctly. 
        """

        try:
            # Connect to Redis using the configured parameters
            conn_redis = redis.Redis(
                host=self.redis_config['host'],
                port=self.redis_config['port'],
                password=self.redis_config.get('password', None),
                db=self.redis_config.get('db', 0)
            )

            # Iterate over the keys in Redis
            for key in conn_redis.keys():
                type_of_value = conn_redis.type(key)
                if type_of_value == b'string':
                    value = conn_redis.get(key)
                elif type_of_value == b'list':
                    value = conn_redis.lrange(key, 0, -1)  # Get all elements in the list
                else:
                    value = 'Unsupported data type'
                print(f"Key: {key}, Value: {value}")
        except Exception as e:
            print(f"Error accessing data from Redis: {e}")

    def redis_data_to_dataframe(self):
        """
        Retrieves data from Redis and converts it into a pandas DataFrame.

        Returns:
        - df (pd.DataFrame): A pandas DataFrame containing the data retrieved from Redis.
        """
        try:
            # Initialize an empty list to store the data
            data = []

            # Iterate over the keys in Redis, add locally
            for key in self.redis_client.keys():
                value = self.redis_client.get(key)
                value_dict = json.loads(value)
                data.append(value_dict)

            # turn data into df
            df = pd.DataFrame(data)
            return df
        
        except Exception as e:
            print(f"Error converting Redis data to DataFrame: {e}")
            return None