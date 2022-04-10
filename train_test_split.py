import os
from math import ceil

def distance(x, y):
    return (x[1] - y[1])**2 + (x[0] - y[0])**2

def coors(filename):
    with open(filename) as fp:
        f = fp.read()
        f = f.split(' ')
        f = f[5:7]
        f = [float(x) for x in f]
    return tuple(f)

def folders_to_coors(folder_name):
    coor_set = list()
    for file in os.listdir(folder_name):
        if file[-3:] == 'txt':
            try:
                coords = coors(os.path.join(folder_name, file))
            except UnicodeDecodeError:
                continue
        try:
            coords
        except UnboundLocalError:
            continue
        if coords not in coor_set:
            coor_set.append(coords)
    return coor_set


def train_test_split(path_to_unzipped):
    coordinates = folders_to_coors(path_to_unzipped)

    train_set = []
    test_set = []
    chunks_size = ceil(0.1*len(coordinates))

    i = 0
    while coordinates != []:
        anchor_point = min(coordinates, key=lambda x: x[0])
        distances = [distance(x, anchor_point) for x in coordinates]
        coors_and_dists = list(zip(coordinates, distances))
        coors_and_dists = sorted(coors_and_dists, key=lambda x: x[1])
        first_chunk = coors_and_dists[:chunks_size]
        second_chunk = coors_and_dists[chunks_size:]
        chunk = [x[0] for x in first_chunk]
        coordinates = [x[0] for x in second_chunk]
        if i % 2 == 0:
            train_set += chunk
        else:
            test_set += chunk
        i += 1

    split = {'train' : [], 'test' : []}
    for file in os.listdir(path_to_unzipped):
        if file[-3:] == 'txt':
            try:
                coords = coors(os.path.join(path_to_unzipped, file))
            except UnicodeDecodeError:
                continue
        try:
            coords
        except UnboundLocalError:
            continue
        if coords in train_set:
            split['train'].append(file[:-4])
        else:
            split['test'].append(file[:-4])
    return split['train'], split['test']
