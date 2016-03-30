import pandas as pd
from itertools import repeat
import numpy as np
from Demo_List_Names import sum_dict_names
from Preempt_Credit import preempt_credit_names
from Ratings_Import import import_ratings
from copy import deepcopy


def convert_to_seconds(time):
    return int(time.split(":")[1]) if time.split(":")[0] == "" else int(time.split(":")[0]) * 60 + int(
        time.split(":")[1])


def place_spots(spots_lists, time_dict, id_list, spots_list, demo_frame, demo_list, running_imps,
                random_trial, keep_imps, after_placed_imps, aggressive_factor):
    np.random.seed(random_trial)
    spots_list['Random'] = np.random.uniform(0.0, 10.0, len(spots_list))
    spots_list = spots_list.sort_values('Random', ascending=False)
    # [0][0] - Imps  [0][1] - Advertiser  [0][2] - Demo  [0][3] - Length
    running_imps_total = after_placed_imps
    unplaced_spots = []

    # Find the best available place for each spot in the dataframe
    for x in range(0, len(spots_list['Length'])):
        if spots_list.iloc[x][3] == "Not Yet Placed":
            current_imps = find_best_fit(spots_lists, time_dict, id_list, demo_frame, spots_list.iloc[x][7],
                                         spots_list.iloc[x][6],
                                         spots_list.iloc[x][2], spots_list.iloc[x][8], spots_list.iloc[x][1],
                                         demo_list, False, spots_list.iloc[x][10])
            if isinstance(current_imps, str) and keep_imps:
                unplaced_spots.append(current_imps)
            elif isinstance(current_imps, str):
                pass
            else:
                running_imps_total += current_imps
        else:
            pass
    running_imps.append(running_imps_total - (len(unplaced_spots) * aggressive_factor))
    return unplaced_spots


def place_placed_spots(spots_frame, id_list, demo_frame, first, time_dict, spots_list):
    running_imps_total = 0
    for x in range(0, len(spots_frame['Length'])):
        if spots_frame.iloc[x][3] != "Not Yet Placed":
            needed_location = id_list.index(int(spots_frame.iloc[x][3]))
            needed_demo = np.where(first == spots_frame.iloc[x][7])[0][0]
            current_imps_deficit = -spots_frame.iloc[x][8] + (
                demo_frame.iloc[needed_location][needed_demo + 1] * float(spots_frame.iloc[x][6]))
            spots_list[needed_location].append(
                (spots_frame.iloc[x][2], spots_frame.iloc[x][10], str(spots_frame.iloc[x][1]) + '**', spots_frame.iloc[x][6],
                 round(current_imps_deficit), 2))
            time_dict[int(spots_frame.iloc[x][3])] = time_dict[int(spots_frame.iloc[x][3])] - spots_frame.iloc[x][6]
            running_imps_total += current_imps_deficit
        else:
            pass
    return running_imps_total


def plus_minus(demo_frame, id_list, current_hour, current_demo, current_imps, length):
    return abs(-current_imps + (demo_frame.iloc[id_list.index(current_hour)][current_demo] * float(length)))


def find_best_fit(spots_lists, time_dict, id_list, demo_data_frame, current_spot, length_of_spot, advertiser, imps,
                  spot_id, list_of_demos,
                  best_available, product):
    # Sort passed dataframe by the appropriate demo if best_available is True
    if best_available:
        demo_data_frame = demo_data_frame.sort_values(current_spot, ascending=False)
    else:
        demo_data_frame['+/-'] = demo_data_frame.apply(lambda x:
                                                       plus_minus(demo_data_frame, id_list, x['ID'], current_spot, imps,
                                                                  length_of_spot), axis=1)
        demo_data_frame.sort_values(['+/-'], ascending=True, inplace=True)

    current_index = list_of_demos.index(current_spot) + 1
    # Find the string of the show name that has the highest demo
    # current_show = str(demo_data_frame.loc[demo_data_frame[current_spot].idxmax()][0])
    for potentials in range(0, len(id_list)):
        current_show = demo_data_frame.iloc[potentials][0]
        current_location = id_list.index(current_show)
        if len(spots_lists[current_location]) > 2:
            too_many_product = sum(t[1] == product.strip() for t in spots_lists[current_location]) >= 5
        else:
            too_many_product = False
        too_many = sum(t[0] == advertiser.strip() for t in spots_lists[current_location]) >= 2
        # current_imps_deficit = -imps + (demo_data_frame.iloc[potentials][current_index] * float(length_of_spot))
        # Subtract that spots length from that shows current length and
        # see if it has room for one more spot - not going over two
        # I tried not having any positives on any spots, but it was worse.  current_imps_deficit < 0
        if time_dict[current_show] - length_of_spot >= 0 and not too_many and not too_many_product:
            time_dict[current_show] = time_dict[current_show] - length_of_spot
            # Find the position in id_list where that show is
            current_location = id_list.index(current_show)
            # Take that location and add to it the current spots information since it should go in that show
            current_imps_deficit = -imps + (demo_data_frame.iloc[potentials][current_index] * float(length_of_spot))
            spots_lists[current_location].append(
                (advertiser.strip(), product.strip(), spot_id, length_of_spot, round(current_imps_deficit, 2)))
            # Figure out the impressions difference and add it to the running total
            return current_imps_deficit
        elif potentials < len(id_list) - 1:
            pass
        else:
            return advertiser.strip()


def start(daypart, number_of_trials, aggressive_factor):
    # Combine Ratings Projection/Actual Files to get the list of actual shows that we can
    # place commercials in
    frame = import_ratings(daypart)

    # Create a blank dictionary and then fill it with the rows from frame and the number of seconds
    # available for commercials
    time_dict = {}
    id_list = frame['ID'].tolist()
    # Create List Lists that will hold the id_list plus all of the spots (in tuples) that are being
    # placed in that show
    spots_lists = [[] for i in repeat(None, len(id_list))]
    for ids in id_list:
        time_dict[ids] = 780
    for x in range(0, len(id_list)):
        spots_lists[x].append(str(id_list[x]) + ' ')
    spots_frame = preempt_credit_names(daypart)

    first = spots_frame[' Primary Demo'].unique()

    # Here we create a new dataframe that is going to hold all of the used demos and their
    # impressions for each individual demo.
    demo_frame = pd.DataFrame()
    demo_frame['ID'] = frame['ID']
    for demo_cats in first:
        demo_frame[demo_cats] = frame[sum_dict_names[demo_cats]].sum(axis=1) / 30

    demo_list = list(first)

    running_imps = []

    after_placed_imps_shortfall = place_placed_spots(spots_frame, id_list, demo_frame, first, time_dict,
                                                     spots_lists)


    starter_spots_list = deepcopy(spots_lists)

    for trial in range(0, number_of_trials):

        place_spots(spots_lists, time_dict, id_list, spots_frame, demo_frame, demo_list, running_imps,
                    trial, True, after_placed_imps_shortfall, aggressive_factor)


        spots_lists = deepcopy(starter_spots_list)
        for ids in id_list:
            time_dict[ids] = 780



    unplaced_spots = pd.Series(
        place_spots(spots_lists, time_dict, id_list, spots_frame, demo_frame, demo_list, running_imps,
                    running_imps.index(max(running_imps)), True, after_placed_imps_shortfall, aggressive_factor))


    # Save the resulting list to a csv file for placing
    final_spots = pd.DataFrame(spots_lists)
    final_spots = final_spots.transpose()
    final_spots['Unplaced'] = unplaced_spots
    final_spots.to_csv('output.csv')

    returned_list = [max(running_imps), len(unplaced_spots)]

    return returned_list


