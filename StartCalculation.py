__author__ = '143740'

from Ratings_Import import import_ratings
from Preempt_Credit import preempt_credit_names
import pandas as pd
from itertools import repeat
from Demo_List_Names import sum_dict_names
from Start import place_placed_spots
from Start import finish


def start_calculation(daypart, ratings_path, spots_path, default_potential, day, network):
    frame = import_ratings(daypart, ratings_path, network, day)
    id_list = frame['ID'].tolist()
    spots_lists = [[] for i in repeat(None, len(id_list))]
    for x in range(0, len(id_list)):
        spots_lists[x].append(str(id_list[x]) + '  ')
    spots_frame = preempt_credit_names(daypart, spots_path, network)
    first = spots_frame[' Primary Demo'].unique()
    demo_frame = pd.DataFrame()
    demo_frame['ID'] = frame['ID']
    for demo_cats in first:
        demo_frame[demo_cats] = frame[sum_dict_names[demo_cats]].sum(axis=1) / 30

    demo_list = list(first)

    running_imps = []




    time_dict = dict(zip(get_hours_from_daypart(daypart),
                         get_potential_from_daypart(daypart, default_potential, network)))



    after_placed_imps_shortfall = place_placed_spots(spots_frame, id_list, demo_frame, first, time_dict,
                                                     spots_lists)


    returned = finish(spots_lists, time_dict, id_list, spots_frame, demo_frame, demo_list,
                      0, after_placed_imps_shortfall, 50,
                      ratings_path, daypart, day)

    return returned[1]


def get_hours_from_daypart(daypart):
    options = [i for i in range(7, 24)]
    if daypart == "Prime Access":
        hour_options = options[11:13]
    elif daypart == "Morning":
        hour_options = options[:2]
    elif daypart == "Weekend":
        hour_options = options[:13]
    elif daypart == "Weekend Morning":
        hour_options = options[:7]
    elif daypart == "Weekend Day":
        hour_options = options[6:11]
    elif daypart == "Daytime":
        hour_options = options[2:8]
    elif daypart == "Early Fringe":
        hour_options = options[8:11]
    elif daypart == "Prime 1":
        hour_options = options[13:14]
    else:
        hour_options = options[14:]
    return hour_options


def get_potential_from_daypart(daypart, default_potential, network):
    if daypart == "Prime Access":
        hour_options = default_potential[11:13]
    elif daypart == "Morning":
        hour_options = default_potential[:3]
    elif daypart == "Weekend":
        hour_options = default_potential[:13]
    elif daypart == "Weekend Morning":
        hour_options = default_potential[:7]
    elif daypart == "Weekend Day":
        hour_options = default_potential[6:11]
    elif daypart == "Daytime":
        hour_options = default_potential[2:8]
        if network == 0:
            hour_options[0] = hour_options[0]//2
    elif daypart == "Early Fringe":
        hour_options = default_potential[8:11]
    elif daypart == "Prime 1":
        hour_options = default_potential[13:14]
    else:
        hour_options = default_potential[14:]
    return hour_options
