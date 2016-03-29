__author__ = '143740'
import pandas as pd
import glob
import time
from Preempt_Credit import assign_day_part


def clean_ratings(ratings_frame, daypart):
    ratings_frame.drop_duplicates('Nielsen Program', inplace=True)
    ratings_frame.reset_index(inplace=True, drop=True)
    ratings_frame['ID'] = ratings_frame.apply(lambda x: convert_to_military(x['Start Time']), axis=1)
    ratings_frame.drop(
        ["Start Time", "End Time", "Network Program", "Nielsen Program", "Program Duration", "Commercial Duration",
         "HH"],
        axis=1, inplace=True)
    military = ratings_frame['ID']
    ratings_frame.drop(labels=['ID'], axis=1, inplace=True)
    ratings_frame.insert(0, 'ID', military)
    ratings_frame = ratings_frame.groupby('ID').mean().reset_index()
    ratings_names_list = list(ratings_frame.columns.values)[1:]
    military_list = ratings_frame['ID'].tolist()
    mirror_indexes = [3, 0, 1, 2]
    for i in range(military_list.index(20), military_list.index(23)+1):
        for names in ratings_names_list:
            ratings_frame.set_value(i, names, ratings_frame[names][i] + ratings_frame[names][mirror_indexes[i - military_list.index(20)]])
    ratings_frame.drop([0, 1, 2, 3], inplace=True)
    ratings_frame.reset_index(inplace=True, drop=True)
    weekend = True if ratings_frame['ID'][0] == 7 else False
    ratings_frame['Daypart'] = ratings_frame.apply(lambda row: assign_daypart(weekend, row['ID']), axis=1)
    ratings_frame = ratings_frame.drop(ratings_frame[ratings_frame['Daypart'] != daypart].index)
    return ratings_frame

def convert_to_military(current_time):
    return time.strptime(current_time, "%H:%M:%S")[3]


def assign_daypart(weekend, current_hour):
    if weekend:
        return assign_day_part(6, current_hour)
    else:
        return assign_day_part(5, current_hour)


def import_ratings(daypart):
    path = r'C:\Users\143740\Desktop\Travel Ratings'
    allFiles = glob.glob(path + "/*.csv")
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_, index_col=None, header=0)
        list_.append(df)
    return clean_ratings(pd.concat(list_), daypart)


