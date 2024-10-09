#!/usr/bin/env python3

import header
import json
import logger
import os

def readAttributes():
    attributes_list = []
    attributes_map = {}

    return (attributes_list, attributes_map)

def readMappings(attributes):
    mappings = {}

    return mappings

def main():
    attributes = readAttributes()
    mappings = readMappings(attributes)
    config = {}
    config["attributes"] = attributes[0]
    config["mappings"] = mappings

    with open(os.path.join(header.config_dir, header.dataset_config_file_name), 'w') as file_config:
        json.dump(config, file_config, indent = 4)

    return

if __name__ == "__main__":
    main()
