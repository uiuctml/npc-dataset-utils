#!/usr/bin/env python3

import codecs
import cv2
import header
import json
import logger
import multiprocessing
import multiprocessing.shared_memory
import numpy
import os
import tqdm

def readFromSharedMemory(shared_memory, process_id, entry_id):
    start = process_id * header.slice_shared_memory_size_process + entry_id * header.slice_shared_memory_size_entry
    size = int(shared_memory.buf[start])
    end = start + 1 + size

    if end >= header.slice_shared_memory_size_total:
        logger.log_error("Shared memory segmentation fault")
        return ""

    return str(codecs.decode(shared_memory.buf[start + 1:end], "ascii"))

def writeToSharedMemory(shared_memory, process_id, entry_id, data):
    data = str(data)
    start = process_id * header.slice_shared_memory_size_process + entry_id * header.slice_shared_memory_size_entry
    end = start + 1 + len(data)

    if end >= header.slice_shared_memory_size_total:
        logger.log_error("Shared memory segmentation fault")
        return

    shared_memory.buf[start] = len(data)
    shared_memory.buf[start + 1:end] = codecs.encode(data, "ascii")

    return

def monitor():
    shared_memory = multiprocessing.shared_memory.SharedMemory(name = header.slice_shared_memory_name)
    done = int(readFromSharedMemory(shared_memory, header.slice_process_count, 0))
    progress_bars = []

    for process_id in range(0, header.slice_process_count):
        file_name_annotations = readFromSharedMemory(shared_memory, process_id, 0)
        file_annotations_counter = int(readFromSharedMemory(shared_memory, process_id, 1))
        dataset_dir_annotations_list_size = int(readFromSharedMemory(shared_memory, process_id, 2))

        progress_bar = tqdm.tqdm(total = dataset_dir_annotations_list_size, position = process_id, leave = False)
        progress_bar.set_description_str("Processing \"" + file_name_annotations + "\"")
        progress_bars.append(progress_bar)

    while not done:
        for process_id in range(0, header.slice_process_count):
            file_name_annotations = readFromSharedMemory(shared_memory, process_id, 0)
            file_annotations_counter = int(readFromSharedMemory(shared_memory, process_id, 1))
            dataset_dir_annotations_list_size = int(readFromSharedMemory(shared_memory, process_id, 2))
            progress_bar = progress_bars[process_id]
            progress_bar.set_description_str("Processing \"" + file_name_annotations + "\"")
            progress_bar.n = file_annotations_counter
            progress_bar.refresh()

        done = int(readFromSharedMemory(shared_memory, header.slice_process_count, 0))

    for process_id in range(0, header.slice_process_count):
        progress_bars[process_id].close()

    return

def slice(process_id, dataset_dir_annotations_list):
    file_annotations_counter = 1
    shared_memory = multiprocessing.shared_memory.SharedMemory(name = header.slice_shared_memory_name)

    for file_name_annotations in dataset_dir_annotations_list:
        file_key = file_name_annotations.split(".")[0]
        file_name_images = file_key + header.dataset_file_extension_images
        file_path_images = os.path.join(header.slice_dataset_dir_images, file_name_images)

        writeToSharedMemory(shared_memory, process_id, 0, file_name_annotations)
        writeToSharedMemory(shared_memory, process_id, 1, file_annotations_counter)
        writeToSharedMemory(shared_memory, process_id, 2, len(dataset_dir_annotations_list))

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
                os.makedirs(dataset_dir_images_sliced_label, exist_ok = True)

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

def main():
    if os.path.isdir(os.path.join(header.dataset_dir_images_sliced, header.slice_dataset_dir_annotations.split("/")[-1])):
        return

    if not os.path.isdir(header.slice_dataset_dir_annotations):
        logger.log_error("Invalid dataset annotations directory.")
        return

    dataset_dir_annotations_list = numpy.array(os.listdir(header.slice_dataset_dir_annotations))
    dataset_dir_annotations_list_split = numpy.array_split(dataset_dir_annotations_list, header.slice_process_count)
    processes = []
    shared_memory = multiprocessing.shared_memory.SharedMemory(name = header.slice_shared_memory_name, create = True, size = header.slice_shared_memory_size_total)

    for process_id in range(0, header.slice_process_count):
        process = multiprocessing.Process(target = slice, args = (process_id, list(dataset_dir_annotations_list_split[process_id])))
        process.start()
        processes.append(process)

    writeToSharedMemory(shared_memory, header.slice_process_count, 0, 0)
    process_monitor = multiprocessing.Process(target = monitor)
    process_monitor.start()

    for process in processes:
        process.join()

    writeToSharedMemory(shared_memory, header.slice_process_count, 0, 1)
    process_monitor.join()
    shared_memory.unlink()

    return

if __name__ == "__main__":
    main()
