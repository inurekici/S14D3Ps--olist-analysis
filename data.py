import pandas as pd
from pathlib import Path

class Olist:
    """
    Data provider class to load Olist datasets from the centralized data directory.
    """
    def __init__(self):
        """
        Initializes the Olist class with a dynamic path to the 'data' directory.
        """
        # Path(__file__).parent is 'olist/'
        # .parent reaches the root 'olist-analysis/'
        # then we access the 'data/' folder
        self.data_path = Path(__file__).parent.parent / "data"

    def get_data(self):
        """
        Reads all CSV files from the data directory and returns a dictionary of DataFrames.

        Returns:
            dict: A dictionary where keys are table names and values are pandas DataFrames.

        Example:
            >>> from olist.data import Olist
            >>> data = Olist().get_data()
            >>> data['orders'].head()
        """
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data directory not found at: {self.data_path}")

        # Collect all .csv files from the data folder
        file_paths = [p for p in self.data_path.iterdir() if p.is_file() and p.suffix == '.csv']

        data = {}
        for path in file_paths:
            # Clean name: olist_sellers_dataset.csv -> sellers
            key = (path.name
                   .replace('olist_', '')
                   .replace('_dataset.csv', '')
                   .replace('.csv', ''))
            data[key] = pd.read_csv(path)

        return data

    def ping(self):
        """
        Returns 'pong' to verify the class setup.
        """
        return "pong"
