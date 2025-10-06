#!/usr/bin/env python3

"""
@file   examine.py
@author Simon Yu
@date   01/08/2024
@brief  NPC Attribute Examining Utility.
"""

import functools
import header
import json
import logger
import os
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
import random

attribute_config = {}
application = PyQt5.QtWidgets.QApplication([])
combo_box_application_control_attribute = PyQt5.QtWidgets.QComboBox()
combo_box_application_control_label = PyQt5.QtWidgets.QComboBox()
group_box_viewer = PyQt5.QtWidgets.QGroupBox()

def updateViewerWidget(shuffle_viewer_images = True, shuffle_viewer_labels = False):
    attribute = combo_box_application_control_attribute.currentText()
    label_attribute = combo_box_application_control_label.currentText()

    if attribute == "" or label_attribute == "":
        for i in range(0, group_box_viewer.layout().count()):
            label_viewer = group_box_viewer.layout().itemAt(i).layout().itemAt(0).widget()
            label_label = group_box_viewer.layout().itemAt(i).layout().itemAt(1).widget()
            pixmap = PyQt5.QtGui.QPixmap(header.examine_viewer_width, header.examine_viewer_height)
            pixmap.fill(PyQt5.QtCore.Qt.black)

            label_viewer.setPixmap(pixmap)
            label_label.setText("N/A")

        return

    labels_class = []
    file_paths_image = []

    for label_class in attribute_config["mappings"]:
        label_attribute_current = attribute_config["mappings"][label_class]["labels"][attribute]

        if label_attribute_current == label_attribute:
            labels_class.append(label_class)

    for label_class in labels_class:
        file_path_images = os.path.join(header.examine_dataset_dir_images, label_class)

        if not os.path.isdir(file_path_images):
            continue

        file_names_images = sorted(os.listdir(file_path_images))

        if shuffle_viewer_images:
            file_names_images = random.sample(file_names_images, len(file_names_images))

        for file_name_images in file_names_images:
            file_path_image = os.path.join(header.examine_dataset_dir_images, label_class, file_name_images)

            if os.path.isfile(file_path_image):
                file_paths_image.append((file_path_image, label_class))
                break

    for i in range(0, group_box_viewer.layout().count()):
        label_viewer = group_box_viewer.layout().itemAt(i).layout().itemAt(0).widget()
        label_label = group_box_viewer.layout().itemAt(i).layout().itemAt(1).widget()

        if shuffle_viewer_labels:
            file_paths_image = random.sample(file_paths_image, len(file_paths_image))

        if i < len(file_paths_image):
            label_class = file_paths_image[i][1]
            label_label_font_metrics = PyQt5.QtGui.QFontMetrics(label_label.font())
            label_class_elided = label_label_font_metrics.elidedText(label_class, PyQt5.QtCore.Qt.ElideRight, label_label.width())
            pixmap = PyQt5.QtGui.QPixmap(file_paths_image[i][0])

            label_viewer.setPixmap(pixmap.scaled(header.examine_viewer_width, header.examine_viewer_height, PyQt5.QtCore.Qt.IgnoreAspectRatio))
            label_label.setText(label_class_elided)
            label_label.setToolTip(label_class)
        else:
            pixmap = PyQt5.QtGui.QPixmap(header.examine_viewer_width, header.examine_viewer_height)
            pixmap.fill(PyQt5.QtCore.Qt.black)

            label_viewer.setPixmap(pixmap)
            label_label.setText("N/A")

    return

def comboBoxApplicationControlAttributeSlot():
    combo_box_application_control_label.clear()

    for attribute in attribute_config["attributes"]:
        if attribute["name"] == combo_box_application_control_attribute.currentText():
            for label in attribute["labels"]:
                if label != "":
                    combo_box_application_control_label.addItem(label)

            break

    return

def pushButtonLastLabelSlot():
    if combo_box_application_control_label.currentIndex() <= 0:
        return

    combo_box_application_control_label.setCurrentIndex(combo_box_application_control_label.currentIndex() - 1)

    return

def pushButtonNextLabelSlot():
    if combo_box_application_control_label.currentIndex() >= combo_box_application_control_label.count() - 1:
        return

    combo_box_application_control_label.setCurrentIndex(combo_box_application_control_label.currentIndex() + 1)

    return

def pushButtonReloadSlot():
    global attribute_config

    file_attribute_config = open(os.path.join(header.config_dir, header.examine_config_file_name), "r")
    attribute_config = json.load(file_attribute_config)
    file_attribute_config.close()

    combo_box_application_control_attribute.clear()

    for attribute in attribute_config["attributes"]:
        combo_box_application_control_attribute.addItem(attribute["name"])

    comboBoxApplicationControlAttributeSlot()

    return

