import pandas as pd
import numpy as np
from copy import deepcopy
import os


def place_spots(spots_lists, time_dict, id_list, spots_list, demo_frame, demo_list,
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
                unplaced_spots.append(current_imps)
            else:
                running_imps_total += current_imps
            if len(unplaced_spots) > aggressive_factor:
                return 80000, len(unplaced_spots)
        else:
            pass

    return running_imps_total, unplaced_spots


def place_placed_spots(spots_frame, id_list, demo_frame, first, time_dict, spots_list):
    running_imps_total = 0
    for x in range(0, len(spots_frame['Length'])):
        if spots_frame.iloc[x][3] != "Not Yet Placed":
            needed_location = id_list.index(int(spots_frame.iloc[x][3]))
            needed_demo = np.where(first == spots_frame.iloc[x][7])[0][0]
            if spots_frame.iloc[x][8] > 0:
                current_imps_deficit = -spots_frame.iloc[x][8] + (
                    demo_frame.iloc[needed_location][needed_demo + 1] * float(spots_frame.iloc[x][6]))
            else:
                current_imps_deficit = 0
            spots_list[needed_location].append(
                (spots_frame.iloc[x][2], spots_frame.iloc[x][10], str(spots_frame.iloc[x][1]) + '**',
                 spots_frame.iloc[x][6],
                 str(round(current_imps_deficit, 2))))
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
            if imps > 0:
                current_imps_deficit = round(-imps +
                                             (demo_data_frame.iloc[potentials][current_index] * float(length_of_spot)),
                                             2)
            else:
                current_imps_deficit = 0
            spots_lists[current_location].append(
                (advertiser.strip(), product.strip(), spot_id, length_of_spot, str(current_imps_deficit)))
            # Figure out the impressions difference and add it to the running total
            demo_data_frame.sort_index(inplace=True)
            return current_imps_deficit
        elif potentials < len(id_list) - 1:
            pass
        else:
            demo_data_frame.sort_index(inplace=True)
            return advertiser.strip()


def get_sum(running_imps):
    counter = 0
    for imps in running_imps:
        if imps != 80000:
            counter += imps
    return counter


def start(spots_lists, time_dict, id_list, spots_frame, demo_frame, demo_list, trial, after_placed_imps_shortfall,
          aggressive_factor):
    running_imps = place_spots(spots_lists, time_dict, id_list, spots_frame, demo_frame, demo_list, trial,
                               False, after_placed_imps_shortfall, aggressive_factor)

    # absRunningImps = [abs(number) for number in running_imps]
    # positiveornegative = get_sum(running_imps)
    # if positiveornegative < 0:
    # returned_number = min(absRunningImps) * -1
    # else:
    #     returned_number = min(absRunningImps)
    #
    # unplaced_spots = pd.Series(
    #     place_spots(spots_lists, time_dict, id_list, spots_frame, demo_frame, demo_list, running_imps,
    #                 absRunningImps.index(min(absRunningImps)), True, after_placed_imps_shortfall, aggressive_factor))
    #


    return trial, running_imps[0]


def finish(spots_lists, time_dict, id_list, spots_frame, demo_frame, demo_list, trial, after_placed_imps_shortfall,
           aggressive_factor, ratings_path, daypart):
    # absRunningImps = [abs(number) for number in running_imps]
    # positiveornegative = get_sum(running_imps)
    # if positiveornegative < 0:
    # returned_number = min(absRunningImps) * -1
    # else:
    #     returned_number = min(absRunningImps)

    unplaced_spots = pd.Series(
        place_spots(spots_lists, time_dict, id_list, spots_frame, demo_frame, demo_list,
                    trial, True, after_placed_imps_shortfall, aggressive_factor))

    # Save the resulting list to a csv file for placing
    os.chdir(ratings_path)
    os.chdir('../Completed')
    final_spots = pd.DataFrame(spots_lists)
    final_spots = final_spots.transpose()
    final_spots['Unplaced'] = unplaced_spots
    final_spots.to_csv(daypart + '.csv')

    return unplaced_spots[0], len(unplaced_spots[1])