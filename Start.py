import pandas as pd
import numpy as np
import os
import random


def assign_random(imps):
    return random.randrange(-5000, -101) if imps < -100 else imps


def place_spots(spots_lists, time_dict, id_list, spots_list, demo_frame, demo_list,
                random_trial, keep_imps, after_placed_imps, aggressive_factor):

    in_tact = spots_list
    preplace_list = ['Advertiser', 'Primary Product Category']
    high_qualifier = [1.25, 3]
    running_imps_total = after_placed_imps
    unplaced_spots = []

    # Get list of high categories and then loop through the list placing those
    for j in preplace_list:
        l = 0
        spots_list['Frequency'] = spots_list.groupby(j)[j].transform('count')
        highs = spots_list[spots_list['Frequency'] >= (len(time_dict) * high_qualifier[l])]
        l += 1
        high_numbers = list(highs[j].unique())

        for y in high_numbers:
            spots_list = spots_list[spots_list[j] == y]
            spots_list = spots_list.sort_values('Imps', ascending=False)
            # Find the best available place for each spot in the dataframe
            for x in range(0, len(spots_list['Length'])):

                if spots_list.iloc[x][3] == "Not Yet Placed":
                    current_imps = find_best_fit(spots_lists, time_dict, id_list, demo_frame, spots_list.iloc[x][7],
                                                 spots_list.iloc[x][6],
                                                 spots_list.iloc[x][2], spots_list.iloc[x][8], spots_list.iloc[x][1],
                                                 demo_list, False, spots_list.iloc[x][9], spots_list.iloc[x][12],
                                                 spots_list.iloc[x][4], spots_list.iloc[x][5])
                    if isinstance(current_imps, str) and keep_imps:
                        unplaced_spots.append(current_imps)
                    elif isinstance(current_imps, str):
                        unplaced_spots.append(current_imps)
                    else:
                        running_imps_total += current_imps
                    if len(unplaced_spots) > aggressive_factor:
                        return -80000, len(unplaced_spots)
                else:
                    pass

            spots_list = in_tact.drop(in_tact[in_tact[j] == y].index)
            spots_list = spots_list.sort_values('Imps', ascending=False)
            in_tact = spots_list

    spots_list['Imps'] = spots_list.apply(lambda x: assign_random(x['Imps']), axis=1)
    spots_list = spots_list.sort_values('Imps', ascending=False)
    print(spots_list.tail(30))

    for x in range(0, len(spots_list['Length'])):
        if spots_list.iloc[x][3] == "Not Yet Placed":
            current_imps = find_best_fit(spots_lists, time_dict, id_list, demo_frame, spots_list.iloc[x][7],
                                         spots_list.iloc[x][6],
                                         spots_list.iloc[x][2], spots_list.iloc[x][8], spots_list.iloc[x][1],
                                         demo_list, False, spots_list.iloc[x][9], spots_list.iloc[x][12],
                                         spots_list.iloc[x][4], spots_list.iloc[x][5])
            if isinstance(current_imps, str) and keep_imps:
                unplaced_spots.append(current_imps)
            elif isinstance(current_imps, str):
                unplaced_spots.append(current_imps)
            else:
                running_imps_total += current_imps
            if len(unplaced_spots) > aggressive_factor:
                return -80000, len(unplaced_spots)
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
                (spots_frame.iloc[x][2], spots_frame.iloc[x][9], str(spots_frame.iloc[x][1]) + '#',
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
                  best_available, product, imps_deficit_or_surplus, start_time, end_time):
    if (imps_deficit_or_surplus <= 0) or (imps_deficit_or_surplus == 888888.0):
        demo_data_frame = demo_data_frame.sort_values(current_spot, ascending=True)
    else:
        demo_data_frame = demo_data_frame.sort_values(current_spot, ascending=False)

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

        if end_time == 0:
            end_time = 24

        within_time = start_time <= int(current_show) <= end_time
        try:
            previous_hour_total = sum(t[0] == advertiser.strip() for t in spots_lists[current_location - 1])
        except IndexError:
            previous_hour_total = 0

        current_hour_total = sum(t[0] == advertiser.strip() for t in spots_lists[current_location])

        try:
            next_hour_total = sum(t[0] == advertiser.strip() for t in spots_lists[current_location + 1])
        except IndexError:
            next_hour_total = 0

        if (previous_hour_total + current_hour_total > 2) or (current_hour_total + next_hour_total > 2):
            spread_enough = False
        else:
            spread_enough = True

        if time_dict[
            current_show] - length_of_spot >= 0 and not too_many and not too_many_product and within_time and spread_enough:
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

    return trial, running_imps[0]


def finish(spots_lists, time_dict, id_list, spots_frame, demo_frame, demo_list, trial, after_placed_imps_shortfall,
           aggressive_factor, ratings_path, daypart):
    unplaced_spots = place_spots(spots_lists, time_dict, id_list, spots_frame, demo_frame, demo_list,
                                 trial, True, after_placed_imps_shortfall, aggressive_factor)

    # Save the resulting list to a csv file for placing
    os.chdir(ratings_path)
    os.chdir('../Completed')
    final_spots = pd.DataFrame(spots_lists)
    final_spots = final_spots.transpose()
    final_spots['Unplaced'] = pd.Series(unplaced_spots[1])
    final_spots.to_csv(daypart + '.csv')
    return unplaced_spots[0], len(unplaced_spots[1])