# CelebFaces Attributes (CelebA)

## Table of Contents

1. [Overview](#overview)
1. [Initial Directory Structure](#initial-directory-structure)
1. [Download Dataset](#download-dataset)
1. [Dataset Annotations](#dataset-annotations)
1. [Dataset Instances](#dataset-instances)
1. [Dataset Processing and Configurations](#dataset-processing-and-configurations)
1. [Dataset Splits](#dataset-splits)
1. [PC Datasets](#pc-datasets)
1. [Final Directory Structure](#final-directory-structure)

## Overview

The [CelebFaces Attributes (CelebA)](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html) dataset consists of 202,599 face images and 40 binary attribute annotations for each image.

Within the NPC project, the attribute labeling of the CelebA dataset is:

- **Instance-Wise:** Instances may have different attribute labels, even if they belong to the same class.
- **Multi-Hot:** Each attribute labeling may be assigned multiple values, e.g., an object may be labeled with more than one color.

## Initial Directory Structure

Start by creating the following directories under `npc/datasets/celeba`:

```bash
cd npc/datasets/celeba
mkdir -pv annotations archives instances
```

## Download Dataset

Download [img_align_celeba.zip](https://drive.google.com/file/d/0B7EVK8r0v71pZjFTYXZWM3FlRnM/view?usp=drive_link&resourcekey=0-dYn9z10tMJOBAkviAcfdyQ) and place the archive under `npc/datasets/celeba/archives` for future reference. Then, extract the archive:

```bash
cd npc/datasets/celeba/archives
unzip img_align_celeba.zip
```

Verify the existence of the extracted directory `npc/datasets/celeba/archives/img_align_celeba`.

## Dataset Annotations

Download the original annotation file [list_attr_celeba.txt](https://drive.google.com/file/d/0B7EVK8r0v71pblRyaVFSWGxPY0U/view?usp=drive_link&resourcekey=0-YW2qIuRcWHy_1C2VaRGL3Q) and place the file under `npc/datasets/celeba/annotations`.

Optionally, write-protect `npc/datasets/celeba/annotations` to preserve the original annotation file:

```bash
chmod -Rv a-w npc/datasets/celeba/annotations
```

## Dataset Instances

Move dataset instances into `npc/datasets/celeba/instances`:

```bash
cd npc/datasets/celeba/archives
mv -v img_align_celeba ../../instances/original
```

Verify that `npc/datasets/celeba/instances/original` contains 202,599 files, one for each instance.

Optionally, write-protect `npc/datasets/celeba/instances/original` to preserve the original instance files:

```bash
chmod -Rv a-w npc/datasets/celeba/instances/original
```

## Dataset Processing and Configurations

First, set the following parameter in `header.py`:

```python
dataset_prefix = "celeba"
dataset_file_extension_images = ".jpg"
```

Next, process and configure the dataset:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./celeba.py
```

The processed dataset instances are stored under `npc/datasets/celeba/instances/processed` as symlinks.

The generated dataset configurations are stored as `npc/npc-dataset-utils/configs/npc-dataset-utils/celeba.json`.

## Dataset Splits

The processed instances of the dataset can be split into training, validation, and testing subsets:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./split.py
```

The generated splits are stored under `npc/datasets/celeba/splits/instances`. These splits are created as symlinks pointing to the processed instances.

By default, `split.py` loads existing split configurations under `npc/npc-dataset-utils/configs/npc-dataset-utils` instead of generating new ones. This behavior ensures that the splits are deterministic and can be consistently reproduced across different environments. To generate new random splits, update the following parameters in `header.py`:

```python
split_load = False
split_save = True
```

With the above parameters, `split.py` generates, compresses, and saves new split configurations as `npc/npc-dataset-utils/configs/npc-dataset-utils/celeba_split.json.gz`. Additional aspects of split.py, e.g., random seed, split percentages, may also be customized via parameters in `header.py`.

## PC Datasets

After the dataset has been split, generate the PC datasets, which are used by the `learnspn` project to construct PCs, as follows:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./pc.py
```

The generated PC datasets are stored under `npc/datasets/celeba/splits/pc`.

## Final Directory Structure

After completing all steps above, the CelebA dataset directory structure should resemble the following:

    npc
    ├── datasets
    │   ├── celeba
    │   │   ├── annotations
    │   │   │   └── list_attr_celeba.txt
    │   │   ├── archives
    │   │   │   └── img_align_celeba.zip
    │   │   ├── instances
    │   │   │   ├── original
    │   │   │   │   ├── 000001.jpg
    │   │   │   │   └── ...
    │   │   │   └── processed
    │   │   │       ├── 0
    │   │   │       └── ...
    │   │   └── splits
    │   │       ├── instances
    │   │       │   ├── test
    │   │       │   │   ├── 0
    │   │       │   │   └── ...
    │   │       │   ├── train
    │   │       │   │   ├── 0
    │   │       │   │   └── ...
    │   │       │   └── validate
    │   │       │       ├── 0
    │   │       │       └── ...
    │   │       └── pc
    │   │           ├── test.txt
    │   │           ├── train.txt
    │   │           └── validate.txt
    │   └── ...
    └── ...

Written by [Simon Yu](https://www.simonyu.net/).
