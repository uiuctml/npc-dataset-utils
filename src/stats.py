#!/usr/bin/env python3

import dataset as dset
import gzip
import header
import json
import logger
import os
import torch
import torchvision
import tqdm

def saveAverageBrightnesses(average_brightnesses, file_keys):
    average_brightnesses = average_brightnesses.cpu()
    config = {}
    file_path_config = os.path.join(header.config_dir, header.stats_config_file_name)

    if os.path.isfile(file_path_config):
        file_config = gzip.open(file_path_config, "r")
        config_json_encoded = file_config.read()
        file_config.close()

        config_json = config_json_encoded.decode("utf-8")
        config = json.loads(config_json)

    config["average_brightnesses"] = {}

    for (average_brightness, file_key) in zip(average_brightnesses, file_keys):
        config["average_brightnesses"][file_key] = average_brightness.item()

    with open(file_path_config, "w") as file_config:
        json.dump(config, file_config, indent = 4)

    config_json = json.dumps(config, indent = 4)
    config_json_encoded = config_json.encode("utf-8")

    with gzip.open(file_path_config, "w") as file_config:
        file_config.write(config_json_encoded)

    logger.log_info("Saved dataset splits to \"" + file_path_config + "\".")

    return

def main():
    average_brightnesses = torch.Tensor()
    dataset_transforms = torchvision.transforms.Compose([
        torchvision.transforms.Resize((header.stats_model_input_height, header.stats_model_input_width)),
        torchvision.transforms.ToTensor(),
    ])
    dataset = dset.DatasetStats(header.dataset_dir_images_sliced_original, dataset_transforms)
    data_loader = torch.utils.data.DataLoader(dataset, batch_size = header.stats_data_loader_batch_size, shuffle = False, num_workers = header.stats_data_loader_worker_count, pin_memory = True)
    device = torch.device("cuda")
    file_keys = []
    progress_bar = tqdm.tqdm(total = len(data_loader), position = 0, leave = False)

    average_brightnesses = average_brightnesses.to(device, non_blocking = True)
    progress_bar.set_description_str("[INFO]: Batch")

    for (batch_index, (input, file_key)) in enumerate(data_loader):
        input = input.to(device, non_blocking = True)

        brightness = input[:, 2, :, :]
        average_brightness = torch.mean(brightness, dim = [1, 2])
        average_brightnesses = torch.cat((average_brightnesses, average_brightness))
        file_keys += file_key

        progress_bar.n = batch_index + 1
        progress_bar.refresh()

    progress_bar.close()

    saveAverageBrightnesses(average_brightnesses, file_keys)

    return

if __name__ == "__main__":
    main()
