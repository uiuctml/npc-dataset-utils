import logger

config_dir = "../config"
dataset_dir = "../dataset"
dataset_dir_annotations = dataset_dir + "/annotations"
dataset_dir_annotations_generated = dataset_dir_annotations + "/generated"
dataset_dir_annotations_original = dataset_dir_annotations + "/original"
dataset_dir_images = dataset_dir + "/images"
dataset_dir_images_original = dataset_dir_images + "/original"
dataset_dir_images_sliced = dataset_dir_images + "/sliced"
dataset_dir_splits = dataset_dir + "/splits"
dataset_file_extension_annotations = ".json"
dataset_file_extension_images = ".jpg"

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

generate_config_file_name = "generate.config"

label_combo_box_width = 250
label_config_file_name = "label.config"
label_dataset_dir_images = dataset_dir_images_sliced + "/original"
label_viewer_height = 150
label_viewer_width = 150
label_line_edit_width = 250
label_viewer_count = 15
label_viewer_count_row = 5

log_level = logger.LogLevel.trace

slice_dataset_dir_annotations = dataset_dir_annotations_original
slice_dataset_dir_images = dataset_dir_images_original

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
