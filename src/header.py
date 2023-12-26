import multiprocessing
import type

config_dir = "../config"

corrupt_corruption_algorithm = type.CorruptionAlgorithm.imagenet_c
corrupt_corruption_imagenet_c = type.CorruptionImageNetC.snow
corrupt_image_size = 224
corrupt_original = True
corrupt_progress_bar_description_length = 15
corrupt_random_seed = 42
corrupt_severity = 5

dataset_config_file_name = "dataset.json"
dataset_delimiter_file_name = "---"
dataset_delimiter_label = "--"
dataset_dir = "../../mapillary-dataset"
dataset_dir_annotations = dataset_dir + "/annotations"
dataset_dir_annotations_generated = dataset_dir_annotations + "/generated"
dataset_dir_annotations_original = dataset_dir_annotations + "/original"
dataset_dir_images = dataset_dir + "/images"
dataset_dir_images_original = dataset_dir_images + "/original"
dataset_dir_images_sliced = dataset_dir_images + "/sliced"
dataset_dir_images_sliced_generated = dataset_dir_images_sliced + "/generated"
dataset_dir_images_sliced_original = dataset_dir_images_sliced + "/original"
dataset_dir_images_split = dataset_dir_images + "/split"
dataset_dir_images_split_corrupted = dataset_dir_images_split + "/corrupted"
dataset_dir_images_split_corrupted_original = dataset_dir_images_split_corrupted + "/original"
dataset_dir_images_split_corrupted_original_test = dataset_dir_images_split_corrupted_original + "/test"
dataset_dir_images_split_corrupted_generated = dataset_dir_images_split_corrupted + "/generated"
dataset_dir_images_split_corrupted_generated_test = dataset_dir_images_split_corrupted_generated + "/test"
dataset_dir_images_split_generated = dataset_dir_images_split + "/generated"
dataset_dir_images_split_generated_test = dataset_dir_images_split_generated + "/test"
dataset_dir_images_split_generated_train = dataset_dir_images_split_generated + "/train"
dataset_dir_images_split_generated_validate = dataset_dir_images_split_generated + "/validate"
dataset_dir_images_split_original = dataset_dir_images_split + "/original"
dataset_dir_images_split_original_test = dataset_dir_images_split_original + "/test"
dataset_dir_images_split_original_train = dataset_dir_images_split_original + "/train"
dataset_dir_images_split_original_validate = dataset_dir_images_split_original + "/validate"
dataset_file_extension_annotations = ".json"
dataset_file_extension_images = ".jpg"
dataset_file_name_split_test = "test.txt"
dataset_file_name_split_train = "train.txt"
dataset_file_name_split_validate = "val.txt"
dataset_label_undefined_keyword = "undefined"
dataset_types = "/home/spn/Downloads/datasets"
dataset_mtsd_test = dataset_types + "/MTSD/test"
dataset_gtsrb_test = dataset_types + "/GTSRB/Train"
dataset_mixed_test = dataset_types + "/MIXED/test"

generate_config_file_name = "generate.json"
generate_dataset_dir_images = dataset_dir_images_sliced_original

group_config_file_name = "group.json.gz"
group_dataset_dir_images = dataset_dir_images_sliced_original
group_keyword_test = "test"
group_keyword_train_validate = "train_validate"
group_viewer_center_height = 300
group_viewer_center_width = 300
group_viewer_side_count = 3
group_viewer_side_height = 150
group_viewer_side_width = 150

label_combo_box_width = 250
label_config_file_name = dataset_config_file_name
label_dataset_dir_images = dataset_dir_images_sliced_original
label_enable_weight = False
label_viewer_height = 150
label_viewer_width = 150
label_line_edit_width = 250
label_viewer_count = 12
label_viewer_count_col = 6

mapping_file_path = dataset_types + "/GTSRB/mappings_to_mtsd.json"

log_level = type.LogLevel.debug

parallel_process_count = multiprocessing.cpu_count()
parallel_shared_memory_size_entry = 64
parallel_shared_memory_size_process = 256
parallel_shared_memory_size_total = parallel_shared_memory_size_process * (parallel_process_count + 1)

ratio_for_mixing = 0.5

slice_duplicates = {
    "vfym8z46xdpftlzctrgl78": "other-sign",
    "dchqt8ir2pap7ir940nab9315k": "other-sign",
    "5phehhkikwa0z4jrbev9vc": "other-sign"
}
slice_dataset_dir_annotations = dataset_dir_annotations_original
slice_dataset_dir_images = dataset_dir_images_original
slice_parallel_shared_memory_name = "slice"

split_basis = type.SplitBasis.percentage
split_config_file_name = "split_percentage.json.gz"
split_create_symlinks = True
split_load = True
split_percentage_train = 0.8
split_percentage_validate = 0.1
split_random_seed_percentage = 80241652
split_random_seed_stats = 11558952
split_save = False
split_std_scaler = 1.3

stats_config_file_name = "stats.json.gz"
stats_data_loader_batch_size = 384
stats_data_loader_worker_count = multiprocessing.cpu_count()
stats_gather = False
stats_model_input_height = 224
stats_model_input_width = 224
stats_plot = True
stats_save = False

test_dataset_size = 30000
