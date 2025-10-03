# German Traffic Sign Recognition Benchmark (GTSRB)

## Table of Contents

1. [Overview](#overview)
1. [Initial Directory Structure](#initial-directory-structure)
1. [Download Dataset](#download-dataset)
1. [Dataset Annotations](#dataset-annotations)
1. [Dataset Instances](#dataset-instances)
1. [Dataset Processing and Configuration](#dataset-processing-and-configuration)
1. [Dataset Splits](#dataset-splits)
1. [Dataset Verification](#dataset-verification)
1. [PC Datasets](#pc-datasets)
1. [Final Directory Structure](#final-directory-structure)

## Overview

The [German Traffic Sign Recognition Benchmark (GTSRB)](https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign) dataset consists of more than 50,000 images spanning over 40 traffic sign classes. Unlike other datasets, GTSRB does not provide native attribute annotations.

Within the NPC project, the attribute labeling of the GTSRB dataset is created using the [NPC Attribute Labeling Utility](docs/npc-dataset-utils/utilities/label.md). The labeling is:

- **Class-Wise:** All instances within the same class share identical attribute labels.
- **One-Hot:** Each attribute labeling is assigned a single value, e.g., an object is labeled with a single color, typically the most prominent one, even if multiple colors are present.

## Initial Directory Structure

Start by creating the following directories under `npc/datasets/gtsrb`:

```bash
cd npc/datasets/gtsrb
mkdir -pv archives instances
```

## Download Dataset

Download [archive.zip](https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign) and place the archive under `npc/datasets/gtsrb/archives` for future reference. Then, extract the archive:

```bash
cd npc/datasets/gtsrb/archives
unzip archive.zip -d GTSRB
```

Verify the existence of the extracted directory `npc/datasets/gtsrb/archives/GTSRB`.

## Dataset Annotations

The GTSRB dataset does not provide native attribute annotations. Within the NPC project, the GTSRB attribute labels are created using the [NPC Attribute Labeling Utility](docs/npc-dataset-utils/utilities/label.md).

In addition, the official testing split of GTSRB does not include class annotations, as it was originally intended for competition use. Therefore, only the training split is used in the NPC project.

## Dataset Instances

Move dataset instances into `npc/datasets/gtsrb/instances`:

```bash
cd npc/datasets/gtsrb/archives/GTSRB
mv -v Train ../../instances/original
```

Verify that `npc/datasets/gtsrb/instances/original` contains 43 directories, one for each class.

Optionally, write-protect `npc/datasets/gtsrb/instances/original` to preserve the original instance files:

```bash
chmod -Rv a-w npc/datasets/gtsrb/instances/original
```

After this step, the extracted directory `npc/datasets/gtsrb/archives/GTSRB` from `npc/datasets/gtsrb/archives/archive.zip` is no longer required and may be removed.

## Dataset Processing and Configuration

First, set the following parameters in `header.py`:

```python
dataset_prefix = "gtsrb"
dataset_file_extension_images = ".png"
```

Next, process the dataset:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./gtsrb.py
```

The processed dataset instances are stored under `npc/datasets/gtsrb/instances/processed` as symlinks.

Note that `gtsrb.py` does not generate the dataset configuration, which is instead created using the [NPC Attribute Labeling Utility](docs/npc-dataset-utils/utilities/label.md) during the attribute labeling process and is stored as `npc/npc-dataset-utils/configs/npc-dataset-utils/gtsrb.json`.

## Dataset Splits

The processed instances of the dataset can be split into training, validation, and testing subsets:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./split.py
```

The generated splits are stored under `npc/datasets/gtsrb/splits/instances`. These splits are created as symlinks pointing to the processed instances.

By default, `split.py` loads the existing split configuration under `npc/npc-dataset-utils/configs/npc-dataset-utils` instead of generating new ones. This behavior ensures that the splits are deterministic and can be consistently reproduced across different environments. To generate new random splits, update the following parameters in `header.py`:

```python
split_load = False
split_save = True
```

With the above parameters, `split.py` generates, compresses, and saves the new split configuration as `npc/npc-dataset-utils/configs/npc-dataset-utils/gtsrb_split.json.gz`. Additional aspects of split.py, e.g., random seed, split percentages, may also be customized via parameters in `header.py`.

## Dataset Verification

Once the dataset has been processed and configured, run the verification to check for any duplicated, invalid, missing, or unused attributes in the dataset configuration, as well as any empty categories within the dataset splits.

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./verify.py
```

Note that `verify.py` does not currently support instance-wise datasets.

## PC Datasets

After the dataset has been split, generate the PC datasets, which are used by the `learnspn` project to construct PCs, as follows:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./pc.py
```

The generated PC datasets are stored under `npc/datasets/gtsrb/splits/pc`.

## Final Directory Structure

After completing all steps above, the GTSRB dataset directory structure should resemble the following:

    npc
    ├── datasets
    │   ├── gtsrb
    │   │   ├── archives
    │   │   │   └── archive.zip
    │   │   ├── instances
    │   │   │   ├── original
    │   │   │   │   ├── 0
    │   │   │   │   └── ...
    │   │   │   └── processed
    │   │   │       ├── regulatory--end-of-maximum-speed-limit-80
    │   │   │       └── ...
    │   │   └── splits
    │   │       ├── instances
    │   │       │   ├── test
    │   │       │   │   ├── regulatory--end-of-maximum-speed-limit-80
    │   │       │   │   └── ...
    │   │       │   ├── train
    │   │       │   │   ├── regulatory--end-of-maximum-speed-limit-80
    │   │       │   │   └── ...
    │   │       │   └── validate
    │   │       │       ├── regulatory--end-of-maximum-speed-limit-80
    │   │       │       └── ...
    │   │       └── pc
    │   │           ├── test.txt
    │   │           ├── train.txt
    │   │           └── validate.txt
    │   └── ...
    └── ...

Written by [Simon Yu](https://www.simonyu.net/).
