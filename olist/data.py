import os
import pandas as pd

class Olist:
    """
    The Olist class provides methods to interact with Olist's e-commerce data.
    """
    def __init__(self):
        """
        Initializes the data path relative to this file's location.

        Example:
            >>> olist = Olist()
            >>> print(olist.data_path)
        """
        # Bu dosyanın (data.py) bulunduğu yerin bir üst klasöründeki 'data' klasörüne gider.
        # olist-analysis/01-Statistical-Inference/data-orders/data/ yapısına uygundur.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(current_dir, "..", "data")

    def get_data(self):
        """
        Reads all CSV files from the data directory and returns them as a dictionary of DataFrames.

        Returns:
            dict: A dictionary where keys are table names and values are pandas DataFrames.

        Example:
            >>> olist = Olist()
            >>> data = olist.get_data()
            >>> if data: print(data.keys())
        """
        if not os.path.exists(self.data_path):
            print(f"Error: Data path not found at {self.data_path}")
            return None

        # List all csv files in the directory
        file_names = [f for f in os.listdir(self.data_path) if f.endswith('.csv')]

        # Create keys by removing 'olist_', '_dataset' and '.csv' from filenames
        key_names = [
            f.replace('olist_', '').replace('_dataset', '').replace('.csv', '')
            for f in file_names
        ]

        # Load each CSV into a DataFrame
        data = {
            key: pd.read_csv(os.path.join(self.data_path, file))
            for key, file in zip(key_names, file_names)
        }
        return data

    def ping(self):
        """
        Simple health check. Returns 'pong'.

        Example:
            >>> Olist().ping()
            'pong'
        """
        return "pong"
