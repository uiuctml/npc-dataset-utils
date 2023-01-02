#!/usr/bin/env python3

import header
import json
import logger
import os

def main():
    if (not os.path.isdir(header.dataset_annotations_original_dir)):
        logger.log_error("Invalid original dataset annotations directory.")
        return

    dataset_annotations_original_dir_list = os.listdir(header.dataset_annotations_original_dir)
    file_annotations_counter = 1
    label_set = set()

    for file_name_annotations in dataset_annotations_original_dir_list:
        if (file_annotations_counter >= len(dataset_annotations_original_dir_list)):
            logger.log_info("Processing \"" + file_name_annotations + "\" (" + str(file_annotations_counter) + "/" + str(len(dataset_annotations_original_dir_list)) + ")...")
        else:
            logger.log_info("Processing \"" + file_name_annotations + "\" (" + str(file_annotations_counter) + "/" + str(len(dataset_annotations_original_dir_list)) + ")...", end = "\r")

        file_annotations_counter += 1
        file_path_annotations = os.path.join(header.dataset_annotations_original_dir, file_name_annotations)

        if (not os.path.isfile(file_path_annotations)):
            continue

        file_annotations = open(file_path_annotations, "r")
        annotations = json.load(file_annotations)
        file_annotations.close()

        for object in annotations["objects"]:
            label_set.add(object["label"])

    label_set = sorted(label_set)

    file_label = open(header.label_file_name, "w")

    for label in label_set:
        file_label.write(label + "\n")

    file_label.close()

    logger.log_info("Label saved to \"" + header.label_file_name + "\".")

    return

if __name__ == "__main__":
    main()
