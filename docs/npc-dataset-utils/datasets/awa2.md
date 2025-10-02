# Animals with Attributes 2 (AwA2)

## Table of Contents

1. [Overview](#overview)
1. [Initial Directory Structure](#initial-directory-structure)
1. [Download Dataset](#download-dataset)
1. [Dataset Annotations](#dataset-annotations)
1. [Dataset Instances](#dataset-instances)
1. [Dataset Processing and Configurations](#dataset-processing-and-configurations)
1. [Dataset Splits](#dataset-splits)
1. [Dataset Verification](#dataset-verification)
1. [PC Datasets](#pc-datasets)
1. [Final Directory Structure](#final-directory-structure)

## Overview

The [Animals with Attributes 2 (AwA2)](https://cvml.ista.ac.at/AwA2/) dataset consists of 37,322 images of 50 animal classes, with 85 numeric attribute values for each class. Within the NPC project, the attribute labeling of the AwA2 dataset is _class-wise_, where all instances within the same class share identical attribute labels, and _multi-hot_, where the labeled attribute categories may have multiple values, e.g., an object may be labeled with more than one color.

## Initial Directory Structure

Start by creating the following directories under `npc/datasets/awa2`:

```bash
cd npc/datasets/awa2
mkdir -pv annotations archives instances
```

## Download Dataset

Download [AwA2-data.zip](https://cvml.ista.ac.at/AwA2/AwA2-data.zip) and place the archive under `npc/datasets/awa2/archives` for future reference. Then, extract the archive:

```bash
cd npc/datasets/awa2/archives
unzip AwA2-data.zip
```

Verify that the extracted directory `Animals_with_Attributes2` appears under `npc/datasets/awa2/archives`.

## Dataset Annotations

Move the original annotation files into `npc/datasets/awa2/annotations`:

```bash
cd npc/datasets/awa2/archives/Animals_with_Attributes2
mv -v classes.txt ../../annotations
mv -v predicate-matrix-binary.txt ../../annotations
mv -v predicates.txt ../../annotations
```

Optionally, write-protect `npc/datasets/awa2/annotations` to preserve the original annotation files:

```bash
chmod -Rv a-w npc/datasets/awa2/annotations
```

## Dataset Instances

Move dataset instances into `npc/datasets/awa2/instances`:

```bash
cd npc/datasets/awa2/archives/Animals_with_Attributes2
mv -v JPEGImages ../../instances/original
```

Verify that `npc/datasets/awa2/instances/original` contains 50 directories, one for each class.

Optionally, write-protect `npc/datasets/awa2/instances/original` to preserve the original instance files:

```bash
chmod -Rv a-w npc/datasets/awa2/instances/original
```

After this step, the extracted directory `npc/datasets/awa2/archives/Animals_with_Attributes2` from `npc/datasets/awa2/archives/AwA2-data.zip` is no longer required and shall be removed.

## Dataset Processing and Configurations

For the NPC project, the original AwA2 instances are left unmodified. To maintain compatibility, create a symlink named `processed` that points to `npc/datasets/awa2/instances/original`:

```bash
cd npc/datasets/awa2/instances
ln -sv original processed
```

At this point, the AwA2 dataset is ready to be configured. First, set the following parameter in `header.py`:

```python
dataset_prefix = "awa2"
```

Next, configure the dataset:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./awa2.py
```

The generated dataset configurations are stored as `npc/npc-dataset-utils/configs/npc-dataset-utils/awa2.json`.

## Dataset Splits

The processed instances of the dataset can be split into training, validation, and testing subsets:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./split.py
```

The generated splits are stored under `npc/datasets/awa2/splits/instances`. These splits are created as symlinks pointing to the processed instances.

By default, `split.py` loads existing split configurations under `npc/npc-dataset-utils/configs/npc-dataset-utils` instead of generating new ones. This behavior ensures that the splits are deterministic and can be consistently reproduced across different environments. To generate new random splits, update the following parameters in `header.py`:

```python
split_load = False
split_save = True
```

With the above parameters, `split.py` generates, compresses, and saves new split configurations as `npc/npc-dataset-utils/configs/npc-dataset-utils/awa2_split.json.gz`. Additional aspects of split.py, e.g., random seed, split percentages, may also be customized via parameters in `header.py`.

## Dataset Verification

Once the dataset has been processed and configured, run the verification to check for any duplicated, invalid, missing, or unused attributes in the dataset configurations, as well as any empty categories within the dataset splits.

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

The generated PC datasets are stored under `npc/datasets/awa2/splits/pc`.

## Final Directory Structure

After completing all steps above, the AwA2 dataset directory structure should resemble the following:

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

Written by [Simon Yu](https://www.simonyu.net/).
