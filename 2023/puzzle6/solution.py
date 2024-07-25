"""Solution to Puzzle 6 of Hannukah of Data 2023."""

import pandas as pd


if __name__ == "__main__":
    
    noahs_customers = pd.read_csv("../noahs-customers.csv")

    noahs_orders_items = pd.read_csv("../noahs-orders_items.csv")

    noahs_orders = pd.read_csv("../noahs-orders.csv")

    noahs_products = pd.read_csv("../noahs-products.csv")