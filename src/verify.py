#!/usr/bin/env python3

import header
import json
import logger
import os

def main():
    file_path_config = os.path.join(header.config_dir, header.generate_config_file_name)

    logger.log_info("Verifying \"" + file_path_config + "\"...")

    file_generate_config = open(file_path_config, "r")
    generate_config = json.load(file_generate_config)
    file_generate_config.close()

    for label in generate_config.keys():
        if len(generate_config[label]) == 0:
            logger.log_error("\"" + label + "\" does not contain any label.")
        else:
            for dataset_name in generate_config[label].keys():
                if generate_config[label][dataset_name] == "":
                    logger.log_error("\"" + label + "\" contains an empty label for dataset \"" + dataset_name + "\".")
                elif generate_config[label][dataset_name].split(header.dataset_delimiter_label)[0] != dataset_name:
                    logger.log_error("\"" + label + "\" contains an invalid label for dataset \"" + dataset_name + "\".")

    logger.log_info_raw("\n")
    logger.log_info("Verifying \"" + header.dataset_dir_images_split + "\"...")

    if os.path.isdir(header.verify_dataset_dir_images_split):
        dataset_dir_images_split_list = os.listdir(header.verify_dataset_dir_images_split)

        for dataset_name_split in dataset_dir_images_split_list:
            dataset_split = os.listdir(os.path.join(header.verify_dataset_dir_images_split, dataset_name_split))

            for dataset_dir_labels in dataset_split:
                dataset_dir_labels_split = os.path.join(header.verify_dataset_dir_images_split, dataset_name_split, dataset_dir_labels)
                dataset_dir_labels_split_list = os.listdir(dataset_dir_labels_split)

                if len(dataset_dir_labels_split_list) == 0:
                    logger.log_error("\"" + dataset_dir_labels + "\" has no data for split dataset \"" + dataset_name_split + "\".")
                elif len(dataset_dir_labels_split_list) == 1 and dataset_dir_labels_split_list[-1] == header.split_file_name_symlink_placeholder:
                    logger.log_warn("\"" + dataset_dir_labels + "\" has placeholder data for split dataset \"" + dataset_name_split + "\".")

    return

if __name__ == "__main__":
    main()
