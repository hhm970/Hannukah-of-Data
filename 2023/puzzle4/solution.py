"""Solution to Puzzle 4 of Hannukah of Data 2023."""

import pandas as pd


START_TIME_DAWN = "00:00:00"

END_TIME_DAWN = "05:00:00"

VALID_DAYS = {0, 1, 2, 3, 6}


def day_in_list(input_day: int) -> bool:
    if input_day in VALID_DAYS:
        return True
    return False


def filter_orders(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Given a pd.DataFrame object containing columns 'orderid', 'customerid', 'ordered', 
    returns a pd.DataFrame object which formats the 'ordered' column into datetime 
    data type, and filters all values in 'ordered' so that the date is in the 
    specified valid days, and the timestamp is between 00:00:00 and 05:00:00.
    """

    input_df["ordered"] = pd.to_datetime(input_df["ordered"])

    input_df = input_df[(input_df["ordered"].dt.time >= pd.Timestamp(START_TIME_DAWN).time()) & 
                        (input_df["ordered"].dt.time <= pd.Timestamp(END_TIME_DAWN).time())]

    input_df = input_df[input_df["ordered"].dt.day_of_week.apply(day_in_list) == True]

    return input_df


def join_all_df(customer_df: pd.DataFrame, order_df: pd.DataFrame, 
                                      order_item_df: pd.DataFrame, product_df: 
                                      pd.DataFrame) -> pd.DataFrame:
    """
    Given four pd.DataFrame objects; 
    customer_df with columns 'customerid', 'name', 'phone'; 
    order_df  with columns 'customerid', 'orderid', 'ordered';
    order_item_df with columns 'orderid', 'qty', 'sku';
    product_df with columns 'sku, 'desc'; 
    returns a singular merged pd.DataFrame object.
    """

    customer_order_df = pd.merge(customer_df, order_df, how="inner", on="customerid")

    customer_order_items_df = pd.merge(customer_order_df, order_item_df, how="inner", on="orderid")

    result_df = pd.merge(customer_order_items_df, product_df, how="inner", on="sku")

    return result_df


if __name__ == "__main__":
    
    customer_data = pd.read_csv("../noahs-customers.csv")

    orders_items_data = pd.read_csv("../noahs-orders_items.csv")

    orders_data = pd.read_csv("../noahs-orders.csv")

    products_data = pd.read_csv("../noahs-products.csv")

    customer_data = customer_data[['customerid', 'name', 'phone']]

    orders_data = orders_data[['orderid', 'customerid', 'ordered']]

    orders_items_data = orders_items_data[['orderid', 'qty', 'sku']]

    products_data = products_data[['sku', 'desc']]

    orders_data = filter_orders(orders_data)

    orders_items_data = orders_items_data[orders_items_data["qty"] > 1]

    products_data = products_data[products_data['sku'].str.contains("BKY")]

    aggregate_data = join_all_df(customer_data, orders_data, orders_items_data, products_data)

    print(aggregate_data["phone"].mode())