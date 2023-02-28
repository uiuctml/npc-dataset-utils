#!/usr/bin/env python3

import header
import os
import random
import tqdm

def splitGenerated():
    if os.path.isdir(header.dataset_dir_images_split_generated):
        return

    os.makedirs(header.dataset_dir_images_split_generated_test, exist_ok = True)
    os.makedirs(header.dataset_dir_images_split_generated_train, exist_ok = True)
    os.makedirs(header.dataset_dir_images_split_generated_validate, exist_ok = True)

    file_names = os.listdir(header.dataset_dir_images_sliced_generated)
    split_point_validate_test = int(len(file_names) * (header.split_generated_percentage_train + header.split_generated_percentage_validate))
    split_point_train_validate = int(len(file_names) * header.split_generated_percentage_train)

    random.shuffle(file_names)

    file_names_test = file_names[split_point_validate_test:]
    file_names_train = file_names[:split_point_train_validate]
    file_names_validate = file_names[split_point_train_validate:split_point_validate_test]

    progress_bar_test = tqdm.tqdm(total = len(file_names_test))
    progress_bar_test.set_description_str("Splitting testing dataset")
    file_name_counter_test = 1

    for file_name_test in file_names_test:
        progress_bar_test.n = file_name_counter_test
        progress_bar_test.refresh()

        os.symlink(os.path.abspath(os.path.join(header.dataset_dir_images_sliced_generated, file_name_test)), os.path.join(header.dataset_dir_images_split_generated_test, file_name_test))

        file_name_counter_test += 1

    progress_bar_test.close()
    progress_bar_train = tqdm.tqdm(total = len(file_names_train))
    progress_bar_train.set_description_str("Splitting training dataset")
    file_name_counter_train = 1

    for file_name_train in file_names_train:
        progress_bar_train.n = file_name_counter_train
        progress_bar_train.refresh()

        os.symlink(os.path.abspath(os.path.join(header.dataset_dir_images_sliced_generated, file_name_train)), os.path.join(header.dataset_dir_images_split_generated_train, file_name_train))

        file_name_counter_train += 1

    progress_bar_train.close()
    progress_bar_validate = tqdm.tqdm(total = len(file_names_validate))
    progress_bar_validate.set_description_str("Splitting validation dataset")
    file_name_counter_validate = 1

    for file_name_validate in file_names_validate:
        progress_bar_validate.n = file_name_counter_validate
        progress_bar_validate.refresh()

        os.symlink(os.path.abspath(os.path.join(header.dataset_dir_images_sliced_generated, file_name_validate)), os.path.join(header.dataset_dir_images_split_generated_validate, file_name_validate))

        file_name_counter_validate += 1

    progress_bar_validate.close()

    return

def splitOriginal():
    if os.path.isdir(header.dataset_dir_images_split_original):
        return

    return

def main():
    splitGenerated()
    splitOriginal()

    return

if __name__ == "__main__":
    main()
