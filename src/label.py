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
combo_box_application_control = PyQt5.QtWidgets.QComboBox()
combo_boxes_label_labeling_control = {}
group_box_viewer = PyQt5.QtWidgets.QGroupBox()

file_label_config = open(os.path.join(header.config_dir, header.label_config_file_name), "r")
label_config = json.load(file_label_config)
file_label_config.close()

def updateLabelConfig():
    with open(os.path.join(header.config_dir, header.label_config_file_name), "w") as file_label_config:
        json.dump(label_config, file_label_config, indent = 4)

    return

def updateLabelingControlWidget():
    for dataset_name in combo_boxes_label_labeling_control.keys():
        if dataset_name not in label_config["mappings"][combo_box_application_control.currentText()]["labels"]:
            combo_boxes_label_labeling_control[dataset_name].setCurrentText("")
            continue

        label_text = label_config["mappings"][combo_box_application_control.currentText()]["labels"][dataset_name]

        if combo_boxes_label_labeling_control[dataset_name].findText(label_text) == -1:
            combo_boxes_label_labeling_control[dataset_name].addItem(label_text)

            for dataset in label_config["attributes"]:
                if dataset["name"] == dataset_name:
                    dataset["labels"].append(label_text)
                    updateLabelConfig()

        combo_boxes_label_labeling_control[dataset_name].setCurrentText(label_text)

    return

def updateViewerWidget():
    label_text = combo_box_application_control.currentText()
    file_path_images = os.path.join(header.label_dataset_dir_images, label_text)

    if not os.path.isdir(file_path_images):
        for i in range(0, header.label_viewer_count):
            label = group_box_viewer.layout().itemAt(i).widget()
            pixmap = PyQt5.QtGui.QPixmap(header.label_viewer_width, header.label_viewer_height)
            pixmap.fill(PyQt5.QtCore.Qt.black)
            label.setPixmap(pixmap)

        return

    file_names_images = sorted(os.listdir(file_path_images))
    file_names_images = random.sample(file_names_images, len(file_names_images))

    for file_name_images in file_names_images:
        file_path_image = os.path.join(header.label_dataset_dir_images, label_text, file_name_images)

        if not os.path.isfile(file_path_image):
            file_names_images.remove(file_path_image)

    for i in range(0, group_box_viewer.layout().count()):
        label = group_box_viewer.layout().itemAt(i).widget()

        if i < len(file_names_images):
            file_path_image = os.path.join(header.label_dataset_dir_images, label_text, file_names_images[i])
            pixmap = PyQt5.QtGui.QPixmap(file_path_image)
            label.setPixmap(pixmap.scaled(header.label_viewer_width, header.label_viewer_height, PyQt5.QtCore.Qt.IgnoreAspectRatio))
        else:
            pixmap = PyQt5.QtGui.QPixmap(header.label_viewer_width, header.label_viewer_height)
            pixmap.fill(PyQt5.QtCore.Qt.black)
            label.setPixmap(pixmap)

    return

def comboBoxApplicationControlSlot():
    updateLabelingControlWidget()
    updateViewerWidget()

    return

def comboBoxLabelingControlSlot(combo_box_label, line_edit_label):
    line_edit_label.setText(combo_box_label.currentText())

    return

def pushButtonAddLabelSlot(dataset_name, combo_box, line_edit):
    label_text = line_edit.text().lower()

    if (label_text == dataset_name + "--" or
        combo_box.findText(label_text, PyQt5.QtCore.Qt.MatchExactly) >= 0):
        return

    for dataset in label_config["attributes"]:
        if dataset["name"] == dataset_name:
            dataset["labels"].append(label_text)
            dataset["labels"].sort()
            updateLabelConfig()

    combo_box.addItem(label_text)
    combo_box.model().sort(0)

    label_text_index = combo_box.findText(label_text)

    if label_text_index >= 0:
        combo_box.setCurrentIndex(label_text_index)

    return

def pushButtonSaveSlot():
    for dataset_name in combo_boxes_label_labeling_control.keys():
        label_config["mappings"][combo_box_application_control.currentText()]["labels"][dataset_name] = combo_boxes_label_labeling_control[dataset_name].currentText()

    updateLabelConfig()

    return

def pushButtonSaveAndLastSlot():
    pushButtonSaveSlot()

    if combo_box_application_control.currentIndex() <= 0:
        return

    combo_box_application_control.setCurrentIndex(combo_box_application_control.currentIndex() - 1)

    return

def pushButtonSaveAndNextSlot():
    pushButtonSaveSlot()

    if combo_box_application_control.currentIndex() >= combo_box_application_control.count() - 1:
        return

    combo_box_application_control.setCurrentIndex(combo_box_application_control.currentIndex() + 1)

    return

def pushButtonRemoveLabelSlot(dataset_name, combo_box):
    label_text = combo_box.currentText()

    if label_text == "":
        return

    for dataset in label_config["attributes"]:
        if dataset["name"] == dataset_name:
            dataset["labels"].remove(label_text)
            updateLabelConfig()

    combo_box.removeItem(combo_box.currentIndex())

    label_text_index = combo_box.findText(dataset_name + header.dataset_delimiter_label + header.dataset_label_undefined_keyword)

    if label_text_index >= 0:
        combo_box.setCurrentIndex(label_text_index)
    else:
        combo_box.setCurrentIndex(0)

    return

