#!/usr/bin/env python3

import header
import json
import logger
import os

attribute_whitelist = {}
class_whitelist = {}

def readAttributes():
    return {}

def readMappings():
    return {}

def main():
    config = {}
    config["attributes"] = readAttributes()
    config["mappings"] = readMappings()

    with open(os.path.join(header.config_dir, header.dataset_config_file_name), 'w') as file_config:
        json.dump(config, file_config, indent = 4)

    return

if __name__ == "__main__":
    main()
