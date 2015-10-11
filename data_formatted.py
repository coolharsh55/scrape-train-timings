
from itertools import chain
from json import load
from json import dump
import time


def load_from_file(filename):
    """load json data from filename.json"""
    with open(filename + '.json', 'r') as f:
        data = load(f)

    return data


def make_station_list(data):
    """make station name list from given json data"""
    assert type(data) == dict

    station_list = []
    for i in range(0, len(data.keys())):
        station_list.append(data[str(i)])

    return station_list


def normalize_avg(averages):
    """normalize the averages through splicing"""
    averages = averages[1:]
    averages.append(0)
    return averages


def make_station_averages(stations, up_averages, down_averages):
    """create station objects containing time averages for
    next and previous stations"""
    assert type(stations) == list
    assert type(up_averages) == list
    assert type(down_averages) == list

    station_objects = []
    for index, name in enumerate(stations):
        time_to_next = up_averages[index]
        time_to_prev = down_averages[len(stations) - index - 1]
        station_objects.append({
            'name': name,
            'time_next': time_to_next,
            'time_prev': time_to_prev,
        })

    return station_objects


def make_trains(data):
    """create train lists from given json data"""
    assert type(data) == dict

    train_lists = []
    for i in range(0, len(data.keys())):
        train_lists.append(data[str(i)])

    for train_list in train_lists:
        for index, value in enumerate(train_list):
            if value == 'XX:XX':
                train_list[index] = None
            else:
                stop_time = time.strptime(value, '%H:%M')
                # time_struct format - 3: hour 4: minutes
                stop_time = stop_time[3] * 60 + stop_time[4]
                train_list[index] = stop_time

    return train_lists


def make_train_objects(train_lists):
    """make train objects with station and timing info"""
    train_objects = []
    for train_list in train_lists:
        for index, timing in enumerate(train_list):
            if timing is not None:
                departure = timing
                origin_index = index
                break
        for index, timing in enumerate(reversed(train_list)):
            if timing is not None:
                destination_index = len(train_list) - index - 1
                break
        train_objects.append({
            'departure_time': departure,
            'origin_station': origin_index,
            'destination_station': destination_index,
        })

    return train_objects


def normalize_down_trains(down_train_objects, station_nos):
    """normalize down train objects into uniform format as up trains"""
    train_objects = []
    for train_object in down_train_objects:
        departure = train_object['departure_time']
        origin_index = train_object['origin_station']
        destination_index = train_object['destination_station']
        train_objects.append({
            'departure_time': departure,
            'origin_station': station_nos - 1 - origin_index,
            'destination_station': station_nos - 1 - destination_index,
        })

    return train_objects


def make_timing_objects(station_objects, train_objects):
    """make timings for every train"""
    timing_objects = []
    for index, train in enumerate(train_objects):
        departure = train['departure_time']
        origin_index = train['origin_station']
        destination_index = train['destination_station']

        if origin_index < destination_index:
            # up train
            stop_time = lambda index: station_objects[index]['time_next']
        else:
            # down train
            stop_time = lambda index: station_objects[index]['time_prev']
            origin_index, destination_index = destination_index, origin_index

        timing_object = []
        train_time = departure
        for station in range(0, len(station_objects)):
            if station < origin_index or station > destination_index:
                train_time = None
            elif station == origin_index:
                train_time = departure
            else:
                train_time += stop_time(station)
            timing_object.append({
                'station': station,
                'train': index,
                'timing': train_time,
            })

        timing_objects.append(timing_object)

    return timing_objects


def run():
    """run script with default bindings"""
    data = load_from_file('data/up_stations')
    stations = make_station_list(data)

    data = load_from_file('data/up_data')
    up_averages = normalize_avg(data['avg_list'])
    data = load_from_file('data/down_data')
    down_averages = normalize_avg(data['avg_list'])
    station_objects = make_station_averages(
        stations, up_averages, down_averages)

    data = load_from_file('data/up_trains')
    up_trains = make_trains(data)
    up_train_objects = make_train_objects(up_trains)

    data = load_from_file('data/down_trains')
    down_trains = make_trains(data)
    down_train_objects = make_train_objects(down_trains)
    down_train_objects = normalize_down_trains(
        down_train_objects, len(stations))

    train_objects = list(chain(up_train_objects, down_train_objects))

    timing_objects = make_timing_objects(station_objects, train_objects)

    with open('data/data_formatted.json', 'w') as f:
        dump({
            'stations': station_objects,
            'trains': train_objects,
            'timings': timing_objects,
        }, f)

    # mktime = lambda x: str('{0:02}'.format(x // 60)) + \
    #     ':' + str('{0:02}'.format(x % 60))

    # print('STATIONS')
    # for index, value in enumerate(station_objects):
    #     name = value['name']
    #     t_next = value['time_next']
    #     t_prev = value['time_prev']
    #     print('{0:2}: {1:15} :: {2:2} :: {3:2}'.format(
    #         index, name, t_next, t_prev))

    # print('\n\nTRAINS')
    # for index, value in enumerate(train_objects):
    #     departure = value['departure_time']
    #     origin = value['origin_station']
    #     destination = value['destination_station']
    #     print('{0:2}: {1:4} :: {2:15} to {3:15}'.format(
    #         index, mktime(departure),
    #         stations[origin], stations[destination]))

    # print('\n\nTIMINGS')
    # # print(timing_objects)
    # for index, value in enumerate(timing_objects):
    #     departure = train_objects[index]['departure_time']
    #     origin = train_objects[index]['origin_station']
    #     destination = train_objects[index]['destination_station']
    #     print('{0:2}: {1:4} :: {2:15} to {3:15}'.format(
    #         index, mktime(departure),
    #         stations[origin], stations[destination]))

    #     for timing in value:
    #         # print(timing)
    #         if timing['timing']:
    #             print('{0:4} '.format(mktime(timing['timing']))),
    #         else:
    #             print('0'),
    #     print('')


if __name__ == '__main__':
    run()
