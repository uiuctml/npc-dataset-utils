"""
@file   utility.py
@author Simon Yu
@date   05/26/2023
@brief  Utility functions.
"""

import natsort
import numpy
import random

def getLabelsAttribute(dataset_config):
    labels_attribute = {}

    for attribute in dataset_config["attributes"]:
        if "" in attribute["labels"]:
            attribute["labels"].remove("")

        labels_attribute[attribute["name"]] = attribute["labels"]

    return labels_attribute

def getLabelsOriginal(dataset_config):
    if "instance_wise" in dataset_config and dataset_config["instance_wise"]:
        labels_original = []
        labels_original_set = set()

        for image_name in dataset_config["mappings"].keys():
            class_name = image_name.split('/')[0]

            if class_name not in labels_original_set:
                labels_original.append(class_name)
                labels_original_set.add(class_name)

        return natsort.natsorted(labels_original)
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

def getIndicesFromLabelsOriginal(labels_original):
    labels_to_indices = {}

    for i in range(len(labels_original)):
        labels_to_indices[labels_original[i]] = i

    return labels_to_indices

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

def setSeed(seed):
    random.seed(seed)
    numpy.random.seed(seed)

    return

def shuffleUniform(list, seed):
    rand = random.Random()
    rand.seed(seed)
    rand.shuffle(list)

    return list
