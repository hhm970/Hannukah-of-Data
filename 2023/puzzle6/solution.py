"""Solution to Puzzle 6 of Hannukah of Data 2023."""

import pandas as pd


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


def format_profit_column(combined_df: pd.DataFrame) -> pd.DataFrame:
    """
    Given our combined pd.DataFrame object, we create a 'profit' column using
    the 'qty', 'unit_price', 'wholesale_cost' columns.
    """

    combined_df["profit"] = combined_df["qty"] * (combined_df["unit_price"] - combined_df["wholesale_cost"])

    return combined_df


if __name__ == "__main__":
    
    noahs_customers = pd.read_csv("../noahs-customers.csv")

    noahs_orders_items = pd.read_csv("../noahs-orders_items.csv")

    noahs_orders = pd.read_csv("../noahs-orders.csv")

    noahs_products = pd.read_csv("../noahs-products.csv")

    noahs_customers = noahs_customers[["customerid", "phone"]]

    noahs_orders = noahs_orders[["orderid", "customerid"]]

    noahs_products = noahs_products[["sku", "wholesale_cost"]]

    noahs_combined_df = get_combined_customer_order_df(noahs_customers, noahs_orders, 
                                                       noahs_orders_items, noahs_products)

    noahs_combined_df_profit = format_profit_column(noahs_combined_df)

    noahs_combined_df = noahs_combined_df_profit[["phone", "profit"]]

    result_df = noahs_combined_df.groupby("phone").sum().sort_values(by="profit")

    print(result_df.iloc[0])