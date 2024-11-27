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
        labels = [header.dataset_delimiter_label.join([attribute_name, "none"])]

        for label in attributes_types[attribute_name]:
            labels.append(header.dataset_delimiter_label.join([attribute_name, label]))

        attribute["labels"] = [""] + sorted(labels)
        attributes.append(attribute)

    return attributes

def readMappings():
    classes = []
    categories = []
    categories_types = []
    labels_default = {}
    mappings = {}
    matrix = {}

    for values in attributes_types.values():
        categories_types += list(values)

    categories_types = set(categories_types)

    with open(os.path.join(header.dataset_dir_annotations, header.awa_file_name_classes), 'r') as file_classes:
        for line in file_classes.readlines():
            line = line.rstrip()
            classes.append(line.split('\t')[1])

    with open(os.path.join(header.dataset_dir_annotations, header.awa_file_name_predicates), 'r') as file_predicates:
        for line in file_predicates.readlines():
            line = line.rstrip()
            categories.append(line.split('\t')[1])

    with open(os.path.join(header.dataset_dir_annotations, header.awa_file_name_matrix), 'r') as file_matrix:
        index_classes = 0

        for line in file_matrix.readlines():
            line = line.rstrip()
            flags = line.split(' ')
            index_categories = 0

            matrix[classes[index_classes]] = []

            for flag in flags:
                if flag == '1':
                    category_name = categories[index_categories]

                    if category_name in categories_types:
                        matrix[classes[index_classes]].append(category_name)

                index_categories += 1

            index_classes += 1

    for attribute_name in attributes_types.keys():
        labels_default[attribute_name] = header.dataset_delimiter_label.join([attribute_name, "none"])

    for class_name in classes:
        mappings[class_name] = {"labels": labels_default.copy()}

    for class_name in matrix.keys():
        for category_name in matrix[class_name]:
            for attribute_name in attributes_types.keys():
                if category_name in attributes_types[attribute_name]:
                    category_name = header.dataset_delimiter_label.join([attribute_name, category_name])

                    if isinstance(mappings[class_name]["labels"][attribute_name], list):
                        mappings[class_name]["labels"][attribute_name].append(category_name)
                    else:
                        if mappings[class_name]["labels"][attribute_name] == header.dataset_delimiter_label.join([attribute_name, "none"]):
                            mappings[class_name]["labels"][attribute_name] = category_name
                        else:
                            mappings[class_name]["labels"][attribute_name] = [mappings[class_name]["labels"][attribute_name], category_name]

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
