#!/usr/bin/env python3

import header
import json
import logger
import os

def print_params():
    logger.log_info("Filter parameters:")
    logger.log_info("filter_frame_ispano:\t\t\t" + str(header.filter_frame_ispano) + ".")
    logger.log_info("filter_object_keys:\t\t\t" + str(header.filter_object_keys) + ".")
    logger.log_info("filter_object_labels:\t\t\t" + str(header.filter_object_labels) + ".")
    logger.log_info("filter_object_properties:\t\t" + str(header.filter_object_properties) + ".")
    logger.log_info("filter_object_barrier:\t\t\t" + str(header.filter_object_barrier) + ".")
    logger.log_info("filter_object_occluded:\t\t\t" + str(header.filter_object_occluded) + ".")
    logger.log_info("filter_object_out_of_frame:\t\t" + str(header.filter_object_out_of_frame) + ".")
    logger.log_info("filter_object_exterior:\t\t\t" + str(header.filter_object_exterior) + ".")
    logger.log_info("filter_object_ambiguous:\t\t" + str(header.filter_object_ambiguous) + ".")
    logger.log_info("filter_object_included:\t\t\t" + str(header.filter_object_included) + ".")
    logger.log_info("filter_object_direction_or_information:\t" + str(header.filter_object_direction_or_information) + ".")
    logger.log_info("filter_object_highway:\t\t\t" + str(header.filter_object_highway) + ".")
    logger.log_info("filter_object_dummy:\t\t\t" + str(header.filter_object_dummy) + ".")

    return

def main():
    if header.filter_print_params:
        print_params()

    if not os.path.isdir(header.filter_dataset_dir_annotations):
        logger.log_error("Invalid dataset annotations directory.")
        return

    dataset_dir_annotations_list = os.listdir(header.filter_dataset_dir_annotations)
    file_filter = open(header.filter_file_name, "w")
    file_annotations_counter = 1

    for file_name_annotations in dataset_dir_annotations_list:
        if file_annotations_counter >= len(dataset_dir_annotations_list):
            logger.log_info("Processing \"" + file_name_annotations + "\" (" + str(file_annotations_counter) + "/" + str(len(dataset_dir_annotations_list)) + ")...")
        else:
            logger.log_info("Processing \"" + file_name_annotations + "\" (" + str(file_annotations_counter) + "/" + str(len(dataset_dir_annotations_list)) + ")...", end = "\r")

        file_annotations_counter += 1
        file_path_annotations = os.path.join(header.filter_dataset_dir_annotations, file_name_annotations)

        if not os.path.isfile(file_path_annotations):
            continue

        file_annotations = open(file_path_annotations, "r")
        annotations = json.load(file_annotations)
        file_annotations.close()

        ispano = annotations["ispano"]
        objects = annotations["objects"]
        match = False

        if ((header.filter_frame_ispano > 0 and ispano == False) or
            (header.filter_frame_ispano < 0 and ispano == True)):
            continue

        for object in objects:
            key = object["key"]
            label = object["label"]
            properties = object["properties"]
            barrier = properties["barrier"]
            occluded = properties["occluded"]
            out_of_frame = properties["out-of-frame"]
            exterior = properties["exterior"]
            ambiguous = properties["ambiguous"]
            included = properties["included"]
            direction_or_information = properties["direction-or-information"]
            highway = properties["highway"]
            dummy = properties["dummy"]

            if ((len(header.filter_object_keys) > 0) and
                (key not in header.filter_object_keys)):
                continue

            if ((len(header.filter_object_labels) > 0) and
                (label not in header.filter_object_labels)):
                continue

            if header.filter_object_properties == True:
                if ((header.filter_object_barrier > 0 and barrier == False) or
                    (header.filter_object_barrier < 0 and barrier == True)):
                    continue

                if ((header.filter_object_occluded > 0 and occluded == False) or
                    (header.filter_object_occluded < 0 and occluded == True)):
                    continue

                if ((header.filter_object_out_of_frame > 0 and out_of_frame == False) or
                    (header.filter_object_out_of_frame < 0 and out_of_frame == True)):
                    continue

                if ((header.filter_object_exterior > 0 and exterior == False) or
                    (header.filter_object_exterior < 0 and exterior == True)):
                    continue

                if ((header.filter_object_ambiguous > 0 and ambiguous == False) or
                    (header.filter_object_ambiguous < 0 and ambiguous == True)):
                    continue

                if ((header.filter_object_included > 0 and included == False) or
                    (header.filter_object_included < 0 and included == True)):
                    continue

                if ((header.filter_object_direction_or_information > 0 and direction_or_information == False) or
                    (header.filter_object_direction_or_information < 0 and direction_or_information == True)):
                    continue

                if ((header.filter_object_highway > 0 and highway == False) or
                    (header.filter_object_highway < 0 and highway == True)):
                    continue

                if ((header.filter_object_dummy > 0 and dummy == False) or
                    (header.filter_object_dummy < 0 and dummy == True)):
                    continue

            match = True
            break

        if match == False:
            continue
    
        file_filter.write(file_name_annotations.split(".")[0] + "\n")

    file_filter.close()

    logger.log_info("Filter saved to \"" + header.filter_file_name + "\".")

    return

if __name__ == "__main__":
    main()
