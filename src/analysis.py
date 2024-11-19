#!/usr/bin/env python3

import header
import json
import logger
import os
import random

attribute_types = {
    "color": [
        "primary-color",
        "upperparts-color",
        "wing-color",
        "bill-color",
        "underparts-color",
        "back-color",
        "nape-color",
        "leg-color",
        "breast-color",
        "under-tail-color",
        "crown-color",
        "forehead-color",
        "belly-color",
        "upper-tail-color",
        "throat-color",
        "eye-color"
    ],
    "shape": [
        "tail-shape",
        "wing-shape",
        "shape",
        "bill-shape"
    ],
    "size": [
        "size",
        "bill-length"
    ],
    "pattern": [
        "wing-pattern",
        "head-pattern",
        "back-pattern",
        "tail-pattern",
        "breast-pattern",
        "belly-pattern"
    ]
}

attribute_type_thresholds = {
    "color": 0.51,
    "shape": 0.62,
    "size": 0.61,
    "pattern": 0.72
}

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

def computeAttributeClassSpread(class_occurrences):
    class_spreads = {}
    classes = class_occurrences["classes"]

    for attribute_name in class_occurrences.keys():
        if attribute_name == "classes":
            continue

        class_spread = 0

        for attribute_category in class_occurrences[attribute_name].keys():
            class_spread += (len(class_occurrences[attribute_name][attribute_category]) / classes)

        class_spread /= len(list(class_occurrences[attribute_name].keys()))
        class_spreads[attribute_name] = round(class_spread, 2)

    class_spreads = dict(sorted(class_spreads.items(), key=lambda item: item[1], reverse = True))

    return class_spreads

def computeCategoryClassSpread(class_occurrences):
    class_spreads = {}
    classes = class_occurrences["classes"]

    for attribute_name in class_occurrences.keys():
        if attribute_name == "classes":
            continue

        for attribute_category in class_occurrences[attribute_name].keys():
            class_spread = len(class_occurrences[attribute_name][attribute_category]) / classes
            class_spreads[attribute_category] = class_spread

    class_spreads = dict(sorted(class_spreads.items(), key=lambda item: item[1], reverse = True))

    return class_spreads

def filterAttribute(attribute_class_spreads):
    attributes_filtered = []

    for attribute_type in attribute_types.keys():
        for attribute_name in attribute_types[attribute_type]:
            if attribute_class_spreads[attribute_name] <= attribute_type_thresholds[attribute_type]:
                continue

            tabs_attribute_name = "\t"
            tabs_attribute_type = " "

            if len(attribute_name) <= 9:
                tabs_attribute_name = "\t\t"

            if len(attribute_type) <= 5:
                tabs_attribute_type = "\t "

            logger.log_info("Attribute type \"" + attribute_type + "\"" + tabs_attribute_type + "with class spread > " + str(attribute_type_thresholds[attribute_type]) + ": " "\"" + attribute_name + "\"," + tabs_attribute_name + str(attribute_class_spreads[attribute_name]))

            attributes_filtered.append(attribute_name)

    return attributes_filtered

def filterAttributeCategory(config, category_class_spreads, attributes_filtered):
    categories_filtered = {}

    for attribute_name in attributes_filtered:
        pass

    return categories_filtered

def computeMatrixASize(config):
    classes = set()
    cols = 1
    rows = 0

    for attribute in config["attributes"]:
        count_categories = 0

        for attribute_category in attribute["labels"]:
            if attribute_category == "":
                continue

            count_categories += 1

        logger.log_info("Number of categories for \"" + attribute["name"] + "\": " + str(count_categories) + ".")

        cols *= count_categories

    for image_name in config["mappings"].keys():
        class_name = image_name.split('.')[0]
        classes.add(class_name)

    logger.log_info("Number of classes: " + str(len(classes)) + ".")

    rows = len(classes)
    bytes = rows * cols * 4
    gigabytes = bytes / 1000000000

    logger.log_info("\"" + header.analysis_config_file_name + "\" yields a " + str(gigabytes) + " GB matrix A.")

    return

def main():
    config = {}

    with open(os.path.join(header.config_dir, header.analysis_config_file_name), 'r') as file_config:
        config = json.load(file_config)

    computeMatrixASize(config)
    class_occurrences = countAttributeClassOccurrences(config)
    attribute_class_spreads = computeAttributeClassSpread(class_occurrences)
    category_class_spreads = computeCategoryClassSpread(class_occurrences)
    attributes_filtered = filterAttribute(attribute_class_spreads)
    filterAttributeCategory(config, category_class_spreads, attributes_filtered)

    return

if __name__ == "__main__":
    main()