def createApplicationControlWidget():
    group_box_application_control = PyQt5.QtWidgets.QGroupBox()
    layout_application_control = PyQt5.QtWidgets.QGridLayout()
    push_button_shuffle_viewer_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_save_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_save_and_last_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_save_and_next_application_control = PyQt5.QtWidgets.QPushButton()

    for label_text in label_config["mappings"].keys():
        combo_box_application_control.addItem(label_text)

    combo_box_application_control.currentIndexChanged.connect(comboBoxApplicationControlSlot)
    combo_box_application_control.model().sort(0)
    combo_box_application_control.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
    group_box_application_control.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_application_control.setLayout(layout_application_control)
    group_box_application_control.setTitle("Application Control")
    layout_application_control.addWidget(push_button_save_and_last_application_control, 0, 0)
    layout_application_control.addWidget(combo_box_application_control, 0, 1)
    layout_application_control.addWidget(push_button_shuffle_viewer_application_control, 0, 2)
    layout_application_control.addWidget(push_button_save_application_control, 0, 3)
    layout_application_control.addWidget(push_button_save_and_next_application_control, 0, 4)
    push_button_shuffle_viewer_application_control.clicked.connect(updateViewerWidget)
    push_button_shuffle_viewer_application_control.setText("Shuffle Viewer")
    push_button_save_application_control.clicked.connect(pushButtonSaveSlot)
    push_button_save_application_control.setText("Save")
    push_button_save_and_last_application_control.clicked.connect(pushButtonSaveAndLastSlot)
    push_button_save_and_last_application_control.setText("Save && Last")
    push_button_save_and_next_application_control.clicked.connect(pushButtonSaveAndNextSlot)
    push_button_save_and_next_application_control.setText("Save && Next")

    return group_box_application_control

def createLabelingControlWidget():
    group_box_labeling_control = PyQt5.QtWidgets.QGroupBox()
    layout_dataset = PyQt5.QtWidgets.QGridLayout()
    layout_labeling_control = PyQt5.QtWidgets.QVBoxLayout()

    group_box_labeling_control.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_labeling_control.setLayout(layout_labeling_control)
    group_box_labeling_control.setTitle("Labeling Control")

    layout_labeling_control.addLayout(layout_dataset)

    for (i, dataset) in enumerate(label_config["attributes"]):
        combo_box_label = PyQt5.QtWidgets.QComboBox()
        group_box_label = PyQt5.QtWidgets.QGroupBox()
        layout_label = PyQt5.QtWidgets.QGridLayout()
        line_edit_label = PyQt5.QtWidgets.QLineEdit()
        push_button_add_label = PyQt5.QtWidgets.QPushButton()
        push_button_remove_label = PyQt5.QtWidgets.QPushButton()

        if "" not in dataset["labels"]:
            dataset["labels"].insert(0, "")
            updateLabelConfig()

        for label_text in dataset["labels"]:
            combo_box_label.addItem(label_text)

        combo_box_label.currentIndexChanged.connect(functools.partial(comboBoxLabelingControlSlot, combo_box_label, line_edit_label))
        combo_box_label.setFixedWidth(header.label_combo_box_width)
        combo_box_label.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
        group_box_label.setLayout(layout_label)
        group_box_label.setTitle("Label for \"" + dataset["name"] + "\"")
        layout_label.addWidget(combo_box_label, 0, 0)
        layout_label.addWidget(line_edit_label, 0, 1)
        layout_label.addWidget(push_button_add_label, 0, 2)
        layout_label.addWidget(push_button_remove_label, 0, 3)
        layout_dataset.addWidget(group_box_label, i, 0)
        line_edit_label.setFixedWidth(header.label_line_edit_width)
        line_edit_label.setText(dataset["name"] + "--")
        push_button_add_label.clicked.connect(functools.partial(pushButtonAddLabelSlot, dataset["name"], combo_box_label, line_edit_label))
        push_button_add_label.setText("Add Label")
        push_button_remove_label.clicked.connect(functools.partial(pushButtonRemoveLabelSlot, dataset["name"], combo_box_label))
        push_button_remove_label.setText("Remove Label")

        combo_boxes_label_labeling_control[dataset["name"]] = combo_box_label

    return group_box_labeling_control

def createViewerWidget():
    layout_viewer = PyQt5.QtWidgets.QGridLayout()

    group_box_viewer.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_viewer.setLayout(layout_viewer)
    group_box_viewer.setTitle("Viewer")

    for i in range(0, header.label_viewer_count):
        label = PyQt5.QtWidgets.QLabel()
        pixmap = PyQt5.QtGui.QPixmap(header.label_viewer_width, header.label_viewer_height)
        pixmap.fill(PyQt5.QtCore.Qt.black)
        label.setPixmap(pixmap)
        layout_viewer.addWidget(label, i // header.label_viewer_count_col, i % header.label_viewer_count_col)

    return group_box_viewer

def createWindowLayout():
    layout_window = PyQt5.QtWidgets.QGridLayout()
    splitter = PyQt5.QtWidgets.QSplitter()
    widget_application_control = createApplicationControlWidget()
    widget_labeling_control = createLabelingControlWidget()
    widget_viewer = createViewerWidget()

    layout_window.addWidget(splitter)
    splitter.addWidget(widget_viewer)
    splitter.addWidget(widget_labeling_control)
    splitter.addWidget(widget_application_control)
    splitter.setOrientation(PyQt5.QtCore.Qt.Vertical)

    return layout_window

def sortLabelConfigAttributes(label_config):
    for attribute in label_config["attributes"]:
        attribute["labels"].sort()

    updateLabelConfig()

    return

def main():
    sortLabelConfigAttributes(label_config)

    window = PyQt5.QtWidgets.QWidget()

    window.setLayout(createWindowLayout())
    window.setWindowTitle("VISAT Labeling Tool")

    comboBoxApplicationControlSlot()

    window.show()
    window.setFixedSize(window.size())

    exit(application.exec())

if __name__ == "__main__":
    main()
