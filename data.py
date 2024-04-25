import numpy as np
import pandas as pd
import random
from faker import Faker
from datetime import datetime
from datetime import timedelta

fake = Faker()
fake.seed_instance(42)
np.random.seed(42)
random.seed(42)


# Helper functions
def random_time(start, end):
    return timedelta(
        seconds=random.randrange(int(timedelta(hours=start).total_seconds()), int(timedelta(hours=end).total_seconds()))
    )


# Product table
def create_product():
    product_name = [
        "Espresso",
        "Double Espresso",
        "Americano",
        "Long Black",
        "Macchiato",
        "Cappuccino",
        "Flat White",
        "Cafe Latte",
        "Mocha",
    ]
    product_id = np.arange(1, len(product_name) + 1, 1)
    data = {"product_id": product_id, "product_name": product_name}
    df = pd.DataFrame(data)

    return df


# Payment type table
def create_payment_mode():
    payment_mode = [
        "Card",
        "Cash",
        "GrabPay",
        "TnG",
    ]
    payment_mode_id = np.arange(1, len(payment_mode) + 1, 1)
    data = {"payment_mode_id": payment_mode_id, "payment_mode": payment_mode}
    df = pd.DataFrame(data)

    return df


# Outlet table
def create_outlet():
    outlet_location = [
        ["Pavilion KL", "Central", "Kuala Lumpur"],
        ["The Gardens Mall", "Central", "Kuala Lumpur"],
        ["Sungei Wang Plaza", "Central", "Kuala Lumpur"],
        ["Mid Valley Megamall", "Central", "Kuala Lumpur"],
        ["Bangsar Shopping Centre", "Central", "Kuala Lumpur"],
        ["One Utama", "Central", "Selangor"],
        ["Sunway Pyramid Shopping Mall", "Central", "Selangor"],
        ["Sunway Giza Mall", "Central", "Selangor"],
        ["Queensbay Mall", "North", "Penang"],
        [" Gurney Plaza", "North", "Penang"],
        ["Johor Bahru City Square", "South", "Johor"],
        ["IOI City Mall", "Central", "Putrajaya"],
        ["Dataran Pahlawan Melaka Megamall", "South", "Malacca"],
        ["Palm Mall", "Central", "Negeri Sembilan"],
        ["Suria Sabah", "Borneo", "Sabah"],
        ["Suria Sabah", "Borneo", "Sabah"],
        ["Centre Point Sabah", "Borneo", "Sabah"],
        ["Kota Kinabalu City Waterfront", "Borneo", "Sabah"],
        ["Vivacity Megamall", "Borneo", "Sarawak"],
        ["Genting Highlands Premium Outlets", "East", "Pahang"],
        ["East Coast Mall", "East", "Pahang"],
        ["Ipoh Parade Shopping Centre", "North", "Perak"],
        ["Taiping Sentral Mall", "North", "Perak"],
        ["Financial Park", "Borneo", "Labuan"],
        ["Kota Bharu Mall", "East", "Kelantan"],
        ["KTCC MALL", "East", "Terengganu"],
        ["Aman Central", "North", "Kedah"],
    ]
    payment_type_id = np.arange(1, len(outlet_location) + 1, 1)
    df = pd.DataFrame(outlet_location, columns=["outlet_loation", "region", "state"])
    df = pd.merge(pd.DataFrame(payment_type_id, columns=["outlet_id"]), df, left_index=True, right_index=True)

    return df


# Date table
def create_date():
    df = pd.DataFrame(pd.date_range(start="2021-01-01", end="2024-03-31"), columns=["order_date"])
    df = df.assign(order_date_id=lambda x: (x["order_date"].dt.strftime("%Y-%m-%d").str.replace("-", "")))

    df = df.assign(day_no=lambda x: (x["order_date_id"].str[6:8]).astype(int))
    df = df.assign(day_name=lambda x: (x["order_date"].dt.day_name(locale="English")))

    df = df.assign(month_no=lambda x: (x["order_date_id"].str[4:6]).astype(int))
    df = df.assign(month_name=lambda x: (x["order_date"].dt.month_name(locale="English")))

    df = df.assign(quarter_no=lambda x: (x["order_date"].dt.quarter))
    df = df.assign(quarter_name=lambda x: ("Quarter " + x["quarter_no"].astype(str)))

    df = df.assign(year_no=lambda x: (x["order_date_id"].str[0:4]).astype(int))

    return df


product_df = create_product()
payment_mode_df = create_payment_mode()
outlet_df = create_outlet()
date_df = create_date()

product_df.to_csv("dim_product.csv", index=False)
payment_mode_df.to_csv("dim_payment_mode.csv", index=False)
outlet_df.to_csv("dim_outlet.csv", index=False)
date_df.to_csv("dim_date.csv", index=False)


# Sales table
def create_sales(num_orders):
    product_id_list = product_df["product_id"].to_list()
    payment_mode_id_list = payment_mode_df["payment_mode_id"].to_list()
    outlet_id_list = outlet_df["outlet_id"].to_list()

    orders = []
    for x in range(num_orders):
        outlet_id = np.random.choice(
            outlet_id_list,
            p=[
                0.06,
                0.055,
                0.045,
                0.055,
                0.045,
                0.06,
                0.06,
                0.055,
                0.04,
                0.04,
                0.035,
                0.035,
                0.03,
                0.03,
                0.03,
                0.03,
                0.03,
                0.03,
                0.03,
                0.04,
                0.03,
                0.025,
                0.025,
                0.02,
                0.025,
                0.025,
                0.015,
            ],
        )
        payment_mode_id = np.random.choice(payment_mode_id_list, p=[0.4, 0.35, 0.1, 0.15])

        order_date = fake.date_between_dates(date_start=datetime(2021, 1, 1), date_end=datetime(2024, 3, 31))
        order_date_id = order_date.strftime("%Y-%m-%d").replace("-", "")
        order_time = str(random_time(10, 22))
        order_time_id = order_time.replace(":", "")
        order_id = order_date_id + order_time_id
        order = {
            "order_id": order_id,
            "order_date_id": order_date_id,
            "order_time": order_time,
            "outlet_id": outlet_id,
            "payment_mode_id": payment_mode_id,
        }

        # Each order can have multiple line items
        line_id = 1
        num_products = np.random.randint(1, 5)
        selected_product_id_list = random.sample(product_id_list, num_products)

        for product in selected_product_id_list:
            order["line_id"] = line_id
            order["product_id"] = product
            order["unit_count"] = np.random.randint(1, 9)
            add_order = order.copy()
            orders.append(add_order)
            line_id += 1

    df = pd.DataFrame(orders)
    return df


sales_df = create_sales(1000)
sales_df.to_csv("fact_sales.csv", index=False)
