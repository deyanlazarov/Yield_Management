import pandas as pd
import glob

def combine_liability_and_orders(network):
    if network == 2:
        liabilityLocation = 'F:\\Traffic Logs\\TRAVEL\\OptiEdit\\Travel Liability\\' + "/*.csv"
        ordersLocations = 'F:\\Traffic Logs\\TRAVEL\\OptiEdit\\Travel Orders\\' + "/*.csv"
    elif network == 1:
        liabilityLocation = 'F:\\Traffic Logs\\HGTV\\OptiEdit\\HGTV Liability\\' + "/*.csv"
        ordersLocations = 'F:\\Traffic Logs\\HGTV\\OptiEdit\\HGTV Orders\\' + "/*.csv"
    else:
        liabilityLocation = 'F:\\Traffic Logs\\FOOD LOGS\\OptiEdit\\Food Liability\\' + "/*.csv"
        ordersLocations = 'F:\\Traffic Logs\\FOOD LOGS\\OptiEdit\\Food Orders\\' + "/*.csv"
        
    all_files = glob.glob(liabilityLocation)
    list_ = []
    for file_ in all_files:
        df = pd.read_csv(file_, index_col=None, header=0)
        list_.append(df)
    liability_file = pd.concat(list_)

    all_files = glob.glob(ordersLocations)
    list_ = []
    for file_ in all_files:
        df = pd.read_csv(file_, index_col=None, header=0)
        list_.append(df)
    orders_file = pd.concat(list_)



    orders_file = orders_file.merge(liability_file, on="Deal", how="left")
    orders_file.drop('Deal', axis=1, inplace=True)
    return orders_file

