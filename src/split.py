#!/usr/bin/env python3

import gzip
import header
import json
import logger
import numpy
import os
import random as rand
import tqdm
import type

def createSymlinks(dataset_name, file_keys, file_map, dir_source, dir_target, create_config_symlinks = False):
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

    if create_config_symlinks:
        os.symlink(os.path.abspath(os.path.join(dir_source, header.dataset_config_file_name)), os.path.join(dir_target, header.dataset_config_file_name))
        os.symlink(os.path.abspath(os.path.join(dir_source, header.generate_config_file_name)), os.path.join(dir_target, header.generate_config_file_name))

    progress_bar.close()

    return

def shuffleUniform(file_keys, random_seed):
    random = rand.Random()
    random.seed(random_seed)
    random.shuffle(file_keys)

    return file_keys

def thresholdOutsideSTD(value, mean, std):
    std_scaled = std * header.split_std_scaler

    if value > (mean + std_scaled) or value < (mean - std_scaled):
        return True

    return False

def generateSplitsByPercentage(file_keys):
    split_point_validate_test = int(len(file_keys) * (header.split_percentage_train + header.split_percentage_validate))
    split_point_train_validate = int(len(file_keys) * header.split_percentage_train)

    shuffleUniform(file_keys, header.split_random_seed_percentage)

    file_keys_test = file_keys[split_point_validate_test:]
    file_keys_train = file_keys[:split_point_train_validate]
    file_keys_validate = file_keys[split_point_train_validate:split_point_validate_test]

    logger.log_info("Generated dataset splits from seed " + str(header.split_random_seed_percentage) + ".")

    return (file_keys_test, file_keys_train, file_keys_validate)

def generateSplitsByStatistics(file_keys):
    config_stats = {}
    file_path_config_stats = os.path.join(header.config_dir, header.stats_config_file_name)

    if os.path.isfile(file_path_config_stats):
        file_config_stats = gzip.open(file_path_config_stats, "r")
        config_stats_json_encoded = file_config_stats.read()
        file_config_stats.close()

        config_stats_json = config_stats_json_encoded.decode("utf-8")
        config_stats = json.loads(config_stats_json)

    average_brightnesses = numpy.array(list(config_stats["average_brightnesses"].values()))

    average_brightnesses_mean = numpy.mean(average_brightnesses)
    average_brightnesses_std = numpy.std(average_brightnesses)

    file_keys_test = []
    file_keys_train_validate = []

    for file_key in file_keys:
        average_brightness = config_stats["average_brightnesses"][file_key]

        if thresholdOutsideSTD(average_brightness, average_brightnesses_mean, average_brightnesses_std):
            file_keys_test.append(file_key)
        else:
            file_keys_train_validate.append(file_key)

    logger.log_info("Generated testing dataset split from \"" + file_path_config_stats + "\".")

    split_point_train_validate = int(len(file_keys_train_validate) * header.split_percentage_train)

    shuffleUniform(file_keys_train_validate, header.split_random_seed_stats)

    file_keys_train = file_keys_train_validate[:split_point_train_validate]
    file_keys_validate = file_keys_train_validate[split_point_train_validate:]

    logger.log_info("Generated training and validation dataset splits from seed " + str(header.split_random_seed_stats) + ".")

    return (file_keys_test, file_keys_train, file_keys_validate)

def generateSplits(file_keys):
    if header.split_basis == type.SplitBasis.percentage:
        return generateSplitsByPercentage(file_keys)
    elif header.split_basis == type.SplitBasis.statistics:
        return generateSplitsByStatistics(file_keys)

    logger.log_warn("Unknown split basis.")

    return generateSplitsByPercentage(file_keys)

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

    logger.log_info("Loaded dataset splits from \"" + file_path_config_split + "\".")

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
    dataset_name = os.path.basename(header.dataset_dir_images_split_original)
    file_keys = []
    file_keys_test = []
    file_keys_train = []
    file_keys_validate = []
    file_map = {}
    dirs_label = os.listdir(header.dataset_dir_images_sliced_original)

    for dir_label in dirs_label:
        file_names = os.listdir(os.path.join(header.dataset_dir_images_sliced_original, dir_label))

        for file_name in file_names:
            file_key = file_name.split(header.dataset_file_extension_images)[0]
            file_keys.append(file_key)

            if file_key in file_map:
                logger.log_error("Duplicated file key \"" + file_key + "\".")
                return

            file_map[file_key] = os.path.join(dir_label, file_name)

    if header.split_load:
        (file_keys_test, file_keys_train, file_keys_validate) = loadSplits(header.dataset_dir_images_split_original_test, header.dataset_dir_images_split_original_train, header.dataset_dir_images_split_original_validate)
    else:
        (file_keys_test, file_keys_train, file_keys_validate) = generateSplits(file_keys)

        if header.split_save:
            saveSplits(file_keys_test, file_keys_train, file_keys_validate, header.dataset_dir_images_split_original_test, header.dataset_dir_images_split_original_train, header.dataset_dir_images_split_original_validate)

    if header.split_create_symlinks and not os.path.isdir(header.dataset_dir_images_split_original):
        createSymlinks(dataset_name, file_keys_test, file_map, header.dataset_dir_images_sliced_original, header.dataset_dir_images_split_original_test)
        createSymlinks(dataset_name, file_keys_train, file_map, header.dataset_dir_images_sliced_original, header.dataset_dir_images_split_original_train)
        createSymlinks(dataset_name, file_keys_validate, file_map, header.dataset_dir_images_sliced_original, header.dataset_dir_images_split_original_validate)

    dataset_name = os.path.basename(header.dataset_dir_images_split_generated)
    file_map = {}
    file_names = os.listdir(header.dataset_dir_images_sliced_generated)

    for file_name in file_names:
        file_key = file_name.split(header.dataset_delimiter_file_name)[-1].split(header.dataset_file_extension_images)[0]
        file_map[file_key] = file_name

    if header.split_create_symlinks and not os.path.isdir(header.dataset_dir_images_split_generated):
        createSymlinks(dataset_name, file_keys_test, file_map, header.dataset_dir_images_sliced_generated, header.dataset_dir_images_split_generated_test, True)
        createSymlinks(dataset_name, file_keys_train, file_map, header.dataset_dir_images_sliced_generated, header.dataset_dir_images_split_generated_train, True)
        createSymlinks(dataset_name, file_keys_validate, file_map, header.dataset_dir_images_sliced_generated, header.dataset_dir_images_split_generated_validate, True)

    return

if __name__ == "__main__":
    main()
