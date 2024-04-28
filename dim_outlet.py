import pandas as pd
import numpy as np


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
