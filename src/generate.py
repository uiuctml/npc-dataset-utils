#!/usr/bin/env python3

import header
import json
import logger
import os
import shutil
import tqdm

def main():
    if os.path.isdir(os.path.join(header.dataset_dir_images_sliced_generated)):
        return

    dataset_dir_images_list = os.listdir(header.generate_dataset_dir_images)
    dataset_dir_labels_counter = 1
    progress_bar = tqdm.tqdm(total = len(dataset_dir_images_list))

    file_generate_config = open(os.path.join(header.config_dir, header.generate_config_file_name), "r")
    generate_config = json.load(file_generate_config)
    file_generate_config.close()

    for dataset_dir_labels in dataset_dir_images_list:
        progress_bar.set_description_str("Processing \"" + dataset_dir_labels + "\"")
        progress_bar.n = dataset_dir_labels_counter
        progress_bar.refresh()

        dataset_dir_labels_counter += 1

        label_combined = ""

        for dataset_name in generate_config[dataset_dir_labels]["labels"].keys():
            label = generate_config[dataset_dir_labels]["labels"][dataset_name]

            if label == "":
                logger.log_warn("\"" + dataset_dir_labels + "\" contains an empty label for dataset \"" + dataset_name + "\".")
                label = dataset_name + header.dataset_delimiter_label + header.dataset_label_undefined_keyword

            if label_combined != "":
                label_combined += header.dataset_delimiter_file_name

            label_combined += label

        label_combined += header.dataset_delimiter_file_name
        label_combined += dataset_dir_labels

        dataset_dir_images_original_label = os.path.join(header.generate_dataset_dir_images, dataset_dir_labels)
        dataset_images_list = os.listdir(dataset_dir_images_original_label)

        if len(dataset_images_list) == 0:
            logger.log_warn("\"" + dataset_dir_labels + "\" has no data.")

        if not os.path.isdir(header.dataset_dir_images_sliced_generated):
            os.makedirs(header.dataset_dir_images_sliced_generated, exist_ok = True)

        for file_name_image in dataset_images_list:
            file_key = file_name_image.split(".")[0]
            file_name_image_generated = label_combined + header.dataset_delimiter_file_name + file_key + header.dataset_file_extension_images

            os.symlink(os.path.abspath(os.path.join(dataset_dir_images_original_label, file_name_image)), os.path.join(header.dataset_dir_images_sliced_generated, file_name_image_generated))

        shutil.copyfile(os.path.join(header.config_dir, header.dataset_config_file_name), os.path.join(header.dataset_dir_images_sliced_generated, header.dataset_config_file_name))
        shutil.copyfile(os.path.join(header.config_dir, header.generate_config_file_name), os.path.join(header.dataset_dir_images_sliced_generated, header.generate_config_file_name))

    progress_bar.close()

    return

if __name__ == "__main__":
    main()
