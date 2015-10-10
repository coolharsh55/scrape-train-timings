from json import load
from json import dump


def convert_timings_from_station_to_train(timing_matrix):
    """
    """
    trains = []
    for i in range(len(timing_matrix[0])):
        trains.append(list())
    for index_i, list_station in enumerate(timing_matrix):
        for index_j, timing in enumerate(list_station):
            trains[index_j].append(timing)

    return trains


if __name__ == '__main__':
    with open('up.json', 'r') as f:
        data = load(f)
    train_matrix = []
    for dat in data:
        for index, item in enumerate(dat['stops']):
            if item == 'DOES_NOT_STOP':
                dat['stops'][index] = None

        train_matrix.append(dat['stops'])
    # print train_matrix
    trains = convert_timings_from_station_to_train(train_matrix)

    print trains
