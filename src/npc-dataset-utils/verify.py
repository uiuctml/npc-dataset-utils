#!/usr/bin/env python3

"""
@file   verify.py
@author Simon Yu
@date   01/23/2023
@brief  Script for verifying dataset configuration.
"""

import header
import json
import logger
import os

def verifyDatasetConfigDuplicates(config_dataset):
    label_map = {}

    for label_class in config_dataset["mappings"].keys():
        if len(config_dataset["mappings"][label_class]["labels"]) > 0:
            labels_dataset = ""

            for dataset_name in config_dataset["mappings"][label_class]["labels"].keys():
                label_dataset = config_dataset["mappings"][label_class]["labels"][dataset_name]

                if labels_dataset != "":
                    labels_dataset += header.dataset_delimiter_file_name

                if isinstance(label_dataset, list):
                    for label in label_dataset:
                        labels_dataset += label
                else:
                    labels_dataset += label_dataset

            if labels_dataset not in label_map:
                label_map[labels_dataset] = [label_class]
            else:
                label_map[labels_dataset].append(label_class)

    for label_dataset in label_map.keys():
        labels_class_list = label_map[label_dataset]

        if len(labels_class_list) > 1:
            labels_class = ", ".join(labels_class_list)
            logger.log_warn("Identical attributes: \"" + labels_class + "\".")

    return

def verifyDatasetConfigLabels(config_dataset):
    for label_class in config_dataset["mappings"].keys():
        if len(config_dataset["mappings"][label_class]["labels"]) == 0:
            logger.log_warn("Missing attributes: \"" + label_class + "\".")
        else:
            for dataset_name in config_dataset["mappings"][label_class]["labels"].keys():
                if config_dataset["mappings"][label_class]["labels"][dataset_name] == "":
                    logger.log_warn("Empty attribute: \"" + dataset_name + "\", \"" + label_class + "\".")
                else:
                    labels = config_dataset["mappings"][label_class]["labels"][dataset_name]

                    if isinstance(labels, list):
                        for label in labels:
                            if label.split(header.dataset_delimiter_label)[0] != dataset_name:
                                logger.log_warn("Invalid attribute: \"" + dataset_name + "\", \"" + label_class + "\".")
                    else:
                        if labels.split(header.dataset_delimiter_label)[0] != dataset_name:
                            logger.log_warn("Invalid attribute: \"" + dataset_name + "\", \"" + label_class + "\".")

    return

def verifyDatasetConfigMissing(config_dataset):
    names_dataset_set = set()
    labels_dataset_set_dataset = set()
    labels_dataset_set_generate = set()

    for dataset in config_dataset["attributes"]:
        name_dataset = dataset["name"]
        labels_dataset = dataset["labels"]
        names_dataset_set.add(name_dataset)

        for label_dataset in labels_dataset:
            labels_dataset_set_dataset.add(label_dataset)

    for label_class in config_dataset["mappings"].keys():
        labels_class = os.listdir(header.dataset_dir_instances_processed)

        if label_class not in labels_class:
            logger.log_warn("Unknown label: \"" + label_class + "\".")

        labels_decomposed = config_dataset["mappings"][label_class]["labels"]

        for name_dataset_set in names_dataset_set:
            if name_dataset_set not in labels_decomposed.keys():
                logger.log_warn("Missing attribute: \"" + name_dataset_set + "\", \"" + label_class + "\".")

        if len(labels_decomposed) > 0:
            for dataset_name in labels_decomposed.keys():
                if isinstance(labels_decomposed[dataset_name], list):
                    for label in labels_decomposed[dataset_name]:
                        labels_dataset_set_generate.add(label)
                else:
                    labels_dataset_set_generate.add(labels_decomposed[dataset_name])

                if dataset_name not in names_dataset_set:
                    logger.log_warn("Unknown attribute: \"" + dataset_name + "\", \"" + label_class + "\".")

    for label_dataset_generate in labels_dataset_set_generate:
        if label_dataset_generate not in labels_dataset_set_dataset:
            logger.log_warn("Missing label: \"" + label_dataset_generate + "\".")

    return

def verifyDatasetConfigUnused(config_dataset):
    labels_dataset_set = set()

    for label_class in config_dataset["mappings"].keys():
        if len(config_dataset["mappings"][label_class]["labels"]) > 0:
            for dataset_name in config_dataset["mappings"][label_class]["labels"].keys():
                labels = config_dataset["mappings"][label_class]["labels"][dataset_name]

                if isinstance(labels, list):
                    for label in labels:
                        labels_dataset_set.add(label)
                else:
                    labels_dataset_set.add(labels)

    for dataset in config_dataset["attributes"]:
        labels_dataset = dataset["labels"]

        for label_dataset in labels_dataset:
            if label_dataset != "" and label_dataset not in labels_dataset_set:
                logger.log_warn("Unused attribute: \"" + label_dataset + "\".")

    return

def verifyDatasetSplitsEmpty():
    if os.path.isdir(header.dataset_dir_splits_instances):
        dataset_dir_images_split_list = os.listdir(header.dataset_dir_splits_instances)

        for dataset_name_split in dataset_dir_images_split_list:
            dataset_split = os.listdir(os.path.join(header.dataset_dir_splits_instances, dataset_name_split))

            for dataset_dir_labels in dataset_split:
                dataset_dir_labels_split = os.path.join(header.dataset_dir_splits_instances, dataset_name_split, dataset_dir_labels)
                dataset_dir_labels_split_list = os.listdir(dataset_dir_labels_split)

                if len(dataset_dir_labels_split_list) == 0:
                    logger.log_warn("Empty label: \"" + dataset_dir_labels + "\", \"" + dataset_name_split + "\".")

    return

def main():
    file_path_config_dataset = os.path.join(header.config_dir, header.dataset_config_file_name)

    logger.log_info("Verifying \"" + file_path_config_dataset + "\"...")

    file_config_dataset = open(file_path_config_dataset, "r")
    config_dataset = json.load(file_config_dataset)
    file_config_dataset.close()

    if "instance_wise" in config_dataset and config_dataset["instance_wise"]:
        logger.log_fatal("Instance-wise dataset not supported. Quit.")
        exit(-1)

    verifyDatasetConfigDuplicates(config_dataset)
    verifyDatasetConfigLabels(config_dataset)
    verifyDatasetConfigMissing(config_dataset)
    verifyDatasetConfigUnused(config_dataset)

    logger.log_info("Verifying \"" + header.dataset_dir_splits + "\"...")

    verifyDatasetSplitsEmpty()

    return

if __name__ == "__main__":
    main()
