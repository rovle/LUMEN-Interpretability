import os
from math import ceil
import shutil
from tqdm import tqdm

def coors(filename):
    with open(filename) as fp:
        f = fp.read()
        f = f.split(' ')
        f = f[5:7]
        f = [float(x) for x in f]
    return tuple(f)

def halve(lst):
    return lst[:round(len(lst)/2)], lst[round(2+len(lst)/2):]

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

    coordinates.sort(key=lambda x: x[0])

    first_chunk, second_chunk = halve(coordinates)

    first_chunk.sort(key=lambda x: x[1])
    second_chunk.sort(key=lambda x: x[1])

    a, b = halve(first_chunk)
    c, d = halve(second_chunk)

    train_set = a + d
    test_set = b + c
    
    split = {'train' : [], 'test' : []}
    for file in os.listdir(path_to_unzipped):
        if file[-3:] == 'txt':
            try:
                coords = coors(os.path.join(path_to_unzipped, file))
                if coords in train_set:
                    split['train'].append(file[:-4])
                elif coords in test_set:
                    split['test'].append(file[:-4])
            except UnicodeDecodeError:
                continue
    return split['train'], split['test']

path = '/home/src/LUMEN-Interpretability/dataset/'
for city in tqdm(['NYC', 'LasVegas', 'Firenca']):
    train, test = train_test_split(os.path.join(path, 'unzipped_and_pruned',
                                                    city))

    train = [x + y for x in train
                    for y in ['.jpg', '.txt']]
    test = [x + y for x in test
                    for y in ['.jpg', '.txt']]
    for f in train:
        try:
            shutil.copy(os.path.join(path, 'unzipped_and_pruned',
                                    city, f),
                        os.path.join(path, 'train', city))
        except FileNotFoundError:
            continue
        except shutil.Error:
            continue
    for f in test:
        try:
            shutil.copy(os.path.join(path, 'unzipped_and_pruned',
                                    city, f),
                        os.path.join(path, 'test', city))
        except FileNotFoundError:
            continue
        except shutil.Error:
            continue
