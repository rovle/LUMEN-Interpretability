"""
Used this to get all
- train datasets to ~250k files (125k images), except Amsterdam which is at 190k
- test datasets to ~80k files (40k images), except Amsterdam which at 60k
"""

import os
from random import sample
from math import ceil

path = '/home/src/LUMEN-Interpretability/dataset'

folds = ["train", "test"]
classes = ["NYC", "LasVegas", "Firenca", "Amsterdam"]

def remove_some(fold, clas, n=0):
    files = os.listdir(os.path.join(path, fold, clas))

    files = [x[:-4] for x in files]
    files = set(files)

    to_remove = sample(files, k=ceil(n/2))

    for fp in to_remove:
        os.remove(os.path.join(path, fold, clas, fp + '.jpg'))
        os.remove(os.path.join(path, fold, clas, fp + '.txt'))

remove_some('train', 'LasVegas', n=220000)
remove_some('train', 'Firenca', n=120000)
remove_some('test', 'NYC', n=120000)
remove_some('test', 'LasVegas', n=200000)
# remove_some('test', 'Firenca', n=260000)
remove_some('test', 'Firenca', n=170000)
