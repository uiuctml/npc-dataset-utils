#!/usr/bin/env python3

import cv2
import header
import json
import logger
import numpy
import os
import PIL.Image
import struct
import tqdm
import utility

def extractImages(file_name_images):
    with open(os.path.join(header.dataset_dir_images_original, file_name_images),"rb") as file:
        (magic, image_count) = struct.unpack(">II", file.read(8))
        (image_height, image_width) = struct.unpack(">II", file.read(8))
        images = numpy.fromfile(file, dtype = numpy.dtype(numpy.uint8).newbyteorder('>'))
        images = images.reshape((image_count, image_height, image_width))

    return images

def extractLabels(file_name_labels):
    with open(os.path.join(header.dataset_dir_annotations, file_name_labels),"rb") as file:
        (magic, label_count) = struct.unpack(">II", file.read(8))
        labels = numpy.fromfile(file, dtype = numpy.dtype(numpy.uint8).newbyteorder('>'))
        labels = labels.reshape((label_count,))

    return labels

def saveImages(images, labels):
    image_count = images.shape[0]
    progress_bar = tqdm.tqdm(total = image_count)
    progress_bar.set_description_str("[INFO]: Saving images")

    os.makedirs(header.dataset_dir_images_sliced, exist_ok = True)

    for i in range(0, image_count):
        image = PIL.Image.fromarray(images[i])
        label = labels[i]
        file_name_image = str(i).rjust(len(str(image_count)), '0') + header.mnist_file_extension_images
        file_path_label = os.path.join(header.dataset_dir_images_sliced, str(label))
        progress_bar.n = i + 1
        progress_bar.refresh()

        if not os.path.exists(file_path_label):
            os.mkdir(file_path_label)

        image.save(os.path.join(file_path_label, file_name_image))

    progress_bar.close()

    return

def createAdditionAttributes():
    classes = [""] + sorted(os.listdir(header.dataset_dir_images_sliced))
    config_attributes = []

    for attribute_name in header.mnist_attributes:
        attribute = {}
        attribute["name"] = attribute_name
        attribute["labels"] = classes
        config_attributes.append(attribute)

    return config_attributes

def createAdditionDataset():
    classes = os.listdir(header.dataset_dir_images_sliced)
    config = {}
    config_mappings = {}
    file_paths = []
    image_combined_count = 0

    for class_index in classes:
        file_names = os.listdir(os.path.join(header.dataset_dir_images_sliced, class_index))
        file_paths += [os.path.join(header.dataset_dir_images_sliced, class_index, file_name) for file_name in file_names]

    file_paths = utility.shuffleUniform(file_paths, header.mnist_random_seed)
    progress_bar = tqdm.tqdm(total = len(file_paths) // 2)
    progress_bar.set_description_str("[INFO]: Creating addition dataset")

    os.makedirs(header.mnist_dir_images_addition, exist_ok = True)

    for i in range(0, len(file_paths) - 1, 2):
        progress_bar.n = image_combined_count + 1
        progress_bar.refresh()
        image_combined_count += 1
        labels = {}

        file_path_first = file_paths[i]
        file_path_second = file_paths[i + 1]
        class_first = os.path.basename(os.path.dirname(file_path_first))
        class_second = os.path.basename(os.path.dirname(file_path_second))
        class_combined = str(int(class_first) + int(class_second))
        file_name_first = os.path.basename(file_path_first)
        file_name_second = os.path.basename(file_path_second)
        file_name_combined = file_name_first.split('.')[0] + '_' + file_name_second.split('.')[0] + header.mnist_file_extension_images
        file_path_combined = os.path.join(header.mnist_dir_images_addition, class_combined, file_name_combined)
        image_first = cv2.imread(file_path_first)
        image_second = cv2.imread(file_path_second)
        image_combined = cv2.hconcat([image_first, image_second])

        os.makedirs(os.path.join(header.mnist_dir_images_addition, class_combined), exist_ok = True)
        cv2.imwrite(file_path_combined, image_combined)

        labels[header.mnist_attributes[0]] = class_first
        labels[header.mnist_attributes[1]] = class_second
        config_mappings[os.path.join(class_combined, file_name_combined)] = {}
        config_mappings[os.path.join(class_combined, file_name_combined)]["labels"] = labels

    progress_bar.close()

    config["instance_wise"] = True
    config["attributes"] = createAdditionAttributes()
    config["mappings"] = config_mappings

    with open(os.path.join(header.config_dir, header.dataset_config_file_name), 'w') as file_config:
        json.dump(config, file_config, indent = 4)

    return

def main():
    if not os.path.exists(header.dataset_dir_images_sliced):
        images_test = extractImages(header.mnist_file_name_images_test)
        images_train = extractImages(header.mnist_file_name_images_train)
        labels_test = extractLabels(header.mnist_file_name_labels_test)
        labels_train = extractLabels(header.mnist_file_name_labels_train)
        images = numpy.concatenate((images_test, images_train), axis = 0)
        labels = numpy.concatenate((labels_test, labels_train), axis = 0)

        logger.log_debug("Testing image array shape:", images_test.shape)
        logger.log_debug("Training image array shape:", images_train.shape)
        logger.log_debug("Combined image array shape:", images.shape)
        logger.log_debug("Testing label array shape:", labels_test.shape)
        logger.log_debug("Training label array shape:", labels_train.shape)
        logger.log_debug("Combined label array shape:", labels.shape)

        saveImages(images, labels)
    else:
        logger.log_info("Images exist. Skip.")

    if not os.path.exists(header.mnist_dir_images_addition):
        createAdditionDataset()
    else:
        logger.log_info("Addition dataset exists. Skip.")

    return

if __name__ == "__main__":
    main()
