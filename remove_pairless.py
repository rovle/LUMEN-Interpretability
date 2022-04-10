import os
from itertools import product

path = '/home/src/LUMEN-Interpretability/dataset'

folds = ["train", "test"]
classes = ["NYC", "LasVegas", "Firenca", "Amsterdam"]

def check_pairs(path_to_dataset):
    for (fold, class_) in product(folds, classes):
        files = os.listdir(os.path.join(path, fold, class_))
    
        jpgs = set([x[:-4] for x in files if x[-3:] == 'jpg'])
        txts = set([x[:-4] for x in files if x[-3:] == 'txt'])

        to_remove = jpgs.symmetric_difference(txts)

        print(f"There's {len(to_remove)} things to remove because they lack pairs!")

        to_remove = list(to_remove)
        for fp in to_remove:
            if fp in jpgs:
                os.remove(os.path.join(path_to_dataset, fold, class_, fp + '.jpg'))
            if fp in txts:
                os.remove(os.path.join(path_to_dataset, fold, class_, fp + '.txt'))

check_pairs(path)
