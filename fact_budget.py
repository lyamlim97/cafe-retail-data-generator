import csv
import pandas as pd
import math


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
    with open(r"fact_budget.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(cols)

    for outlet in outlet_list:
        budgets = []

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
        for year_month in year_month_list:
            try:
                count = num_hols_per_year_month_df[num_hols_per_year_month_df["year_month"] == year_month][
                    "count"
                ].tolist()[0]
            except:
                count = 0

            holiday_factor = 1 + (count * 0.5)
            num_products = len(product_id_list)
            for product in product_id_list:
                match product:
                    case 1:
                        product_factor = 0.8
                    case 2:
                        product_factor = 0.2
                    case 3:
                        product_factor = 1.3
                    case 4:
                        product_factor = 1.2
                    case 5:
                        product_factor = 1
                    case 6:
                        product_factor = 1
                    case 7:
                        product_factor = 1.8
                    case 8:
                        product_factor = 1.7
                    case 9:
                        product_factor = 1
                    case _:
                        product_factor = 1

                num_cups_adjusted = (
                    math.floor(num_cups * outlet_factor * holiday_factor * product_factor) / num_products
                )
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
