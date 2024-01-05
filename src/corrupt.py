#!/usr/bin/env python3

import corrupt_color
import header
import imagenet_c
import logger
import multiprocessing
import numpy
import os
import PIL.Image
import sys
import tqdm
import type
import utility

def corruptImageNetC(image, corruption, severity):
    image = image.resize((header.corrupt_image_size, header.corrupt_image_size))

    if corruption == type.CorruptionImageNetC.gaussian_noise:
        image = imagenet_c.gaussian_noise(image, severity)
    elif corruption == type.CorruptionImageNetC.shot_noise:
        image = imagenet_c.shot_noise(image, severity)
    elif corruption == type.CorruptionImageNetC.impulse_noise:
        image = imagenet_c.impulse_noise(image, severity)
    elif corruption == type.CorruptionImageNetC.defocus_blur:
        image = imagenet_c.defocus_blur(image, severity)
    elif corruption == type.CorruptionImageNetC.glass_blur:
        image = imagenet_c.glass_blur(image, severity)
    elif corruption == type.CorruptionImageNetC.motion_blur:
        image = imagenet_c.motion_blur(image, severity)
    elif corruption == type.CorruptionImageNetC.zoom_blur:
        image = imagenet_c.zoom_blur(image, severity)
    elif corruption == type.CorruptionImageNetC.snow:
        image = imagenet_c.snow(image, severity)
    elif corruption == type.CorruptionImageNetC.frost:
        image = imagenet_c.frost(image, severity)
    elif corruption == type.CorruptionImageNetC.fog:
        image = imagenet_c.fog(image, severity)
    elif corruption == type.CorruptionImageNetC.brightness:
        image = imagenet_c.brightness(image, severity)
    elif corruption == type.CorruptionImageNetC.contrast:
        image = imagenet_c.contrast(image, severity)
    elif corruption == type.CorruptionImageNetC.elastic_transform:
        image = imagenet_c.elastic_transform(image, severity)
    elif corruption == type.CorruptionImageNetC.pixelate:
        image = imagenet_c.pixelate(image, severity)
    elif corruption == type.CorruptionImageNetC.jpeg_compression:
        image = imagenet_c.jpeg_compression(image, severity)
    elif corruption == type.CorruptionImageNetC.speckle_noise:
        image = imagenet_c.speckle_noise(image, severity)
    elif corruption == type.CorruptionImageNetC.gaussian_blur:
        image = imagenet_c.gaussian_blur(image, severity)
    elif corruption == type.CorruptionImageNetC.spatter:
        image = imagenet_c.spatter(image, severity)
    elif corruption == type.CorruptionImageNetC.saturate:
        image = imagenet_c.saturate(image, severity)
    else:
        logger.log_warn("Unknown ImageNet-C corruption \"" + corruption.name + "\"")

    image = numpy.array(image).astype(numpy.uint8)

    return image

def corrupt(file_path_image):
    file_dir_class = file_path_image.split("/")[-2]
    file_name_image = file_path_image.split("/")[-1]

    image = PIL.Image.open(file_path_image)
    image_corrupted = image
    file_dir_corruption_params = "unknown"

    if header.corrupt_corruption_algorithm == type.CorruptionAlgorithm.imagenet_c:
        image_corrupted = corruptImageNetC(image, header.corrupt_corruption_imagenet_c, header.corrupt_severity)
        file_dir_corruption_params = header.corrupt_corruption_imagenet_c.name + "_" + str(header.corrupt_severity)
    elif header.corrupt_corruption_algorithm == type.CorruptionAlgorithm.color:
        image_corrupted = corrupt_color.corruptColor(image)
        file_dir_corruption_params = "color"
    else:
        logger.log_warn("Unknown corruption algorithm \"" + header.corrupt_corruption_algorithm.name + "\"")

    image_corrupted = PIL.Image.fromarray(image_corrupted)

    file_path_class_corrupted = os.path.join(header.dataset_dir_images_split_corrupted_test, file_dir_corruption_params, file_dir_class)
    file_path_image_corrupted = os.path.join(file_path_class_corrupted, file_name_image)

    os.makedirs(file_path_class_corrupted, exist_ok = True)
    image_corrupted.save(file_path_image_corrupted)

    return

