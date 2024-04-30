import os
import csv
import pandas as pd
import math

from dim_outlet import get_outlet_factor


def create_budget(num_cups, date_df, product_df, payment_mode_df, outlet_df, hols_flipped):
    outlet_list = outlet_df[["outlet_id", "outlet_location"]].values.tolist()

    year_month_list = date_df[["order_date", "year_month_id"]].values.tolist()
    year_month_list = date_df["year_month_id"].to_list()
    year_month_list = list(dict.fromkeys(year_month_list))

    product_id_list = product_df["product_id"].to_list()

    # Count how many public holidays per year_month
    hols_year_month_df = pd.DataFrame(hols_flipped[1], columns=["order_date"])
    hols_year_month_df["year_month"] = hols_year_month_df["order_date"].str.replace("-", "").str.slice(0, 6)
    num_hols_per_year_month_df = (
        hols_year_month_df.groupby("year_month")
        .count()
        .reset_index()
        .rename(columns={"order_date": "count"})
        .astype({"year_month": "int64"})
    )

    # Write column names
    cols = [
        "outlet_id",
        "year_month_id",
        "product_id",
        "gross_sales_budget",
        "discount_budget",
        "cost_budget",
        "net_sales_budget",
        "gross_profit_budget",
    ]

    # Delete file if exists
    file = "fact_budget.csv"
    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)
        print("File delete")
    else:
        print("File not found")

    with open(r"fact_budget.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(cols)

    for outlet in outlet_list:
        budgets = []
        outlet_factor = get_outlet_factor(outlet[1])

        for year_month in year_month_list:
            try:
                count = num_hols_per_year_month_df[num_hols_per_year_month_df["year_month"] == year_month][
                    "count"
                ].tolist()[0]
            except:
                count = 0

            holiday_factor = 1 + (count * 0.5)
            for product in product_id_list:
                match product:
                    case 1:
                        product_factor = 0.08
                    case 2:
                        product_factor = 0.02
                    case 3:
                        product_factor = 0.13
                    case 4:
                        product_factor = 0.12
                    case 5:
                        product_factor = 0.1
                    case 6:
                        product_factor = 0.1
                    case 7:
                        product_factor = 0.18
                    case 8:
                        product_factor = 0.17
                    case 9:
                        product_factor = 0.1
                    case _:
                        product_factor = 0.1

                num_cups_adjusted = math.floor(num_cups * outlet_factor * holiday_factor * product_factor)
                budget = {
                    "outlet_id": outlet[0],
                    "year_month_id": year_month,
                    "product_id": product,
                    "gross_sales_budget": num_cups_adjusted * 1000,  # Estimate average 1000 cents per cup
                    "discount_budget": math.floor(num_cups_adjusted * 1000 * 0.05),  # Estimate average 5% discount
                    "cost_budget": num_cups_adjusted * 250,  # Estimate average 250 cents per cup
                }
                budget["net_sales_budget"] = int(budget["gross_sales_budget"] - budget["discount_budget"])
                budget["gross_profit_budget"] = int(budget["net_sales_budget"] - budget["cost_budget"])

                add_budget = budget.copy()
                budgets.append(add_budget)

        for budget in budgets:
            reordered_budget = {col: budget[col] for col in cols}
            val = reordered_budget.values()
            with open(r"fact_budget.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(val)

    return 0
