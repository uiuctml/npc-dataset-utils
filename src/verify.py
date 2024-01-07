#!/usr/bin/env python3

import header
import json
import logger
import os

def verifyDatasetConfigDuplicates(config_dataset):
    label_map = {}

    for label_original in config_dataset["mappings"].keys():
        if len(config_dataset["mappings"][label_original]["labels"]) > 0:
            labels_dataset = ""

            for dataset_name in config_dataset["mappings"][label_original]["labels"].keys():
                label_dataset = config_dataset["mappings"][label_original]["labels"][dataset_name]

                if labels_dataset != "":
                    labels_dataset += header.dataset_delimiter_file_name

                labels_dataset += label_dataset

            if labels_dataset not in label_map:
                label_map[labels_dataset] = [label_original]
            else:
                label_map[labels_dataset].append(label_original)

    for label_dataset in label_map.keys():
        labels_original_list = label_map[label_dataset]

        if len(labels_original_list) > 1:
            labels_original = ", ".join(labels_original_list)
            logger.log_error("\"" + labels_original + "\" contain identical labels.")

    return

def verifyDatasetConfigLabels(config_dataset):
    for label_original in config_dataset["mappings"].keys():
        if len(config_dataset["mappings"][label_original]["labels"]) == 0:
            logger.log_error("\"" + label_original + "\" does not contain any labels.")
        else:
            for dataset_name in config_dataset["mappings"][label_original]["labels"].keys():
                if config_dataset["mappings"][label_original]["labels"][dataset_name] == "":
                    logger.log_error("\"" + label_original + "\" contains an empty label for dataset \"" + dataset_name + "\".")
                elif config_dataset["mappings"][label_original]["labels"][dataset_name].split(header.dataset_delimiter_label)[0] != dataset_name:
                    logger.log_error("\"" + label_original + "\" contains an invalid label for dataset \"" + dataset_name + "\".")

    return

def verifyDatasetConfigMissing(config_dataset):
    labels_dataset_set_dataset = set()
    labels_dataset_set_generate = set()

    for dataset in config_dataset["attributes"]:
        labels_dataset = dataset["labels"]

        for label_dataset in labels_dataset:
            labels_dataset_set_dataset.add(label_dataset)

    for label_original in config_dataset["mappings"].keys():
        if len(config_dataset["mappings"][label_original]["labels"]) > 0:
            for dataset_name in config_dataset["mappings"][label_original]["labels"].keys():
                labels_dataset_set_generate.add(config_dataset["mappings"][label_original]["labels"][dataset_name])

    for label_dataset_generate in labels_dataset_set_generate:
        if label_dataset_generate not in labels_dataset_set_dataset:
            logger.log_error("\"" + label_dataset_generate + "\" is missing.")

    return

def verifyDatasetConfigUnused(config_dataset):
    labels_dataset_set = set()

    for label_original in config_dataset["mappings"].keys():
        if len(config_dataset["mappings"][label_original]["labels"]) > 0:
            for dataset_name in config_dataset["mappings"][label_original]["labels"].keys():
                labels_dataset_set.add(config_dataset["mappings"][label_original]["labels"][dataset_name])

    for dataset in config_dataset["attributes"]:
        labels_dataset = dataset["labels"]

        for label_dataset in labels_dataset:
            if label_dataset != "" and label_dataset not in labels_dataset_set:
                logger.log_error("\"" + label_dataset + "\" is unused.")

    return

def verifyDatasetSplitsEmpty():
    if os.path.isdir(header.dataset_dir_images_split_original):
        dataset_dir_images_split_list = os.listdir(header.dataset_dir_images_split_original)

        for dataset_name_split in dataset_dir_images_split_list:
            dataset_split = os.listdir(os.path.join(header.dataset_dir_images_split_original, dataset_name_split))

            for dataset_dir_labels in dataset_split:
                dataset_dir_labels_split = os.path.join(header.dataset_dir_images_split_original, dataset_name_split, dataset_dir_labels)
                dataset_dir_labels_split_list = os.listdir(dataset_dir_labels_split)

                if len(dataset_dir_labels_split_list) == 0:
                    logger.log_error("\"" + dataset_dir_labels + "\" has no data for dataset split \"" + dataset_name_split + "\".")

    return

def main():
    file_path_config_dataset = os.path.join(header.config_dir, header.dataset_config_file_name)

    logger.log_info("Verifying \"" + file_path_config_dataset + "\"...")

    file_config_dataset = open(file_path_config_dataset, "r")
    config_dataset = json.load(file_config_dataset)
    file_config_dataset.close()

    verifyDatasetConfigDuplicates(config_dataset)
    verifyDatasetConfigLabels(config_dataset)
    verifyDatasetConfigMissing(config_dataset)
    verifyDatasetConfigUnused(config_dataset)

    logger.log_info("Verifying \"" + header.dataset_dir_images_split + "\"...")

    verifyDatasetSplitsEmpty()

    return

if __name__ == "__main__":
    main()
