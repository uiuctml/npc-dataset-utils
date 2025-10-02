#!/usr/bin/env python3

"""
@file   gtsrb.py
@author Simon Yu
@date   01/09/2024
@brief  Script for GTSRB dataset.
"""

import header
import json
import logger
import os
import tqdm

def main():
    if os.path.exists(header.dataset_dir_instances_processed):
        logger.log_info("Processed instance directory exists. Skip.")
        return

    file_gtsrb_config = open(os.path.join(header.config_dir, header.label_config_file_name), "r")
    gtsrb_config = json.load(file_gtsrb_config)
    file_gtsrb_config.close()

    dir_name_counter = 1
    dir_names = os.listdir(header.dataset_dir_instances_original)
    progress_bar = tqdm.tqdm(total = len(dir_names))

    os.makedirs(header.dataset_dir_instances_processed, exist_ok = True)

    for dir_name in dir_names:
        if dir_name not in gtsrb_config["labels"]:
            dir_name_counter += 1
            continue

        label_name = gtsrb_config["labels"][dir_name]

        progress_bar.set_description_str("[INFO]: Creating symlink for category \"" + label_name + "\"")
        progress_bar.n = dir_name_counter
        progress_bar.refresh()

        if os.path.isdir(os.path.join(header.dataset_dir_instances_original, dir_name)):
            os.symlink(os.path.abspath(os.path.join(header.dataset_dir_instances_original, dir_name)), os.path.join(header.dataset_dir_instances_processed, label_name))

        dir_name_counter += 1

    progress_bar.close()

    return

if __name__ == "__main__":
    main()
