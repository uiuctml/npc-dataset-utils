#!/usr/bin/env python3

import header
import json
import logger
import os

def constructFileKeySetOriginal(dir_split):
    file_key_set = set()

    if os.path.isdir(dir_split):
        dirs_label = os.listdir(dir_split)

        for dir_label in dirs_label:
            file_names = os.listdir(os.path.join(dir_split, dir_label))

            for file_name in file_names:
                file_key = file_name.split(header.dataset_file_extension_images)[0]

                if file_key in file_key_set:
                    logger.log_error("Duplicated file key \"" + file_key + "\" in \"" + dir_split + "\".")
                    continue

                file_key_set.add(file_key)

    return file_key_set

def constructFileKeySetGenerated(dir_split):
    file_key_set = set()

    if os.path.isdir(dir_split):
        file_names = os.listdir(dir_split)

        for file_name in file_names:
            if file_name == header.dataset_config_file_name or file_name == header.generate_config_file_name:
                continue

            file_key = file_name.split(header.dataset_delimiter_file_name)[-1].split(header.dataset_file_extension_images)[0]

            if file_key in file_key_set:
                logger.log_error("Duplicated file key \"" + file_key + "\" in \"" + dir_split + "\".")
                continue

            file_key_set.add(file_key)

    return file_key_set

def verifyDatasetConfigMissing(config_dataset, config_generate):
    labels_dataset_set_dataset = set()
    labels_dataset_set_generate = set()

    for dataset in config_dataset["datasets"]:
        labels_dataset = dataset["labels"]

        for label_dataset in labels_dataset:
            labels_dataset_set_dataset.add(label_dataset)

    for label_original in config_generate.keys():
        if len(config_generate[label_original]["labels"]) > 0:
            for dataset_name in config_generate[label_original]["labels"].keys():
                labels_dataset_set_generate.add(config_generate[label_original]["labels"][dataset_name])

    for label_dataset_generate in labels_dataset_set_generate:
        if label_dataset_generate not in labels_dataset_set_dataset:
            logger.log_error("\"" + label_dataset_generate + "\" is missing.")

    return

def verifyDatasetConfigUnused(config_dataset, config_generate):
    labels_dataset_set = set()

    for label_original in config_generate.keys():
        if len(config_generate[label_original]["labels"]) > 0:
            for dataset_name in config_generate[label_original]["labels"].keys():
                labels_dataset_set.add(config_generate[label_original]["labels"][dataset_name])

    for dataset in config_dataset["datasets"]:
        labels_dataset = dataset["labels"]

        for label_dataset in labels_dataset:
            if label_dataset != "" and label_dataset not in labels_dataset_set:
                logger.log_error("\"" + label_dataset + "\" is unused.")

    return

def verifyDatasetConfig():
    file_path_config_dataset = os.path.join(header.config_dir, header.dataset_config_file_name)
    file_path_config_generate = os.path.join(header.config_dir, header.generate_config_file_name)

    logger.log_info("Verifying \"" + file_path_config_dataset + "\"...")

    file_config_dataset = open(file_path_config_dataset, "r")
    config_dataset = json.load(file_config_dataset)
    file_config_dataset.close()

    file_config_generate = open(file_path_config_generate, "r")
    config_generate = json.load(file_config_generate)
    file_config_generate.close()

    verifyDatasetConfigMissing(config_dataset, config_generate)
    verifyDatasetConfigUnused(config_dataset, config_generate)

    return

def verifyDatasetSplitsEmpty():
    if os.path.isdir(header.dataset_dir_images_split_original):
        dataset_dir_images_split_list = os.listdir(header.dataset_dir_images_split_original)

        for dataset_name_split in dataset_dir_images_split_list:
            dataset_split = os.listdir(os.path.join(header.dataset_dir_images_split_original, dataset_name_split))

            for dataset_dir_labels in dataset_split:
                dataset_dir_labels_split = os.path.join(header.dataset_dir_images_split_original, dataset_name_split, dataset_dir_labels)
                dataset_dir_labels_split_list = os.listdir(dataset_dir_labels_split)

                if len(dataset_dir_labels_split_list) == 0:
                    logger.log_error("\"" + dataset_dir_labels + "\" has no data for dataset split \"" + dataset_name_split + "\".")

    return

def verifyDatasetSplitsMatching():
    file_key_set_generated_test = constructFileKeySetGenerated(header.dataset_dir_images_split_generated_test)
    file_key_set_generated_train = constructFileKeySetGenerated(header.dataset_dir_images_split_generated_train)
    file_key_set_generated_validate = constructFileKeySetGenerated(header.dataset_dir_images_split_generated_validate)
    file_key_set_original_test = constructFileKeySetOriginal(header.dataset_dir_images_split_original_test)
    file_key_set_original_train = constructFileKeySetOriginal(header.dataset_dir_images_split_original_train)
    file_key_set_original_validate = constructFileKeySetOriginal(header.dataset_dir_images_split_original_validate)

    if len(file_key_set_generated_test) != len(file_key_set_original_test):
        logger.log_error("Mismatch between dataset splits \"" + header.dataset_dir_images_split_generated_test + "\" and \"" + header.dataset_dir_images_split_original_test + "\".")

    if len(file_key_set_generated_train) != len(file_key_set_original_train):
        logger.log_error("Mismatch between dataset splits \"" + header.dataset_dir_images_split_generated_train + "\" and \"" + header.dataset_dir_images_split_original_train + "\".")

    if len(file_key_set_generated_validate) != len(file_key_set_original_validate):
        logger.log_error("Mismatch between dataset splits \"" + header.dataset_dir_images_split_generated_validate + "\" and \"" + header.dataset_dir_images_split_original_validate + "\".")

    for file_key_generated_test in file_key_set_generated_test:
        if file_key_generated_test not in file_key_set_original_test:
            logger.log_error("File key \"" + file_key_generated_test + "\" in \"" + header.dataset_dir_images_split_generated_test + "\" but not in \"" + header.dataset_dir_images_split_original_test + "\".")

    for file_key_generated_train in file_key_set_generated_train:
        if file_key_generated_train not in file_key_set_original_train:
            logger.log_error("File key \"" + file_key_generated_train + "\" in \"" + header.dataset_dir_images_split_generated_train + "\" but not in \"" + header.dataset_dir_images_split_original_train + "\".")

    for file_key_generated_validate in file_key_set_generated_validate:
        if file_key_generated_validate not in file_key_set_original_validate:
            logger.log_error("File key \"" + file_key_generated_validate + "\" in \"" + header.dataset_dir_images_split_generated_validate + "\" but not in \"" + header.dataset_dir_images_split_original_validate + "\".")

    return

def verifyDatasetSplits():
    logger.log_info("Verifying \"" + header.dataset_dir_images_split + "\"...")

    verifyDatasetSplitsEmpty()
    verifyDatasetSplitsMatching()

    return

def verifyGenerateConfigDuplicates(config_generate):
    label_map = {}

    for label_original in config_generate.keys():
        if len(config_generate[label_original]["labels"]) > 0:
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
