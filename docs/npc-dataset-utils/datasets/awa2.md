# Animals with Attributes 2 (AwA2)

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

The AwA2 dataset consists of 37322 images of 50 animals classes, with 85 numeric attribute values for each class. Within the scope of the NPC project, the attribute labeling of the AwA2 dataset is _class-wise_, meaning all instances under the same class have the same attribute labeling, and _multi-hot_, meaning the labeled attribute categories may have more than one values, e.g., an object may have more than one color.

## Initial Directory Structure

Start by creating the following directories under `npc/datasets/awa2` as follows:

```bash
cd npc/datasets/awa2
mkdir -pv annotations archives instances/original
```

## Download Dataset

Download [AwA2-data.zip](https://cvml.ista.ac.at/AwA2/AwA2-data.zip) and save the archive under `npc/datasets/awa2/archives` for future reference. Then, extract the downloaded archive as follows:

```bash
cd npc/datasets/awa2/archives
unzip AwA2-data.zip
```

## Dataset Annotations

Place the original dataset annotation files under `npc/datasets/awa2/annotations` as follows:

```bash
cd npc/datasets/awa2/archives/Animals_with_Attributes2
mv -v classes.txt ../../annotations
mv -v predicate-matrix-binary.txt ../../annotations
mv -v predicates.txt ../../annotations
```

Optionally, write-protect `npc/datasets/awa2/annotations` to prevent modifications to the original annotation files as follows:

```bash
chmod -Rv a-w npc/datasets/awa2/annotations
```

## Dataset Instances

Place all dataset instances under `npc/datasets/awa2/instances/original` as follows:

```bash
mv -v Animals_with_Attributes2/JPEGImages/* npc/datasets/awa2/instances/original
```

Verify the number of categories under `npc/datasets/awa2/instances/original` to be 50.

Optionally, write-protect `npc/datasets/awa2/instances/original` to prevent modifications to the original instance files as follows:

```bash
chmod -Rv a-w npc/datasets/awa2/instances/original
```

At this point, `npc/datasets/awa2/archives/Animals_with_Attributes2`, extracted from `npc/datasets/awa2/archives/AwA2-data.zip`, is no longer needed and may be removed.

## Dataset Processing and Configurations

For the NPC project, there are no manipulations done to the original AwA2 instances. To ensure compatibility, however, create a symlink that points to `npc/datasets/awa2/instances/original` as follows:

```bash
cd npc/datasets/awa2/instances
ln -sv original processed
```

At this point, the AwA2 dataset is ready to be configured. First, set parameters in `header.py` as follows:

```python
dataset_prefix = "awa2"
```

Then, configure the dataset as follows:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./awa2.py
```

The generated dataset configurations are stored as `npc/npc-dataset-utils/configs/npc-dataset-utils/awa2.json`.

## Dataset Splits

The processed instances of the dataset can be split into three subsets, training, validation, and test, as follows:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./split.py
```

The generated splits from processed instances are stored under `npc/datasets/awa2/splits/instances` in the form of symlinks.

By default, `split.py` loads the existing split configurations under `npc/npc-dataset-utils/configs/npc-dataset-utils` instead of generating new ones such that each subsequent splitting of the dataset is deterministic and can be replicated across different environments. However, in the case where generating a brand-new split is needed, set parameters in `header.py` as follows:

```python
split_load = False
split_save = True
```

The above parameters enable `split.py` to generate new, random split configurations, compress them, and save them as `npc/npc-dataset-utils/configs/npc-dataset-utils/awa2_split.json.gz`. Other aspects of `split.py`, such as random seed, split percentages, etc., may also be configured using the additional parameters in `header.py`.

## PC Datasets

After splitting the dataset, the PC datasets, used by the `learnspn` project to generate PCs, are then generated from the splits as follows:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./pc.py
```

The generated PC datasets are stored under `npc/datasets/awa2/splits/pc`.

## Final Directory Structure

In the end, the directory structure for the AwA2 is as follows:

    npc
    ├── datasets
    │   ├── awa2
    │   │   ├── annotations
    │   │   │   ├── classes.txt
    │   │   │   ├── predicate-matrix-binary.txt
    │   │   │   └── predicates.txt
    │   │   ├── archives
    │   │   │   └── AwA2-data.zip
    │   │   ├── instances
    │   │   │   ├── original
    │   │   │   │   ├── antelope
    │   │   │   │   └── ...
    │   │   │   └── processed
    │   │   │       ├── antelope
    │   │   │       └── ...
    │   │   └── splits
    │   │       ├── instances
    │   │       │   ├── test
    │   │       │   │   ├── antelope
    │   │       │   │   └── ...
    │   │       │   ├── train
    │   │       │   │   ├── antelope
    │   │       │   │   └── ...
    │   │       │   └── validate
    │   │       │       ├── antelope
    │   │       │       └── ...
    │   │       └── pc
    │   │           ├── test.txt
    │   │           ├── train.txt
    │   │           └── validate.txt
    │   └── ...
    └── ...
