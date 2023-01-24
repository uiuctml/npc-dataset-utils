#!/usr/bin/env python3

import header
import json
import logger
import os

def main():
    file_generate_config = open(os.path.join(header.config_dir, header.generate_config_file_name), "r")
    generate_config = json.load(file_generate_config)
    file_generate_config.close()

    for label in generate_config.keys():
        if len(generate_config[label]) == 0:
            logger.log_error("\"" + label + "\" does not contain any label.")
        else:
            for dataset_name in generate_config[label].keys():
                if generate_config[label][dataset_name] == "":
                    logger.log_error("\"" + label + "\" contains an empty label for dataset \"" + dataset_name + "\".")
                elif generate_config[label][dataset_name].split(header.dataset_label_delimiter)[0] != dataset_name:
                    logger.log_error("\"" + label + "\" contains an invalid label for dataset \"" + dataset_name + "\".")

    return

if __name__ == "__main__":
    main()
