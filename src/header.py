import multiprocessing
import type

config_dir = "../configs"

dataset_config_file_name = "cub.json"
dataset_delimiter_file_name = "---"
dataset_delimiter_label = "--"
dataset_dir = "../../../datasets/cub-dataset"
dataset_dir_annotations = dataset_dir + "/annotations"
dataset_dir_images = dataset_dir + "/images"
dataset_dir_images_original = dataset_dir_images + "/original"
dataset_dir_images_sliced = dataset_dir_images + "/sliced"
dataset_dir_images_split = dataset_dir_images + "/split"
dataset_dir_images_split_corrupted = dataset_dir_images_split + "/corrupted"
dataset_dir_images_split_corrupted_test = dataset_dir_images_split_corrupted + "/test"
dataset_dir_images_split_original = dataset_dir_images_split + "/original"
dataset_dir_images_split_original_test = dataset_dir_images_split_original + "/test"
dataset_dir_images_split_original_train = dataset_dir_images_split_original + "/train"
dataset_dir_images_split_original_validate = dataset_dir_images_split_original + "/validate"
dataset_dir_images_split_spn = dataset_dir_images_split + "/spn"
dataset_dir_splits = dataset_dir + "/splits"
dataset_file_extension_annotations = ".csv"
dataset_file_extension_images = ".jpg"
dataset_file_name_split_test = "test.txt"
dataset_file_name_split_train = "train.txt"
dataset_file_name_split_validate = "val.txt"
dataset_label_undefined_keyword = "undefined"

analysis_config_file_name = dataset_config_file_name
analysis_threshold_max = False

cub_dir_attributes = dataset_dir_annotations + "/attributes"
cub_dir_splits_cbm = dataset_dir_splits + "/cbm"
cub_file_name_attributes = "attributes.txt"
cub_file_name_images = "images.txt"
cub_file_name_image_attribute_labels = "image_attribute_labels.txt"
cub_file_name_split_cbm_test = "test.pkl"
cub_file_name_split_cbm_train = "train.pkl"
cub_file_name_split_cbm_validate = "val.pkl"
cub_filter_by_attribute_uniqueness = False
cub_filter_by_certainty = False

examine_combo_box_width = 250
examine_config_file_name = dataset_config_file_name
examine_dataset_dir_images = dataset_dir_images_sliced
examine_viewer_height = 150
examine_viewer_width = 150
examine_viewer_count = 24
examine_viewer_count_col = 6

gtsrb_config_file_name = dataset_config_file_name
gtsrb_dataset_dir_images = dataset_dir_images_sliced

label_combo_box_width = 250
label_config_file_name = dataset_config_file_name
label_dataset_dir_images = dataset_dir_images_sliced
label_viewer_height = 150
label_viewer_width = 150
label_line_edit_width = 250
label_viewer_count = 12
label_viewer_count_col = 6

log_level = type.LogLevel.info

mnist_attributes = ["number-first", "number-second"]
mnist_dir_images_addition = dataset_dir_images + "/addition"
mnist_file_extension_images = ".png"
mnist_file_name_images_test = "t10k-images-idx3-ubyte"
mnist_file_name_images_train = "train-images-idx3-ubyte"
mnist_file_name_labels_test = "t10k-labels-idx1-ubyte"
mnist_file_name_labels_train = "train-labels-idx1-ubyte"
mnist_random_seed = 42

parallel_process_count = multiprocessing.cpu_count()
parallel_shared_memory_size_entry = 64
parallel_shared_memory_size_process = 256
parallel_shared_memory_size_total = parallel_shared_memory_size_process * (parallel_process_count + 1)

slice_duplicates = {
    "vfym8z46xdpftlzctrgl78": "other-sign",
    "dchqt8ir2pap7ir940nab9315k": "other-sign",
    "5phehhkikwa0z4jrbev9vc": "other-sign"
}
slice_dataset_dir_annotations = dataset_dir_annotations
slice_dataset_dir_images = dataset_dir_images_original
slice_label_excluded = {
    "other-sign"
}
slice_parallel_shared_memory_name = "slice"

split_config_file_name = "cub_split.json.gz"
split_create_symlinks = True
split_dataset_dir_images = dataset_dir_images_sliced
split_load = True
split_percentage_train = 0.8
split_percentage_validate = 0.1
split_random_seed_percentage = 22333376
split_save = False
