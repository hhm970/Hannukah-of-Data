"""Solution to Puzzle 5 of Hannukah of Data 2023."""

import pandas as pd


def format_customers_df(customers_df: pd.DataFrame) -> pd.DataFrame:
    """
    Given the pd.DataFrame object containing customer data, we create a new
    series called 'area', which is the first part of the 'citystatezip' series,
    and return the corresponding pd.DataFrame with only necessary columns.
    """
    
    customers_df_area = customers_df["citystatezip"].str.split(", ")

    customers_df["area"] = customers_df_area.apply(lambda a: a[0])

    result_df = customers_df[["customerid", "phone", "area"]]

    return result_df


def get_combined_customer_order_df(customers_df: pd.DataFrame, orders_df: pd.DataFrame,
                                   orders_items_df: pd.DataFrame, products_df: pd.DataFrame):
    """
    Given all 4 dataframes, inner joins all 4 of them, with the foreign keys
    
        • customerid between customers_df and orders_df,
        • orderid between orders_df and orders_items_df,
        • sku between orders_items_df and products_df.
    """

    customers_and_orders_df = pd.merge(customers_df, orders_df, how="inner", on="customerid")

    products_and_orders_items_df = pd.merge(products_df, orders_items_df, how="inner", on="sku")

    result_df = pd.merge(customers_and_orders_df, products_and_orders_items_df, how="inner", on="orderid")

    return result_df


if __name__ == "__main__":

    noahs_customers = pd.read_csv("../noahs-customers.csv")

    noahs_orders_items = pd.read_csv("../noahs-orders_items.csv")

    noahs_orders = pd.read_csv("../noahs-orders.csv")

    noahs_products = pd.read_csv("../noahs-products.csv")

    noahs_customers = format_customers_df(noahs_customers)

    noahs_customers = noahs_customers[noahs_customers["area"] == "Staten Island"]

    noahs_orders = noahs_orders[["orderid", "customerid"]]

    noahs_products = noahs_products[["sku", "desc"]]

    noahs_orders_items = noahs_orders_items[["orderid", "sku", "qty"]]

    noahs_combined_data = get_combined_customer_order_df(noahs_customers, noahs_orders, noahs_orders_items, noahs_products)

    noahs_combined_data_cats = noahs_combined_data[noahs_combined_data['desc'].str.contains("Cat", case=False)]

    result = noahs_combined_data_cats[noahs_combined_data_cats["qty"] > 1].sort_values(by="qty", ascending=False)

    print(result.iloc[0]["phone"])