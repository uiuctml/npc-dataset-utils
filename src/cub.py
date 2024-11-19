#!/usr/bin/env python3

import header
import json
import logger
import os

attributes_whitelist = {}
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
        attribute = header.dataset_delimiter_label.join(attribute_split)

        if len(attributes_whitelist) > 0 and attribute_split[0] not in attributes_whitelist:
            continue

        if attribute_split[0] not in attributes:
            attributes[attribute_split[0]] = [header.dataset_delimiter_label.join([attribute_split[0], "none"])]

        attributes[attribute_split[0]].append(attribute)
        attributes_map[line_split[0]] = attribute

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

        attribute = attributes[1][line_split[1]]
        attribute_name = attribute.split(header.dataset_delimiter_label)[0]

        if isinstance(mappings[image_name]["labels"][attribute_name], list):
            mappings[image_name]["labels"][attribute_name].append(attribute)
        else:
            if mappings[image_name]["labels"][attribute_name] == header.dataset_delimiter_label.join([attribute_name, "none"]):
                mappings[image_name]["labels"][attribute_name] = attribute
            else:
                mappings[image_name]["labels"][attribute_name] = [mappings[image_name]["labels"][attribute_name], attribute]

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
