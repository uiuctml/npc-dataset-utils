#!/usr/bin/env python3

import header
import json
import os

attributes_types = {
    "color": {
        "black",
        "white",
        "blue",
        "brown",
        "gray",
        "orange",
        "red",
        "yellow"
    },
    "patterns": {
        "patches",
        "spots",
        "stripes"
    },
    "texture": {
        "furry",
        "hairless",
        "toughskin"
    },
    "physique": {
        "bulbous",
        "lean"
    },
    "feature": {
        "flippers",
        "hands",
        "hooves",
        "pads",
        "paws",
        "longleg",
        "longneck",
        "tail"
    },
    "weapon": {
        "horns",
        "claws",
        "tusks"
    },
    "limb": {
        "bipedal",
        "quadrapedal"
    },
}

def readAttributes():
    attributes = []

    for attribute_name in attributes_types.keys():
        attribute = {}
        attribute["name"] = attribute_name
        labels = []

        for label in attributes_types[attribute_name]:
            labels.append(header.dataset_delimiter_label.join([attribute_name, label]))

        attribute["labels"] = [""] + sorted(labels)
        attributes.append(attribute)

    return attributes

def readMappings():
    classes = []
    categories = []
    labels_default = {}
    mappings = {}

    with open(os.path.join(header.dataset_dir_annotations, header.awa_file_name_classes), 'r') as file_classes:
        for line in file_classes.readlines():
            line = line.rstrip()
            classes.append(line.split('\t')[1])

    with open(os.path.join(header.dataset_dir_annotations, header.awa_file_name_predicates), 'r') as file_predicates:
        for line in file_predicates.readlines():
            line = line.rstrip()
            categories.append(line.split('\t')[1])

    for attribute_name in attributes_types.keys():
        labels_default[attribute_name] = header.dataset_delimiter_label.join([attribute_name, "none"])

    for class_name in classes:
        mappings[class_name] = {"labels": labels_default.copy()}

    return mappings

def main():
    config = {}
    config["attributes"] = readAttributes()
    config["mappings"] = readMappings()

    with open(os.path.join(header.config_dir, header.dataset_config_file_name), 'w') as file_config:
        json.dump(config, file_config, indent = 4)

    return

if __name__ == "__main__":
    main()
