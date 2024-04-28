import csv
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

startTime = datetime.now()

start_date = "2021-01-01"
end_date = "2024-03-31"


# Helper functions
def random_time(start, end):
    return timedelta(
        seconds=random.randrange(int(timedelta(hours=start).total_seconds()), int(timedelta(hours=end).total_seconds()))
    )


# Product table
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
    df = pd.DataFrame(pd.date_range(start=start_date, end=end_date), columns=["order_date"])
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
        "total_cost",
        "gross_profit",
    ]
    # Holiday periods
    hols = [
        # extra col on right is for custom holiday factor
        # 2021
        ["New Year's Day 2021", "2021-01-01", ""],
        ["Chinese New Year 2021", "2021-02-12", ""],
        ["Chinese New Year Holiday 2021", "2021-02-13", ""],
        ["Nuzul Al-Quran 2021", "2021-04-29", ""],
        ["Labour Day 2021", "2021-05-01", ""],
        ["Hari Raya Aidilfitri 2021", "2021-05-13", ""],
        ["Hari Raya Aidilfitri Holiday 2021", "2021-05-14", ""],
        ["Wesak 2021", "2021-05-26", ""],
        ["Agong Birthday 2021", "2021-06-07", ""],
        ["Hari Raya Haji 2021", "2021-07-20", ""],
        ["Awal Muharram 2021", "2021-08-10", ""],
        ["Merdeka Day 2021", "2021-08-31", ""],
        ["Malaysia Day 2021", "2021-09-16", ""],
        ["Prophet Muhammad's Birthday 2021", "2021-10-19", ""],
        ["Deepavali 2021", "2021-11-04", ""],
        ["Christmas Day 2021", "2021-12-25", ""],
        # 2022
        ["New Year's Day 2022", "2022-01-01", ""],
        ["CNY 2022", "2022-02-01", ""],
        ["CNY 2022", "2022-02-02", ""],
        ["Nuzul Al-Quran 2022", "2022-04-19", ""],
        ["Labour Day 2022", "2022-05-01", ""],
        ["Hari Raya Aidilfitri 2022", "2022-05-02", ""],
        ["Hari Raya Aidilfitri Holiday 2022", "2022-05-03", ""],
        ["Labour Day Holiday 2022", "2022-05-04", ""],
        ["Wesak Day 2022", "2022-05-15", ""],
        ["Wesak Day Holiday 2022", "2022-05-16", ""],
        ["Agong Birthday 2022", "2022-06-06", ""],
        ["Hari Raya Haji 2022", "2022-07-10", ""],
        ["Hari Raya Haji Holiday 2022", "2022-07-11", ""],
        ["Awal Muharram 2022", "2022-07-30", ""],
        ["Merdeka Day 2022", "2022-08-31", ""],
        ["Malaysia Day 2022", "2022-09-16", ""],
        ["Prophet Muhammad's Birthday 2022", "2022-10-10", ""],
        ["Deepavali 2022", "2021-10-24", ""],
        ["Special Public Holiday (GE15)	2022", "2022-11-18", ""],
        ["Special Public Holiday (GE15)	2022", "2022-11-19", ""],
        ["Special Public Holiday 28 Nov	2022", "2022-11-28", ""],
        ["Christmas Day 2022", "2022-12-25", ""],
        ["Christmas Holiday 2022", "2022-12-26", ""],
        # 2023
        ["New Year's 2023", "2023-01-01", ""],
        ["New Year Holiday 2023", "2023-01-02", ""],
        ["Chinese New Year 2023", "2023-01-22", ""],
        ["Chinese New Year Holiday 2023", "2023-01-23", ""],
        ["Chinese New Year Holiday 2023", "2023-01-24", ""],
        ["Nuzul Al-Quran 2023", "2023-04-08", ""],
        ["Hari Raya Aidilfitri Holiday 2023", "2023-04-21", ""],
        ["Hari Raya Aidilfitri 2023", "2023-04-22", ""],
        ["Hari Raya Aidilfitri Holiday 2023", "2023-04-23", ""],
        ["Hari Raya Aidilfitri Holiday 2023", "2023-04-24", ""],
        ["Labour Day 2023", "2023-05-01", ""],
        ["Wesak Day 2023", "2023-05-04", ""],
        ["Agong's Birthday 2023", "2023-06-05", ""],
        ["Awal Muharram 2023", "2023-07-19", ""],
        ["Merdeka Day 2023", "2023-08-31", ""],
        ["Malaysia Day 2023", "2023-09-16", ""],
        ["Prophet Muhammad's Birthday 2023", "2023-09-28", ""],
        ["Deepavali 2023", "2023-10-12", ""],
        ["Deepavali Holiday 2023", "2023-10-13", ""],
        ["Christmas Day 2023", "2023-12-25", ""],
        # 2024
        ["New Year's Day 2024", "2024-01-01", ""],
        ["Chinese New Year 2024", "2024-02-10", ""],
        ["Chinese New Year Holiday 2024", "2024-02-11", ""],
        ["Chinese New Year Holiday 2024", "2024-02-12", ""],
        ["Nuzul Al-Quran 2024", "2024-03-28", ""],
        ["Hari Raya Aidilfitri 2024", "2024-04-10", ""],
        ["Hari Raya Aidilfitri Holiday 2024", "2024-04-11", ""],
        ["Labour Day 2024", "2024-05-01", ""],
        ["Wesak Day 2024", "2024-05-22", ""],
        ["Agong's Birthday 2024", "2024-06-03", ""],
        ["Hari Raya Haji 2024", "2024-06-17", ""],
        ["Awal Muharram 2024", "2024-07-07", ""],
        ["Awal Muharram Holiday 2024", "2024-07-08", ""],
        ["Merdeka Day 2024", "2024-08-31", ""],
        ["Prophet Muhammad's Birthday 2024", "2024-09-16", ""],
        ["Malaysia Day 2024", "2024-09-16", ""],
        ["Malaysia Day Holiday 2024", "2024-09-17", ""],
        ["Deepavali 2024", "2024-10-31", ""],
        ["Christmas Day 2024", "2024-12-25", ""],
    ]

    # Flip hols list of lists
    hols_flipped = [list(x) for x in zip(*hols)]

    # Check all are valid dates
    for h in hols_flipped[1]:
        try:
            datetime.strptime(h, "%Y-%m-%d")
        except:
            print("Invalid date")

    # Write column names
    with open(r"fact_sales.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(cols)

    order_date_list = date_df[["order_date", "order_date_id", "day_name"]].values.tolist()
    product_id_list = product_df["product_id"].to_list()
    payment_mode_id_list = payment_mode_df["payment_mode_id"].to_list()
    outlet_list = outlet_df[["outlet_id", "outlet_location"]].values.tolist()
    order_id = 1
    initial_date = order_date_list[0][0]
    for date in order_date_list:

        date_diff = (date[0] - initial_date).days
        date_factor = 1 + (0.0005 * date_diff)

        order_factor = 1
        order_noise_factor = round(np.random.randint(-5, 5) / 1000, 3)

        weekend_noise_factor = round(np.random.randint(-10, 10) / 100, 3)

        if date in hols_flipped[1]:
            holiday_factor = 1.5
            weekend_factor = 1
        else:
            holiday_factor = 1
            # Only apply if not public holiday
            match date[2]:
                case "Friday":
                    weekend_factor = 1.2
                case "Saturday":
                    weekend_factor = 1.5
                case "Sunday":
                    weekend_factor = 1.3
                case _:
                    weekend_factor = 1

        for outlet in outlet_list:
            orders = []

            outlet_noise_factor = round(np.random.randint(-10, 10) / 100, 1)
            match outlet[1]:
                case "Pavilion KL":
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
                num_orders
                * (weekend_factor + weekend_noise_factor)
                * (order_factor + order_noise_factor)
                * (outlet_factor + outlet_noise_factor)
                * date_factor
                * holiday_factor
            )
            for n in range(num_orders_adjusted):
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
                    order["unit_count"] = np.random.choice([1, 2, 3], p=[0.85, 0.1, 0.05])  # 1 to 3 units per product
                    unit_price = product_df[product_df["product_id"] == product]["price"].iloc[0]
                    unit_cost = product_df[product_df["product_id"] == product]["cost"].iloc[0]
                    order["gross_total_sales"] = order["unit_count"] * unit_price
                    order["total_cost"] = order["unit_count"] * unit_cost

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
                    order["gross_profit"] = int(order["net_total_sales"] - order["total_cost"])

                    add_order = order.copy()
                    orders.append(add_order)
                    line_id += 1
                order_id += 1

            # Write data for one outlet at a time
            for order in orders:
                reordered_order = {col: order[col] for col in cols}
                val = reordered_order.values()
                with open(r"fact_sales.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(val)
    return 0


create_sales(100)

print(datetime.now() - startTime)
