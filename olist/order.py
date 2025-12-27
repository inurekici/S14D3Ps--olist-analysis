import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        Calculates times in decimal days and filters by status if specified.

        Example:
            >>> order_instance = Order()
            >>> df = order_instance.get_wait_time(is_delivered=True)
            >>> df.shape[1] == 5
        """
        # Inspect the 'orders' DataFrame from the instance attribute
        orders = self.data['orders'].copy()

        # Filter the DataFrame on 'delivered' orders if requested
        if is_delivered:
            orders = orders.query('order_status == "delivered"').copy()

        # Handle datetime conversions using pandas.to_datetime()
        # This converts string dates to pandas datetime objects
        orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
        orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
        orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

        # Calculate 'wait_time' in decimal days starting from 'order_purchase_timestamp'
        # We divide by np.timedelta64(1, 'D') to get the float representation
        orders['wait_time'] = (
            orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']
        ) / np.timedelta64(1, 'D')

        # Calculate 'expected_wait_time' in decimal days
        orders['expected_wait_time'] = (
            orders['order_estimated_delivery_date'] - orders['order_purchase_timestamp']
        ) / np.timedelta64(1, 'D')

        # Calculate 'delay_vs_expected' in decimal days
        # If the order was delivered earlier than expected, set it to 0
        orders['delay_vs_expected'] = (
            orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']
        ) / np.timedelta64(1, 'D')

        # Using clip(lower=0) ensures we replace negative delays with 0
        orders['delay_vs_expected'] = orders['delay_vs_expected'].clip(lower=0)

        # Final DataFrame check (selecting only requested columns)
        return orders[[
            'order_id',
            'wait_time',
            'expected_wait_time',
            'delay_vs_expected',
            'order_status'
        ]]

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        pass  # YOUR CODE HERE

    def get_number_items(self):
        """
        Returns a DataFrame with:
        order_id, number_of_items
        """
        pass  # YOUR CODE HERE

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        pass  # YOUR CODE HERE

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        pass  # YOUR CODE HERE

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_items', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        pass  # YOUR CODE HERE
