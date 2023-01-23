#!/usr/bin/env python3

import cv2
import header
import json
import logger
import os
import tqdm

def annotate(image, file_key):
    file_name_annotations = file_key + header.dataset_file_extension_annotations
    file_path_annotations = os.path.join(header.dataset_dir_annotations_original, file_name_annotations)

    file_annotations = open(file_path_annotations, "r")
    annotations = json.load(file_annotations)
    file_annotations.close()

    for object in annotations["objects"]:
        label = object["label"]

        if ((len(header.filter_object_labels) > 0) and
            (label not in header.filter_object_labels)):
            continue

        bbox = object["bbox"]

        bounding_box_upper_left_x = int(bbox["xmin"])
        bounding_box_upper_left_y = int(bbox["ymin"])
        bounding_box_lower_right_x = int(bbox["xmax"])
        bounding_box_lower_right_y = int(bbox["ymax"])

        image = cv2.rectangle(image, (bounding_box_upper_left_x, bounding_box_upper_left_y),
            (bounding_box_lower_right_x, bounding_box_lower_right_y),
            header.view_bounding_box_color, header.view_bounding_box_thickness)

        bounding_box_text = label
        bounding_box_text_size = cv2.getTextSize(bounding_box_text,
            cv2.FONT_HERSHEY_SIMPLEX, header.view_bounding_box_text_size, header.view_bounding_box_thickness)[0]
        bounding_box_text_width = int(bounding_box_text_size[0]) + header.view_bounding_box_text_margin_x
        bounding_box_text_height = int(bounding_box_text_size[1]) + header.view_bounding_box_text_margin_y

        image = cv2.rectangle(image, (bounding_box_upper_left_x, bounding_box_upper_left_y - bounding_box_text_height),
            (bounding_box_upper_left_x + bounding_box_text_width, bounding_box_upper_left_y),
            header.view_bounding_box_color, -1)

        image = cv2.putText(image, bounding_box_text,
            (bounding_box_upper_left_x + int(header.view_bounding_box_text_margin_x / 2),
            bounding_box_upper_left_y - int(header.view_bounding_box_text_margin_y / 1.4)), cv2.FONT_HERSHEY_SIMPLEX,
            header.view_bounding_box_text_size, header.view_bounding_box_text_color, header.view_bounding_box_thickness, cv2.LINE_AA)

    return image

def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    width_image = image.shape[1]
    width_resize = image.shape[1]
    height_image = image.shape[0]
    height_resize = image.shape[0]

    if width is None and height is None:
        return image

    if width is None:
        resize_ratio = height / height_image
        width_resize = int(width_image * resize_ratio)
        height_resize = height
    else:
        resize_ratio = width / width_image
        width_resize = width
        height_resize = int(height_image * resize_ratio)

    return cv2.resize(image, (width_resize, height_resize), interpolation=inter)

def main():
    file_filter = open(header.view_filter_file_name, "r")
    file_filter_lines = file_filter.readlines()
    file_filter.close()

    file_images_counter = 1
    progress_bar = tqdm.tqdm(total = len(file_filter_lines))

    cv2.namedWindow(header.view_dataset_dir_images, cv2.WINDOW_NORMAL)

    for line in file_filter_lines:
        file_key = line.strip()
        file_name_images = file_key + header.dataset_file_extension_images
        file_path_images = os.path.join(header.view_dataset_dir_images, file_name_images)

        progress_bar.set_description_str("Showing \"" + file_name_images + "\"")
        progress_bar.n = file_images_counter
        progress_bar.refresh()

        file_images_counter += 1

        if not os.path.isfile(file_path_images):
            continue

        file_images = cv2.imread(file_path_images, cv2.IMREAD_COLOR)
        file_images = annotate(file_images, file_key)
        file_images = resize(file_images, height = header.view_window_height)

        cv2.imshow(header.view_dataset_dir_images, file_images)
        cv2.waitKey(0)

    cv2.destroyAllWindows()
    progress_bar.close()

    return

if __name__ == "__main__":
    main()
