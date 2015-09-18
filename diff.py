from __future__ import division
from datetime import datetime
from datetime import timedelta
import json
from math import ceil


def load(filename):
    """load the data from file
    retrieves station and timing information from a json file

    Args:
        filename: string filename for a valid json file

    Returns:
        list: list of lists
            station_names
            timing lists
    """
    # load json data
    with open(filename, 'r') as json_file:
        file_data = json.load(json_file)
    # get and print station list
    # stations are assigned letters starting from A
    station_list = [train['station'] for train in file_data]
    # get timing lists
    vertical_lists = [train['stops'] for train in file_data]
    for each_list in vertical_lists:
        for index, timing in enumerate(each_list):
            # substiture DOES_NOT_STOP with None
            # the NoneType is easier to use than string for checking
            if timing == u'DOES_NOT_STOP':
                each_list[index] = None
            else:
                each_list[index] = datetime.strptime(timing, "%H.%M")

    return station_list, vertical_lists


def convert(vertical_lists):
    """rotate a given list of lists
    converts a list as if it was a matrix
    interchanges 'row' and 'columns'

    Args:
        vertical_lists: list of lists to be rotated

    Returns:
        list: list of lists
            contains the same elements as original
            except that they are now in different lists
    """
    horizontal_lists = []
    for index_x in range(len(vertical_lists[0])):
        new_list = []
        for v_list in vertical_lists:
            new_list.append(v_list[index_x])
        horizontal_lists.append(new_list)

    return horizontal_lists


def calculate(horizontal_lists):
    """calculate the timing difference between stations

    Args:
        horizontal_lists: list of lists containing timings

    Returns:
        list: list of lists containing the timing differences
    """
    # calculate timing differences
    timings = []
    for h_list in horizontal_lists:
        if h_list[0] is None:
            prev = timedelta()
        else:
            prev = h_list[0]

        t_list = []
        for index, timing in enumerate(h_list):
            if timing is None:
                t_list.append(timedelta())
            elif prev is None:
                t_list.append(timedelta())
            else:
                t_list.append(timing - prev)
            prev = timing
        timings.append(t_list)

    # rotate
    timings = convert(timings)
    # calculate averages
    avg_list = []
    for index, t_list in enumerate(timings):
        # average
        avg = 0
        valid_values = [x.seconds // 60 for x in t_list if x.seconds > 0]
        if len(valid_values) > 0:
            avg = int(ceil(sum(valid_values) / len(valid_values)))
        avg_list.append(avg)

    return timings, avg_list


def output(filename):
    """print pretty output for train timings with average differences

    Args:
        filename: string json file name to parse

    Returns:
        None
    """
    # load data
    station_list, vertical_lists = load(filename)
    # print station list key containing station names
    x = ord('A')
    for index, item in enumerate(station_list):
        print '%s: %s' % (chr(x + index), item)
    print ''
    # convert data
    horizontal_lists = convert(vertical_lists)
    # print station list key for timings
    x = ord('A')
    print ' ',
    for i in range(len(horizontal_lists[0])):
        print '{:^5}'.format(chr(x)),
        x += 1
    print ''
    # print train timings
    for i, v in enumerate(horizontal_lists):
        print "{0:2}".format(i + 1),
        for x in v:
            if x is None:
                print 'XX:XX',
            else:
                print x.strftime('%H:%M'),
        print ''
    print '\n'
    # print station list key for timing diffs
    x = 1
    print '   ',
    for i in range(len(horizontal_lists)):
        print '{:^3}'.format(str(x)),
        x += 1
    print ''
    # calculate timing differences
    timings, avg_list = calculate(horizontal_lists)
    # print timings with averages
    x = ord('A')
    for index, t_list in enumerate(timings):
        print "{0:2}".format(chr(x + index)),
        for timing in t_list:
            print '{0:3}'.format(timing.seconds // 60),
        print '| avg: {0:2}'.format(avg_list[index])
    print ''
    # print station difference information
    for index in range(1, len(station_list)):
        print '{0:<15} --> {1:>15} :: {2:2}mins.'.format(
            station_list[index - 1],
            station_list[index],
            avg_list[index])


if __name__ == '__main__':
    print '---- UP LOCALS ----'
    output('up.json')
    print '\n\n\n'
    print '---- DOWN LOCALS ----'
    output('down.json')
