"""Solution to Puzzle 2 of Hannukah of Data 2023."""


import pandas as pd


def split_name(input_df: pd.DataFrame) -> pd.DataFrame:
    """Given a pd.DataFrame object with a 'name' column, return the same
    pd.DataFrame object, but with a 'firstname' and 'lastname' column instead."""

    input_df_name_split = input_df["name"].str.split(" ")

    input_df["firstname"] = input_df_name_split.apply(lambda a: a[0])

    input_df["lastname"] = input_df_name_split.apply(lambda a: a[1])

    result_df = input_df.drop(columns=["name"])

    return result_df


def combine_customer_order_product_df(customer_df: pd.DataFrame, order_df: pd.DataFrame, 
                                      order_item_df: pd.DataFrame, product_df: 
                                      pd.DataFrame) -> pd.DataFrame:
    """
    Given four pd.DataFrame objects; customer_df with a 'customerid' column, order_df 
    with columns 'customerid', 'orderid', order_item_df with columns 'orderid', 'sku', and
    product_df with columns 'sku, 'desc', returns a singular merged pd.DataFrame object.
    """

    customer_order_df = pd.merge(customer_df, order_df, how="inner", on="customerid")

    customer_order_items_df = pd.merge(customer_order_df, order_item_df, how="inner", on="orderid")

    result_df = pd.merge(customer_order_items_df, product_df, how="inner", on="sku")

    return result_df[["customerid", "firstname", "lastname", "phone", "ordered", "shipped", "desc"]]


def find_orders_2017(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Given a pd.DataFrame object with columns 'ordered' and 'shipped', returns
    a pd.DataFrame object, where the order and/or shipping date are in 2017.
    """

    result_df = input_df[input_df["ordered"].str.startswith("2017") | 
                                  input_df["shipped"].str.startswith("2017")]

    return result_df


def find_coffee_bagel_rug_desc(input_df: pd.DataFrame) -> pd.DataFrame:
    """Given a pd.DataFrame object with column 'desc', returns a pd.DataFrame object, where desc
    contains the word 'Coffee' and/or 'Bagel' and/or 'Rug'."""

    result_df = input_df[input_df["desc"].str.contains("Coffee") | 
                         input_df["desc"].str.contains("Bagel") | 
                         input_df["desc"].str.contains("Rug")]

    return result_df


if __name__ == "__main__":

    # Acquire csv data first into dataframes
    customer_data = pd.read_csv("../noahs-customers.csv")

    orders_items_data = pd.read_csv("../noahs-orders_items.csv")

    orders_data = pd.read_csv("../noahs-orders.csv")

    products_data = pd.read_csv("../noahs-products.csv")

    # Isolate appropriate columns for each dataframe
    customer_names_data = customer_data[["customerid", "name", "phone"]]

    orders_shipping_data = orders_data[["orderid", "customerid", "ordered", "shipped"]]

    orders_items_data = orders_items_data[["orderid", "sku"]]

    products_data = products_data[["sku", "desc"]]

    # Create new columns for first name & last name, and then filter appropriately
    customer_names_data = split_name(customer_names_data)

    customer_JP_name_data = customer_names_data[customer_names_data["firstname"].str.startswith("J") & customer_names_data["lastname"].str.startswith("P")]

    # Join all 4 dataframes via inner joins
    customer_order_items_product_agg_df = combine_customer_order_product_df(customer_JP_name_data, 
                                            orders_shipping_data, orders_items_data, products_data)

    # Filter out orders made/shipped in 2017
    customer_order_items_agg_df_2017 = find_orders_2017(customer_order_items_product_agg_df)

    # Filter out orders with description containing coffee, bagel, rug
    customer_2017_coffee_bagel_rug_df = find_coffee_bagel_rug_desc(customer_order_items_agg_df_2017)

    print(customer_2017_coffee_bagel_rug_df["phone"].nunique)