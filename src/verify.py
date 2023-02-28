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
        if len(generate_config[label]["labels"]) == 0:
            logger.log_error("\"" + label + "\" does not contain any labels.")
        else:
            for dataset_name in generate_config[label]["labels"].keys():
                if generate_config[label]["labels"][dataset_name] == "":
                    logger.log_error("\"" + label + "\" contains an empty label for dataset \"" + dataset_name + "\".")
                elif generate_config[label]["labels"][dataset_name].split(header.dataset_delimiter_label)[0] != dataset_name:
                    logger.log_error("\"" + label + "\" contains an invalid label for dataset \"" + dataset_name + "\".")

        if len(generate_config[label]["weights"]) == 0:
            logger.log_error("\"" + label + "\" does not contain any weights.")
        else:
            weights_sum = 0

            for dataset_name in generate_config[label]["weights"].keys():
                weights_sum += generate_config[label]["weights"][dataset_name]

            if weights_sum == 0:
                logger.log_error("\"" + label + "\" contains zero weights.")
            elif weights_sum < 1:
                logger.log_error("\"" + label + "\" contains weights summing up less than one.")
            elif weights_sum > 1:
                logger.log_error("\"" + label + "\" contains weights summing up greater than one.")

        reduction = generate_config[label]["reduction"]

        if reduction == "":
            logger.log_error("\"" + label + "\" contains an empty reduction.")

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
