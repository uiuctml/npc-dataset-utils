#!/usr/bin/env python3

import header
import json
import os
import random
import tqdm

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

def createObjectSplits(dataset_file_name_split):
    file_split_resplit = open(os.path.join(header.dataset_dir_splits_resplit, dataset_file_name_split), "r")
    file_split_resplit_lines = file_split_resplit.readlines()
    file_split_resplit.close()

    if not os.path.isdir(header.dataset_dir_splits_object):
        os.makedirs(header.dataset_dir_splits_object, exist_ok = True)

    file_split_object = open(os.path.join(header.dataset_dir_splits_object, dataset_file_name_split), "w")
    line_counter = 1
    progress_bar = tqdm.tqdm(total = len(file_split_resplit_lines))

    for line in file_split_resplit_lines:
        file_key = line.strip()
        file_name_annotations = file_key + header.dataset_file_extension_annotations
        progress_bar.set_description_str("Processing \"" + file_name_annotations + "\" in \"" + dataset_file_name_split + "\"")
        progress_bar.n = line_counter
        progress_bar.refresh()

        line_counter += 1
        file_path_annotations = os.path.join(header.split_dataset_dir_annotations, file_name_annotations)

        if not os.path.isfile(file_path_annotations):
            continue

        file_annotations = open(file_path_annotations, "r")
        annotations = json.load(file_annotations)
        file_annotations.close()

        for object in annotations["objects"]:
            file_split_object.write(object["key"] + "\n")

    file_split_object.close()

    return

def main():
    resplit()

    createObjectSplits(header.dataset_file_name_split_train)
    createObjectSplits(header.dataset_file_name_split_validation)
    createObjectSplits(header.dataset_file_name_split_test)

    return

if __name__ == "__main__":
    main()
