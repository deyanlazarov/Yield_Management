__author__ = '143740'
import pandas as pd
import time

# TODO - Deal with DR


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


def assign_day_part(day_number, start_hour):
    day_part = ""
    if day_number >= 6 and start_hour < 20:
        day_part = "Weekend"
    elif start_hour == 20:
        day_part = "Prime 1"
    elif start_hour < 15:
        day_part = "Daytime"
    elif start_hour < 18:
        day_part = "Early Fringe"
    elif start_hour < 20:
        day_part = "Prime Access"
    else:
        day_part = "Prime 2"
    return day_part


def prepare_frame(current_frame, daypart):
    list_of_desired_columns = ['Air Date', 'Spot ID', 'Advertiser', 'Hit Time', 'Start Time', 'End Time',
                                'Length', ' Primary Demo', 'Unit Cost', 'Proposal Qtr. CPM', 'Primary Product Category']
    current_frame = current_frame[list_of_desired_columns]
    current_frame['Length'] = current_frame.apply(lambda x: convert_to_seconds(x['Length']), axis=1)
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
    current_frame['Daypart'] = current_frame.apply(lambda x: assign_day_part(x['Air Date'], x['Start Time']), axis=1)
    current_frame = current_frame.drop(current_frame[current_frame['Daypart'] != daypart].index)
    current_frame.drop('Unit Cost', axis=1, inplace=True)
    current_frame.drop('Proposal Qtr. CPM', axis=1, inplace=True)
    current_frame.reset_index(inplace=True, drop=True)
    military = current_frame['Primary Product Category']
    current_frame.drop(labels=['Primary Product Category'], axis=1, inplace=True)
    current_frame.insert(10, 'Primary Product Category', military)
    current_frame['Derived Imps'].fillna(0, inplace=True)
    current_frame[' Primary Demo'].fillna('M21-34', inplace=True)
    return current_frame


def preempt_credit_names(daypart):
    pd.options.mode.chained_assignment = None
    df = pd.read_csv(r'C:\Users\143740\Desktop\Sunday Spots.csv')
    return prepare_frame(df, daypart)


preempt_credit_names('Daytime')