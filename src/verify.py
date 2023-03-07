#!/usr/bin/env python3

import header
import json
import logger
import os

def verifyDatasetConfig():
    return

def verifyDatasetSplits():
    logger.log_info("Verifying \"" + header.verify_dataset_dir_images_split + "\"...")

    if os.path.isdir(header.verify_dataset_dir_images_split):
        dataset_dir_images_split_list = os.listdir(header.verify_dataset_dir_images_split)

        for dataset_name_split in dataset_dir_images_split_list:
            dataset_split = os.listdir(os.path.join(header.verify_dataset_dir_images_split, dataset_name_split))

            for dataset_dir_labels in dataset_split:
                dataset_dir_labels_split = os.path.join(header.verify_dataset_dir_images_split, dataset_name_split, dataset_dir_labels)
                dataset_dir_labels_split_list = os.listdir(dataset_dir_labels_split)

                if len(dataset_dir_labels_split_list) == 0:
                    logger.log_error("\"" + dataset_dir_labels + "\" has no data for dataset split \"" + dataset_name_split + "\".")

    return

def verifyGenerateConfigLabels(generate_config, label):
    if len(generate_config[label]["labels"]) == 0:
        logger.log_error("\"" + label + "\" does not contain any labels.")
    else:
        for dataset_name in generate_config[label]["labels"].keys():
            if generate_config[label]["labels"][dataset_name] == "":
                logger.log_error("\"" + label + "\" contains an empty label for dataset \"" + dataset_name + "\".")
            elif generate_config[label]["labels"][dataset_name].split(header.dataset_delimiter_label)[0] != dataset_name:
                logger.log_error("\"" + label + "\" contains an invalid label for dataset \"" + dataset_name + "\".")

    return

def verifyGenerateConfigWeights(generate_config, label):
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

    return

def verifyGenerateConfigReductions(generate_config, label):
    reduction = generate_config[label]["reduction"]

    if reduction == "":
        logger.log_error("\"" + label + "\" contains an empty reduction.")

    return

def verifyGenerateConfig():
    file_path_generate_config = os.path.join(header.config_dir, header.generate_config_file_name)

    logger.log_info("Verifying \"" + file_path_generate_config + "\"...")

    file_generate_config = open(file_path_generate_config, "r")
    generate_config = json.load(file_generate_config)
    file_generate_config.close()

    for label in generate_config.keys():
        verifyGenerateConfigLabels(generate_config, label)
        verifyGenerateConfigWeights(generate_config, label)
        verifyGenerateConfigReductions(generate_config, label)

    return

def main():
    verifyDatasetSplits()
    verifyGenerateConfig()

    return

if __name__ == "__main__":
    main()
