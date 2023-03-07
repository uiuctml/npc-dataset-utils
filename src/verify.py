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

def verifyGenerateConfigDuplicates(config_generate):
    label_map = {}

    for label_original in config_generate.keys():
        if len(config_generate[label_original]["labels"]) != 0:
            labels_dataset = ""

            for dataset_name in config_generate[label_original]["labels"].keys():
                label_dataset = config_generate[label_original]["labels"][dataset_name]

                if labels_dataset != "":
                    labels_dataset += header.dataset_delimiter_file_name

                labels_dataset += label_dataset

            if labels_dataset not in label_map:
                label_map[labels_dataset] = [label_original]
            else:
                label_map[labels_dataset].append(label_original)

    for label_dataset in label_map.keys():
        labels_original_list = label_map[label_dataset]

        if len(labels_original_list) > 1:
            labels_original = ", ".join(labels_original_list)
            logger.log_error("\"" + labels_original + "\" contain identical labels.")

    return

def verifyGenerateConfigLabels(config_generate):
    for label_original in config_generate.keys():
        if len(config_generate[label_original]["labels"]) == 0:
            logger.log_error("\"" + label_original + "\" does not contain any labels.")
        else:
            for dataset_name in config_generate[label_original]["labels"].keys():
                if config_generate[label_original]["labels"][dataset_name] == "":
                    logger.log_error("\"" + label_original + "\" contains an empty label for dataset \"" + dataset_name + "\".")
                elif config_generate[label_original]["labels"][dataset_name].split(header.dataset_delimiter_label)[0] != dataset_name:
                    logger.log_error("\"" + label_original + "\" contains an invalid label for dataset \"" + dataset_name + "\".")

    return

def verifyGenerateConfigWeights(config_generate):
    for label_original in config_generate.keys():
        if len(config_generate[label_original]["weights"]) == 0:
                logger.log_error("\"" + label_original + "\" does not contain any weights.")
        else:
            weights_sum = 0

            for dataset_name in config_generate[label_original]["weights"].keys():
                weights_sum += config_generate[label_original]["weights"][dataset_name]

            if weights_sum == 0:
                logger.log_error("\"" + label_original + "\" contains zero weights.")

    return

def verifyGenerateConfigReductions(config_generate):    
    for label_original in config_generate.keys():
        reduction = config_generate[label_original]["reduction"]

        if reduction == "":
            logger.log_error("\"" + label_original + "\" contains an empty reduction.")

    return

def verifyGenerateConfig():
    file_path_config_generate = os.path.join(header.config_dir, header.generate_config_file_name)

    logger.log_info("Verifying \"" + file_path_config_generate + "\"...")

    file_config_generate = open(file_path_config_generate, "r")
    config_generate = json.load(file_config_generate)
    file_config_generate.close()

    verifyGenerateConfigDuplicates(config_generate)
    verifyGenerateConfigLabels(config_generate)
    verifyGenerateConfigWeights(config_generate)
    verifyGenerateConfigReductions(config_generate)

    return

def main():
    verifyDatasetConfig()
    verifyDatasetSplits()
    verifyGenerateConfig()

    return

if __name__ == "__main__":
    main()
