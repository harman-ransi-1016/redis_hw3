import yaml
from CMC_api import CMC
from RedisUploader import RedisUploader
import secrets_1
import redis
import matplotlib.pyplot as plt
import pandas as pd
from PlotHelper import PlotHelper

class MainProcess:
    """
    A class for managing the main process of gathering data from CoinMarketCap, uploading it to Redis, and performing operations on the data.

    Attributes:
    - config_file (str): The path to the YAML configuration file.
    - redis_config (dict): A dictionary containing Redis configuration parameters.
    - cmc_data (list): A list containing data fetched from CoinMarketCap.
    """

    def __init__(self, config_file='config.yaml'):
        """
        Initializes the MainProcess object.

        Args:
        - config_file (str): The path to the YAML configuration file containing Redis configurations.
        """
        self.config_file = config_file
        self.redis_config = None
        self.cmc_data = None
        self.load_config()

    def load_config(self):
        """
        Loads Redis configurations from the specified YAML configuration file.
        """ 
        with open(self.config_file, 'r') as file:
            config_data = yaml.safe_load(file)
            self.redis_config = config_data['redis']

    def gather_cmc_data(self):
        """
        Fetches data from CoinMarketCap using the API.
        """

        cmc = CMC(secrets_1.API_KEY)
        self.cmc_data = cmc.getAllCoins()

    def process_and_upload(self):
        """
        Processes the data fetched from CoinMarketCap and uploads it to Redis.
        """
        if self.cmc_data:
            try:
                # Upload the data from CMC directly to Redis
                redis_uploader = RedisUploader(self.config_file)
                redis_uploader.upload_to_redis(self.cmc_data)
                
                print("Data processing and upload completed successfully.")
            except Exception as e:
                print(f"Error in processing and upload: {e}")
        else:
            print("No data fetched from CMC.")

    def print_redis_data(self):
        """
        Prints data stored in Redis.
        """
        try:
            # Connect to Redis and print data
            redis_uploader = RedisUploader(self.config_file)
            redis_uploader.print_redis_data()
        except Exception as e:
            print(f"Error printing Redis data: {e}")

    def redis_data_to_dataframe(self):
        """
        Converts data stored in Redis to a pandas DataFrame.
        """
        try:
            # Connect to Redis and convert data to DataFrame
            redis_uploader = RedisUploader(self.config_file)
            df = redis_uploader.redis_data_to_dataframe()
            return df
        except Exception as e:
            print(f"Error converting Redis data to DataFrame: {e}")

    def data_aggregation_plots(self, dataframe):
        """
        Produces matplotlib plots about data
        """
        PlotHelper.plot_crypto_introduction(dataframe)
        PlotHelper.plot_rank_distribution(dataframe)
        PlotHelper.plot_top_10_table(dataframe)
    

# Example usage
if __name__ == "__main__":
    main_process = MainProcess()
    main_process.gather_cmc_data()
    main_process.process_and_upload()
    main_process.print_redis_data() 
    x = main_process.redis_data_to_dataframe()
    main_process.data_aggregation_plots(x)

