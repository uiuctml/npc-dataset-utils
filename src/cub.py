#!/usr/bin/env python3

import header
import json
import logger
import os

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
        images_map[line_split[0]] = line_split[1]
        mappings[line_split[1]] = {"labels": labels_default.copy()}

    file_images.close()

    for line in file_image_attribute_labels.readlines():
        line = line.rstrip()
        line_split = line.split(' ')
        image_name = images_map[line_split[0]]

        if line_split[2] == "0":
            continue

        logger.log_info_raw("[INFO]: Reading mappings for \"" + image_name + "\"", end = '\r')

        attribute = attributes[1][line_split[1]]
        attribute_name = attribute.split(header.dataset_delimiter_label)[0]

        if isinstance(mappings[image_name]["labels"][attribute_name], str):
            if mappings[image_name]["labels"][attribute_name] == header.dataset_delimiter_label.join([attribute_name, "none"]):
                mappings[image_name]["labels"][attribute_name] = attribute
            else:
                logger.log_warn("Multiple values for attribute \"" + attribute_name + "\" for instance \"" + image_name + "\".")
                mappings[image_name]["labels"][attribute_name] = [mappings[image_name]["labels"][attribute_name], attribute]
        elif isinstance(mappings[image_name]["labels"][attribute_name], list):
            mappings[image_name]["labels"][attribute_name].append(attribute)

    file_image_attribute_labels.close()

    logger.log_info_raw()

    return mappings

def main():
    attributes = readAttributes()
    mappings = readMappings(attributes)
    config = {}
    config["instance_wise"] = True
    config["attributes"] = attributes[0]
    config["mappings"] = mappings

    with open(os.path.join(header.config_dir, header.dataset_config_file_name), 'w') as file_config:
        json.dump(config, file_config, indent = 4)

    return

if __name__ == "__main__":
    main()
