import logger

dataset_dir = "../data"
dataset_annotations_dir = dataset_dir + "/annotations"
dataset_annotations_generated_dir = dataset_annotations_dir + "/generated"
dataset_annotations_original_dir = dataset_annotations_dir + "/original"
dataset_images_dir = dataset_dir + "/images"
dataset_splits_dir = dataset_dir + "/splits"

filter_file_name = "filter.txt"
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

generate_dataset_color = {
    "name": "color",
    "regulatory--one-way-left--g1": "color--blue",
    "regulatory--one-way-right--g1": "color--blue"
}
generate_dataset_shape = {
    "name": "shape",
    "regulatory--one-way-left--g1": "shape--rectangle--wide",
    "regulatory--one-way-right--g1": "shape--rectangle--wide"
}
generate_dataset_symbol = {
    "name": "symbol",
    "regulatory--one-way-left--g1": "symbol--arrow--left",
    "regulatory--one-way-right--g1": "symbol--arrow--right"
}
generate_dataset_text = {
    "name": "text",
    "regulatory--stop--g1": "text--stop"
}
generate_datasets = [
    generate_dataset_color,
    generate_dataset_shape,
    generate_dataset_symbol,
    generate_dataset_text
]

label_file_name = "label.txt"

log_level = logger.LogLevel.trace

view_file_extension = ".jpg"
view_window_height = 720