def main():
    utility.setSeed(header.corrupt_random_seed)

    if len(sys.argv) > 1:
        corruption_imagenet_c = sys.argv[1]

        if corruption_imagenet_c == type.CorruptionImageNetC.gaussian_noise.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.gaussian_noise
        elif corruption_imagenet_c == type.CorruptionImageNetC.shot_noise.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.shot_noise
        elif corruption_imagenet_c == type.CorruptionImageNetC.impulse_noise.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.impulse_noise
        elif corruption_imagenet_c == type.CorruptionImageNetC.defocus_blur.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.defocus_blur
        elif corruption_imagenet_c == type.CorruptionImageNetC.glass_blur.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.glass_blur
        elif corruption_imagenet_c == type.CorruptionImageNetC.motion_blur.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.motion_blur
        elif corruption_imagenet_c == type.CorruptionImageNetC.zoom_blur.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.zoom_blur
        elif corruption_imagenet_c == type.CorruptionImageNetC.snow.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.snow
        elif corruption_imagenet_c == type.CorruptionImageNetC.frost.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.frost
        elif corruption_imagenet_c == type.CorruptionImageNetC.fog.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.fog
        elif corruption_imagenet_c == type.CorruptionImageNetC.brightness.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.brightness
        elif corruption_imagenet_c == type.CorruptionImageNetC.contrast.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.contrast
        elif corruption_imagenet_c == type.CorruptionImageNetC.elastic_transform.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.elastic_transform
        elif corruption_imagenet_c == type.CorruptionImageNetC.pixelate.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.pixelate
        elif corruption_imagenet_c == type.CorruptionImageNetC.jpeg_compression.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.jpeg_compression
        elif corruption_imagenet_c == type.CorruptionImageNetC.speckle_noise.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.speckle_noise
        elif corruption_imagenet_c == type.CorruptionImageNetC.gaussian_blur.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.gaussian_blur
        elif corruption_imagenet_c == type.CorruptionImageNetC.spatter.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.spatter
        elif corruption_imagenet_c == type.CorruptionImageNetC.saturate.name:
            header.corrupt_corruption_imagenet_c = type.CorruptionImageNetC.saturate
        else:
            logger.log_error("Unknown ImageNet-C corruption \"" + corruption_imagenet_c + "\". Quit")
            exit(-1)

    if len(sys.argv) > 2:
        corruption_severity = sys.argv[2]

        try:
            header.corrupt_severity = int(corruption_severity)
        except:
            logger.log_error("Invalid corruption severity \"" + corruption_severity + "\". Quit")
            exit(-1)

    file_dir_corruption_params = header.corrupt_corruption_imagenet_c.name + "_" + str(header.corrupt_severity)
    file_path_corruption = os.path.join(header.dataset_dir_images_split_corrupted_test, file_dir_corruption_params)
    file_path_image_counters = []
    file_path_image_list = []
    progress_bars = []

    if header.corrupt_corruption_algorithm == type.CorruptionAlgorithm.imagenet_c:
        if os.path.isdir(file_path_corruption):
            logger.log_info("Directory \"" + file_dir_corruption_params + "\" exists. Quit")
            return

    # Gather image file paths
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
            process = None

            progress_bars[process_id].set_description_str("Processing \"" + description + "\"")
            progress_bars[process_id].n = file_path_image_counters[process_id]
            progress_bars[process_id].refresh()
            file_path_image_counters[process_id] += 1

            process = multiprocessing.Process(target = corrupt, args = args)

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

                process = None
                logger.log_info("Failed on \"" + file_key + "\". Retrying...")

                process = multiprocessing.Process(target = corrupt, args = args)

                process.start()
                process.join()
                process_exit_code = process.exitcode

    # Close progress bars
    for progress_bar in progress_bars:
        progress_bar.close()

    return

if __name__ == "__main__":
    main()
