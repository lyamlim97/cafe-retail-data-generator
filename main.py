import numpy as np
import random
from faker import Faker
from datetime import datetime


from dim_product import create_product
from dim_payment_mode import create_payment_mode
from dim_outlet import create_outlet
from dim_date import create_date

from fact_sales import create_sales
from fact_budget import create_budget


if __name__ == "__main__":
    fake = Faker()
    fake.seed_instance(42)
    np.random.seed(42)
    random.seed(42)

    startTime = datetime.now()

    start_date = "2021-01-01"
    end_date = "2024-03-31"

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

    product_df = create_product()
    payment_mode_df = create_payment_mode()
    outlet_df = create_outlet()
    date_df = create_date(start_date, end_date)

    product_df.to_csv("dim_product.csv", index=False)
    payment_mode_df.to_csv("dim_payment_mode.csv", index=False)
    outlet_df.to_csv("dim_outlet.csv", index=False)
    date_df.to_csv("dim_date.csv", index=False)

    create_sales(100, date_df, product_df, payment_mode_df, outlet_df, hols_flipped)
    create_budget(3000, date_df, product_df, payment_mode_df, outlet_df, hols_flipped)

    print(datetime.now() - startTime)
