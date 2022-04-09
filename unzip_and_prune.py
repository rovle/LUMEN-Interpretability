"""
Unzips all the files, and deletes 2/3 of pictures, to reduce the
amount of really-similar images in the dataset.
"""


import tarfile
import os
from random import sample
from math import ceil
from train_test_split import train_test_split
import shutil

from cities import tars

path = '/home/lovre/utils.SOVA/ML/src/LUMEN-Interpretability/dataset'
zipped_files_folder = 'zipped'

for tar_name in tars.keys():
    tar = tarfile.open(os.path.join(path, f'{tar_name}.tar'))
    tar.extractall(os.path.join(path, 'unzipped_and_pruned'))
    tar.close()

    files = os.listidr(os.path.join(path, 'unzipped_and_pruned', tar_name))
    
    files = [x[:-4] for x in files]
    
    to_delete = sample(files, k = ceil( 2 * len(files) / 3 ))
    to_delete_filelist = [x + y for x in to_delete
                                for y in ['.jpg', '.txt']]

    for fp in to_delete_filelist:
        os.remove(os.path.join(path, 'unzipped_and_pruned', tar_name, fp))

    train, test = train_test_split(os.path.join(path,
                                                'unzipped_and_pruned',
                                                tar_name)
                                                )
   
    train = [x + y for x in train
                    for y in ['.jpg', '.txt']]
    test = [x + y for x in test
                    for y in ['.jpg', '.txt']]

    for f in train:
        try:
            shutil.move(os.path.join(path, 'unzipped_and_pruned', tar_name, f),
                        os.path.join(path, 'train', tars[tar_name]))
        except FileNotFoundError:
            continue  

   for f in test:
       try:
           shutil.move(os.path.join(path, 'unzipped_and_pruned', tar_name, f),
                        os.path.join(path, 'test', tars[tar_name]))
       except FileNotFoundError:
           continue  




