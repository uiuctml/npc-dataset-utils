import header
import logger
import os
import PIL
import PIL.Image
import torch

class DatasetStats(torch.utils.data.Dataset):
    def __init__(self, root, transform = None):
        self.class_to_idx = []
        self.file_keys = []
        self.file_paths = []
        self.root = root
        self.transform = transform

        if not os.path.isdir(root):
            logger.log_error("Invalid dataset directory.")
            return

        for dir_name in os.listdir(root):
            dir_path = os.path.join(root, dir_name)

            for file_name in os.listdir(dir_path):
                file_key = file_name.split(header.dataset_file_extension_images)[0]
                file_path = os.path.join(root, dir_name, file_name)

                self.file_keys.append(file_key)
                self.file_paths.append(os.path.abspath(file_path))

        return

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, index):
        file_key = self.file_keys[index]
        image = PIL.Image.open(self.file_paths[index]).convert("HSV")

        if self.transform is not None:
            image = self.transform(image)

        return (image, file_key)