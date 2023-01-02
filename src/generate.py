#!/usr/bin/env python3

import header
import json
import logger
import os
import shutil

def initialize():
    if (not os.path.isdir(header.dataset_annotations_generated_dir)):
        os.mkdir(header.dataset_annotations_generated_dir)

    dataset_annotations_original_dir_list = os.listdir(header.dataset_annotations_original_dir)

    for dataset in header.generate_datasets:
        dataset_name = dataset["name"]
        dataset_annotations_generated_dataset_dir = os.path.join(header.dataset_annotations_generated_dir, dataset_name)
        file_annotations_counter = 1

        if (os.path.isdir(dataset_annotations_generated_dataset_dir)):
            continue

        os.mkdir(dataset_annotations_generated_dataset_dir)

        for file_name_annotations in dataset_annotations_original_dir_list:
            if (file_annotations_counter >= len(dataset_annotations_original_dir_list)):
                logger.log_info("Initializing dataset \"" + dataset_name + "\" (" + str(file_annotations_counter) + "/" + str(len(dataset_annotations_original_dir_list)) + ")...")
            else:
                logger.log_info("Initializing dataset \"" + dataset_name + "\" (" + str(file_annotations_counter) + "/" + str(len(dataset_annotations_original_dir_list)) + ")...", end = "\r")

            file_annotations_counter += 1
            file_path_annotations_original = os.path.join(header.dataset_annotations_original_dir, file_name_annotations)

            if (not os.path.isfile(file_path_annotations_original)):
                continue

            shutil.copy(file_path_annotations_original, dataset_annotations_generated_dataset_dir)

    return

def main():
    if (not os.path.isdir(header.dataset_annotations_dir)):
        logger.log_error("Invalid dataset annotations directory.")
        return

    if (not os.path.isdir(header.dataset_annotations_original_dir)):
        logger.log_error("Invalid original dataset annotations directory.")
        return

    initialize()

    for dataset in header.generate_datasets:
        dataset_name = dataset["name"]
        dataset_annotations_generated_dataset_dir = os.path.join(header.dataset_annotations_generated_dir, dataset_name)
        dataset_annotations_generated_dataset_dir_list = os.listdir(dataset_annotations_generated_dataset_dir)
        file_annotations_counter = 1

        if (not os.path.isdir(dataset_annotations_generated_dataset_dir)):
            logger.log_error("Invalid generated dataset annotations directory.")
            continue

        for file_name_annotations in dataset_annotations_generated_dataset_dir_list:
            if (file_annotations_counter >= len(dataset_annotations_generated_dataset_dir_list)):
                logger.log_info("Processing \"" + file_name_annotations + "\" for dataset \"" + dataset_name + "\" (" + str(file_annotations_counter) + "/" + str(len(dataset_annotations_generated_dataset_dir_list)) + ")...")
            else:
                logger.log_info("Processing \"" + file_name_annotations + "\" for dataset \"" + dataset_name + "\" (" + str(file_annotations_counter) + "/" + str(len(dataset_annotations_generated_dataset_dir_list)) + ")...", end = "\r")

            file_annotations_counter += 1
            file_path_annotations = os.path.join(dataset_annotations_generated_dataset_dir, file_name_annotations)

            if (not os.path.isfile(file_path_annotations)):
                continue

            file_annotations = open(file_path_annotations, "r")
            annotations = json.load(file_annotations)
            file_annotations.close()

            for object in annotations["objects"]:
                if (object["label"] in dataset.values()):
                    continue

                if (object["label"] in dataset):
                    object["label"] = dataset[object["label"]]
                else:
                    object["label"] = dataset_name + "--" + "undefined"

            file_annotations = open(file_path_annotations, "w")
            json.dump(annotations, file_annotations, indent = 2)
            file_annotations.close()

    return

if __name__ == "__main__":
    main()
