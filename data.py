import numpy as np
import pandas as pd


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
        ["Johor Bahru City Square", "South", "Johor"],
        ["Aman Central", "North", "Kedah"],
        ["Kota Bharu Mall", "East", "Kelantan"],
        ["Dataran Pahlawan Melaka Megamall", "South", "Malacca"],
        ["Palm Mall", "Central", "Negeri Sembilan"],
        ["Genting Highlands Premium Outlets", "East", "Pahang"],
        ["East Coast Mall", "East", "Pahang"],
        ["Queensbay Mall", "North", "Penang"],
        [" Gurney Plaza", "North", "Penang"],
        ["Ipoh Parade Shopping Centre", "North", "Perak"],
        ["Taiping Sentral Mall", "North", "Perak"],
        ["Suria Sabah", "Borneo", "Sabah"],
        ["Suria Sabah", "Borneo", "Sabah"],
        ["Centre Point Sabah", "Borneo", "Sabah"],
        ["Kota Kinabalu City Waterfront", "Borneo", "Sabah"],
        ["Vivacity Megamall", "Borneo", "Sarawak"],
        ["One Utama", "Central", "Selangor"],
        ["Sunway Pyramid Shopping Mall", "Central", "Selangor"],
        ["Sunway Giza Mall", "Central", "Selangor"],
        ["KTCC MALL", "East", "Terengganu"],
        ["Pavilion KL", "Central", "Kuala Lumpur"],
        ["The Gardens Mall", "Central", "Kuala Lumpur"],
        ["Sungei Wang Plaza", "Central", "Kuala Lumpur"],
        ["Mid Valley Megamall", "Central", "Kuala Lumpur"],
        ["Bangsar Shopping Centre", "Central", "Kuala Lumpur"],
        ["Financial Park", "Borneo", "Labuan"],
        ["IOI City Mall", "Central", "Putrajaya"],
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
