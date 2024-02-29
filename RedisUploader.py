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
        - data (dict or list): A dictionary or a list containing the JSON data to be uploaded to Redis.
                            Keys represent Redis JSON keys and values represent corresponding values.

        Returns:
        - bool: True if the upload is successful, False otherwise.
        """
        self.redis_client.flushall()
        try:
            for idx, item in enumerate(data):
                # Ensure each item is a dictionary
                if not isinstance(item, dict):
                    raise TypeError(f"Item at index {idx} is not a dictionary.")

                # Use the 'id' field as the key for each item
                key = item['id']
                self.redis_client.json().set(key, '.', json.dumps(item))
            return True
        except Exception as e:
            print(f"Error uploading data to Redis: {e}")
            return False
        
    def print_redis_data(self):
        """
        Prints data from Redis. Visual to see if data went through correctly. 
        """
        try:
            conn_redis = redis.Redis(
                host=self.redis_config['host'],
                port=self.redis_config['port'],
                password=self.redis_config.get('password', None),
                db=self.redis_config.get('db', 0)
            )

            for key in conn_redis.keys():
                json_data = conn_redis.json().get(key)
                print(f"Key: {key}, JSON Data: {json_data}")

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

            # Iterate over the keys in Redis
            for key in self.redis_client.keys():
                # Get the JSON data using the JSON.GET command
                json_data = self.redis_client.json().get(key)
                
                # Load the JSON data into a dictionary
                data_dict = json.loads(json_data)

                # Append the dictionary to the list
                data.append(data_dict)

            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(data)
            return df
                
        except Exception as e:
            print(f"Error converting Redis data to DataFrame: {e}")


