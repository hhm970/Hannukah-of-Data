"""Solution to Puzzle 3 of Hannukah of Data 2023."""


import pandas as pd


CONTRACTOR_PHONE = "332-274-4185"


def cancer_birth_daymonth(daymonth_list: list[str]) -> bool:
    """Given a list with two numeric elements, the first representing a month,
    and the second representing the day of a month, return True if the list
    represents a Cancer-born birthdate, and False otherwise."""

    month = int(daymonth_list[0])

    day = int(daymonth_list[1])

    if month == 6 and day >= 21:
        return True
    if month == 7 and day <= 22:
        return True
    
    return False


def get_customer_row_from_phone(input_df: pd.DataFrame, 
                                phone_number: str) -> pd.DataFrame:
    """Given a customer's phone number, returns their row 
    in the input pd.DataFrame object."""

    return input_df[input_df["phone"] == phone_number]


def split_birthdate(input_df: pd.DataFrame) -> pd.DataFrame:
    """Given a pd.DataFrame object with column 'birthdate', 
    returns a pd.DataFrame object with columns 'birth_year'and 'birth_day&month'."""
    
    birthdate_split = input_df["birthdate"].str.split("-")

    input_df["birth_year"] = birthdate_split.apply(lambda a: a[0])

    input_df["birth_day&month"] = birthdate_split.apply(lambda a: a[1:])

    return input_df.drop(columns=["birthdate"])


if __name__ == "__main__":

    customer_data = pd.read_csv("../noahs-customers.csv")

    customer_data = customer_data[["customerid", "name", "birthdate", "phone", "citystatezip"]]

    customer_data = split_birthdate(customer_data)

    customer_data["birth_year"] = customer_data["birth_year"].astype('int64')

    contractor_row = get_customer_row_from_phone(customer_data, CONTRACTOR_PHONE)

    contractor_zip = contractor_row.to_dict()['citystatezip'][474]

    customer_data = customer_data[customer_data["birth_year"].mod(12) == 7]

    customer_data = customer_data[customer_data["birth_day&month"].apply(cancer_birth_daymonth) == True]

    customer_data = customer_data[customer_data["citystatezip"].str.contains(contractor_zip)]

    print(customer_data.to_dict()['phone'][1549])