import multiprocessing
import type

config_dir = "../config"

corrupt_corruption_algorithm = type.CorruptionAlgorithm.imagenet_c
corrupt_corruption_imagenet_c = type.CorruptionImageNetC.snow
corrupt_image_size = 224
corrupt_progress_bar_description_length = 15
corrupt_random_seed = 42
corrupt_severity = 5

dataset_config_file_name = "gtsrb.json"
dataset_delimiter_file_name = "---"
dataset_delimiter_label = "--"
dataset_dir = "../../gtsrb-dataset"
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
dataset_file_extension_annotations = ".csv"
dataset_file_extension_images = ".png"
dataset_file_name_split_test = "test.txt"
dataset_file_name_split_train = "train.txt"
dataset_file_name_split_validate = "val.txt"
dataset_label_undefined_keyword = "undefined"

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

split_config_file_name = "gtsrb_split.json.gz"
split_create_symlinks = True
split_load = True
split_percentage_train = 0.8
split_percentage_validate = 0.1
split_random_seed_percentage = 22333376
split_save = False
