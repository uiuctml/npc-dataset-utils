#!/usr/bin/env python3

import cv2
import header
import json
import logger
import numpy
import os
import tqdm

def resplit():
    if not os.path.isdir(header.dataset_dir_splits_resplit):
        os.makedirs(header.dataset_dir_splits_resplit, exist_ok = True)
    else:
        return

    file_split_original_validation = open(os.path.join(header.dataset_dir_splits_original, header.dataset_file_name_split_validation), "r")
    file_split_original_validation_lines = file_split_original_validation.readlines()
    file_split_original_validation.close()

    with open(os.path.join(header.dataset_dir_splits_resplit, header.dataset_file_name_split_test), "w") as file_split_resplit_test:
        file_split_resplit_test.writelines(file_split_original_validation_lines)

    for i in range(0, len(file_split_original_validation_lines)):
        file_split_original_validation_lines[i] = file_split_original_validation_lines[i].strip()

    dataset_dir_annotations_list = os.listdir(header.split_dataset_dir_annotations)
    file_split_resplit_test_lines = set(file_split_original_validation_lines)
    file_split_resplit_train_validation = open(os.path.join(header.dataset_dir_splits_resplit, header.split_file_name_resplit_train_validation), "w")

    for file_name_annotations in dataset_dir_annotations_list:
        file_key = file_name_annotations.split(".")[0]

        if file_key not in file_split_resplit_test_lines:
            file_split_resplit_train_validation.write(file_key + "\n")

    file_split_resplit_train_validation.close()

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
    progress_bar.close()

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
    labels_empty = []
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
                os.symlink(os.path.abspath(os.path.join(header.split_dataset_dir_images, dataset_dir_labels, file_name_image)), os.path.join(dataset_dir_labels_split, file_name_image))

        if len(os.listdir(dataset_dir_labels_split)) == 0:
            labels_empty.append(dataset_dir_labels)
            image_placeholder = numpy.zeros(header.split_file_symlink_placeholder_shape, numpy.uint8)
            image_placeholder[:][:] = header.split_file_symlink_placeholder_color
            cv2.imwrite(os.path.join(dataset_dir_labels_split, header.split_file_name_symlink_placeholder), image_placeholder)

    progress_bar.close()

    for label_empty in labels_empty:
        logger.log_warn("\"" + label_empty + "\" has placeholder data for split dataset \"" + dataset_name_split + "\".")

    return

def main():
    resplit()

    createObjectSplits(header.split_file_name_resplit_train_validation)
    createObjectSplits(header.dataset_file_name_split_test)

    createSplitSymlinks(header.split_file_name_resplit_train_validation)
    createSplitSymlinks(header.dataset_file_name_split_test)

    return

if __name__ == "__main__":
    main()
