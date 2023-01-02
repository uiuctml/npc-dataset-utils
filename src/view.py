#!/usr/bin/env python3

import cv2
import header
import logger
import os

def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    width_image = image.shape[1]
    width_resize = image.shape[1]
    height_image = image.shape[0]
    height_resize = image.shape[0]

    if (width is None and height is None):
        return image

    if (width is None):
        resize_ratio = height / height_image
        width_resize = int(width_image * resize_ratio)
        height_resize = height
    else:
        resize_ratio = width / width_image
        width_resize = width
        height_resize = int(height_image * resize_ratio)

    return cv2.resize(image, (width_resize, height_resize), interpolation=inter)

def main():
    file_filter = open(header.filter_file_name, "r")
    file_filter_lines = file_filter.readlines()
    file_filter.close()

    file_images_counter = 1
    cv2.namedWindow(header.dataset_images_dir, cv2.WINDOW_NORMAL)

    for line in file_filter_lines:
        line = line.strip()
        file_name_images = line + header.view_file_extension
        file_path_images = os.path.join(header.dataset_images_dir, file_name_images)

        if (file_images_counter >= len(file_filter_lines)):
            logger.log_info("Showing", file_name_images, "(" + str(file_images_counter) + "/" + str(len(file_filter_lines)) + ")...")
        else:
            logger.log_info("Showing", file_name_images, "(" + str(file_images_counter) + "/" + str(len(file_filter_lines)) + ")...", end = "\r")

        file_images_counter += 1

        if (not os.path.isfile(file_path_images)):
            continue

        file_images = cv2.imread(file_path_images, cv2.IMREAD_COLOR)
        file_images = resize(file_images, height = header.view_window_height)

        cv2.imshow(header.dataset_images_dir, file_images)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

    return

if __name__ == "__main__":
    main()
