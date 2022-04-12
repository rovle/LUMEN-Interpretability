"""
Unzips all the files, and deletes 2/3 of pictures, to reduce the
amount of really-similar images in the dataset.
"""

import tarfile
import os
from random import sample
from math import ceil
import shutil
from tqdm import tqdm
from cities import tars

path = '/home/src/LUMEN-Interpretability/dataset'
zipped_files_folder = 'zipped'

for tar_name in tqdm(tars.keys()):
    tar = tarfile.open(os.path.join(path, 'zipped', f"{tar_name}.tar"))
    tar.extractall(os.path.join(path, 'unzipped_and_pruned'))
    tar.close()

    files = os.listdir(os.path.join(path, 'unzipped_and_pruned', tar_name))
    
    files = [x[:-4] for x in files]
    files = list(set(files))
    
    to_delete = sample(files, k = ceil( 2 * len(files) / 3 ))
    to_delete_filelist = [x + y for x in to_delete
                                for y in ['.jpg', '.txt']]
    i = 0
    j = 0
    for fp in to_delete_filelist:
        try:
            os.remove(os.path.join(path, 'unzipped_and_pruned', tar_name, fp))
            j += 1
        except FileNotFoundError:
            i += 1
            continue
    print(f"{i} nonexistent files out of {len(to_delete_filelist)}.")
    
    files = os.listdir(os.path.join(path, 'unzipped_and_pruned', tar_name))

    for fp in files:
        try:
            shutil.move(os.path.join(path, 'unzipped_and_pruned', tar_name, fp),
                        os.path.join(path, 'unzipped_and_pruned', tars[tar_name]))
        except FileNotFoundError:
            continue
        except shutil.Error:
            continue
"""
    train, test = train_test_split(os.path.join(path,
                                                'unzipped_and_pruned',
                                                tar_name)
                                                )
   
    train = [x + y for x in train
                    for y in ['.jpg', '.txt']]
    test = [x + y for x in test
                    for y in ['.jpg', '.txt']]
    i = 0
    for f in train:
        try:
            shutil.move(os.path.join(path, 'unzipped_and_pruned', tars[tar_name], f),
                        os.path.join(path, 'train', tars[tar_name]))
        except FileNotFoundError:
            continue
        except shutil.Error:
            i += 1
    for f in test:
        try:
            shutil.move(os.path.join(path, 'unzipped_and_pruned', tars[tar_name], f),
                        os.path.join(path, 'test', tars[tar_name]))
        except FileNotFoundError:
            continue
        except shutil.Error:
            i += 1
    print(f"Failed to move {i} out of {len(train)+len(test)}")
"""
