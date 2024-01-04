#!/usr/bin/env python3

import argparse
import header
import json
import logger
import os
import random
import shutil

def initialize_directories():
    mtsd_sign_labels = os.listdir(header.dataset_dir_images_split_original_test)
    if not (os.path.isdir(header.mix_dataset_dir_images_split_mixed)):
        os.makedirs(header.mix_dataset_dir_images_split_mixed, exist_ok = True)

    for dir_name in mtsd_sign_labels:
        if os.path.isdir(os.path.join(header.mix_dataset_dir_images_split_mixed, dir_name)):
            continue
        path = os.path.join(header.mix_dataset_dir_images_split_mixed, dir_name)
        os.makedirs(path, exist_ok = True)

def sample_from_mtsd():
    mtsd_baseline_signs = []
    mtsd_signs = []
    mtsd_sign_dict = {}
    mtsd_sub_folders = os.listdir(header.dataset_dir_images_split_original_test)

    for sub_folder in mtsd_sub_folders:
        sub_folder_path = os.path.join(header.dataset_dir_images_split_original_test, sub_folder)
        mtsd_image_location = {os.path.join(sub_folder_path, i) : sub_folder for i in os.listdir(sub_folder_path)}
        mtsd_sub_signs = [os.path.join(sub_folder_path, i) for i in os.listdir(sub_folder_path)]
        mtsd_sign_dict.update(mtsd_image_location)
        random.shuffle(mtsd_sub_signs)

        mtsd_baseline_signs.append(mtsd_sub_signs[0])

        mtsd_sub_signs = mtsd_sub_signs[1:]
        mtsd_signs += mtsd_sub_signs

    mtsd_signs_count = len(mtsd_signs) + len(mtsd_baseline_signs)

    random.shuffle(mtsd_signs)
    signs_in_test = mtsd_baseline_signs + mtsd_signs[:int(header.mix_ratio * mtsd_signs_count)-len(mtsd_baseline_signs)]

    logger.log_debug(signs_in_test[0])
    logger.log_debug(mtsd_sign_dict[signs_in_test[0]])

    for sample in signs_in_test:
        source = sample
        destination = os.path.join(header.mix_dataset_dir_images_split_mixed, mtsd_sign_dict[sample])
        temp = os.path.split(source)[1]
        destination = os.path.join(destination, temp)
        logger.log_debug(source)
        logger.log_debug(destination)
        shutil.copyfile(source, destination)

    return mtsd_signs_count

def sample_from_gtsrb(arguments, mtsd_signs_count):
    non_existent_mappings = ["6", "30", "41", "42"]
    mapping_file = open(os.path.join(header.config_dir, header.mix_mapping_file_name_gtsrb))
    mappings = json.load(mapping_file)
    gtsrb_signs = []
    gtsrb_sign_dict = {}
    gtsrb_sub_folders = os.listdir(arguments.path_to_gtsrb)

    for sub_folder in gtsrb_sub_folders:
        if sub_folder in non_existent_mappings:
            continue
        sub_folder_path = os.path.join(arguments.path_to_gtsrb, sub_folder)
        gtsrb_image_location = {os.path.join(sub_folder_path, i) : sub_folder for i in os.listdir(sub_folder_path)}
        gtsrb_sub_signs =  [os.path.join(sub_folder_path, i) for i in os.listdir(sub_folder_path)]
        gtsrb_sign_dict.update(gtsrb_image_location)
        gtsrb_signs += gtsrb_sub_signs

    random.shuffle(gtsrb_signs)
    signs_in_test = gtsrb_signs[:int((1 - header.mix_ratio) * mtsd_signs_count)]

    for sample in signs_in_test:
        source = sample
        destination = os.path.join(header.mix_dataset_dir_images_split_mixed, mappings[gtsrb_sign_dict[sample]]["MTSD"])
        temp = os.path.split(source)[1]
        destination = os.path.join(destination, temp)
        logger.log_debug(source)
        logger.log_debug(destination)
        shutil.copyfile(source, destination)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-g", "--path-to-gtsrb", type = str, default = "", help = "Path to GTSRB dataset.", required = True)

    arguments = parser.parse_args()

    initialize_directories()
    mtsd_signs_count = sample_from_mtsd()
    sample_from_gtsrb(arguments, mtsd_signs_count)

if __name__ == "__main__":
    main()
