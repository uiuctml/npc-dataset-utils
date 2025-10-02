import os
import type

config_dir = "../../configs/npc-dataset-utils"

dataset_prefix = "awa2"
dataset_config_file_name = dataset_prefix + ".json"
dataset_delimiter_file_name = "---"
dataset_delimiter_label = "--"
dataset_dir = os.path.join("../../../datasets", dataset_prefix)
dataset_dir_annotations = os.path.join(dataset_dir, "annotations")
dataset_dir_instances = os.path.join(dataset_dir, "instances")
dataset_dir_instances_archived = os.path.join(dataset_dir_instances, "archived")
dataset_dir_instances_original = os.path.join(dataset_dir_instances, "original")
dataset_dir_instances_processed = os.path.join(dataset_dir_instances, "processed")
dataset_dir_splits = os.path.join(dataset_dir, "splits")
dataset_dir_splits_instances = os.path.join(dataset_dir_splits, "instances")
dataset_dir_splits_instances_test = os.path.join(dataset_dir_splits_instances, "test")
dataset_dir_splits_instances_train = os.path.join(dataset_dir_splits_instances, "train")
dataset_dir_splits_instances_validate = os.path.join(dataset_dir_splits_instances, "validate")
dataset_dir_splits_pc = os.path.join(dataset_dir_splits, "pc")
dataset_file_extension_images = ".jpg"
dataset_label_undefined_keyword = "none"

awa2_file_name_classes = "classes.txt"
awa2_file_name_matrix = "predicate-matrix-binary.txt"
awa2_file_name_predicates = "predicates.txt"

celeba_count_attributes = 8
celeba_file_name_attributes = "list_attr_celeba.txt"

examine_config_file_name = dataset_config_file_name
examine_dataset_dir_images = dataset_dir_instances_processed
examine_viewer_height = 150
examine_viewer_width = 150
examine_viewer_count = 24
examine_viewer_count_col = 6

label_combo_box_width = 250
label_config_file_name = dataset_config_file_name
label_dataset_dir_images = dataset_dir_instances_processed
label_viewer_height = 150
label_viewer_width = 150
label_line_edit_width = 250
label_viewer_count = 12
label_viewer_count_col = 6

log_level = type.LogLevel.info

mnist_attributes = ["number-first", "number-second"]
mnist_file_extension_images = ".png"
mnist_file_name_images_test = "t10k-images-idx3-ubyte"
mnist_file_name_images_train = "train-images-idx3-ubyte"
mnist_file_name_labels_test = "t10k-labels-idx1-ubyte"
mnist_file_name_labels_train = "train-labels-idx1-ubyte"
mnist_random_seed = 42

pc_random_seed = 42

split_config_file_name = dataset_prefix + "_split.json.gz"
split_create_symlinks = True
split_dataset_dir_images = dataset_dir_instances_processed
split_load = True
split_percentage_train = 0.8
split_percentage_validate = 0.1
split_random_seed_percentage = 22333376
split_save = False
