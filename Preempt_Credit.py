__author__ = '143740'
import pandas as pd
import time
import glob
import LiabilityClean
import numpy as np


def convert_to_seconds(current_time):
    return int(current_time.split(":")[2]) if current_time.split(":")[1] == "" else int(
        current_time.split(":")[1]) * 60 + int(
        current_time.split(":")[2])


def convert_to_military(current_time):
    return time.strptime(current_time, "%I:%M:%S %p")[3] if not pd.isnull(current_time) else "Not Yet Placed"


def convert_to_military_string(current_time):
    return str(time.strptime(current_time, "%I:%M:%S %p")[3]) if not pd.isnull(current_time) else "Not Yet Placed"


def convert_to_numeric_day(current_day):
    return time.strptime(current_day, '%m/%d/%Y')[6] + 1


def derived_imps(current_cost, current_CPM):
    return 0 if current_CPM == 0 else current_cost / current_CPM


def assign_day_part(day_number, start_hour, hit_time):
    start_or_hit = int(start_hour) if hit_time == "Not Yet Placed" else int(hit_time)
    day_part = ""
    if day_number >= 6 and int(start_or_hit) < 20:
        day_part = "Weekend"
    elif start_or_hit == 20:
        day_part = "Prime 1"
    elif start_or_hit < 15:
        day_part = "Daytime"
    elif start_or_hit < 18:
        day_part = "Early Fringe"
    elif start_or_hit < 20:
        day_part = "Prime Access"
    else:
        day_part = "Prime 2"
    return day_part

def account_for_vignettes(length, program):
    modifier = 0
    if 'Custom Vignette' in program:
        modifier = 30
    elif 'Custom 60 sec Vignette' in program:
        modifier = 60
    elif 'Intromercial' in program:
        modifier = 15
    return length + modifier


def prepare_frame(current_frame, daypart):
    current_frame = current_frame[(current_frame.MG.isnull() == True) | (current_frame.MG == 'M')]
    current_frame = current_frame[(current_frame.CR != True)]
    list_of_desired_columns = ['Air Date', 'Spot ID', 'Advertiser', 'Hit Time', 'Start Time', 'End Time',
                               'Length', ' Primary Demo', 'Unit Cost', 'Proposal Qtr. CPM', 'Primary Product Category',
                               'Order #', "Program Ordered As"]

    current_frame = current_frame[list_of_desired_columns]
    current_frame['Length'] = current_frame.apply(lambda x: convert_to_seconds(x['Length']), axis=1)
    current_frame['Length'] = current_frame.apply(lambda x: account_for_vignettes(x['Length'], x['Program Ordered As']), axis=1)
    dollar_conversion = ['Unit Cost', 'Proposal Qtr. CPM']
    for dollars in dollar_conversion:
        current_frame[[dollars]] = current_frame[[dollars]].replace('[\$,]', '', regex=True).astype(float)
    military_column_list = ['Start Time', 'End Time']
    for military in military_column_list:
        current_frame[military] = current_frame.apply(lambda x: convert_to_military(x[military]), axis=1)
    current_frame['Hit Time'] = current_frame.apply(lambda x: convert_to_military_string(x['Hit Time']), axis=1)
    current_frame['Air Date'] = current_frame.apply(lambda x: convert_to_numeric_day(x['Air Date']), axis=1)
    current_frame = current_frame.drop(current_frame[current_frame['Start Time'] < 6].index)
    # current_frame = current_frame.drop(current_frame[pd.isnull(current_frame[' Primary Demo'])].index)
    current_frame['Derived Imps'] = current_frame.apply(lambda x: derived_imps(x['Unit Cost'], x['Proposal Qtr. CPM']),
                                                        axis=1)
    current_frame['Daypart'] = current_frame.apply(lambda x: assign_day_part(x['Air Date'], x['Start Time'], x['Hit Time']), axis=1)
    current_frame = current_frame.drop(current_frame[current_frame['Daypart'] != daypart].index)
    if daypart == 'Daytime':
        current_frame = current_frame.drop(current_frame[current_frame['Hit Time'] == '8'].index)
    current_frame.drop('Unit Cost', axis=1, inplace=True)
    current_frame.drop('Proposal Qtr. CPM', axis=1, inplace=True)
    current_frame.reset_index(inplace=True, drop=True)
    list_of_desired_columns = ['Air Date', 'Spot ID', 'Advertiser', 'Hit Time', 'Start Time', 'End Time',
                               'Length', ' Primary Demo', 'Derived Imps', 'Primary Product Category', 'Daypart',
                               'Order #']
    current_frame = current_frame[list_of_desired_columns]
    current_frame['Derived Imps'].fillna(0, inplace=True)
    current_frame[' Primary Demo'].fillna('P25-54', inplace=True)
    current_frame = pd.merge(current_frame, LiabilityClean.combine_liability_and_orders(), left_on='Order #',
                             right_on='Order', how='left')
    current_frame.loc[pd.isnull(current_frame.Order), 'Imps'] = 888888
    current_frame.drop('Order', axis=1, inplace=True)
    current_frame['Imps'].fillna(0, inplace=True)

    all_files = glob.glob('F:\\Traffic Logs\\TRAVEL\\Reports\\' + "/*.csv")
    list_ = []
    for file_ in all_files:
        df = pd.read_csv(file_, index_col=None, header=0)
        list_.append(df)
    products_file = pd.concat(list_)

    current_frame = pd.merge(current_frame, products_file, left_on='Primary Product Category',
                             right_on='Pri. Prod. Category', how='left')

    return current_frame


def preempt_credit_names(daypart, path):
    allFiles = glob.glob(path + "/*.csv")
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_, index_col=None, header=0)
        list_.append(df)
    pd.options.mode.chained_assignment = None
    return prepare_frame(pd.concat(list_), daypart)




