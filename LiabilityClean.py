import pandas as pd
import glob
from datetime import datetime
from math import ceil
from GetDataFromServer import getDataForOrders


def combine_liability_and_orders(network):
    path = r'F:\Scripps Networks\Pricing & Planning\Ad Sales\Daily Stewardship Runs'
    if network == 2:
        liabilityLocation = path + "\\TRAVEL_DPS THRU " + get_quarter() + "*.csv"
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

    liability_file = liability_file[['Master Deal', 'Deal', 'Variance +/- Imps (000)']]
    liability_file.columns = ['MDeal', 'Deal', 'Variance']
    liability_file.Deal = liability_file.Deal.str[0:8].astype(int)
    liability_file.Variance = liability_file.Variance.str.replace(',', '').astype(float)
    liability_file['Variance'] = liability_file.groupby('MDeal')['Variance'].transform('sum') * -1
    liability_file = liability_file[['MDeal', 'Variance']].drop_duplicates()
    liability_file.columns = ['Deal', 'Imps']

    # all_files = glob.glob(ordersLocations)
    # list_ = []
    # for file_ in all_files:
    #     df = pd.read_csv(file_, index_col=None, header=0)
    #     list_.append(df)
    # orders_file = pd.concat(list_)

    orders_file = getDataForOrders(8).merge(liability_file, on="Deal", how="left")

    orders_file.drop('Deal', axis=1, inplace=True)
    orders_file.columns = ['Order', 'Imps']
    return orders_file


def get_quarter():
    return str(ceil(datetime.now().month / 3)) + 'Q'
