#!/usr/bin/env python3

import header
import json
import logger
import os

attribute_category_whitelist = {
    "belly-color": {
        "belly-color--grey": 0.955,
        "belly-color--white": 0.93,
        "belly-color--buff": 0.885,
        "belly-color--black": 0.845,
        "belly-color--brown": 0.755,
        "belly-color--yellow": 0.575,
        "belly-color--orange": 0.46,
        "belly-color--iridescent": 0.35,
        "belly-color--olive": 0.34,
        "belly-color--red": 0.335,
        "belly-color--blue": 0.295,
        "belly-color--green": 0.255,
        "belly-color--rufous": 0.225,
        "belly-color--pink": 0.205,
        "belly-color--purple": 0.12,
        "belly-color--none": 0.0
    },
    "wing-color": {
        "wing-color--black": 1.0,
        "wing-color--grey": 0.99,
        "wing-color--brown": 0.96,
        "wing-color--buff": 0.915,
        "wing-color--white": 0.91,
        "wing-color--yellow": 0.495,
        "wing-color--iridescent": 0.45,
        "wing-color--orange": 0.435,
        "wing-color--blue": 0.415,
        "wing-color--olive": 0.365,
        "wing-color--red": 0.31,
        "wing-color--green": 0.27,
        "wing-color--rufous": 0.24,
        "wing-color--purple": 0.21,
        "wing-color--pink": 0.2,
        "wing-color--none": 0.0
    },
    "bill-shape": {
        "bill-shape--all-purpose": 0.98,
        "bill-shape--cone": 0.905,
        "bill-shape--dagger": 0.79,
        "bill-shape--hooked": 0.42,
        "bill-shape--curved-(up-or-down)": 0.385,
        "bill-shape--hooked-seabird": 0.375,
        "bill-shape--needle": 0.285,
        "bill-shape--specialized": 0.24,
        "bill-shape--spatulate": 0.235,
        "bill-shape--none": 0.0
    },
    "wing-pattern": {
        "wing-pattern--multi-colored": 0.995,
        "wing-pattern--striped": 0.98,
        "wing-pattern--solid": 0.965,
        "wing-pattern--spotted": 0.775,
        "wing-pattern--none": 0.0
    },
    "shape": {
        "shape--perching-like": 0.955,
        "shape--pigeon-like": 0.91,
        "shape--sandpiper-like": 0.815,
        "shape--swallow-like": 0.815,
        "shape--tree-clinging-like": 0.795,
        "shape--hummingbird-like": 0.74,
        "shape--upland-ground-like": 0.71,
        "shape--gull-like": 0.655,
        "shape--hawk-like": 0.64,
        "shape--chicken-like-marsh": 0.485,
        "shape--upright-perching-water-like": 0.43,
        "shape--duck-like": 0.315,
        "shape--long-legged-like": 0.215,
        "shape--owl-like": 0.155
    }
}
class_whitelist = {
    "007.Parakeet_Auklet",
    "013.Bobolink",
    "014.Indigo_Bunting",
    "015.Lazuli_Bunting",
    "016.Painted_Bunting",
    "025.Pelagic_Cormorant",
    "028.Brown_Creeper",
    "036.Northern_Flicker",
    "040.Olive_sided_Flycatcher",
    "042.Vermilion_Flycatcher",
    "066.Western_Gull",
    "068.Ruby_throated_Hummingbird",
    "082.Ringed_Kingfisher",
    "090.Red_breasted_Merganser",
    "092.Nighthawk",
    "095.Baltimore_Oriole",
    "101.White_Pelican",
    "147.Least_Tern",
    "163.Cape_May_Warbler",
    "184.Louisiana_Waterthrush",
    "190.Red_cockaded_Woodpecker"
}

def pruneAttributes(attributes, mappings):
    attributes_map = {}

    for attribute in attributes:
        attribute["labels"] = [""]
        attributes_map[attribute["name"]] = set()

    for image_name in mappings.keys():
        labels = mappings[image_name]["labels"]

        for attribute_name in labels.keys():
            if isinstance(labels[attribute_name], list):
                for label in labels[attribute_name]:
                    attributes_map[attribute_name].add(label)
            else:
                attributes_map[attribute_name].add(labels[attribute_name])

    for attribute in attributes:
        attribute["labels"] += sorted(list(attributes_map[attribute["name"]]))

    return attributes

