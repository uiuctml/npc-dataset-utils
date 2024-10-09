#!/usr/bin/env python3

import header
import json
import logger
import os

def countAttributeVariations(config):
    counts = {}
    labels_map = {}
    mappings = config["mappings"]

    for image_name in mappings.keys():
        class_name = image_name.split('/')[0]

        if class_name not in labels_map:
            labels_map[class_name] = set()

        if class_name not in counts:
            counts[class_name] = 0

    for image_name in mappings.keys():
        class_name = image_name.split('/')[0]
        labels = json.dumps(mappings[image_name]["labels"])

        if labels not in labels_map[class_name]:
            counts[class_name] += 1

        labels_map[class_name].add(labels)

    return counts

def main():
    config = {}
    file_name_config_list = header.dataset_config_file_name.split('.')
    file_name_config = '.'.join([file_name_config_list[0] + "_test", file_name_config_list[1]])

    with open(os.path.join(header.config_dir, file_name_config), 'r') as file_config:
        config = json.load(file_config)

    counts = countAttributeVariations(config)

    logger.log_info(counts)

    return

if __name__ == "__main__":
    main()
