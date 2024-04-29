import csv
import numpy as np
import math

from helper_functions import random_time
from dim_outlet import get_outlet_factor


def create_sales(num_orders, date_df, product_df, payment_mode_df, outlet_df, hols_flipped):
    # Write column names
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

        noise_factor = 1 + round(np.random.randint(-10, 10) / 100, 3)

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
            outlet_factor = get_outlet_factor(outlet[1])

            num_orders_adjusted = math.floor(
                num_orders * weekend_factor * order_factor * outlet_factor * date_factor * holiday_factor * noise_factor
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
