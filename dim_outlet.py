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


def get_outlet_factor(outlet_name):
    match outlet_name:
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

    return outlet_factor
