import multiprocessing
import type

config_dir = "../config"
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

filter_dataset_dir_annotations = dataset_dir_annotations_original
filter_file_name = "filter_" + filter_dataset_dir_annotations.split("/")[-1] + ".txt"
filter_print_params = True
filter_frame_ispano = 0
filter_object_keys = []
filter_object_labels = ["regulatory--one-way-left--g1", "regulatory--one-way-right--g1"]
filter_object_properties = False
filter_object_barrier = 0
filter_object_occluded = 0
filter_object_out_of_frame = 0
filter_object_exterior = 0
filter_object_ambiguous = 0
filter_object_included = 0
filter_object_direction_or_information = 0
filter_object_highway = 0
filter_object_dummy = 0

generate_config_file_name = "generate.json"
generate_dataset_dir_images = dataset_dir_images_sliced + "/original"

label_combo_box_width = 250
label_config_file_name = dataset_config_file_name
label_dataset_dir_images = dataset_dir_images_sliced + "/original"
label_viewer_height = 150
label_viewer_width = 150
label_line_edit_width = 250
label_viewer_count = 12
label_viewer_count_col = 6

log_level = type.LogLevel.trace

slice_dataset_dir_annotations = dataset_dir_annotations_original
slice_dataset_dir_images = dataset_dir_images_original
slice_process_count = multiprocessing.cpu_count()
slice_shared_memory_name = "slice"
slice_shared_memory_size_entry = 64
slice_shared_memory_size_process = 256
slice_shared_memory_size_total = slice_shared_memory_size_process * (slice_process_count + 1)

split_generated_percentage_train = 0.8
split_generated_percentage_validate = 0.1
split_original_percentage_train = 0.8
split_original_percentage_validate = 0.1
split_random_seed = 10241048

verify_dataset_dir_images_split = dataset_dir_images_split + "/original"

view_bounding_box_color = (0, 255, 0)
view_bounding_box_text_color = (0, 0, 0)
view_bounding_box_text_margin_x = 10
view_bounding_box_text_margin_y = 10
view_bounding_box_text_size = 1
view_bounding_box_thickness = 3
view_dataset_dir_annotations = dataset_dir_annotations_original
view_dataset_dir_images = dataset_dir_images_original
view_filter_file_name = "filter_" + filter_dataset_dir_annotations.split("/")[-1] + ".txt"
view_window_height = 900
