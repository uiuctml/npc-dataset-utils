#!/usr/bin/env python3

import header
import json
import os
import random
import tqdm

def resplit():
    if not os.path.isdir(header.dataset_dir_splits_resplit):
        os.makedirs(header.dataset_dir_splits_resplit, exist_ok = True)
    else:
        return

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
    if os.path.isfile(os.path.join(header.dataset_dir_splits_object, dataset_file_name_split)):
        return

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

def createSplitSymlinks(dataset_file_name_split):
    dataset_dir_images_list = os.listdir(header.split_dataset_dir_images)
    dataset_name_split = dataset_file_name_split.split(".")[0]

    if os.path.isdir(os.path.join(header.dataset_dir_images_split, dataset_name_split)):
        return

    file_split_object = open(os.path.join(header.dataset_dir_splits_object, dataset_file_name_split), "r")
    file_split_object_lines = file_split_object.readlines()
    file_split_object.close()

    for i in range(0, len(file_split_object_lines)):
        file_split_object_lines[i] = file_split_object_lines[i].strip()

    file_split_object_lines = set(file_split_object_lines)

    dataset_dir_labels_counter = 1
    progress_bar = tqdm.tqdm(total = len(dataset_dir_images_list))

    for dataset_dir_labels in dataset_dir_images_list:
        dataset_dir_labels_split = os.path.join(header.dataset_dir_images_split, dataset_name_split, dataset_dir_labels)
        progress_bar.set_description_str("Processing \"" + dataset_dir_labels + "\" for \"" + dataset_name_split + "\" dataset split")
        progress_bar.n = dataset_dir_labels_counter
        progress_bar.refresh()

        dataset_dir_labels_counter += 1
        dataset_images_list = os.listdir(os.path.join(header.split_dataset_dir_images, dataset_dir_labels))

        if not os.path.isdir(dataset_dir_labels_split):
            os.makedirs(dataset_dir_labels_split, exist_ok = True)

        for file_name_image in dataset_images_list:
            file_key = file_name_image.split(".")[0]

            if file_key in file_split_object_lines:
                os.symlink(os.path.join(header.split_dataset_dir_images, dataset_dir_labels, file_name_image), os.path.join(dataset_dir_labels_split, file_name_image))

    return

def main():
    resplit()

    createObjectSplits(header.dataset_file_name_split_train)
    createObjectSplits(header.dataset_file_name_split_validation)
    createObjectSplits(header.dataset_file_name_split_test)

    createSplitSymlinks(header.dataset_file_name_split_train)
    createSplitSymlinks(header.dataset_file_name_split_validation)
    createSplitSymlinks(header.dataset_file_name_split_test)

    return

if __name__ == "__main__":
    main()
