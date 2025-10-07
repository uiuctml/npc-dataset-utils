"""
@file   utility.py
@author Simon Yu
@date   05/26/2023
@brief  Utility functions.
"""

import random

def pruneAttributes(attributes, mappings):
    attributes_map = {}

    for attribute in attributes:
        attribute["labels"] = [""]
        attributes_map[attribute["name"]] = set()

    for image_name in mappings.keys():
        labels = mappings[image_name]["labels"]

        for attribute_name in labels.keys():
            if isinstance(labels[attribute_name], list):
                for label in labels[attribute_name]:
                    attributes_map[attribute_name].add(label)
            else:
                attributes_map[attribute_name].add(labels[attribute_name])

    for attribute in attributes:
        attribute["labels"] += sorted(list(attributes_map[attribute["name"]]))

    return attributes

def shuffleUniform(list, seed):
    rand = random.Random()
    rand.seed(seed)
    rand.shuffle(list)

    return list
