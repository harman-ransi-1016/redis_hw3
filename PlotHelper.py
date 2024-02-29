import pandas as pd
import matplotlib.pyplot as plt
import os

class PlotHelper:
    """
    A class for plotting cryptocurrency data.
    """

    @staticmethod
    def plot_crypto_introduction(dataframe, filename='crypto_introduction.jpg'):
        """
        Plots the introduction of cryptocurrencies over time based on the provided DataFrame and saves it as a JPEG file.

        Args:
        - dataframe (pd.DataFrame): DataFrame containing cryptocurrency data.
        - filename (str): Name of the JPEG file to save the plot. Default is 'crypto_introduction.jpg'.

        Returns:
        - str: Filepath of the saved plot.
        """

        # Isolating data
        dataframe['first_historical_data'] = pd.to_datetime(dataframe['first_historical_data'])
        dataframe['year'] = dataframe['first_historical_data'].dt.year
        dataframe['month'] = dataframe['first_historical_data'].dt.month
        historical_data_count = dataframe.groupby(['year', 'month']).size().reset_index(name='count')

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.bar(historical_data_count['year'].astype(str) + '-' + historical_data_count['month'].astype(str), historical_data_count['count'], color='skyblue')
        plt.xlabel('Year-Month')
        plt.ylabel('Number of Cryptocurrencies')
        plt.title('Number of Cryptocurrencies Introduced Each Month')
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Save the plot into the 'plots' folder
        plot_dir = 'plots'
        os.makedirs(plot_dir, exist_ok=True)
        filepath = os.path.join(plot_dir, filename)
        plt.savefig(filepath)
        
        # Show the plot
        plt.show()

        # Return the filepath
        return filepath

    @staticmethod
    def plot_rank_distribution(dataframe, filename='rank_distribution.jpg'):
        """
        Plots the distribution of the top 10 cryptocurrency ranks and saves it as a JPEG file.

        Args:
        - dataframe (pd.DataFrame): DataFrame containing cryptocurrency data.
        - filename (str): Name of the JPEG file to save the plot. Default is 'rank_distribution.jpg'.

        Returns:
        - str: Filepath of the saved plot.
        """

        # Isolating data
        sorted_dataframe = dataframe.sort_values(by='rank', ascending=True)
        top_10 = sorted_dataframe.head(10)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.barh(top_10['name'], 1 / top_10['rank'], color='skyblue')  # Plot the reciprocal of the rank
        plt.xlabel('Reciprocal of Rank')
        plt.ylabel('Cryptocurrency')
        plt.title('Top 10 Cryptocurrency Ranks')
        plt.gca().invert_yaxis()  # Invert the y-axis to display the highest rank at the top
        plt.tight_layout()

        # Save the plot into the 'plots' folder
        plot_dir = 'plots'
        os.makedirs(plot_dir, exist_ok=True)
        filepath = os.path.join(plot_dir, filename)
        plt.savefig(filepath)
        
        # Show the plot
        plt.show()

        # Return the filepath
        return filepath

    @staticmethod
    def plot_top_10_table(dataframe, filename='top_10_cryptos_table.jpg'):
        """
        Creates a table in Matplotlib displaying the names and symbols of the top 10 cryptocurrencies and saves it as a JPEG file.

        Args:
        - dataframe (pd.DataFrame): DataFrame containing cryptocurrency data.
        - filename (str): Name of the JPEG file to save the plot. Default is 'top_10_cryptos_table.jpg'.

        Returns:
        - str: Filepath of the saved plot.
        """

        # Isolating data
        sorted_dataframe = dataframe.sort_values(by='rank', ascending=True)
        top_10 = sorted_dataframe.head(10)

        # Plotting
        plt.figure(figsize=(8, 4))
        table = plt.table(cellText=top_10[['name', 'symbol']].values,
                          colLabels=['Name', 'Symbol'],
                          loc='center')
        plt.axis('off')

        # Save the plot as a JPEG file
        plot_dir = 'plots'
        os.makedirs(plot_dir, exist_ok=True)
        filepath = os.path.join(plot_dir, filename)
        plt.savefig(filepath)

        # Show the plot
        plt.show()

        # Return the filepath
        return filepath







