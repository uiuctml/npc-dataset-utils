#!/usr/bin/env python3

import header
import json
import logger
import os

attribute_whitelist = [
    "bill-shape",
    "shape",
    "head-pattern",
    "wing-pattern",
    "wing-color",
    "belly-color",
    "back-color"
]

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
    "color": 0.52,
    "shape": 0.63,
    "size": 0.64,
    "pattern": 0.73
}

attribute_category_thresholds = {
    "bill-shape": 0.4,
    "shape": 0.4,
    "head-pattern": 0.7,
    "wing-pattern": 1.0,
    "wing-color": 0.3,
    "belly-color": 0.3,
    "back-color": 0.3,
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
    attribute_whitelist = []

    for attribute_type in attribute_types.keys():
        for attribute_name in attribute_types[attribute_type]:
            if header.analysis_threshold_max:
                if attribute_class_spreads[attribute_name] < attribute_type_thresholds[attribute_type]:
                    continue
            else:
                if attribute_class_spreads[attribute_name] > attribute_type_thresholds[attribute_type]:
                    continue

            spaces = " "
            inequality = ">"

            if not header.analysis_threshold_max:
                inequality = "<"

            if len(attribute_type) <= 5:
                spaces = "\t "

            logger.log_info("Attribute type \"" + attribute_type + "\"" + spaces + "with class spread " + inequality + "= " + str(attribute_type_thresholds[attribute_type]) + ":\t" + str(attribute_class_spreads[attribute_name]) + "\tfor \"" + attribute_name + "\".")

            attribute_whitelist.append(attribute_name)

    return attribute_whitelist

def filterAttributeCategory(config, category_class_spreads, attribute_whitelist):
    categories_whitelist = {}

    for attribute_name in attribute_whitelist:
        for attribute in config["attributes"]:
            if attribute["name"] != attribute_name:
                continue

            categories_whitelist[attribute_name] = {}

            for category_name in attribute["labels"]:
                if category_name == "":
                    continue

                if attribute_name not in attribute_category_thresholds:
                    logger.log_fatal("Missing attribute category threshold for \"" + attribute_name + "\". Quit.")
                    exit(-1)

                if header.analysis_threshold_max:
                    if category_class_spreads[category_name] < attribute_category_thresholds[attribute_name]:
                        continue
                else:
                    if category_class_spreads[category_name] > attribute_category_thresholds[attribute_name]:
                        continue

                categories_whitelist[attribute_name][category_name] = category_class_spreads[category_name]

            categories_whitelist[attribute_name] = dict(sorted(categories_whitelist[attribute_name].items(), key=lambda item: item[1], reverse = True))

    inequality = ">"

    if not header.analysis_threshold_max:
        inequality = "<"

    for attribute_name in categories_whitelist.keys():
        for category_name in categories_whitelist[attribute_name].keys():
            logger.log_info("Attribute category with class spread " + inequality + "= " + str(attribute_category_thresholds[attribute_name]) + ":\t" + str(category_class_spreads[category_name]) + "\tfor \"" + category_name + "\".")

    logger.log_info("attribute_category_whitelist =", json.dumps(categories_whitelist, indent = 4))

    return categories_whitelist

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
    global attribute_whitelist
    config = {}

    with open(os.path.join(header.config_dir, header.analysis_config_file_name), 'r') as file_config:
        config = json.load(file_config)

    if header.analysis_compute_matrix_a_size:
        computeMatrixASize(config)

    if header.analysis_filter_attributes_categories:
        class_occurrences = countAttributeClassOccurrences(config)
        attribute_class_spreads = computeAttributeClassSpread(class_occurrences)
        category_class_spreads = computeCategoryClassSpread(class_occurrences)

        if len(attribute_whitelist) <= 0:
            attribute_whitelist = filterAttribute(attribute_class_spreads)
        else:
            logger.log_info("Manual attribute whitelist used.")

        filterAttributeCategory(config, category_class_spreads, attribute_whitelist)

    if header.analysis_filter_classes_instances:
        pass

    return

if __name__ == "__main__":
    main()
