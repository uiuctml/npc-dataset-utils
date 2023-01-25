#!/usr/bin/env python3

import header
import logger
import os
import random

def resplit():
    if not os.path.isdir(header.dataset_dir_splits_resplit):
        os.makedirs(header.dataset_dir_splits_resplit, exist_ok = True)

    file_split_original_train = open(os.path.join(header.dataset_dir_splits_original, header.dataset_file_name_split_train), "r")
    file_split_original_train_lines = file_split_original_train.readlines()
    file_split_original_train.close()

    random.shuffle(file_split_original_train_lines)
    resplit_point = int(len(file_split_original_train_lines) * header.split_resplit_training_percentage_training)

    with open(os.path.join(header.dataset_dir_splits_resplit, header.dataset_file_name_split_train), "w") as file_split_resplit_train:
        file_split_resplit_train.writelines(file_split_original_train_lines[0:resplit_point])

    with open(os.path.join(header.dataset_dir_splits_resplit, header.dataset_file_name_split_validation), "w") as file_split_resplit_validation:
        file_split_resplit_validation.writelines(file_split_original_train_lines[resplit_point:-1])

    file_split_original_validation = open(os.path.join(header.dataset_dir_splits_original, header.dataset_file_name_split_validation), "r")
    file_split_original_validation_lines = file_split_original_validation.readlines()
    file_split_original_validation.close()

    with open(os.path.join(header.dataset_dir_splits_resplit, header.dataset_file_name_split_test), "w") as file_split_resplit_test:
        file_split_resplit_test.writelines(file_split_original_validation_lines)

    return

def createObjectSplits():
    return

def main():
    resplit()

    return

if __name__ == "__main__":
    main()
