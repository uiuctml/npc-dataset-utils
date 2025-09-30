#!/usr/bin/env python3

import header
import json
import os
import tqdm

def main():
    file_gtsrb_config = open(os.path.join(header.config_dir, header.label_config_file_name), "r")
    gtsrb_config = json.load(file_gtsrb_config)
    file_gtsrb_config.close()

    dir_name_counter = 1
    dir_names = os.listdir(header.dataset_dir_instances_processed)
    progress_bar = tqdm.tqdm(total = len(dir_names))

    for dir_name in dir_names:
        if dir_name not in gtsrb_config["labels"]:
            dir_name_counter += 1
            continue

        label_name = gtsrb_config["labels"][dir_name]

        progress_bar.set_description_str("[INFO]: Renaming \"" + dir_name + "\" to \"" + label_name + "\"")
        progress_bar.n = dir_name_counter
        progress_bar.refresh()

        if os.path.isdir(os.path.join(header.dataset_dir_instances_processed, dir_name)):
            os.rename(os.path.join(header.dataset_dir_instances_processed, dir_name), os.path.join(header.dataset_dir_instances_processed, label_name))

        dir_name_counter += 1

    progress_bar.close()

    return

if __name__ == "__main__":
    main()