def readAttributes():
    attributes = {}
    attributes_list = []
    attributes_map = {}
    file_attributes = open(os.path.join(header.cub_dir_attributes, header.cub_file_name_attributes), 'r')

    for line in file_attributes.readlines():
        line = line.rstrip()
        line_split = line.split(' ')
        attribute = '-'.join(line_split[1].split('_')[1:])
        attribute_split = attribute.split("::")
        attribute_name = attribute_split[0]
        attribute_category = header.dataset_delimiter_label.join(attribute_split)

        if len(attribute_category_whitelist) > 0 and attribute_name not in attribute_category_whitelist:
            continue

        if attribute_name not in attributes:
            attributes[attribute_name] = [header.dataset_delimiter_label.join([attribute_name, "none"])]

        if len(attribute_category_whitelist) <= 0 or attribute_category in attribute_category_whitelist[attribute_name]:
            attributes[attribute_name].append(attribute_category)
            attributes_map[line_split[0]] = attribute_category

    file_attributes.close()

    for attribute_name in attributes.keys():
        attribute = {}

        attribute["name"] = attribute_name
        attribute["labels"] = [""] + sorted(attributes[attribute_name])

        attributes_list.append(attribute)

    return (attributes_list, attributes_map)

def readMappings(attributes):
    file_images = open(os.path.join(header.dataset_dir_annotations, header.cub_file_name_images), 'r')
    file_image_attribute_labels = open(os.path.join(header.cub_dir_attributes, header.cub_file_name_image_attribute_labels), 'r')
    images_map = {}
    labels_default = {}
    mappings = {}

    for attribute in attributes[0]:
        labels_default[attribute["name"]] = header.dataset_delimiter_label.join([attribute["name"], "none"])

    for line in file_images.readlines():
        line = line.rstrip()
        line_split = line.split(' ')
        image_name = line_split[1]
        class_name = image_name.split('/')[0]

        if len(class_whitelist) > 0 and class_name not in class_whitelist:
            continue

        images_map[line_split[0]] = image_name
        mappings[image_name] = {"labels": labels_default.copy()}

    file_images.close()

    for line in file_image_attribute_labels.readlines():
        line = line.rstrip()
        line_split = line.split(' ')

        if line_split[0] not in images_map:
            continue

        image_name = images_map[line_split[0]]
        class_name = image_name.split('/')[0]
        file_name = image_name.split('/')[1]

        if len(class_whitelist) > 0 and class_name not in class_whitelist:
            continue

        if line_split[2] == "0":
            continue

        logger.log_info_raw("\033[K[INFO]: Reading mappings for \"" + file_name + "\"", end = '\r')

        if line_split[1] not in attributes[1]:
            continue

        attribute_category = attributes[1][line_split[1]]
        attribute_name = attribute_category.split(header.dataset_delimiter_label)[0]

        if len(attribute_category_whitelist) <= 0 or attribute_category in attribute_category_whitelist[attribute_name]:
            if isinstance(mappings[image_name]["labels"][attribute_name], list):
                mappings[image_name]["labels"][attribute_name].append(attribute_category)
            else:
                if mappings[image_name]["labels"][attribute_name] == header.dataset_delimiter_label.join([attribute_name, "none"]):
                    mappings[image_name]["labels"][attribute_name] = attribute_category
                else:
                    mappings[image_name]["labels"][attribute_name] = [mappings[image_name]["labels"][attribute_name], attribute_category]

    file_image_attribute_labels.close()

    logger.log_info_raw()

    return mappings

def main():
    attributes = readAttributes()
    mappings = readMappings(attributes)
    config = {}
    config["instance_wise"] = True
    config["attributes"] = pruneAttributes(attributes[0], mappings)
    config["mappings"] = mappings

    with open(os.path.join(header.config_dir, header.dataset_config_file_name), 'w') as file_config:
        json.dump(config, file_config, indent = 4)

    return

if __name__ == "__main__":
    main()
