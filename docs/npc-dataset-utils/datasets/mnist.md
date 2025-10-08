# Modified National Institute of Standards and Technology (MNIST)

## Table of Contents

1. [Overview](#overview)
1. [Initial Directory Structure](#initial-directory-structure)
1. [Download Dataset](#download-dataset)
1. [Dataset Annotations](#dataset-annotations)
1. [Dataset Instances](#dataset-instances)
1. [Dataset Processing and Configuration](#dataset-processing-and-configuration)
1. [Dataset Splits](#dataset-splits)
1. [PC Datasets](#pc-datasets)
1. [Final Directory Structure](#final-directory-structure)

## Overview

The [Modified National Institute of Standards and Technology (MNIST)](https://www.kaggle.com/datasets/hojjatk/mnist-dataset) dataset consists of 70,000 images of handwritten digits.

Within the NPC project, the MNIST dataset is further processed into the _MNIST Addition_ dataset, as described in this [paper](https://proceedings.neurips.cc/paper_files/paper/2018/file/dc5d637ed5e62c36ecb73b654b05ba2a-Paper.pdf). In the processed MNIST Addition dataset:

- The original class annotations (digit labels) are treated as attribute annotations.
- The sum of digit pairs becomes the new class annotation, which can be automatically computed.

The attribute labeling of the MNIST Addition dataset is:

- **Instance-Wise:** Instances may have different attribute labels, even if they belong to the same class.
- **One-Hot:** Each attribute labeling is assigned a single value.

## Initial Directory Structure

Start by creating the following directories under `npc/datasets/mnist`:

```bash
cd npc/datasets/mnist
mkdir -pv annotations archives instances/archived
```

## Download Dataset

Download [archive.zip](https://www.kaggle.com/datasets/hojjatk/mnist-dataset) and place the archive under `npc/datasets/mnist/archives` for future reference. Then, extract the archive:

```bash
cd npc/datasets/mnist/archives
unzip archive.zip -d MNIST
```

Verify the existence of the extracted directory `npc/datasets/mnist/archives/MNIST`.

## Dataset Annotations

Move the original annotation files into `npc/datasets/mnist/annotations`:

```bash
cd npc/datasets/mnist/archives/MNIST
mv -v t10k-labels-idx1-ubyte/t10k-labels-idx1-ubyte ../../annotations
mv -v train-labels-idx1-ubyte/train-labels-idx1-ubyte ../../annotations
```

Optionally, write-protect `npc/datasets/mnist/annotations` to preserve the original annotation files:

```bash
chmod -Rv a-w npc/datasets/mnist/annotations
```

## Dataset Instances

Move dataset instance archives into `npc/datasets/mnist/instances/archived`:

```bash
cd npc/datasets/mnist/archives/MNIST
mv -v t10k-images-idx3-ubyte/t10k-images-idx3-ubyte ../../instances/archived
mv -v train-images-idx3-ubyte/train-images-idx3-ubyte ../../instances/archived
```

Verify that `npc/datasets/mnist/instances/archived` contains two archived files, one for each split, training and testing.

Optionally, write-protect `npc/datasets/mnist/instances/archived` to preserve the archived instance files:

```bash
chmod -Rv a-w npc/datasets/mnist/instances/archived
```

After this step, the extracted directory `npc/datasets/mnist/archives/MNIST` from `npc/datasets/mnist/archives/archive.zip` is no longer required and may be removed.

## Dataset Processing and Configuration

First, set the following parameter in `header.py`:

```python
dataset_prefix = "mnist"
dataset_file_extension_images = ".png"
```

Next, process and configure the dataset:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./mnist.py
```

The original dataset instances, extracted from the archived instance files, are stored under `npc/datasets/mnist/instances/original`.

The processed dataset instances are stored under `npc/datasets/mnist/instances/processed`.

The generated dataset configuration is stored as `npc/npc-dataset-utils/configs/npc-dataset-utils/mnist.json`. Note that the generated configuration differs from the default since the pair-matching step performed during dataset processing is randomized and not saved to file.

Optionally, write-protect `npc/datasets/mnist/instances/original` to preserve the original instance files:

```bash
chmod -Rv a-w npc/datasets/mnist/instances/original
```

## Dataset Splits

Unlike other datasets, the MNIST Addition dataset requires generating a new split configuration after processing, since the pair-matching step performed during dataset processing is randomized and not saved to file. Therefore, the default MNIST dataset split configuration provided under `npc/npc-dataset-utils/configs/npc-dataset-utils` cannot be reused and must be regenerated from the newly processed dataset.

By default, `split.py` loads the existing split configuration under `npc/npc-dataset-utils/configs/npc-dataset-utils` instead of generating new ones. This behavior ensures that the splits are deterministic and can be consistently reproduced across different environments. To generate new random splits, update the following parameters in `header.py`:

```python
split_load = False
split_save = True
```

With the above parameters, `split.py` generates, compresses, and saves the new split configuration as `npc/npc-dataset-utils/configs/npc-dataset-utils/mnist_split.json.gz`. Additional aspects of split.py, e.g., split percentages, may also be customized via parameters in `header.py`.

After updating the parameters, the processed instances of the dataset can be split into training, validation, and testing subsets:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./split.py
```

The generated splits are stored under `npc/datasets/mnist/splits/instances`. These splits are created as symlinks pointing to the processed instances.

## PC Datasets

After the dataset has been split, generate the PC datasets, which are used by the `learnspn` project to construct PCs, as follows:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./pc.py
```

The generated PC datasets are stored under `npc/datasets/mnist/splits/pc`.

## Final Directory Structure

After completing all steps above, the MNIST dataset directory structure should resemble the following:

    npc
    ├── datasets
    │   ├── mnist
    │   │   ├── annotations
    │   │   │   ├── t10k-labels-idx1-ubyte
    │   │   │   └── train-labels-idx1-ubyte
    │   │   ├── archives
    │   │   │   └── archive.zip
    │   │   ├── instances
    │   │   │   ├── archived
    │   │   │   │   ├── t10k-images-idx3-ubyte
    │   │   │   │   └── train-images-idx3-ubyte
    │   │   │   ├── original
    │   │   │   │   ├── 0
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
