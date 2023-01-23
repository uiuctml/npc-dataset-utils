#!/usr/bin/env python3

import cv2
import header
import json
import logger
import numpy
import os

def main():
    if not os.path.isdir(header.slice_dataset_dir_annotations):
        logger.log_error("Invalid dataset annotations directory.")
        return

    dataset_dir_annotations_list = os.listdir(header.slice_dataset_dir_annotations)
    file_annotations_counter = 1

    for file_name_annotations in dataset_dir_annotations_list:
        file_key = file_name_annotations.split(".")[0]
        file_name_images = file_key + header.dataset_file_extension_images
        file_path_images = os.path.join(header.slice_dataset_dir_images, file_name_images)

        if file_annotations_counter >= len(dataset_dir_annotations_list):
            logger.log_info("Processing \"" + file_name_annotations + "\" (" + str(file_annotations_counter) + "/" + str(len(dataset_dir_annotations_list)) + ")...")
        else:
            logger.log_info("Processing \"" + file_name_annotations + "\" (" + str(file_annotations_counter) + "/" + str(len(dataset_dir_annotations_list)) + ")...", end = "\r")

        file_annotations_counter += 1
        file_path_annotations = os.path.join(header.slice_dataset_dir_annotations, file_name_annotations)

        if not os.path.isfile(file_path_annotations):
            continue

        if not os.path.isfile(file_path_images):
            continue

        file_annotations = open(file_path_annotations, "r")
        annotations = json.load(file_annotations)
        file_annotations.close()

        file_images = cv2.imread(file_path_images, cv2.IMREAD_COLOR)

        objects = annotations["objects"]

        for object in objects:
            key = object["key"]
            label = object["label"]
            bbox = object["bbox"]

            bounding_box_upper_left_x = int(bbox["xmin"])
            bounding_box_upper_left_y = int(bbox["ymin"])
            bounding_box_lower_right_x = int(bbox["xmax"])
            bounding_box_lower_right_y = int(bbox["ymax"])

            dataset_dir_images_sliced_label = os.path.join(header.dataset_dir_images_sliced, header.slice_dataset_dir_annotations.split("/")[-1], label)

            if not os.path.isdir(dataset_dir_images_sliced_label):
                os.makedirs(dataset_dir_images_sliced_label)

            if "cross_boundary" in bbox:
                bounding_box_left_upper_left_x = int(bbox["cross_boundary"]["left"]["xmin"])
                bounding_box_left_upper_left_y = int(bbox["cross_boundary"]["left"]["ymin"])
                bounding_box_left_lower_right_x = int(bbox["cross_boundary"]["left"]["xmax"])
                bounding_box_left_lower_right_y = int(bbox["cross_boundary"]["left"]["ymax"])
                bounding_box_right_upper_left_x = int(bbox["cross_boundary"]["right"]["xmin"])
                bounding_box_right_upper_left_y = int(bbox["cross_boundary"]["right"]["ymin"])
                bounding_box_right_lower_right_x = int(bbox["cross_boundary"]["right"]["xmax"])
                bounding_box_right_lower_right_y = int(bbox["cross_boundary"]["right"]["ymax"])

                file_images_bounding_box_left = file_images[bounding_box_left_upper_left_y:bounding_box_left_lower_right_y, bounding_box_left_upper_left_x:bounding_box_left_lower_right_x]
                file_images_bounding_box_right = file_images[bounding_box_right_upper_left_y:bounding_box_right_lower_right_y, bounding_box_right_upper_left_x:bounding_box_right_lower_right_x]
                file_images_bounding_box = numpy.concatenate((file_images_bounding_box_left, file_images_bounding_box_right), axis = 1)
                cv2.imwrite(dataset_dir_images_sliced_label + "/" + key + header.dataset_file_extension_images, file_images_bounding_box)
            else:
                file_images_bounding_box = file_images[bounding_box_upper_left_y:bounding_box_lower_right_y, bounding_box_upper_left_x:bounding_box_lower_right_x]
                cv2.imwrite(dataset_dir_images_sliced_label + "/" + key + header.dataset_file_extension_images, file_images_bounding_box)

    return

if __name__ == "__main__":
    main()
