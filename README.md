# NPC Dataset Utilities

## Table of Contents

1. [Project Overview](#project-overview)
1. [Project Prerequisites](#project-prerequisites)
1. [Project Hierarchy](#project-hierarchy)
1. [Setting Up the Datasets](#setting-up-the-datasets)
1. [NPC Attribute Utilities](#npc-attribute-utilities)
1. [Publications](#publications)
1. [Acknowledgements](#acknowledgements)
1. [License](#license)
1. [Contact](#contact)

## Project Overview

This codebase provides utilities for processing and manipulating datasets for the Neural Probabilistic Circuit (NPC) project. The NPC project focuses on the following four datasets:

- [Animals with Attributes 2 (AwA2)](https://cvml.ista.ac.at/AwA2/)
- [CelebFaces Attributes (CelebA)](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)
- [German Traffic Sign Recognition Benchmark (GTSRB)](https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign)
- [Modified National Institute of Standards and Technology (MNIST)](https://www.kaggle.com/datasets/hojjatk/mnist-dataset)

Scripts are provided for each dataset to process and organize them into the format and structure required by the NPC pipeline. For the NPC project, the MNIST dataset is further processed into the _MNIST Addition_ dataset, as described in this [paper](https://proceedings.neurips.cc/paper_files/paper/2018/file/dc5d637ed5e62c36ecb73b654b05ba2a-Paper.pdf).

Certain datasets, such as GTSRB, lack attribute labels. To address this, the codebase includes [NPC Attribute Utilities](#npc-attribute-utilities), which allows users to create and examine attribute labels for any dataset. A verification script is also included to check the dataset configuration for the consistency and correctness of user-created labels.

In addition, utility scripts are available for splitting datasets into training, validation, and testing subsets, and for generating Probabilistic Circuit (PC) datasets from those splits. These PC datasets are then used by the `learnspn` project to construct and generate PCs.

## Project Prerequisites

This project requires the following system packages:

Ubuntu:

```bash
apt install libgl1-mesa-dev python3-natsort python3-numpy python3-opencv python3-pil python3-pyqt5 python3-tqdm unzip
```

Arch Linux:

```bash
pacman -S mesa python-natsort python-numpy python-opencv python-pillow python-pyqt5 python-tqdm unzip
```

This project was developed on Ubuntu and tested on both Ubuntu and Arch Linux. Other Linux distributions, macOS, or Windows Subsystem for Linux (WSL) may also work with additional setup. However, these platforms are not officially supported.

This project is designed to run directly on the operating system, without any Python virtual environments such as Conda. Using such environments is unnecessary and not recommended. Additionally, avoid installing Python packages via `pip` unless explicitly instructed. Packages from the system package manager are preferred.

## Project Hierarchy

This project is part of the NPC pipeline. To ensure compatibility and maintain consistent references across the pipeline, organize the project directories as follows:

    npc
    ├── datasets
    │   ├── awa2
    │   ├── celeba
    │   ├── gtsrb
    │   └── mnist
    ├── learnspn
    ├── npc-dataset-utils
    └── npc-models

All subsequent instructions assume the above project hierarchy.

The `npc/datasets` directory does not exist by default. Create the initial directory structure as follows:

```bash
cd npc
mkdir -pv datasets/awa2 datasets/celeba datasets/gtsrb datasets/mnist
```

## Setting Up the Datasets

The NPC pipeline relies on multiple datasets, each requiring setup steps to ensure compatibility and reproducibility. To clarify this process, dedicated setup guides are provided for each dataset, covering directory structures, file handling, processing, configuration, and PC dataset generation.

Detailed instructions for setting up and organizing dataset contents within `npc/datasets` are provided in the following documents:

- [Animals with Attributes 2 (AwA2)](docs/npc-dataset-utils/datasets/awa2.md)
- [CelebFaces Attributes (CelebA)](docs/npc-dataset-utils/datasets/celeba.md)
- [German Traffic Sign Recognition Benchmark (GTSRB)](docs/npc-dataset-utils/datasets/gtsrb.md)
- [Modified National Institute of Standards and Technology (MNIST)](docs/npc-dataset-utils/datasets/mnist.md)

## NPC Attribute Utilities

The NPC attribute utilities are a set of Qt-based graphical software designed for labeling and examining dataset attributes within the NPC pipeline. These utilities are especially important for datasets that lack native attribute annotations, such as GTSRB, enabling users to define, edit, and review attributes in a consistent format that downstream components expect.

Together, the utilities streamline both the creation of new attribute labels and the examination of labeled data across classes, helping ensure the correctness, consistency, and validity of the attribute labels created for datasets used in the NPC project.

Detailed usage instructions are available in the following documents:

- [NPC Attribute Labeling Utility](docs/npc-dataset-utils/utilities/label.md)
- [NPC Attribute Examining Utility](docs/npc-dataset-utils/utilities/examine.md)

Preview of the NPC attribute utilities:

![NPC Attribute Labeling Utility](docs/npc-dataset-utils/images/label.png)
![NPC Attribute Examining Utility](docs/npc-dataset-utils/images/examine.png)

## Publications

Upon using this project, cite any relevant publications listed below:

### Neural Probabilistic Circuit (NPC)

```
@article{chen2025neural,
  title={Neural probabilistic circuits: Enabling compositional and interpretable predictions through logical reasoning},
  author={Chen, Weixin and Yu, Simon and Shao, Huajie and Sha, Lui and Zhao, Han},
  journal={arXiv preprint arXiv:2501.07021},
  year={2025}
}
```

```
@inproceedings{chenneural,
  title={Neural Probabilistic Circuits: An Overview},
  author={Chen, Weixin and Yu, Simon and Shao, Huajie and Sha, Lui and Zhao, Han},
  booktitle={Eighth Workshop on Tractable Probabilistic Modeling}
}
```

### Animals with Attributes 2 (AwA2)

```
@inproceedings{xian2017zero,
  title={Zero-shot learning-the good, the bad and the ugly},
  author={Xian, Yongqin and Schiele, Bernt and Akata, Zeynep},
  booktitle={Proceedings of the IEEE conference on computer vision and pattern recognition},
  pages={4582--4591},
  year={2017}
}
```

### CelebFaces Attributes (CelebA)

```
@inproceedings{liu2015deep,
  title={Deep learning face attributes in the wild},
  author={Liu, Ziwei and Luo, Ping and Wang, Xiaogang and Tang, Xiaoou},
  booktitle={Proceedings of the IEEE international conference on computer vision},
  pages={3730--3738},
  year={2015}
}
```

### German Traffic Sign Recognition Benchmark (GTSRB)

```
@article{stallkamp2012man,
  title={Man vs. computer: Benchmarking machine learning algorithms for traffic sign recognition},
  author={Stallkamp, Johannes and Schlipsing, Marc and Salmen, Jan and Igel, Christian},
  journal={Neural networks},
  volume={32},
  pages={323--332},
  year={2012},
  publisher={Elsevier}
}
```

### Modified National Institute of Standards and Technology (MNIST)

```
@article{lecun2010mnist,
  title={MNIST handwritten digit database},
  author={LeCun, Yann and Cortes, Corinna and Burges, Chris and others},
  year={2010},
  publisher={Florham Park, NJ, USA}
}
```

```
@article{manhaeve2018deepproblog,
  title={Deepproblog: Neural probabilistic logic programming},
  author={Manhaeve, Robin and Dumancic, Sebastijan and Kimmig, Angelika and Demeester, Thomas and De Raedt, Luc},
  journal={Advances in neural information processing systems},
  volume={31},
  year={2018}
}
```

## Acknowledgements

Special thanks to Rahim Khan, Tommy Tang, Alex Tanthiptham, and Trusha Vernekar for their contributions to the implementation, testing, and experiments involved in this project.

## License

This codebase is released under the [Creative Commons Attribution NonCommercial ShareAlike (CC BY-NC-SA)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en) license, which can be viewed under `LICENSE`.

## Contact

For questions, feedback, or comments, open an issue or reach out to [Simon Yu](mailto:simonyu@simonyu.net).

Written by [Simon Yu](https://www.simonyu.net/).
