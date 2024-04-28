import pandas as pd


def create_date(start_date, end_date):
    df = pd.DataFrame(pd.date_range(start=start_date, end=end_date), columns=["order_date"])
    df = df.assign(order_date_id=lambda x: (x["order_date"].dt.strftime("%Y-%m-%d").str.replace("-", "")))

    df = df.assign(day_no=lambda x: (x["order_date_id"].str[6:8]).astype(int))
    df = df.assign(day_name=lambda x: (x["order_date"].dt.day_name(locale="English")))

    df = df.assign(month_no=lambda x: (x["order_date_id"].str[4:6]).astype(int))
    df = df.assign(month_name=lambda x: (x["order_date"].dt.month_name(locale="English")))

    df = df.assign(quarter_no=lambda x: (x["order_date"].dt.quarter))
    df = df.assign(quarter_name=lambda x: ("Quarter " + x["quarter_no"].astype(str)))

    df = df.assign(year_no=lambda x: (x["order_date_id"].str[0:4]).astype(int))
    df = df.assign(year_month_id=lambda x: (x["order_date_id"].str[0:6]).astype(int))

    return df
