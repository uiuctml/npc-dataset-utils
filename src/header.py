import logger

dataset_dir = "../data"
dataset_annotations_dir = dataset_dir + "/annotations"
dataset_images_dir = dataset_dir + "/images"
dataset_splits_dir = dataset_dir + "/splits"

filter_file_name = "filter.txt"
filter_print_params = True
filter_frame_ispano = 0
filter_object_keys = []
filter_object_labels = ["regulatory--stop--g1"]
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

log_level = logger.LogLevel.trace

view_file_extension = ".jpg"
view_window_height = 720
