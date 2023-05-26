#!/usr/bin/env python3

import header
import imagenet_c
import logger
import matplotlib.pyplot
import numpy
import os
import PIL.Image
import tqdm
import type
import utility

def corrupt(image, corruption, severity):
    if corruption == type.Corruption.gaussian_noise:
        return imagenet_c.gaussian_noise(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.shot_noise:
        return imagenet_c.shot_noise(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.impulse_noise:
        return imagenet_c.impulse_noise(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.defocus_blur:
        return imagenet_c.defocus_blur(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.glass_blur:
        return imagenet_c.glass_blur(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.motion_blur:
        return imagenet_c.motion_blur(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.zoom_blur:
        return imagenet_c.zoom_blur(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.snow:
        return imagenet_c.snow(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.frost:
        return imagenet_c.frost(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.fog:
        return imagenet_c.fog(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.brightness:
        return imagenet_c.brightness(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.contrast:
        return imagenet_c.contrast(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.elastic_transform:
        return imagenet_c.elastic_transform(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.pixelate:
        return imagenet_c.pixelate(image, severity).astype(numpy.uint8)
    elif corruption == type.Corruption.jpeg_compression:
        return imagenet_c.jpeg_compression(image, severity).astype(numpy.uint8)

    logger.log_warn("Unknown corruption \"" + corruption.name + "\"")
    return image

def corruptOriginal(file_path_image):
    file_dir_class = file_path_image.split("/")[-2]
    file_name_image = file_path_image.split("/")[-1]

    image = PIL.Image.open(file_path_image)
    image = image.resize((header.corrupt_image_size, header.corrupt_image_size))
    image = numpy.array(image)

    if header.log_level >= type.LogLevel.trace:
        matplotlib.pyplot.imshow(image)
        matplotlib.pyplot.show()

    image_corrupted = corrupt(image, header.corrupt_corruption, header.corrupt_severity)

    if header.log_level >= type.LogLevel.trace:
        matplotlib.pyplot.imshow(image_corrupted)
        matplotlib.pyplot.show()

    image_corrupted = PIL.Image.fromarray(image_corrupted)

    file_dir_corruption_params = header.corrupt_corruption.name + "_" + str(header.corrupt_severity)
    file_path_class_corrupted = os.path.join(header.dataset_dir_images_split_corrupted_original_test, file_dir_corruption_params, file_dir_class)
    file_path_image_corrupted = os.path.join(file_path_class_corrupted, file_name_image)

    os.makedirs(file_path_class_corrupted, exist_ok = True)
    image_corrupted.save(file_path_image_corrupted)

    return

def main():
    utility.setSeed(header.corrupt_random_seed)

    file_path_image_counter = 0
    file_path_image_list = []

    for file_dir_class in os.listdir(header.dataset_dir_images_split_original_test):
        file_path_class = os.path.join(header.dataset_dir_images_split_original_test, file_dir_class)

        for file_name_image in os.listdir(file_path_class):
            file_path_image = os.path.join(file_path_class, file_name_image)
            file_path_image_list.append(file_path_image)

    progress_bar = tqdm.tqdm(total = len(file_path_image_list))

    for file_path_image in file_path_image_list:
        file_key = file_path_image.split(header.dataset_file_extension_images)[0].split("/")[-1]

        progress_bar.set_description_str("[INFO]: Processing \"" + file_key + "\"")
        progress_bar.n = file_path_image_counter
        progress_bar.refresh()
        file_path_image_counter += 1

        corruptOriginal(file_path_image)

    progress_bar.close()

    return

if __name__ == "__main__":
    main()
