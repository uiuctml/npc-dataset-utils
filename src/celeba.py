#!/usr/bin/env python3

import header
import json
import logger
import os
import utility

def readMatrix():
    attributes = []
    count_instances = -1
    lines = []
    matrix = {}

    with open(os.path.join(header.dataset_dir_annotations, header.celeba_file_name_attributes), 'r') as file_attributes:
        lines = file_attributes.readlines()

    count_instances = int(lines.pop(0))

    if count_instances <= 0:
        logger.log_fatal("Invalid instance count. Quit.")
        exit(-1)

    attributes = lines.pop(0).strip().split(' ')

    for i in range(len(attributes)):
        attributes[i] = attributes[i].lower()
        attributes[i] = attributes[i].replace('_', '-')

    for i in range(count_instances):
        attribute_values = lines[i].strip().split()
        instance_name = attribute_values.pop(0)

        if len(attribute_values) != len(attributes):
            logger.log_fatal("Invalid attribute values. Quit.")
            exit(-1)

        logger.log_info_raw("\033[K[INFO]: Reading instance \"" + instance_name + "\"", end = '\r')

        matrix[instance_name] = {}

        for j in range(len(attribute_values)):
            attribute_name = attributes[j]

            if attribute_values[j] == "1":
                matrix[instance_name][attribute_name] = True
            else:
                matrix[instance_name][attribute_name] = False

    logger.log_info_raw()

    return (matrix, attributes)

def processAttributes(matrix, attributes):
    balance_scores = {}

    for attribute_name in attributes:
        count_false = 0
        count_true = 0

        logger.log_info_raw("\033[K[INFO]: Processing attribute \"" + attribute_name + "\"", end = '\r')

        for instance_name in matrix.keys():
            if matrix[instance_name][attribute_name]:
                count_true += 1
            else:
                count_false += 1

        balance_scores[attribute_name] = abs(count_true - count_false)

    logger.log_info_raw()

    balance_scores = dict(sorted(balance_scores.items(), key=lambda item: item[1], reverse = False))
    labels = list(balance_scores.keys())[:header.celeba_count_attributes]

    attribute = {}
    attribute["name"] = "attributes"
    attribute["labels"] = [""] + sorted(labels)
    attributes = [attribute]

    return attributes

def processMappings():
    mappings = {}

    return mappings

def main():
    (matrix, attributes) = readMatrix()
    attributes = processAttributes(matrix, attributes)
    mappings = processMappings()
    config = {}
    config["attributes"] = attributes
    # TODO config["attributes"] = utility.pruneAttributes(attributes, mappings)
    config["mappings"] = mappings

    with open(os.path.join(header.config_dir, header.dataset_config_file_name), 'w') as file_config:
        json.dump(config, file_config, indent = 4)

    return

if __name__ == "__main__":
    main()
