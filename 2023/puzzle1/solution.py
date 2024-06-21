"""Solution to Puzzle 1 of Hannukah of Code 2023."""


import pandas as pd


LETTERS_TO_INT = {
    "a": 2, "b": 2, "c": 2, "d": 3,
    "e": 3, "f": 3, "g": 4, "h": 4,
    "i": 4, "j": 5, "k": 5, "l": 5,
    "m": 6, "n": 6, "o": 6, "p": 7,
    "q": 7, "r": 7, "s": 7, "t": 8,
    "u": 8, "v": 8, "w": 9, "x": 9,
    "y": 9, "z": 9
}

def translate(word):
    return "".join([str(LETTERS_TO_INT[i]) for i in word])


def extract_last_name(input_df : pd.DataFrame) -> pd.Series:
    """Given a pd.Dataframe object with a 'name' column, extract the
    last name and format it in lowercase, and return it as a pd.Series object."""

    input_df_name_split = input_df["name"].str.split()

    result = input_df_name_split.apply(lambda a: a[-1]).str.lower()

    return result


def format_phone(input_df: pd.DataFrame) -> pd.Series:
    """Given a pd.Dataframe object with a 'phone' column, returns it as a
    pd.Series object, where it is formatted without hyphens, all values
    with a 0 and/or 1 are excluded."""

    input_df["phone"] = input_df["phone"].str.replace("-", '')

    result = input_df[~(input_df["phone"].str.contains("0") | input_df["phone"].str.contains("1"))]

    return result["phone"]


if __name__ == "__main__":

    customer_data = pd.read_csv("../noahs-customers.csv")

    customer_data = customer_data[["name", "phone"]]

    customer_data["last_name"] = extract_last_name(customer_data)

    customer_data = customer_data[["phone", "last_name"]]

    customer_data["phone"] = format_phone(customer_data)

    customer_data = customer_data[customer_data["last_name"].str.len() == customer_data["phone"].str.len()]

    customer_data = customer_data[customer_data["phone"] == customer_data["last_name"].apply(translate)]
    
    print(customer_data["phone"])