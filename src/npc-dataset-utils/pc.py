#!/usr/bin/env python3

"""
@file   pc.py
@author Simon Yu
@date   10/09/2024
@brief  Script for PC datasets.
"""

import header
import json
import logger
import natsort
import os
import random
import utility

def getLabelsAttribute(dataset_config):
    labels_attribute = {}

    for attribute in dataset_config["attributes"]:
        if "" in attribute["labels"]:
            attribute["labels"].remove("")

        labels_attribute[attribute["name"]] = attribute["labels"]

    return labels_attribute

def getLabelsClass(dataset_config):
    if "instance_wise" in dataset_config and dataset_config["instance_wise"]:
        labels_class = []
        labels_class_set = set()

        for image_name in dataset_config["mappings"].keys():
            class_name = image_name.split('/')[0]

            if class_name not in labels_class_set:
                labels_class.append(class_name)
                labels_class_set.add(class_name)

        return natsort.natsorted(labels_class)
    else:
        return list(dataset_config["mappings"].keys())

def getIndicesFromLabelsAttribute(labels_attribute):
    indices = {}

    for attribute in labels_attribute.keys():
        labels_to_indices = {}

        for i in range(len(labels_attribute[attribute])):
            labels_to_indices[labels_attribute[attribute][i]] = i

        indices[attribute] = labels_to_indices

    return indices

def getIndicesFromLabelsClass(labels_class):
    labels_to_indices = {}

    for i in range(len(labels_class)):
        labels_to_indices[labels_class[i]] = i

    return labels_to_indices

def main():
    if os.path.exists(header.dataset_dir_splits_pc):
        logger.log_info("PC dataset splits exist in \"" + header.dataset_dir_splits_pc + "\". Skip.")
        return

    random.seed(header.seed)

    file_dataset_config = open(os.path.join(header.config_dir, header.dataset_config_file_name), "r")
    dataset_config = json.load(file_dataset_config)
    file_dataset_config.close()

    labels_attribute = getLabelsAttribute(dataset_config)
    labels_class = getLabelsClass(dataset_config)
    indices_attribute = getIndicesFromLabelsAttribute(labels_attribute)
    indices_class = getIndicesFromLabelsClass(labels_class)

    categories = {}
    dirs_dataset_splt = [header.dataset_dir_splits_instances_test, header.dataset_dir_splits_instances_train, header.dataset_dir_splits_instances_validate]

    for attribute in dataset_config["attributes"]:
        attribute_name = attribute["name"]
        attribute_categories = attribute["labels"]

        if "" in attribute_categories:
            attribute_categories.remove("")

        categories[attribute_name] = attribute_categories

    for i in range(len(dirs_dataset_splt)):
        logger.log_info("Generating PC dataset split \"" + dirs_dataset_splt[i] + "\".")

        lines = []

        if "instance_wise" in dataset_config and dataset_config["instance_wise"]:
            for label_class in os.listdir(dirs_dataset_splt[i]):
                for instance_name in os.listdir(os.path.join(dirs_dataset_splt[i], label_class)):
                    image_name = os.path.join(label_class, instance_name)
                    attributes = dataset_config["mappings"][image_name]["labels"]
                    line = ""

                    logger.log_debug(image_name)

                    for attribute_name in attributes.keys():
                        if isinstance(attributes[attribute_name], list):
                            count_categories = len(categories[attribute_name])

                            if count_categories <= 0:
                                logger.log_fatal("Empty attribute. Quit.")
                                exit(-1)

                            index_label_attribute = random.randint(0, count_categories - 1)
                        else:
                            index_label_attribute = indices_attribute[attribute_name][attributes[attribute_name]]

                        line += str(index_label_attribute) + ","

                    index_label_class = indices_class[label_class]
                    line += str(index_label_class) + "\n"
                    lines.append(line)
        else:
            for label_class in labels_class:
                attributes = dataset_config["mappings"][label_class]["labels"]

                for _ in os.listdir(os.path.join(dirs_dataset_splt[i], label_class)):
                    line = ""

                    for attribute_name in attributes.keys():
                        if isinstance(attributes[attribute_name], list):
                            count_categories = len(categories[attribute_name])

                            if count_categories <= 0:
                                logger.log_fatal("Empty attribute. Quit.")
                                exit(-1)

                            index_label_attribute = random.randint(0, count_categories - 1)
                        else:
                            index_label_attribute = indices_attribute[attribute_name][attributes[attribute_name]]

                        line += str(index_label_attribute) + ","

                    index_label_class = indices_class[label_class]
                    line += str(index_label_class) + "\n"
                    lines.append(line)

        lines[-1] = lines[-1].rstrip("\n")

        if not os.path.exists(header.dataset_dir_splits_pc):
            os.makedirs(header.dataset_dir_splits_pc, exist_ok = True)

        file_name_pc_dataset = os.path.basename(dirs_dataset_splt[i]) + ".txt"
        file_path_pc_dataset = os.path.join(header.dataset_dir_splits_pc, file_name_pc_dataset)

        with open(file_path_pc_dataset, "w+") as file_dataset_pc:
            file_dataset_pc.writelines(lines)

        logger.log_info("Saved PC dataset split to \"" + file_path_pc_dataset + "\".")

    return

if __name__ == "__main__":
    main()
