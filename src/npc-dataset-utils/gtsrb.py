#!/usr/bin/env python3

"""
@file   gtsrb.py
@author Simon Yu
@date   01/09/2024
@brief  Script for GTSRB dataset.
"""

import header
import logger
import os
import tqdm

class_names = {
    "0": "regulatory--maximum-speed-limit-20",
    "1": "regulatory--maximum-speed-limit-30",
    "2": "regulatory--maximum-speed-limit-50",
    "3": "regulatory--maximum-speed-limit-60",
    "4": "regulatory--maximum-speed-limit-70",
    "5": "regulatory--maximum-speed-limit-80",
    "6": "regulatory--end-of-maximum-speed-limit-80",
    "7": "regulatory--maximum-speed-limit-100",
    "8": "regulatory--maximum-speed-limit-120",
    "9": "regulatory--no-overtaking",
    "10": "regulatory--no-overtaking-by-heavy-goods-vehicles",
    "11": "warning--crossroads",
    "12": "regulatory--priority-road",
    "13": "regulatory--yield",
    "14": "regulatory--stop",
    "15": "regulatory--road-closed-to-vehicles",
    "16": "regulatory--no-heavy-goods-vehicles",
    "17": "regulatory--no-entry",
    "18": "warning--other-danger",
    "19": "warning--curve-left",
    "20": "warning--curve-right",
    "21": "warning--double-curve-first-left",
    "22": "warning--uneven-road",
    "23": "warning--slippery-road-surface",
    "24": "warning--road-narrows-right",
    "25": "warning--roadworks",
    "26": "warning--traffic-signals",
    "27": "warning--pedestrians-crossing",
    "28": "warning--children",
    "29": "warning--bicycles-crossing",
    "30": "warning--ice-or-snow",
    "31": "warning--wild-animals",
    "32": "regulatory--end-of-prohibition",
    "33": "regulatory--turn-right-ahead",
    "34": "regulatory--turn-left-ahead",
    "35": "regulatory--go-straight",
    "36": "regulatory--go-straight-or-turn-right",
    "37": "regulatory--go-straight-or-turn-left",
    "38": "regulatory--keep-right",
    "39": "regulatory--keep-left",
    "40": "regulatory--roundabout",
    "41": "regulatory--end-of-no-overtaking",
    "42": "regulatory--end-of-no-overtaking-by-heavy-goods-vehicles"
}

def main():
    if os.path.exists(header.dataset_dir_instances_processed):
        logger.log_info("Processed instance directory exists. Skip.")
        return

    dir_name_counter = 1
    dir_names = os.listdir(header.dataset_dir_instances_original)
    progress_bar = tqdm.tqdm(total = len(dir_names))

    os.makedirs(header.dataset_dir_instances_processed, exist_ok = True)

    for dir_name in dir_names:
        if dir_name not in class_names:
            dir_name_counter += 1
            continue

        label_name = class_names[dir_name]

        progress_bar.set_description_str("[INFO]: Creating symlink for category \"" + label_name + "\"")
        progress_bar.n = dir_name_counter
        progress_bar.refresh()

        if os.path.isdir(os.path.join(header.dataset_dir_instances_original, dir_name)):
            os.symlink(os.path.abspath(os.path.join(header.dataset_dir_instances_original, dir_name)), os.path.join(header.dataset_dir_instances_processed, label_name))

        dir_name_counter += 1

    progress_bar.close()

    return

if __name__ == "__main__":
    main()
