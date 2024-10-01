#!/usr/bin/env python3

import header
import json
import os

def readAttributes():
    config_attributes = {}
    config_attributes_list = []
    config_attributes_map = {}

    file_config_attributes = open(os.path.join(header.cub_dir_attributes, header.cub_file_name_attributes), 'r')

    for line in file_config_attributes.readlines():
        line = line.rstrip()
        line_split = line.split(' ')
        attribute = '-'.join(line_split[1].split('_')[1:])
        attribute_split = attribute.split("::")
        attribute = header.dataset_delimiter_label.join(attribute_split)

        if attribute_split[0] not in config_attributes:
            config_attributes[attribute_split[0]] = [header.dataset_delimiter_label.join([attribute_split[0], "none"])]

        config_attributes[attribute_split[0]].append(attribute)
        config_attributes_map[line_split[0]] = attribute

    file_config_attributes.close()

    for attribute_name in config_attributes.keys():
        config_attribute = {}

        config_attribute["name"] = attribute_name
        config_attribute["labels"] = [""] + sorted(config_attributes[attribute_name])

        config_attributes_list.append(config_attribute)

    return (config_attributes_list, config_attributes_map)

def readMappings(config_attributes_map):
    config_mappings = {}

    file_config_attributes = open(os.path.join(header.cub_dir_attributes, header.cub_file_name_attributes), 'r')

    return config_mappings

def main():
    config = {}

    config_attributes = readAttributes()
    config_mappings = readMappings(config_attributes[1])

    config["attributes"] = config_attributes[0]
    config["mappings"] = config_mappings

    with open(os.path.join(header.config_dir, header.dataset_config_file_name), 'w') as file_config:
        json.dump(config, file_config, indent = 4)

    return

if __name__ == "__main__":
    main()
