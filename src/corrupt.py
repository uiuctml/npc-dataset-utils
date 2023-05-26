#!/usr/bin/env python3

import header
import imagenet_c
import logger
import multiprocessing
import numpy
import os
import PIL.Image
import tqdm
import type
import utility

def corruptImageNetC(image, corruption, severity):
    image = image.resize((header.corrupt_image_size, header.corrupt_image_size))
    image = numpy.array(image)

    if corruption == type.CorruptionImageNetC.gaussian_noise:
        return imagenet_c.gaussian_noise(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.shot_noise:
        return imagenet_c.shot_noise(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.impulse_noise:
        return imagenet_c.impulse_noise(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.defocus_blur:
        return imagenet_c.defocus_blur(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.glass_blur:
        return imagenet_c.glass_blur(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.motion_blur:
        return imagenet_c.motion_blur(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.zoom_blur:
        return imagenet_c.zoom_blur(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.snow:
        return imagenet_c.snow(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.frost:
        return imagenet_c.frost(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.fog:
        return imagenet_c.fog(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.brightness:
        return imagenet_c.brightness(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.contrast:
        return imagenet_c.contrast(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.elastic_transform:
        return imagenet_c.elastic_transform(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.pixelate:
        return imagenet_c.pixelate(image, severity).astype(numpy.uint8)
    elif corruption == type.CorruptionImageNetC.jpeg_compression:
        return imagenet_c.jpeg_compression(image, severity).astype(numpy.uint8)

    logger.log_warn("Unknown corruption \"" + corruption.name + "\"")
    return image

def corruptOriginal(file_path_image):
    file_dir_class = file_path_image.split("/")[-2]
    file_name_image = file_path_image.split("/")[-1]

    image = PIL.Image.open(file_path_image)
    image_corrupted = corruptImageNetC(image, header.corrupt_corruption_imagenet_c, header.corrupt_severity)
    image_corrupted = PIL.Image.fromarray(image_corrupted)

    file_dir_corruption_params = header.corrupt_corruption_imagenet_c.name + "_" + str(header.corrupt_severity)
    file_path_class_corrupted = os.path.join(header.dataset_dir_images_split_corrupted_original_test, file_dir_corruption_params, file_dir_class)
    file_path_image_corrupted = os.path.join(file_path_class_corrupted, file_name_image)

    os.makedirs(file_path_class_corrupted, exist_ok = True)
    image_corrupted.save(file_path_image_corrupted)

    return

def main():
    utility.setSeed(header.corrupt_random_seed)

    file_path_image_counters = []
    file_path_image_list = []
    progress_bars = []

    for file_dir_class in os.listdir(header.dataset_dir_images_split_original_test):
        file_path_class = os.path.join(header.dataset_dir_images_split_original_test, file_dir_class)

        for file_name_image in os.listdir(file_path_class):
            file_path_image = os.path.join(file_path_class, file_name_image)
            file_path_image_list.append(file_path_image)

    file_path_image_list = numpy.array(file_path_image_list)
    file_path_image_list_split = numpy.array_split(file_path_image_list, numpy.arange(header.parallel_process_count, len(file_path_image_list), header.parallel_process_count))

    # Create progress bars
    for process_id in range(0, header.parallel_process_count):
        progress_bar_size = len(file_path_image_list) // header.parallel_process_count

        if (len(file_path_image_list_split[-1]) != header.parallel_process_count and
            process_id < len(file_path_image_list_split[-1])):
            progress_bar_size += 1

        progress_bar = tqdm.tqdm(total = progress_bar_size, position = process_id, leave = False)
        progress_bars.append(progress_bar)
        file_path_image_counters.append(1)

    for file_path_image_list_process in file_path_image_list_split:
        processes = []
        process_exit_codes = []

        if len(file_path_image_list_process) > header.parallel_process_count:
            logger.log_warn("Not enough process.")

        # Start processes
        for (process_id, file_path_image) in enumerate(file_path_image_list_process):
            args = (file_path_image,)
            file_key = file_path_image.split(header.dataset_file_extension_images)[0].split("/")[-1]
            description = file_key[0:header.corrupt_progress_bar_description_length] + "..."
            progress_bars[process_id].set_description_str("Processing \"" + description + "\"")
            progress_bars[process_id].n = file_path_image_counters[process_id]
            progress_bars[process_id].refresh()
            file_path_image_counters[process_id] += 1

            process = multiprocessing.Process(target = corruptOriginal, args = args)
            process.start()
            processes.append((process, args))

        # Join processes
        for (process, args) in processes:
            process.join()
            process_exit_codes.append((process.exitcode, args))

        # Retry failed processes
        for (process_exit_code, args) in process_exit_codes:
            while process_exit_code != 0:
                file_path_image = args[0]
                file_key = file_path_image.split(header.dataset_file_extension_images)[0].split("/")[-1]
                logger.log_info("Failed on \"" + file_key + "\". Retrying...")

                process = multiprocessing.Process(target = corruptOriginal, args = args)
                process.start()
                process.join()
                process_exit_code = process.exitcode

    # Close progress bars
    for progress_bar in progress_bars:
        progress_bar.close()

    return

if __name__ == "__main__":
    main()
