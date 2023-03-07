#!/usr/bin/env python3

import header
import json
import logger
import os
import random
import tqdm

def createSymlinks(dataset_name, split_name, file_names, dir_source, dir_target, create_config_symlinks):
    progress_bar = tqdm.tqdm(total = len(file_names))
    progress_bar.set_description_str("[INFO]: Creating dataset split \"" + dataset_name + "/" + split_name + "\".")
    file_name_counter = 1

    for file_name in file_names:
        progress_bar.n = file_name_counter
        progress_bar.refresh()

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

def shuffleUniform(file_names):
    random.seed(header.split_random_seed)
    random.shuffle(file_names)

    return file_names

def split(config_split, dataset_name, file_names, dataset_dir, split_dir_test, split_dir_train, split_dir_validate, split_percentage_train, split_percentage_validate, create_config_symlinks = False):
    file_names_test = []
    file_names_train = []
    file_names_validate = []
    file_path_config_split = os.path.join(header.config_dir, header.split_config_file_name)
    split_name_test = os.path.basename(split_dir_test)
    split_name_train = os.path.basename(split_dir_train)
    split_name_validate = os.path.basename(split_dir_validate)

    if header.split_load:
        file_config_split = open(file_path_config_split, "r")
        config_split = json.load(file_config_split)
        file_config_split.close()

        file_names_test = config_split[dataset_name][split_name_test]
        file_names_train = config_split[dataset_name][split_name_train]
        file_names_validate = config_split[dataset_name][split_name_validate]

        logger.log_info("Loaded splits for dataset \"" + dataset_name + "\" from \"" + file_path_config_split + "\".")
    else:
        split_point_validate_test = int(len(file_names) * (split_percentage_train + split_percentage_validate))
        split_point_train_validate = int(len(file_names) * split_percentage_train)

        shuffleUniform(file_names)

        file_names_test = file_names[split_point_validate_test:]
        file_names_train = file_names[:split_point_train_validate]
        file_names_validate = file_names[split_point_train_validate:split_point_validate_test]

        logger.log_info("Generated splits for dataset \"" + dataset_name + "\" from seed " + str(header.split_random_seed) + ".")

    if header.split_save:
        config_split[dataset_name] = {}
        config_split[dataset_name][split_name_test] = file_names_test
        config_split[dataset_name][split_name_train] = file_names_train
        config_split[dataset_name][split_name_validate] = file_names_validate

        with open(file_path_config_split, "w") as file_config_split:
            json.dump(config_split, file_config_split, indent = 4)

        logger.log_info("Saved splits for dataset \"" + dataset_name + "\" to \"" + file_path_config_split + "\".")

    createSymlinks(dataset_name, split_name_test, file_names_test, dataset_dir, split_dir_test, create_config_symlinks)
    createSymlinks(dataset_name, split_name_train, file_names_train, dataset_dir, split_dir_train, create_config_symlinks)
    createSymlinks(dataset_name, split_name_validate, file_names_validate, dataset_dir, split_dir_validate, create_config_symlinks)

    return

def main():
    config_split = {}

    if not os.path.isdir(header.dataset_dir_images_split_generated):
        dataset_name = os.path.basename(header.dataset_dir_images_split_generated)
        file_names = os.listdir(header.dataset_dir_images_sliced_generated)

        file_names.remove(header.dataset_config_file_name)
        file_names.remove(header.generate_config_file_name)

        os.makedirs(header.dataset_dir_images_split_generated_test, exist_ok = True)
        os.makedirs(header.dataset_dir_images_split_generated_train, exist_ok = True)
        os.makedirs(header.dataset_dir_images_split_generated_validate, exist_ok = True)

        split(config_split, dataset_name, file_names, header.dataset_dir_images_sliced_generated, header.dataset_dir_images_split_generated_test, header.dataset_dir_images_split_generated_train, header.dataset_dir_images_split_generated_validate, header.split_generated_percentage_train, header.split_generated_percentage_validate, True)

    if not os.path.isdir(header.dataset_dir_images_split_original):
        dataset_name = os.path.basename(header.dataset_dir_images_split_original)
        file_names = []
        dirs_label = os.listdir(header.dataset_dir_images_sliced_original)

        for dir_label in dirs_label:
            file_names_label = os.listdir(os.path.join(header.dataset_dir_images_sliced_original, dir_label))

            for file_name_label in file_names_label:
                file_names.append(os.path.join(dir_label, file_name_label))

        os.makedirs(header.dataset_dir_images_split_original_test, exist_ok = True)
        os.makedirs(header.dataset_dir_images_split_original_train, exist_ok = True)
        os.makedirs(header.dataset_dir_images_split_original_validate, exist_ok = True)

        split(config_split, dataset_name, file_names, header.dataset_dir_images_sliced_original, header.dataset_dir_images_split_original_test, header.dataset_dir_images_split_original_train, header.dataset_dir_images_split_original_validate, header.split_original_percentage_train, header.split_original_percentage_validate)

    return

if __name__ == "__main__":
    main()
