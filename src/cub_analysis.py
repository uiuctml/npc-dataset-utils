#!/usr/bin/env python3

import header
import json
import logger
import os
import random

def countAttributeClassOccurrences(config):
    class_occurrences = {}
    classes = set()
    mappings = config["mappings"]

    for attribute in config["attributes"]:
        class_occurrences[attribute["name"]] = {}

        for attribute_category in attribute["labels"]:
            if attribute_category == "":
                continue

            class_occurrences[attribute["name"]][attribute_category] = set()

    for image_name in mappings.keys():
        class_name = int(image_name.split('.')[0])
        classes.add(class_name)

        for attribute_name in mappings[image_name]["labels"].keys():
            attribute_categories = mappings[image_name]["labels"][attribute_name]

            if isinstance(attribute_categories, list):
                for attribute_category in attribute_categories:
                    if attribute_category != header.dataset_delimiter_label.join([attribute_name, "none"]):
                        class_occurrences[attribute_name][attribute_category].add(class_name)
            else:
                if attribute_categories != header.dataset_delimiter_label.join([attribute_name, "none"]):
                    class_occurrences[attribute_name][attribute_categories].add(class_name)

    class_occurrences["classes"] = len(classes)

    return class_occurrences

def computeAttributeClassSpread(config):
    class_spreads = {}
    class_occurrences = countAttributeClassOccurrences(config)
    classes = class_occurrences["classes"]

    for attribute_name in class_occurrences.keys():
        if attribute_name == "classes":
            continue

        class_spread = 0

        for attribute_category in class_occurrences[attribute_name].keys():
            class_spread += (len(class_occurrences[attribute_name][attribute_category]) / classes)

        class_spread /= len(list(class_occurrences[attribute_name].keys()))
        class_spreads[attribute_name] = round(class_spread, 2)

    return class_spreads

def countUniqueAttributes(config):
    labels_map = {}
    mappings = config["mappings"]

    for image_name in mappings.keys():
        class_name = int(image_name.split('.')[0])

        if class_name not in labels_map:
            labels_map[class_name] = set()

    for image_name in mappings.keys():
        class_name = int(image_name.split('.')[0])
        labels = json.dumps(mappings[image_name]["labels"])
        labels_map[class_name].add(labels)

    return labels_map

def findDisjointClasses(labels_map):
    classes_disjoint = {}

    for class_name in labels_map.keys():
        classes_disjoint[class_name] = []

    for class_name in labels_map.keys():
        for class_name_other in labels_map.keys():
            if class_name == class_name_other:
                continue

            if (labels_map[class_name].isdisjoint(labels_map[class_name_other])):
                classes_disjoint[class_name].append(class_name_other)

    return classes_disjoint

def getRandomDisjointClasses(classes_disjoint, labels_map, max = 4):
    class_name = random.choice(list(classes_disjoint.keys()))
    classes_disjoint_random = {class_name}
    count = 1

    while count < max:
        class_name_random = random.choice(classes_disjoint[class_name])

        if classes_disjoint_random.issubset(classes_disjoint[class_name_random]) and len(labels_map[class_name_random]) > 1:
            classes_disjoint_random.add(class_name_random)
            count += 1

    return classes_disjoint_random

def main():
    config = {}

    with open(os.path.join(header.config_dir, header.cub_analysis_config_file_name), 'r') as file_config:
        config = json.load(file_config)

    attribute_class_spreads = computeAttributeClassSpread(config)
    attribute_class_spreads = dict(sorted(attribute_class_spreads.items(), key=lambda item: item[1], reverse = True))
    labels_map = countUniqueAttributes(config)
    classes_disjoint = findDisjointClasses(labels_map)
    classes_disjoint_random = getRandomDisjointClasses(classes_disjoint, labels_map)

    for attribute_name in attribute_class_spreads.keys():
        if attribute_class_spreads[attribute_name] < header.cub_analysis_balance_threshold:
            continue

        tabs = "\t"

        if len(attribute_name) <= 9:
            tabs = "\t\t"

        logger.log_info("Attribute with class spread >= " + str(int(header.cub_analysis_balance_threshold * 100)) + "%: " "\"" + attribute_name + "\"," + tabs + str(attribute_class_spreads[attribute_name]))

    for class_name in labels_map.keys():
        logger.log_debug("Total unique attributes for class " + str(class_name) + ": " + str(len(labels_map[class_name])))

    for class_name in classes_disjoint.keys():
        logger.log_debug("List of classes having disjoint attributes with class " + str(class_name) + ": ")
        logger.log_debug(classes_disjoint[class_name])

    logger.log_debug("List of random classes having disjoint attributes with each other: " + str(classes_disjoint_random))

    return

if __name__ == "__main__":
    main()
