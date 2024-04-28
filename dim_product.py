import pandas as pd
import numpy as np


def create_product():
    product_data = [
        ["Espresso", 700, 170],
        ["Double Espresso", 1200, 320],
        ["Americano", 800, 200],
        ["Long Black", 800, 200],
        ["Macchiato", 900, 190],
        ["Cappuccino", 1100, 230],
        ["Flat White", 1300, 270],
        ["Cafe Latte", 1100, 250],
        ["Mocha", 1200, 240],
    ]
    product_id = np.arange(1, len(product_data) + 1, 1)
    df = pd.DataFrame(product_data, columns=["product_name", "price", "cost"])
    df = pd.merge(pd.DataFrame(product_id, columns=["product_id"]), df, left_index=True, right_index=True)

    return df
