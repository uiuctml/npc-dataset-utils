# VISAT Dataset Tools

## Overview

This codebase contains tools and scripts for creating and processing the VISAT open dataset.

## Prerequisites

This codebase was developed on Ubuntu 20.04 LTS and requires the following packages:

 - (apt) python3-pip [20.0.2-5ubuntu1.8]
 - (apt) python3-opencv [4.2.0+dfsg-5]
 - (pip) pyqt5 [5.15.2]
 - (pip) scikit-image [0.18.0]
 - (pip) tqdm [4.64.1]

Additionally, the ImageNet-C codebase is also required and can be installed as follows:

```bash
git clone https://github.com/hendrycks/robustness.git
cd robustness/
git checkout 8190fe3
cd ImageNet-C/imagenet_c/
python3 -m pip install -e .
```

Before attempting to launch a script, please refer to `header.py` and ensure that all relevant parameters, such as dataset image directory paths, ImageNet-C corruption type, etc., are properly set.

## Dataset Split Symlink Generation

To reduce storage footprint, the dataset splits are encoded as symlinks pointing to the actual dataset images.

Under the project directory, the dataset split symlinks can be generated as follows:

```bash
cd src/
./split.py

```

## Visual Attribute Rapid Labeling Interface

The visual attribute rapid labeling interface allows for the efficient creation of visual attribute labels for the VISAT dataset.

Under the project directory, the labeling interface can be launched as follows:

```bash
cd src/
./label.py

```

## Visual Attribute Symlink Generation

To reduce storage footprint, the mapping between the 401 original class labels and the visual attribute labels is encoded as symlinks pointing to the actual dataset images. Please note that we plan to further improve the visual attribute encoding in the future by eliminating the creation of symlinks altogether. Instead, we shall create a custom data loader that directly parses encoding from the `visual_attribute_mappings.json` JSON file.

Under the project directory, the visual attribute symlinks can be generated as follows:

```bash
cd src/
./generate.py

```

## Distribution Shift Testing Split Generation

The distribution shift testing splits are generated using either ImageNet-C corruptions or color quantization.

Under the project directory, a distribution shift testing split can be generated as follows:

```bash
cd src/
./corrupt.py

```

## Adversarial Attack Testing Split Generation

The adversarial attack testing splits are generated using projected gradient descent (PGD).

Under the project directory, an adversarial attack testing split for a base ResNet-152 model can be generated as follows:

```bash
cd src/
./pgd152.py
```

Under the project directory, an adversarial attack testing split for a base ViT-B/32 model can be generated as follows:

```bash
cd src/
./pgdvit.py
```

Under the project directory, an adversarial attack testing split for an MTL model can be generated as follows:

```bash
cd src/
./mtlattack.py
```

For the above adversarial attack scripts, please use `--help` to examine their respectively required arguments.
