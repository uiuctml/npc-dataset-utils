#!/usr/bin/env python3

"""
@file   split.py
@author Simon Yu
@date   01/25/2023
@brief  Script for splitting datasets.
"""

import gzip
import header
import json
import logger
import os
import tqdm
import utility

def createSymlinks(dataset_name, file_keys, file_map, dir_source, dir_target):
    file_name_counter = 1
    split_name = os.path.basename(dir_target)
    progress_bar = tqdm.tqdm(total = len(file_keys))

    os.makedirs(dir_target, exist_ok = True)
    progress_bar.set_description_str("[INFO]: Creating symlinks for \"" + dataset_name + "/" + split_name + "\"")

    for file_key in file_keys:
        progress_bar.n = file_name_counter
        progress_bar.refresh()

        file_name = file_map[file_key]
        dir_name_test = os.path.dirname(file_name)

        if dir_name_test != "":
            os.makedirs(os.path.join(dir_target, dir_name_test), exist_ok = True)

        os.symlink(os.path.abspath(os.path.join(dir_source, file_name)), os.path.join(dir_target, file_name))

        file_name_counter += 1

    progress_bar.close()

    return

def generateSplits(file_keys):
    split_point_validate_test = int(len(file_keys) * (header.split_percentage_train + header.split_percentage_validate))
    split_point_train_validate = int(len(file_keys) * header.split_percentage_train)

    file_keys = utility.shuffleUniform(file_keys, header.split_seed)

    file_keys_test = file_keys[split_point_validate_test:]
    file_keys_train = file_keys[:split_point_train_validate]
    file_keys_validate = file_keys[split_point_train_validate:split_point_validate_test]

    logger.log_info("Generated dataset splits from seed " + str(header.split_seed) + ".")

    return (file_keys_test, file_keys_train, file_keys_validate)

def loadSplits(split_dir_test, split_dir_train, split_dir_validate):
    file_path_config_split = os.path.join(header.config_dir, header.split_config_file_name)
    split_name_test = os.path.basename(split_dir_test)
    split_name_train = os.path.basename(split_dir_train)
    split_name_validate = os.path.basename(split_dir_validate)

    file_config_split = gzip.open(file_path_config_split, "r")
    config_split_json_encoded = file_config_split.read()
    file_config_split.close()

    config_split_json = config_split_json_encoded.decode("utf-8")
    config_split = json.loads(config_split_json)

    file_keys_test = config_split[split_name_test]
    file_keys_train = config_split[split_name_train]
    file_keys_validate = config_split[split_name_validate]

    logger.log_info("Loaded dataset splits \"" + file_path_config_split + "\".")

    return (file_keys_test, file_keys_train, file_keys_validate)

def saveSplits(file_keys_test, file_keys_train, file_keys_validate, split_dir_test, split_dir_train, split_dir_validate):
    config_split = {}
    file_path_config_split = os.path.join(header.config_dir, header.split_config_file_name)
    split_name_test = os.path.basename(split_dir_test)
    split_name_train = os.path.basename(split_dir_train)
    split_name_validate = os.path.basename(split_dir_validate)

    config_split[split_name_test] = file_keys_test
    config_split[split_name_train] = file_keys_train
    config_split[split_name_validate] = file_keys_validate

    config_split_json = json.dumps(config_split, indent = 4)
    config_split_json_encoded = config_split_json.encode("utf-8")

    with gzip.open(file_path_config_split, "w") as file_config_split:
        file_config_split.write(config_split_json_encoded)

    logger.log_info("Saved dataset splits to \"" + file_path_config_split + "\".")

    return

def main():
    dataset_name = os.path.basename(header.dataset_dir_splits_instances)
    file_keys = []
    file_keys_test = []
    file_keys_train = []
    file_keys_validate = []
    file_map = {}
    dirs_label = os.listdir(header.split_dataset_dir_images)

    for dir_label in dirs_label:
        file_names = os.listdir(os.path.join(header.split_dataset_dir_images, dir_label))

        for file_name in file_names:
            file_key = file_name.split(header.dataset_file_extension_images)[0]
            file_keys.append(file_key)

            if file_key in file_map:
                logger.log_error("Duplicated file key \"" + file_key + "\".")
                return

            file_map[file_key] = os.path.join(dir_label, file_name)

    if header.split_load:
        (file_keys_test, file_keys_train, file_keys_validate) = loadSplits(header.dataset_dir_splits_instances_test, header.dataset_dir_splits_instances_train, header.dataset_dir_splits_instances_validate)
    else:
        (file_keys_test, file_keys_train, file_keys_validate) = generateSplits(file_keys)

        if header.split_save:
            saveSplits(file_keys_test, file_keys_train, file_keys_validate, header.dataset_dir_splits_instances_test, header.dataset_dir_splits_instances_train, header.dataset_dir_splits_instances_validate)

    if header.split_create_symlinks and not os.path.isdir(header.dataset_dir_splits_instances):
        createSymlinks(dataset_name, file_keys_test, file_map, header.split_dataset_dir_images, header.dataset_dir_splits_instances_test)
        createSymlinks(dataset_name, file_keys_validate, file_map, header.split_dataset_dir_images, header.dataset_dir_splits_instances_validate)
        createSymlinks(dataset_name, file_keys_train, file_map, header.split_dataset_dir_images, header.dataset_dir_splits_instances_train)
    else:
        logger.log_info("Split symlink directories exist in \"" + header.dataset_dir_splits_instances + "\". Skip.")

    return

if __name__ == "__main__":
    main()
