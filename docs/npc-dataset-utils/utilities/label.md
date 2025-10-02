# NPC Attribute Labeling Utility

## Table of Contents

1. [Overview](#overview)
2. [Preview](#preview)
3. [Running the Utility](#running-the-utility)
4. [Viewer Panel](#viewer-panel)
5. [Labeling Control Panel](#labeling-control-panel)
6. [Application Control Panel](#application-control-panel)
7. [Adding or Removing Attributes](#adding-or-removing-attributes)
8. [Labeling New Datasets](#labeling-new-datasets)

## Overview

The NPC Attribute Labeling Utility is an interactive, Qt-based graphical software designed to create attribute labels for datasets that do not provide them natively. Within the NPC project, certain datasets, most notably GTSRB, lack attribute annotations. This utility addresses the gap by allowing users to define, assign, and manage attribute labels directly through a visual interface.

The utility streamlines the labeling process by displaying random instances in each class, helping users quickly establish consistent and meaningful attribute labels. These labels are stored in the dataset configuration files under `npc/npc-dataset-utils/configs/npc-dataset-utils` and can later be verified and used by the NPC pipeline.

Key features of the utility include:

- A Viewer Panel that presents random instances from the selected class to provide visual context while labeling.
- A Labeling Control Panel for assigning existing attribute values, adding new labels, or removing existing ones.
- An Application Control Panel for saving progress, navigating among classes/categories, reloading configurations, or shuffling displayed instances.
- Support for class-wise, one-hot attribute labeling for any datasets with user-definable attributes.

The NPC Attribute Labeling Utility provides the foundation for rapidly and efficiently annotating datasets with attributes, enabling their use in downstream tasks across the NPC pipeline.

## Preview

![NPC Attribute Labeling Utility](../images/label.png)

## Running the Utility

The utility can be launched as follows:

```bash
cd npc/npc-dataset-utils/src/npc-dataset-utils
./label.py
```

Note that the current implementation supports only class-wise, one-hot attribute labels.

## Viewer Panel

The Viewer Panel displays a random collection of instances from the selected class, providing visual context to assist with attribute labeling:

- The displayed collection can be refreshed by clicking the `Shuffle Viewer` button in the Application Control Panel.
- The size, number of images, layout, and appearance of the Viewer Panel can be customized through parameters in `header.py`.
- The panel can be collapsed or expanded by dragging the bar directly below.

## Labeling Control Panel

The Labeling Control Panel allows users to create and label the selected class with custom attributes. All available attributes are displayed in rows:

- For each attribute, users may label the selected class by selecting an existing attribute value from the drop-down menu on the left.
- To add a new attribute value, type it into the text box and click `Add Label`.
- The currently selected attribute value in the drop-down menu can be removed with `Remove Label`.
- The panel can be collapsed or expanded towards either top or bottom by dragging the bar directly above or below it.

## Application Control Panel

The Application Control Panel provides controls for managing the labeling process and navigating through the dataset:

- `Save & Last` saves progress and returns to the previous class in sequence.
- `Reload` reloads dataset configurations if changes are made directly to the configuration files while the utility is running.
- The drop-down menu in the middle of the panel allows direct and random access to any class.
- `Shuffle Viewer` draws new random instances from the selected class to be displayed in the Viewer Panel.
- `Save` immediately saves the current labeling for the selected class.
- `Save & Next` saves progress and advances to the next class in sequence.
- The panel can be collapsed or expanded by dragging the bar directly above it.

Note that `Reload` does not pick up attribute additions or removals made directly in the dataset configuration files.

## Adding or Removing Attributes

The current implementation of the utility does not make adding or removing attributes straightforward; nevertheless, it can be done manually or by scripts with some effort. The example below demonstrates how to add a new attribute. Removing an existing attribute follows the same steps in reverse.

Start by opening the dataset configuration file under `npc/npc-dataset-utils/configs/npc-dataset-utils`.

Inside the configuration file, add the new attribute to the `attributes` array:

```json
"attributes": [
    {
        "name": "<new attribute>",
        "labels": []
    },
    ...
]
```

Next, update each class entry in the `mappings` array to include the new attribute:

```json
"mappings": {
    "<class 1>": {
        "labels": {
            "<attribute 1>": "<value 1>",
            "<new attribute>": ""
        }
    },
    ...
}
```

There is no need to pre-populate labels or values for the new attribute since these can be added more intuitively through the graphical utility. After making these changes, restart the utility to ensure the updates take effect.

## Labeling New Datasets

Before labeling a new dataset, a dataset configuration file must first be created with the required basic entries. This file can be generated manually or through a script, and should be placed under `npc/npc-dataset-utils/configs/npc-dataset-utils`.

A minimal dataset configuration file should follow the structure below:

```json
{
    "attributes": [
        {
            "name": "<attribute 1>",
            "labels": []
        },
        ...
    ],
    "mappings": {
        "<class 1>": {
            "labels": {
                "<attribute 1>": "",
                ...
            }
        },
}
```

Written by [Simon Yu](https://www.simonyu.net/).
