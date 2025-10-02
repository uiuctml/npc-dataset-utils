#!/usr/bin/env python3

import header
import json
import logger
import os
import random
import utility

def main():
    if os.path.exists(header.dataset_dir_splits_pc):
        logger.log_info("PC dataset splits exist in \"" + header.dataset_dir_splits_pc + "\". Skip.")
        return

    utility.setSeed(header.pc_random_seed)

    file_dataset_config = open(os.path.join(header.config_dir, header.dataset_config_file_name), "r")
    dataset_config = json.load(file_dataset_config)
    file_dataset_config.close()

    labels_attribute = utility.getLabelsAttribute(dataset_config)
    labels_original = utility.getLabelsOriginal(dataset_config)
    indices_attribute = utility.getIndicesFromLabelsAttribute(labels_attribute)
    indices_original = utility.getIndicesFromLabelsOriginal(labels_original)

    categories = {}
    dirs_dataset_original = [header.dataset_dir_splits_instances_test, header.dataset_dir_splits_instances_train, header.dataset_dir_splits_instances_validate]

    for attribute in dataset_config["attributes"]:
        attribute_name = attribute["name"]
        attribute_categories = attribute["labels"]

        if "" in attribute_categories:
            attribute_categories.remove("")

        categories[attribute_name] = attribute_categories

    for i in range(len(dirs_dataset_original)):
        logger.log_info("Generating PC dataset split from \"" + dirs_dataset_original[i] + "\".")

        lines = []

        if "instance_wise" in dataset_config and dataset_config["instance_wise"]:
            for label_original in os.listdir(dirs_dataset_original[i]):
                for instance_name in os.listdir(os.path.join(dirs_dataset_original[i], label_original)):
                    image_name = os.path.join(label_original, instance_name)
                    attributes = dataset_config["mappings"][image_name]["labels"]
                    line = ""

                    logger.log_debug(image_name)

                    for attribute_name in attributes.keys():
                        if isinstance(attributes[attribute_name], list):
                            count_categories = len(categories[attribute_name])

                            if count_categories <= 0:
                                logger.log_fatal("Empty attribute. Quit.")
                                exit(-1)

                            index_label_attribute = random.randint(0, count_categories - 1)
                        else:
                            index_label_attribute = indices_attribute[attribute_name][attributes[attribute_name]]

                        line += str(index_label_attribute) + ","

                    index_label_original = indices_original[label_original]
                    line += str(index_label_original) + "\n"
                    lines.append(line)
        else:
            for label_original in labels_original:
                attributes = dataset_config["mappings"][label_original]["labels"]

                for _ in os.listdir(os.path.join(dirs_dataset_original[i], label_original)):
                    line = ""

                    for attribute_name in attributes.keys():
                        if isinstance(attributes[attribute_name], list):
                            count_categories = len(categories[attribute_name])

                            if count_categories <= 0:
                                logger.log_fatal("Empty attribute. Quit.")
                                exit(-1)

                            index_label_attribute = random.randint(0, count_categories - 1)
                        else:
                            index_label_attribute = indices_attribute[attribute_name][attributes[attribute_name]]

                        line += str(index_label_attribute) + ","

                    index_label_original = indices_original[label_original]
                    line += str(index_label_original) + "\n"
                    lines.append(line)

        lines[-1] = lines[-1].rstrip("\n")

        if not os.path.exists(header.dataset_dir_splits_pc):
            os.makedirs(header.dataset_dir_splits_pc, exist_ok = True)

        file_name_pc_dataset = os.path.basename(dirs_dataset_original[i]) + ".txt"
        file_path_pc_dataset = os.path.join(header.dataset_dir_splits_pc, file_name_pc_dataset)

        with open(file_path_pc_dataset, "w+") as file_dataset_pc:
            file_dataset_pc.writelines(lines)

    return

if __name__ == "__main__":
    main()
