#!/usr/bin/env python3

import header
import json
import logger
import os
import shutil
import tqdm

def initialize():
    if not os.path.isdir(header.dataset_dir_annotations_generated):
        os.mkdir(header.dataset_dir_annotations_generated)

    dataset_dir_annotations_original_list = os.listdir(header.dataset_dir_annotations_original)

    for dataset in header.generate_datasets:
        dataset_name = dataset["name"]
        dataset_dir_annotations_generated_dataset = os.path.join(header.dataset_dir_annotations_generated, dataset_name)
        file_annotations_counter = 1
        progress_bar = tqdm.tqdm(total = len(dataset_dir_annotations_original_list))

        if os.path.isdir(dataset_dir_annotations_generated_dataset):
            continue

        os.mkdir(dataset_dir_annotations_generated_dataset)

        for file_name_annotations in dataset_dir_annotations_original_list:
            progress_bar.set_description_str("Initializing dataset \"" + dataset_name + "\"")
            progress_bar.n = file_annotations_counter
            progress_bar.refresh()

            file_annotations_counter += 1
            file_path_annotations_original = os.path.join(header.dataset_dir_annotations_original, file_name_annotations)

            if not os.path.isfile(file_path_annotations_original):
                continue

            shutil.copy(file_path_annotations_original, dataset_dir_annotations_generated_dataset)

        progress_bar.close()

    return

def main():
    if not os.path.isdir(header.dataset_dir_annotations):
        logger.log_error("Invalid dataset annotations directory.")
        return

    if not os.path.isdir(header.dataset_dir_annotations_original):
        logger.log_error("Invalid original dataset annotations directory.")
        return

    initialize()

    for dataset in header.generate_datasets:
        dataset_name = dataset["name"]
        dataset_dir_annotations_generated_dataset = os.path.join(header.dataset_dir_annotations_generated, dataset_name)

        if not os.path.isdir(dataset_dir_annotations_generated_dataset):
            logger.log_error("Invalid generated dataset annotations directory.")
            continue

        dataset_dir_annotations_generated_dataset_list = os.listdir(dataset_dir_annotations_generated_dataset)
        file_annotations_counter = 1
        progress_bar = tqdm.tqdm(total = len(dataset_dir_annotations_generated_dataset_list))

        for file_name_annotations in dataset_dir_annotations_generated_dataset_list:
            progress_bar.set_description_str("Processing \"" + file_name_annotations + "\" for dataset \"" + dataset_name + "\"")
            progress_bar.n = file_annotations_counter
            progress_bar.refresh()

            file_annotations_counter += 1
            file_path_annotations = os.path.join(dataset_dir_annotations_generated_dataset, file_name_annotations)

            if not os.path.isfile(file_path_annotations):
                continue

            file_annotations = open(file_path_annotations, "r")
            annotations = json.load(file_annotations)
            file_annotations.close()

            for object in annotations["objects"]:
                if object["label"] in dataset.values():
                    continue

                if object["label"] in dataset:
                    object["label"] = dataset[object["label"]]
                else:
                    object["label"] = dataset_name + "--" + "undefined"

            file_annotations = open(file_path_annotations, "w")
            json.dump(annotations, file_annotations, indent = 2)
            file_annotations.close()

        progress_bar.close()

    return

if __name__ == "__main__":
    main()
