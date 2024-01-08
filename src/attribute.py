#!/usr/bin/env python3

import functools
import header
import json
import os
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
import random

application = PyQt5.QtWidgets.QApplication([])
combo_box_application_control_attribute = PyQt5.QtWidgets.QComboBox()
combo_box_application_control_label = PyQt5.QtWidgets.QComboBox()
group_box_viewer = PyQt5.QtWidgets.QGroupBox()

file_attribute_config = open(os.path.join(header.config_dir, header.attribute_config_file_name), "r")
attribute_config = json.load(file_attribute_config)
file_attribute_config.close()

def updateViewerWidget(shuffle_viewer_images = True, shuffle_viewer_labels = False):
    attribute = combo_box_application_control_attribute.currentText()
    label_attribute = combo_box_application_control_label.currentText()
    labels_original = []
    file_paths_image = []

    for label_original in attribute_config["mappings"]:
        label_attribute_current = attribute_config["mappings"][label_original]["labels"][attribute]

        if label_attribute_current == label_attribute:
            labels_original.append(label_original)

    for label_original in labels_original:
        file_path_images = os.path.join(header.attribute_dataset_dir_images, label_original)

        if not os.path.isdir(file_path_images):
            continue

        file_names_images = sorted(os.listdir(file_path_images))

        if shuffle_viewer_images:
            file_names_images = random.sample(file_names_images, len(file_names_images))

        for file_name_images in file_names_images:
            file_path_image = os.path.join(header.attribute_dataset_dir_images, label_original, file_name_images)

            if os.path.isfile(file_path_image):
                file_paths_image.append((file_path_image, label_original))
                break

    for i in range(0, group_box_viewer.layout().count()):
        label_viewer = group_box_viewer.layout().itemAt(i).layout().itemAt(0).widget()
        label_label = group_box_viewer.layout().itemAt(i).layout().itemAt(1).widget()

        if shuffle_viewer_labels:
            file_paths_image = random.sample(file_paths_image, len(file_paths_image))

        if i < len(file_paths_image):
            label_original = file_paths_image[i][1]
            label_label_font_metrics = PyQt5.QtGui.QFontMetrics(label_label.font())
            label_original_elided = label_label_font_metrics.elidedText(label_original, PyQt5.QtCore.Qt.ElideRight, label_label.width())
            pixmap = PyQt5.QtGui.QPixmap(file_paths_image[i][0])

            label_viewer.setPixmap(pixmap.scaled(header.attribute_viewer_width, header.attribute_viewer_height, PyQt5.QtCore.Qt.IgnoreAspectRatio))
            label_label.setText(label_original_elided)
            label_label.setToolTip(label_original)
        else:
            pixmap = PyQt5.QtGui.QPixmap(header.attribute_viewer_width, header.attribute_viewer_height)
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

def createApplicationControlWidget():
    group_box_application_control = PyQt5.QtWidgets.QGroupBox()
    layout_application_control = PyQt5.QtWidgets.QHBoxLayout()
    push_button_shuffle_viewer_images_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_shuffle_viewer_labels_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_last_label_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_next_label_application_control = PyQt5.QtWidgets.QPushButton()

    for attribute in attribute_config["attributes"]:
        combo_box_application_control_attribute.addItem(attribute["name"])

    comboBoxApplicationControlAttributeSlot()

    combo_box_application_control_attribute.currentIndexChanged.connect(comboBoxApplicationControlAttributeSlot)
    combo_box_application_control_attribute.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
    combo_box_application_control_label.currentIndexChanged.connect(functools.partial(updateViewerWidget, False, False))
    combo_box_application_control_label.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
    group_box_application_control.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_application_control.setLayout(layout_application_control)
    group_box_application_control.setTitle("Application Control")
    layout_application_control.addWidget(push_button_last_label_application_control)
    layout_application_control.addWidget(combo_box_application_control_attribute)
    layout_application_control.addWidget(combo_box_application_control_label)
    layout_application_control.addWidget(push_button_shuffle_viewer_images_application_control)
    layout_application_control.addWidget(push_button_shuffle_viewer_labels_application_control)
    layout_application_control.addWidget(push_button_next_label_application_control)
    push_button_shuffle_viewer_images_application_control.clicked.connect(functools.partial(updateViewerWidget, True, False))
    push_button_shuffle_viewer_images_application_control.setText("Shuffle Viewer Images")
    push_button_shuffle_viewer_labels_application_control.clicked.connect(functools.partial(updateViewerWidget, False, True))
    push_button_shuffle_viewer_labels_application_control.setText("Shuffle Viewer Labels")
    push_button_last_label_application_control.clicked.connect(pushButtonLastLabelSlot)
    push_button_last_label_application_control.setText("Last Label")
    push_button_next_label_application_control.clicked.connect(pushButtonNextLabelSlot)
    push_button_next_label_application_control.setText("Next Label")

    return group_box_application_control

def createViewerWidget():
    layout_viewer = PyQt5.QtWidgets.QGridLayout()

    group_box_viewer.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_viewer.setLayout(layout_viewer)
    group_box_viewer.setTitle("Viewer")

    for i in range(0, header.attribute_viewer_count):
        label_label = PyQt5.QtWidgets.QLabel()
        label_viewer = PyQt5.QtWidgets.QLabel()
        layout = PyQt5.QtWidgets.QVBoxLayout()
        pixmap = PyQt5.QtGui.QPixmap(header.attribute_viewer_width, header.attribute_viewer_height)

        pixmap.fill(PyQt5.QtCore.Qt.black)

        label_label.setText("N/A")
        label_viewer.setPixmap(pixmap)

        layout.addWidget(label_viewer)
        layout.addWidget(label_label)
        layout_viewer.addLayout(layout, i // header.attribute_viewer_count_col, i % header.attribute_viewer_count_col)

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

    window = PyQt5.QtWidgets.QWidget()

    window.setLayout(createWindowLayout())
    window.setWindowTitle("VISAT Examination Tool")

    window.show()
    window.setFixedSize(window.size())

    updateViewerWidget()

    exit(application.exec())

if __name__ == "__main__":
    main()
