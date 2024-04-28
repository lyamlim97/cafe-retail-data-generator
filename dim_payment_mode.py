import pandas as pd
import numpy as np


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
