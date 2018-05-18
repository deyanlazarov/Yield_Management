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

def convert_to_minute(current_time):
    return time.strptime(current_time, "%I:%M:%S %p")[3] * 60 + time.strptime(current_time, "%I:%M:%S %p")[4] if not pd.isnull(current_time) else "Not Yet Placed"


def convert_to_numeric_day(current_day):
    return time.strptime(current_day, '%m/%d/%Y')[6] + 1


def derived_imps(current_cost, current_CPM):
    return 0 if current_CPM == 0 else current_cost / current_CPM


def assign_day_part(day_number, start_hour, hit_time, network):
    start_or_hit = int(start_hour) if hit_time == "Not Yet Placed" else int(hit_time)
    day_part = ""
    if network % 2 == 0:
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
    else:
        if day_number >= 6 and int(start_or_hit) < 13:
            day_part = "Weekend Morning"
        elif day_number >= 6 and int(start_or_hit) < 18:
            day_part = "Weekend Day"
        elif start_or_hit == 20:
            day_part = "Prime 1"
        elif start_or_hit < 15 and start_or_hit >= 9:
            day_part = "Daytime"
        elif start_or_hit < 18 and start_or_hit >=15:
            day_part = "Early Fringe"
        elif start_or_hit < 20 and start_or_hit >= 18:
            day_part = "Prime Access"
        elif start_or_hit < 9:
            day_part = "Morning"
        else:
            day_part = "Prime 2"
    return day_part

def account_for_vignettes(length, program):
    modifier = 0
    if 'Custom Vignettes (pp)' in program:
        modifier = 0
    elif 'Custom Vignette' in program:
        modifier = 30
    elif 'Custom 60 sec Vignette' in program:
        modifier = 60
    elif 'Intromercial' in program:
        modifier = 15
    elif 'Custom Vignettes (:15 Adj)' in program:
        modifier = 30
    elif 'Custom Vignettes (:30 Adj)' in program:
        modifier = 30
    elif 'Custom :60 sec Vigs' in program:
        modifier = 60
    return length + modifier


def prepare_frame(current_frame, daypart, network, liability_file):
    current_frame['MG'].fillna('', inplace=True)
    current_frame = current_frame[(current_frame.MG == '') | (current_frame.MG == 'M')]
    current_frame = current_frame[(current_frame.CR != True)]
    current_frame = current_frame[(current_frame.Category == 'Vignette') | (current_frame.Category == "Commercial")]
    current_frame = current_frame[(current_frame.Category == 'Commercial') | (current_frame['Ordered As Title'].str.startswith("Custom Vignettes (pp)"))]
    list_of_desired_columns = ['Air Date', 'Spot Id', 'Advertiser', 'Hit Time', 'Start Time', 'End Time',
                               'Length', 'Primary Demo', 'Unit Cost', 'Primary Demo CPM', 'Primary Product Category',
                               'Order', 'Ordered As Title']



    current_frame = current_frame[list_of_desired_columns]
    current_frame['Length'] = current_frame.apply(lambda x: convert_to_seconds(x['Length']), axis=1)
    current_frame['Length'] = current_frame.apply(lambda x: account_for_vignettes(x['Length'], x['Ordered As Title']), axis=1)
    dollar_conversion = ['Unit Cost', 'Primary Demo CPM']
    for dollars in dollar_conversion:
        current_frame[[dollars]] = current_frame[[dollars]].replace('[\$,]', '', regex=True).astype(float)
    military_column_list = ['Start Time', 'End Time']
    for military in military_column_list:
        current_frame[military] = current_frame.apply(lambda x: convert_to_military(x[military]), axis=1)
    # current_frame['Hit Time Minute'] = current_frame.apply(lambda x: convert_to_minute(x['Hit Time']), axis=1)
    current_frame['Hit Time'] = current_frame.apply(lambda x: convert_to_military_string(x['Hit Time']), axis=1)
    current_frame['Air Date'] = current_frame.apply(lambda x: convert_to_numeric_day(x['Air Date']), axis=1)
    current_frame = current_frame.drop(current_frame[current_frame['Start Time'] < 6].index)
    # current_frame = current_frame.drop(current_frame[pd.isnull(current_frame[' Primary Demo'])].index)
    current_frame['Derived Imps'] = current_frame.apply(lambda x: derived_imps(x['Unit Cost'], x['Primary Demo CPM']),
                                                        axis=1)
    current_frame['Daypart'] = current_frame.apply(lambda x: assign_day_part(x['Air Date'], x['Start Time'], x['Hit Time'], network), axis=1)
    current_frame = current_frame.drop(current_frame[current_frame['Daypart'] != daypart].index)
    current_frame = current_frame.drop(current_frame[current_frame['Hit Time'] == '6'].index)
    if daypart == 'Daytime':
        current_frame = current_frame.drop(current_frame[current_frame['Hit Time'] == '8'].index)
    current_frame.drop('Unit Cost', axis=1, inplace=True)
    current_frame.drop('Primary Demo CPM', axis=1, inplace=True)
    current_frame.reset_index(inplace=True, drop=True)
    list_of_desired_columns = ['Air Date', 'Spot Id', 'Advertiser', 'Hit Time', 'Start Time', 'End Time',
                               'Length', 'Primary Demo', 'Derived Imps', 'Primary Product Category', 'Daypart',
                               'Order']
    current_frame = current_frame[list_of_desired_columns]
    current_frame['Derived Imps'].fillna(0, inplace=True)
    current_frame['Primary Demo'].fillna('P25-54', inplace=True)

    current_frame = pd.merge(current_frame, liability_file, left_on='Order',
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
    current_frame['Grouped Category'].fillna('Various', inplace=True)

    return current_frame


def preempt_credit_names(daypart, path, network, liability_file):
    allFiles = glob.glob(path + "/*.csv")
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_, index_col=None, header=0)
        list_.append(df)
    pd.options.mode.chained_assignment = None
    return prepare_frame(pd.concat(list_), daypart, network, liability_file)




