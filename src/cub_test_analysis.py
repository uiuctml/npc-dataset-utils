#!/usr/bin/env python3

import header
import json
import logger
import os
import random

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
    file_name_config_list = header.dataset_config_file_name.split('.')
    file_name_config = '.'.join([file_name_config_list[0] + "_test", file_name_config_list[1]])

    with open(os.path.join(header.config_dir, file_name_config), 'r') as file_config:
        config = json.load(file_config)

    labels_map = countUniqueAttributes(config)
    classes_disjoint = findDisjointClasses(labels_map)
    classes_disjoint_random = getRandomDisjointClasses(classes_disjoint, labels_map)

    for class_name in labels_map.keys():
        logger.log_info("Total unique attributes for class " + str(class_name) + ": " + str(len(labels_map[class_name])))

    for class_name in classes_disjoint.keys():
        logger.log_info("List of classes having disjoint attributes with class " + str(class_name) + ": ")
        logger.log_info(classes_disjoint[class_name])

    logger.log_info("List of random classes having disjoint attributes with each other: " + str(classes_disjoint_random))

    return

if __name__ == "__main__":
    main()
