#!/usr/bin/env python3

import header
import os
import logger
import numpy as np
import cv2

def calculate_means():
    total_brightness = 0
    database_dir = os.listdir(header.dataset_dir_images_split_original_test)
    for sub_folder in database_dir:
      sub_folder_path = os.path.join(header.dataset_dir_images_split_original_test, sub_folder)
      for image in sub_folder:
        file_path_image = os.path.join(sub_folder_path, image)
        image = cv2.imread(file_path_image)
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(image_hsv)
        total_brightness += np.mean(v)
    mean_brightness = total_brightness / (len(database_dir)*len(sub_folder))
    logger.log_info(mean_brightness)

def main():
    calculate_means()

if __name__ == "__main__":
    main()
