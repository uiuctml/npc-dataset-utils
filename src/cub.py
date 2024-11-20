#!/usr/bin/env python3

import header
import json
import logger
import os

attribute_category_whitelist = {
    "primary-color": {
        "primary-color--black": 0.995,
        "primary-color--grey": 0.985,
        "primary-color--brown": 0.92,
        "primary-color--white": 0.92,
        "primary-color--buff": 0.89
    },
    "upperparts-color": {
        "upperparts-color--black": 0.995,
        "upperparts-color--grey": 0.99,
        "upperparts-color--white": 0.96,
        "upperparts-color--brown": 0.945,
        "upperparts-color--buff": 0.895
    },
    "tail-shape": {
        "tail-shape--pointed-tail": 1.0,
        "tail-shape--notched-tail": 0.995,
        "tail-shape--rounded-tail": 0.995,
        "tail-shape--squared-tail": 0.975,
        "tail-shape--fan-shaped-tail": 0.96
    },
    "wing-shape": {
        "wing-shape--pointed-wings": 1.0,
        "wing-shape--rounded-wings": 1.0,
        "wing-shape--tapered-wings": 0.96,
        "wing-shape--broad-wings": 0.875,
        "wing-shape--long-wings": 0.845
    },
    "size": {
        "size--small-(5---9-in)": 0.99,
        "size--very-small-(3---5-in)": 0.93,
        "size--medium-(9---16-in)": 0.875
    },
    "bill-length": {
        "bill-length--shorter-than-head": 0.975,
        "bill-length--about-the-same-as-head": 0.965
    },
    "wing-pattern": {
        "wing-pattern--multi-colored": 0.995,
        "wing-pattern--striped": 0.98,
        "wing-pattern--solid": 0.965,
        "wing-pattern--spotted": 0.775
    },
    "head-pattern": {
        "head-pattern--eyering": 0.99,
        "head-pattern--plain": 0.98,
        "head-pattern--eyeline": 0.96,
        "head-pattern--capped": 0.925,
        "head-pattern--malar": 0.92,
        "head-pattern--eyebrow": 0.915,
        "head-pattern--striped": 0.795
    },
    "back-pattern": {
        "back-pattern--multi-colored": 0.99,
        "back-pattern--solid": 0.98,
        "back-pattern--striped": 0.94,
        "back-pattern--spotted": 0.72
    }
}
class_whitelist = {}

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

def readAttributes():
    attributes = {}
    attributes_list = []
    attributes_map = {}
    file_attributes = open(os.path.join(header.cub_dir_attributes, header.cub_file_name_attributes), 'r')

    for line in file_attributes.readlines():
        line = line.rstrip()
        line_split = line.split(' ')
        attribute = '-'.join(line_split[1].split('_')[1:])
        attribute_split = attribute.split("::")
        attribute_name = attribute_split[0]
        attribute_category = header.dataset_delimiter_label.join(attribute_split)

        if len(attribute_category_whitelist) > 0 and attribute_name not in attribute_category_whitelist:
            continue

        if attribute_name not in attributes:
            attributes[attribute_name] = [header.dataset_delimiter_label.join([attribute_name, "none"])]

        if len(attribute_category_whitelist) > 0 and attribute_category in attribute_category_whitelist[attribute_name]:
            attributes[attribute_name].append(attribute_category)
            attributes_map[line_split[0]] = attribute_category

    file_attributes.close()

    for attribute_name in attributes.keys():
        attribute = {}

        attribute["name"] = attribute_name
        attribute["labels"] = [""] + sorted(attributes[attribute_name])

        attributes_list.append(attribute)

    return (attributes_list, attributes_map)

def readMappings(attributes):
    file_images = open(os.path.join(header.dataset_dir_annotations, header.cub_file_name_images), 'r')
    file_image_attribute_labels = open(os.path.join(header.cub_dir_attributes, header.cub_file_name_image_attribute_labels), 'r')
    images_map = {}
    labels_default = {}
    mappings = {}

    for attribute in attributes[0]:
        labels_default[attribute["name"]] = header.dataset_delimiter_label.join([attribute["name"], "none"])

    for line in file_images.readlines():
        line = line.rstrip()
        line_split = line.split(' ')
        image_name = line_split[1]
        class_name = image_name.split('/')[0]

        if len(class_whitelist) > 0 and class_name not in class_whitelist:
            continue

        images_map[line_split[0]] = image_name
        mappings[image_name] = {"labels": labels_default.copy()}

    file_images.close()

    for line in file_image_attribute_labels.readlines():
        line = line.rstrip()
        line_split = line.split(' ')

        if line_split[0] not in images_map:
            continue

        image_name = images_map[line_split[0]]
        class_name = image_name.split('/')[0]
        file_name = image_name.split('/')[1]

        if len(class_whitelist) > 0 and class_name not in class_whitelist:
            continue

        if line_split[2] == "0":
            continue

        logger.log_info_raw("\033[K[INFO]: Reading mappings for \"" + file_name + "\"", end = '\r')

        if line_split[1] not in attributes[1]:
            continue

        attribute_category = attributes[1][line_split[1]]
        attribute_name = attribute_category.split(header.dataset_delimiter_label)[0]

        if len(attribute_category_whitelist) > 0 and attribute_category in attribute_category_whitelist[attribute_name]:
            if isinstance(mappings[image_name]["labels"][attribute_name], list):
                mappings[image_name]["labels"][attribute_name].append(attribute_category)
            else:
                if mappings[image_name]["labels"][attribute_name] == header.dataset_delimiter_label.join([attribute_name, "none"]):
                    mappings[image_name]["labels"][attribute_name] = attribute_category
                else:
                    mappings[image_name]["labels"][attribute_name] = [mappings[image_name]["labels"][attribute_name], attribute_category]

    file_image_attribute_labels.close()

    logger.log_info_raw()

    return mappings

def main():
    attributes = readAttributes()
    mappings = readMappings(attributes)
    config = {}
    config["instance_wise"] = True
    config["attributes"] = pruneAttributes(attributes[0], mappings)
    config["mappings"] = mappings

    with open(os.path.join(header.config_dir, header.dataset_config_file_name), 'w') as file_config:
        json.dump(config, file_config, indent = 4)

    return

if __name__ == "__main__":
    main()
