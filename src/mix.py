import header
import json
import logger
import os
import random
import shutil


def initialize_directories():
    mtsd_sign_labels = os.listdir(header.dataset_mtsd_test)
    if not (os.path.isdir(header.dataset_mixed_test)):
        os.mkdir(header.dataset_mixed_test)

    for dir_name in mtsd_sign_labels:
        if os.path.isdir(os.path.join(header.dataset_mixed_test, dir_name)):
            continue
        path = os.path.join(header.dataset_mixed_test, dir_name)
        os.mkdir(path)

def sample_from_mtsd():
    mtsd_baseline_signs = []
    mtsd_signs = []
    mtsd_sign_dict = {}
    mtsd_sub_folders = os.listdir(header.dataset_mtsd_test)

    for sub_folder in mtsd_sub_folders:
        sub_folder_path = os.path.join(header.dataset_mtsd_test, sub_folder)
        mtsd_image_location = {os.path.join(sub_folder_path, i) : sub_folder for i in os.listdir(sub_folder_path)}
        mtsd_sub_signs =  [os.path.join(sub_folder_path, i) for i in os.listdir(sub_folder_path)]
        mtsd_sign_dict = mtsd_sign_dict | mtsd_image_location
        random.shuffle(mtsd_sub_signs)
        mtsd_baseline_signs += mtsd_sub_signs[0]
        mtsd_sub_signs = mtsd_sub_sign[1:]
        mtsd_signs += mtsd_sub_signs
        

    random.shuffle(mtsd_signs)
    signs_in_test = mtsd_baseline_signs + mtsd_signs[:int(header.ratio_for_mixing * header.test_dataset_size)-len(mtsd_baseline_signs)]

    logger.log_debug(signs_in_test[0])
    logger.log_debug(mtsd_sign_dict[signs_in_test[0]])

    for sample in signs_in_test:
        source = sample
        destination = os.path.join(header.dataset_mixed_test, mtsd_sign_dict[sample])
        temp = os.path.split(source)[1]
        destination = os.path.join(destination, temp)
        logger.log_debug(source)
        logger.log_debug(destination)
        shutil.copyfile(source, destination)

def sample_from_gtsrb():
    non_existent_mappings = ["6", "30", "41", "42"]
    mapping_file = open(header.mapping_file_path)
    mappings = json.load(mapping_file)
    gtsrb_signs = []
    gtsrb_sign_dict = {}
    gtsrb_sub_folders = os.listdir(header.dataset_gtsrb_test)

    for sub_folder in gtsrb_sub_folders:
        if sub_folder in non_existent_mappings:
            continue
        sub_folder_path = os.path.join(header.dataset_gtsrb_test, sub_folder)
        gtsrb_image_location = {os.path.join(sub_folder_path, i) : sub_folder for i in os.listdir(sub_folder_path)}
        gtsrb_sub_signs =  [os.path.join(sub_folder_path, i) for i in os.listdir(sub_folder_path)]
        gtsrb_sign_dict = gtsrb_sign_dict | gtsrb_image_location
        gtsrb_signs += gtsrb_sub_signs

    random.shuffle(gtsrb_signs)
    signs_in_test = gtsrb_signs[:int((1 - header.ratio_for_mixing) * header.test_dataset_size)]

    for sample in signs_in_test:
        source = sample
        destination = os.path.join(header.dataset_mixed_test, mappings[gtsrb_sign_dict[sample]]["MTSD"])
        temp = os.path.split(source)[1]
        destination = os.path.join(destination, temp)
        logger.log_debug(source)
        logger.log_debug(destination)
        shutil.copyfile(source, destination)

def main():
    initialize_directories()
    sample_from_mtsd()
    sample_from_gtsrb()

if __name__ == "__main__":
    main()