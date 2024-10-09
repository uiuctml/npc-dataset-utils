#!/usr/bin/env python3

import header
import json
import logger
import os
import pickle

attributes_cbm = [1, 4, 6, 7, 10, 14, 15, 20, 21, 23, 25, 29, 30, 35, 36, 38, 40, 44, 45, 50, 51, 53, 54, 56, 57, 59, 63, 64, 69, 70, 72, 75, 80, 84, 90, 91, 93, 99, 101, 106, 110, 111, 116, 117, 119, 125, 126, 131, 132, 134, 145, 149, 151, 152, 153, 157, 158, 163, 164, 168, 172, 178, 179, 181, 183, 187, 188, 193, 194, 196, 198, 202, 203, 208, 209, 211, 212, 213, 218, 220, 221, 225, 235, 236, 238, 239, 240, 242, 243, 244, 249, 253, 254, 259, 260, 262, 268, 274, 277, 283, 289, 292, 293, 294, 298, 299, 304, 305, 308, 309, 310, 311]
attributes_cbm_set = set(attributes_cbm)

def readAttributes():
    attributes = {}
    attributes_list = []
    attributes_map = {}
    file_attributes = open(os.path.join(header.cub_dir_attributes, header.cub_file_name_attributes), 'r')

    for line in file_attributes.readlines():
        line = line.rstrip()
        line_split = line.split(' ')

        if int(line_split[0]) not in attributes_cbm_set:
            continue

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

def readImageAttributeLabels():
    image_attribute_labels = {}
    instances = []

    for file_name in [header.cub_file_name_split_cbm_test, header.cub_file_name_split_cbm_train, header.cub_file_name_split_cbm_validate]:
        with open(os.path.join(header.cub_dir_splits_cbm, file_name), 'rb') as file:
            instances += pickle.load(file)

    for instance in instances:
        name = '/'.join(instance["img_path"].split('/')[-2:])
        attribute_labels = instance["attribute_label"]
        image_attribute_labels[name] = attribute_labels

    return image_attribute_labels

def readMappings(attributes):
    file_images = open(os.path.join(header.dataset_dir_annotations, header.cub_file_name_images), 'r')
    image_attribute_labels = readImageAttributeLabels()
    labels_default = {}
    mappings = {}

    for attribute in attributes[0]:
        labels_default[attribute["name"]] = header.dataset_delimiter_label.join([attribute["name"], "none"])

    for line in file_images.readlines():
        line = line.rstrip()
        line_split = line.split(' ')
        image_name = line_split[1]
        mappings[image_name] = {"labels": labels_default.copy()}

        logger.log_info_raw("[INFO]: Reading mappings for \"" + image_name + "\"", end = '\r')

        for (attribute_index, attribute_value) in zip(attributes_cbm, image_attribute_labels[image_name]):
            if attribute_value == 0:
                continue

            attribute = attributes[1][str(attribute_index)]
            attribute_name = attribute.split(header.dataset_delimiter_label)[0]

            if isinstance(mappings[image_name]["labels"][attribute_name], str):
                if mappings[image_name]["labels"][attribute_name] == header.dataset_delimiter_label.join([attribute_name, "none"]):
                    mappings[image_name]["labels"][attribute_name] = attribute
                else:
                    logger.log_warn("Multiple values for attribute \"" + attribute_name + "\" for instance \"" + image_name + "\".")
                    mappings[image_name]["labels"][attribute_name] = [mappings[image_name]["labels"][attribute_name], attribute]
            elif isinstance(mappings[image_name]["labels"][attribute_name], list):
                mappings[image_name]["labels"][attribute_name].append(attribute)

    file_images.close()

    logger.log_info_raw()

    return mappings

def main():
    attributes = readAttributes()
    mappings = readMappings(attributes)
    config = {}
    config["attributes"] = attributes[0]
    config["mappings"] = mappings
    file_name_config_list = header.dataset_config_file_name.split('.')
    file_name_config = '.'.join([file_name_config_list[0] + "_cbm", file_name_config_list[1]])

    with open(os.path.join(header.config_dir, file_name_config), 'w') as file_config:
        json.dump(config, file_config, indent = 4)

    return

if __name__ == "__main__":
    main()
