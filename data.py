import numpy as np
import pandas as pd
import random
import math
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
    product_data = [
        ["Espresso", 700],
        ["Double Espresso", 1200],
        ["Americano", 800],
        ["Long Black", 800],
        ["Macchiato", 900],
        ["Cappuccino", 1100],
        ["Flat White", 1300],
        ["Cafe Latte", 1100],
        ["Mocha", 1200],
    ]
    product_id = np.arange(1, len(product_data) + 1, 1)
    df = pd.DataFrame(product_data, columns=["product_name", "price"])
    df = pd.merge(pd.DataFrame(product_id, columns=["product_id"]), df, left_index=True, right_index=True)

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
    outlet_data = [
        ["Pavilion KL", "Central", "Kuala Lumpur"],
        ["The Gardens Mall", "Central", "Kuala Lumpur"],
        ["Sungei Wang Plaza", "Central", "Kuala Lumpur"],
        ["Mid Valley Megamall", "Central", "Kuala Lumpur"],
        ["Bangsar Shopping Centre", "Central", "Kuala Lumpur"],
        ["One Utama", "Central", "Selangor"],
        ["Sunway Pyramid Shopping Mall", "Central", "Selangor"],
        ["Sunway Giza Mall", "Central", "Selangor"],
        ["Queensbay Mall", "North", "Penang"],
        ["Gurney Plaza", "North", "Penang"],
        ["Johor Bahru City Square", "South", "Johor"],
        ["IOI City Mall", "Central", "Putrajaya"],
        ["Dataran Pahlawan Melaka Megamall", "South", "Malacca"],
        ["Palm Mall", "Central", "Negeri Sembilan"],
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
    payment_type_id = np.arange(1, len(outlet_data) + 1, 1)
    df = pd.DataFrame(outlet_data, columns=["outlet_location", "region", "state"])
    df = pd.merge(pd.DataFrame(payment_type_id, columns=["outlet_id"]), df, left_index=True, right_index=True)

    return df


# Date table
def create_date():
    df = pd.DataFrame(pd.date_range(start="2022-01-01", end="2024-03-31"), columns=["order_date"])
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

    order_date_list = date_df[["order_date", "order_date_id", "day_name"]].values.tolist()[:31]
    product_id_list = product_df["product_id"].to_list()
    payment_mode_id_list = payment_mode_df["payment_mode_id"].to_list()
    outlet_list = outlet_df[["outlet_id", "outlet_location"]].values.tolist()
    orders = []
    order_id = 1
    for date in order_date_list:
        order_factor = 1
        order_noise_factor = round(np.random.randint(-10, 10) / 100, 1)
        match date[2]:
            case "Friday":
                order_factor = order_factor + 0.2
            case "Saturday":
                order_factor = order_factor + 0.5
            case "Sunday":
                order_factor = order_factor + 0.3
            case _:
                order_factor = order_factor

        for outlet in outlet_list:
            outlet_noise_factor = round(np.random.randint(-10, 10) / 100, 1)
            match outlet[1]:
                case "Pavillion KL":
                    outlet_factor = 2
                case "The Gardens Mall":
                    outlet_factor = 1.6
                case "Sungei Wang Plaza":
                    outlet_factor = 0.7
                case "Mid Valley Megamall":
                    outlet_factor = 1.5
                case "Bangsar Shopping Centre":
                    outlet_factor = 1.1
                case "One Utama":
                    outlet_factor = 2
                case "Sunway Pyramid Shopping Mall":
                    outlet_factor = 1.9
                case "Sunway Giza Mall":
                    outlet_factor = 1.2
                case "Queensbay Mall":
                    outlet_factor = 1.4
                case "Gurney Plaza":
                    outlet_factor = 1.2
                case "Johor Bahru City Square":
                    outlet_factor = 1.1
                case "IOI City Mall":
                    outlet_factor = 1.1
                case "Dataran Pahlawan Melaka Megamall":
                    outlet_factor = 0.8
                case "Palm Mall":
                    outlet_factor = 0.7
                case "Kota Kinabalu City Waterfront":
                    outlet_factor = 1.1
                case "Vivacity Megamall":
                    outlet_factor = 0.9
                case "Genting Highlands Premium Outlets":
                    outlet_factor = 1.7
                case "East Coast Mall":
                    outlet_factor = 1.1
                case "Ipoh Parade Shopping Centre":
                    outlet_factor = 1.2
                case "Taiping Sentral Mall":
                    outlet_factor = 0.8
                case "Financial Park":
                    outlet_factor = 0.6
                case "Kota Bharu Mall":
                    outlet_factor = 0.5
                case "KTCC MALL":
                    outlet_factor = 0.7
                case "Aman Central":
                    outlet_factor = 0.6
                case _:
                    outlet_factor = 1
            num_orders_adjusted = math.floor(
                num_orders * (order_factor + order_noise_factor) * (outlet_factor + outlet_noise_factor)
            )
            for x in range(num_orders_adjusted):
                # Each order can have multiple products, each represented by a line item
                payment_mode_id = np.random.choice(payment_mode_id_list, p=[0.4, 0.35, 0.1, 0.15])
                order_date_id = int(date[0].strftime("%Y-%m-%d").replace("-", ""))
                order_time = str(random_time(10, 22))
                order = {
                    "order_id": order_id,
                    "order_date_id": order_date_id,
                    "order_time": order_time,
                    "outlet_id": outlet[0],
                    "payment_mode_id": payment_mode_id,
                }
                line_id = 1
                num_product_choices = [1, 2, 3, 4, 5, 6, 7, 8]
                assert len(num_product_choices) <= len(product_id_list)
                num_products = np.random.choice(
                    num_product_choices, p=[0.65, 0.1, 0.03, 0.1, 0.01, 0.05, 0.01, 0.05]
                )  # 1 to 4 products per order

                selected_product_id_list = np.random.choice(
                    product_id_list,
                    size=num_products,
                    replace=False,
                    p=[0.08, 0.02, 0.13, 0.12, 0.1, 0.1, 0.18, 0.17, 0.1],
                )
                for product in selected_product_id_list:
                    order["line_id"] = line_id
                    order["product_id"] = product
                    order["unit_count"] = np.random.randint(1, 4)  # 1 to 3 units per product
                    unit_price = product_df[product_df["product_id"] == product]["price"].iloc[0]
                    order["gross_total_sales"] = order["unit_count"] * unit_price

                    discount_choices = np.arange(0, 0.41, 0.05)
                    discount_percentage = np.random.choice(
                        discount_choices,
                        p=[
                            0.6,
                            0,
                            0.25,
                            0.06,
                            0.04,
                            0.02,
                            0.02,
                            0,
                            0.01,
                        ],
                    )
                    order["discount"] = math.floor(discount_percentage * order["gross_total_sales"])
                    order["net_total_sales"] = int(order["gross_total_sales"] - order["discount"])
                    add_order = order.copy()
                    orders.append(add_order)
                    line_id += 1
                order_id += 1

    df = pd.DataFrame(orders)
    cols = [
        "order_id",
        "line_id",
        "order_date_id",
        "order_time",
        "payment_mode_id",
        "outlet_id",
        "product_id",
        "unit_count",
        "gross_total_sales",
        "discount",
        "net_total_sales",
    ]
    df = df[cols]

    return df


sales_df = create_sales(50)
sales_df.to_csv("fact_sales.csv", index=False)