def createApplicationControlWidget():
    group_box_application_control = PyQt5.QtWidgets.QGroupBox()
    layout_application_control = PyQt5.QtWidgets.QVBoxLayout()
    layout_application_control_upper = PyQt5.QtWidgets.QHBoxLayout()
    layout_application_control_lower = PyQt5.QtWidgets.QHBoxLayout()
    push_button_shuffle_viewer_images_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_shuffle_viewer_labels_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_last_label_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_next_label_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_reload_application_control = PyQt5.QtWidgets.QPushButton()

    combo_box_application_control_attribute.currentIndexChanged.connect(comboBoxApplicationControlAttributeSlot)
    combo_box_application_control_attribute.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
    combo_box_application_control_label.currentIndexChanged.connect(functools.partial(updateViewerWidget, False, False))
    combo_box_application_control_label.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
    group_box_application_control.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_application_control.setLayout(layout_application_control)
    group_box_application_control.setTitle("Application Control")
    layout_application_control.addLayout(layout_application_control_upper)
    layout_application_control.addLayout(layout_application_control_lower)
    layout_application_control_lower.addWidget(push_button_last_label_application_control)
    layout_application_control_lower.addWidget(push_button_reload_application_control)
    layout_application_control_lower.addWidget(push_button_shuffle_viewer_images_application_control)
    layout_application_control_lower.addWidget(push_button_shuffle_viewer_labels_application_control)
    layout_application_control_lower.addWidget(push_button_next_label_application_control)
    layout_application_control_upper.addWidget(combo_box_application_control_attribute)
    layout_application_control_upper.addWidget(combo_box_application_control_label)
    push_button_shuffle_viewer_images_application_control.clicked.connect(functools.partial(updateViewerWidget, True, False))
    push_button_shuffle_viewer_images_application_control.setText("Shuffle Viewer Images")
    push_button_shuffle_viewer_labels_application_control.clicked.connect(functools.partial(updateViewerWidget, False, True))
    push_button_shuffle_viewer_labels_application_control.setText("Shuffle Viewer Labels")
    push_button_last_label_application_control.clicked.connect(pushButtonLastLabelSlot)
    push_button_last_label_application_control.setText("Last Label")
    push_button_next_label_application_control.clicked.connect(pushButtonNextLabelSlot)
    push_button_next_label_application_control.setText("Next Label")
    push_button_reload_application_control.clicked.connect(pushButtonReloadSlot)
    push_button_reload_application_control.setText("Reload")

    return group_box_application_control

def createViewerWidget():
    layout_viewer = PyQt5.QtWidgets.QGridLayout()

    group_box_viewer.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_viewer.setLayout(layout_viewer)
    group_box_viewer.setTitle("Viewer")

    for i in range(0, header.examine_viewer_count):
        label_label = PyQt5.QtWidgets.QLabel()
        label_viewer = PyQt5.QtWidgets.QLabel()
        layout = PyQt5.QtWidgets.QVBoxLayout()
        pixmap = PyQt5.QtGui.QPixmap(header.examine_viewer_width, header.examine_viewer_height)

        pixmap.fill(PyQt5.QtCore.Qt.black)

        label_label.setText("N/A")
        label_viewer.setPixmap(pixmap)

        layout.addWidget(label_viewer)
        layout.addWidget(label_label)
        layout_viewer.addLayout(layout, i // header.examine_viewer_count_col, i % header.examine_viewer_count_col)

    return group_box_viewer

def createWindowLayout():
    layout_window = PyQt5.QtWidgets.QGridLayout()
    splitter = PyQt5.QtWidgets.QSplitter()
    widget_application_control = createApplicationControlWidget()
    widget_viewer = createViewerWidget()

    layout_window.addWidget(splitter)
    splitter.addWidget(widget_viewer)
    splitter.addWidget(widget_application_control)
    splitter.setOrientation(PyQt5.QtCore.Qt.Vertical)

    return layout_window

def main():
    global attribute_config

    file_attribute_config = open(os.path.join(header.config_dir, header.examine_config_file_name), "r")
    attribute_config = json.load(file_attribute_config)
    file_attribute_config.close()

    if "instance_wise" in attribute_config and attribute_config["instance_wise"]:
        logger.log_fatal("Instance-wise dataset not supported. Quit.")
        exit(-1)

    if "multi_hot" in attribute_config and attribute_config["multi_hot"]:
        logger.log_fatal("Multi-hot dataset not supported. Quit.")
        exit(-1)

    window = PyQt5.QtWidgets.QWidget()

    window.setLayout(createWindowLayout())
    window.setWindowTitle("NPC Attribute Examining Utility")

    window.show()
    window.setFixedSize(window.size())

    pushButtonReloadSlot()

    exit(application.exec())

if __name__ == "__main__":
    main()
