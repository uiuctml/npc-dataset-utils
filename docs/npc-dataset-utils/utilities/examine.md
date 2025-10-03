# NPC Attribute Examining Utility

## Table of Contents

1. [Overview](#overview)
2. [Preview](#preview)
3. [Running the Utility](#running-the-utility)
4. [Viewer Panel](#viewer-panel)
5. [Application Control Panel](#application-control-panel)

## Overview

The NPC Attribute Examining Utility is an interactive, Qt-based graphical software designed as a companion to the [NPC Attribute Labeling Utility](../utilities/label.md). While the labeling utility enables users to create and assign attributes to classes within a dataset, the examining utility works in reverse by displaying all instances across classes within the dataset that share a specific attribute.

Once attributes have been labeled, the examining utility can display every instance in the dataset associated with a chosen attribute, even if those instances belong to different classes. This capability helps users review and validate the consistency and validity of their attribute labeling, assess how effectively attributes distinguish among classes, and gain a broader understanding of their attributes across the entire dataset.

## Preview

![NPC Attribute Examining Utility](../images/examine.png)

## Running the Utility

Before launching the utility, verify the following parameters in `header.py`:

```python
examine_config_file_name = dataset_config_file_name
examine_dataset_dir_images = dataset_dir_instances_processed
```

These parameters default to the values shown above, but can be modified to point to any dataset configuration file and dataset instance directory on the file system.

Once configured, launch the utility with:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./examine.py
```

Note that the current implementation supports only class-wise, one-hot attribute labels.

## Viewer Panel

The Viewer Panel displays a collection of instances from across the dataset that all share the same attribute value. For example, selecting `shape--circle`, as shown in the [Preview](#preview), displays all instances with a circular shape, regardless of their class:

- The displayed instances can be randomized using the `Shuffle Viewer Images` button in the Application Control Panel.
- The set of classes shown can be randomized using the `Shuffle Viewer Labels` button in the Application Control Panel.
- The size, number of images, layout, and appearance of the Viewer Panel can be customized through parameters in `header.py`.
- The panel can be collapsed or expanded by dragging the bar directly below the panel.

## Application Control Panel

The Application Control Panel provides controls for navigating through attributes and their values:

- The drop-down menu on the left selects the attribute.
- The drop-down menu on the right selects the attribute value within the selected attribute.
- `Last Label` and `Next Label` navigate through attribute values sequentially.
- `Shuffle Viewer Images` draws new random instances for the selected attribute value to be displayed in the Viewer Panel.
- `Shuffle Viewer Labels` draws a new random set of classes for the selected attribute value to be displayed in the Viewer Panel.
- `Reload` reloads the dataset configuration if changes are made directly to the configuration file while the utility is running.
- The panel can be collapsed or expanded by dragging the bar directly above the panel.

Written by [Simon Yu](https://www.simonyu.net/).
