#!/usr/bin/env python3

import functools
import header
import json
import os
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
import sys

file_config = open(os.path.join(header.config_dir, header.label_config_file_name), "r")
config = json.load(file_config)
file_config.close()

def addLabelSlot(dataset_name, combo_box, line_edit):
    label = line_edit.text().lower()

    if (label == dataset_name + "--" or
        combo_box.findText(label, PyQt5.QtCore.Qt.MatchExactly) >= 0):
        return

    for dataset in config["datasets"]:
        if dataset["name"] == dataset_name:
            dataset["labels"].append(label)

            with open(os.path.join(header.config_dir, header.label_config_file_name), "w") as file_config:
                json.dump(config, file_config, indent = 4)

    combo_box.addItem(label)

    return

def removeLabelSlot(dataset_name, combo_box):
    label = combo_box.currentText()

    if label == "":
        return

    for dataset in config["datasets"]:
        if dataset["name"] == dataset_name:
            dataset["labels"].remove(label)

            with open(os.path.join(header.config_dir, header.label_config_file_name), "w") as file_config:
                json.dump(config, file_config, indent = 4)

    combo_box.removeItem(combo_box.currentIndex())

    return

def createViewerWidget():
    group_box_viewer = PyQt5.QtWidgets.QGroupBox()
    layout_viewer = PyQt5.QtWidgets.QGridLayout()

    group_box_viewer.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_viewer.setLayout(layout_viewer)
    group_box_viewer.setTitle("Viewer")

    for i in range(0, header.label_viewer_items):
        label = PyQt5.QtWidgets.QLabel()
        pixmap = PyQt5.QtGui.QPixmap(header.label_viewer_width, header.label_viewer_height)
        pixmap.fill(PyQt5.QtCore.Qt.black)
        label.setPixmap(pixmap)
        layout_viewer.addWidget(label, i // header.label_viewer_items_row, i % header.label_viewer_items_row)

    return group_box_viewer

def createLabelingControlWidget():
    group_box_labeling_control = PyQt5.QtWidgets.QGroupBox()
    layout_labeling_control = PyQt5.QtWidgets.QGridLayout()

    group_box_labeling_control.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_labeling_control.setLayout(layout_labeling_control)
    group_box_labeling_control.setTitle("Labeling Control")

    for dataset in config["datasets"]:
        combo_box = PyQt5.QtWidgets.QComboBox()
        group_box_control = PyQt5.QtWidgets.QGroupBox()
        layout_group_box_control = PyQt5.QtWidgets.QGridLayout()
        line_edit = PyQt5.QtWidgets.QLineEdit()
        push_button_add_label = PyQt5.QtWidgets.QPushButton()
        push_button_remove_label = PyQt5.QtWidgets.QPushButton()

        for label in dataset["labels"]:
            combo_box.addItem(label)

        combo_box.setFixedWidth(header.label_combo_box_width)
        group_box_control.setLayout(layout_group_box_control)
        group_box_control.setTitle("Dataset \"" + dataset["name"] + "\"")
        layout_group_box_control.addWidget(combo_box, 0, 0)
        layout_group_box_control.addWidget(line_edit, 0, 1)
        layout_group_box_control.addWidget(push_button_add_label, 0, 2)
        layout_group_box_control.addWidget(push_button_remove_label, 0, 3)
        layout_labeling_control.addWidget(group_box_control)
        line_edit.setFixedWidth(header.label_line_edit_width)
        line_edit.setText(dataset["name"] + "--")
        push_button_add_label.clicked.connect(functools.partial(addLabelSlot, dataset["name"], combo_box, line_edit))
        push_button_add_label.setText("Add Label")
        push_button_remove_label.clicked.connect(functools.partial(removeLabelSlot, dataset["name"], combo_box))
        push_button_remove_label.setText("Remove Label")

    return group_box_labeling_control

def createApplicationControlWidget():
    group_box_application_control = PyQt5.QtWidgets.QGroupBox()
    layout_application_control = PyQt5.QtWidgets.QGridLayout()
    push_button_load = PyQt5.QtWidgets.QPushButton()
    push_button_last = PyQt5.QtWidgets.QPushButton()
    push_button_next = PyQt5.QtWidgets.QPushButton()
    push_button_save = PyQt5.QtWidgets.QPushButton()
    push_button_save_and_last = PyQt5.QtWidgets.QPushButton()
    push_button_save_and_next = PyQt5.QtWidgets.QPushButton()

    group_box_application_control.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_application_control.setLayout(layout_application_control)
    group_box_application_control.setTitle("Application Control")
    layout_application_control.addWidget(push_button_save_and_last, 0, 1)
    layout_application_control.addWidget(push_button_last, 0, 2)
    layout_application_control.addWidget(push_button_load, 0, 3)
    layout_application_control.addWidget(push_button_save, 0, 4)
    layout_application_control.addWidget(push_button_next, 0, 5)
    layout_application_control.addWidget(push_button_save_and_next, 0, 6)
    push_button_load.setText("Load")
    push_button_last.setText("Last")
    push_button_next.setText("Next")
    push_button_save.setText("Save")
    push_button_save_and_last.setText("Save && Last")
    push_button_save_and_next.setText("Save && Next")

    return group_box_application_control

def createWindowLayout():
    layout_window = PyQt5.QtWidgets.QGridLayout()
    splitter = PyQt5.QtWidgets.QSplitter()

    layout_window.addWidget(splitter)
    splitter.addWidget(createViewerWidget())
    splitter.addWidget(createLabelingControlWidget())
    splitter.addWidget(createApplicationControlWidget())
    splitter.setOrientation(PyQt5.QtCore.Qt.Vertical)

    return layout_window

def main():
    application = PyQt5.QtWidgets.QApplication([])
    window = PyQt5.QtWidgets.QWidget()

    window.setLayout(createWindowLayout())
    window.setWindowTitle("Mapillary Dataset Labeling Tool")
    window.show()

    sys.exit(application.exec())

if __name__ == "__main__":
    main()
