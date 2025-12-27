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
            >>> df.shape[0] == 96353
        """

        orders = self.data['orders'].copy()

        if is_delivered:
            orders = orders.query('order_status == "delivered"').copy()

        orders = orders.dropna(subset=[
            'order_purchase_timestamp',
            'order_delivered_customer_date',
            'order_estimated_delivery_date'
        ]).copy()

        orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
        orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
        orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

        orders['wait_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']) / np.timedelta64(1, 'D')
        orders['expected_wait_time'] = (orders['order_estimated_delivery_date'] - orders['order_purchase_timestamp']) / np.timedelta64(1, 'D')
        orders['delay_vs_expected'] = (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']) / np.timedelta64(1, 'D')
        orders['delay_vs_expected'] = orders['delay_vs_expected'].clip(lower=0)

        return orders[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]

    def get_review_score(self):
        """
        Returns a DataFrame with order_id, dim_is_five_star, dim_is_one_star, and review_score.

        Example:
            >>> order = Order()
            >>> df = order.get_review_score()
            >>> df['dim_is_five_star'].sum() > 0
        """

        reviews = self.data['order_reviews'].copy()

        reviews['dim_is_five_star'] = reviews['review_score'].map(lambda x: 1 if x == 5 else 0)
        reviews['dim_is_one_star'] = reviews['review_score'].map(lambda x: 1 if x == 1 else 0)

        return reviews[['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']]

    def get_number_items(self):
        """
        Returns a DataFrame with order_id and number_of_items.

        Example:
            >>> order = Order()
            >>> df = order.get_number_items()
            >>> df['number_of_items'].iloc[0] >= 1
        """
        items_raw = self.data['order_items'].copy()

        items_count = items_raw.groupby('order_id').count()[['product_id']]

        items_count.columns = ['number_of_items']

        return items_count.reset_index()

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers

        Example:
            >>> order = Order()
            >>> df = order.get_number_sellers()
            >>> df['number_of_sellers'].max() == 5
        """
        items = self.data['order_items'].copy()

        number_sellers = items.groupby('order_id')[['seller_id']].nunique()

        number_sellers.columns = ['number_of_sellers']

        return number_sellers.reset_index()

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        Example:
            >>> order = Order()
            >>> df = order.get_price_and_freight()
            >>> df['price'].sum() > 0
        """
        # Load order items data
        items = self.data['order_items'].copy()

        # Group by order_id and sum price and freight_value
        price_freight = items.groupby('order_id').agg({
            'price': 'sum',
            'freight_value': 'sum'
        }).reset_index()

        return price_freight

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
        Example:
            >>> order = Order()
            >>> df = order.get_training_data()
            >>> df.columns.tolist()
        """

        df_wait = self.get_wait_time()
        df_review = self.get_review_score()
        df_items = self.get_number_items()
        df_sellers = self.get_number_sellers()
        df_price = self.get_price_and_freight()

        training_data = df_wait \
            .merge(df_review, on='order_id') \
            .merge(df_items, on='order_id') \
            .merge(df_sellers, on='order_id') \
            .merge(df_price, on='order_id')

        return training_data
