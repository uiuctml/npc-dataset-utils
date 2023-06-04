#!/usr/bin/env python3

import functools
import header
import json
import os
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
import random
import sys

application = PyQt5.QtWidgets.QApplication([])
combo_box_application_control = PyQt5.QtWidgets.QComboBox()
combo_box_reduction_labeling_control = PyQt5.QtWidgets.QComboBox()
combo_boxes_label_labeling_control = {}
double_spin_boxes_weight_labeling_control = {}
group_box_viewer = PyQt5.QtWidgets.QGroupBox()

file_generate_config = open(os.path.join(header.config_dir, header.generate_config_file_name), "r")
generate_config = json.load(file_generate_config)
file_generate_config.close()

file_label_config = open(os.path.join(header.config_dir, header.label_config_file_name), "r")
label_config = json.load(file_label_config)
file_label_config.close()

def updateGenerateConfig():
    with open(os.path.join(header.config_dir, header.generate_config_file_name), "w") as file_generate_config:
        json.dump(generate_config, file_generate_config, indent = 4)

    return

def updateLabelConfig():
    with open(os.path.join(header.config_dir, header.label_config_file_name), "w") as file_label_config:
        json.dump(label_config, file_label_config, indent = 4)

    return

def updateLabelingControlWidget():
    for dataset_name in combo_boxes_label_labeling_control.keys():
        if dataset_name not in generate_config[combo_box_application_control.currentText()]["labels"]:
            combo_boxes_label_labeling_control[dataset_name].setCurrentText("")
            continue

        label_text = generate_config[combo_box_application_control.currentText()]["labels"][dataset_name]

        if combo_boxes_label_labeling_control[dataset_name].findText(label_text) == -1:
            combo_boxes_label_labeling_control[dataset_name].addItem(label_text)

            for dataset in label_config["datasets"]:
                if dataset["name"] == dataset_name:
                    dataset["labels"].append(label_text)
                    updateLabelConfig()

        combo_boxes_label_labeling_control[dataset_name].setCurrentText(label_text)

    for dataset_name in double_spin_boxes_weight_labeling_control.keys():
        if dataset_name not in generate_config[combo_box_application_control.currentText()]["weights"]:
            double_spin_boxes_weight_labeling_control[dataset_name].setValue(0)
            continue

        weight_value = generate_config[combo_box_application_control.currentText()]["weights"][dataset_name]
        double_spin_boxes_weight_labeling_control[dataset_name].setValue(weight_value)

    if "reduction" not in generate_config[combo_box_application_control.currentText()]:
        combo_box_reduction_labeling_control.setCurrentText("")
    else:
        reduction_text = generate_config[combo_box_application_control.currentText()]["reduction"]

        if combo_box_reduction_labeling_control.findText(reduction_text) == -1:
            combo_box_reduction_labeling_control.addItem(reduction_text)
            label_config["reductions"].append(reduction_text)
            updateLabelConfig()

        combo_box_reduction_labeling_control.setCurrentText(reduction_text)

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

def pushButtonAddLabelSlot(dataset_name, combo_box, line_edit):
    label_text = line_edit.text().lower()

    if (label_text == dataset_name + "--" or
        combo_box.findText(label_text, PyQt5.QtCore.Qt.MatchExactly) >= 0):
        return

    for dataset in label_config["datasets"]:
        if dataset["name"] == dataset_name:
            dataset["labels"].append(label_text)
            updateLabelConfig()

    combo_box.addItem(label_text)

    return

def pushButtonAddReductionSlot(combo_box, line_edit):
    reduction_text = line_edit.text().lower()

    if (combo_box.findText(reduction_text, PyQt5.QtCore.Qt.MatchExactly) >= 0):
        return

    label_config["reductions"].append(reduction_text)
    updateLabelConfig()

    combo_box.addItem(reduction_text)

    return

def pushButtonSaveSlot():
    for dataset_name in combo_boxes_label_labeling_control.keys():
        generate_config[combo_box_application_control.currentText()]["labels"][dataset_name] = combo_boxes_label_labeling_control[dataset_name].currentText()

    for dataset_name in double_spin_boxes_weight_labeling_control.keys():
        generate_config[combo_box_application_control.currentText()]["weights"][dataset_name] = double_spin_boxes_weight_labeling_control[dataset_name].value()

    generate_config[combo_box_application_control.currentText()]["reduction"] = combo_box_reduction_labeling_control.currentText()

    updateGenerateConfig()

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

    for dataset in label_config["datasets"]:
        if dataset["name"] == dataset_name:
            dataset["labels"].remove(label_text)
            updateLabelConfig()

    combo_box.removeItem(combo_box.currentIndex())

    return

def pushButtonRemoveReductionSlot(combo_box):
    reduction_text = combo_box.currentText()

    if reduction_text == "":
        return

    label_config["reductions"].remove(reduction_text)
    updateLabelConfig()

    combo_box.removeItem(combo_box.currentIndex())

    return

def createApplicationControlWidget():
    group_box_application_control = PyQt5.QtWidgets.QGroupBox()
    layout_application_control = PyQt5.QtWidgets.QGridLayout()
    push_button_reload_viewer_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_save_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_save_and_last_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_save_and_next_application_control = PyQt5.QtWidgets.QPushButton()

    for label_text in generate_config.keys():
        combo_box_application_control.addItem(label_text)

    combo_box_application_control.currentIndexChanged.connect(comboBoxApplicationControlSlot)
    combo_box_application_control.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
    group_box_application_control.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_application_control.setLayout(layout_application_control)
    group_box_application_control.setTitle("Application Control")
    layout_application_control.addWidget(push_button_save_and_last_application_control, 0, 0)
    layout_application_control.addWidget(combo_box_application_control, 0, 1)
    layout_application_control.addWidget(push_button_reload_viewer_application_control, 0, 2)
    layout_application_control.addWidget(push_button_save_application_control, 0, 3)
    layout_application_control.addWidget(push_button_save_and_next_application_control, 0, 4)
    push_button_reload_viewer_application_control.clicked.connect(updateViewerWidget)
    push_button_reload_viewer_application_control.setText("Reload Viewer")
    push_button_save_application_control.clicked.connect(pushButtonSaveSlot)
    push_button_save_application_control.setText("Save")
    push_button_save_and_last_application_control.clicked.connect(pushButtonSaveAndLastSlot)
    push_button_save_and_last_application_control.setText("Save && Last")
    push_button_save_and_next_application_control.clicked.connect(pushButtonSaveAndNextSlot)
    push_button_save_and_next_application_control.setText("Save && Next")

    return group_box_application_control

def createLabelingControlWidget():
    group_box_labeling_control = PyQt5.QtWidgets.QGroupBox()
    group_box_reduction = PyQt5.QtWidgets.QGroupBox()
    layout_dataset = PyQt5.QtWidgets.QGridLayout()
    layout_labeling_control = PyQt5.QtWidgets.QVBoxLayout()
    layout_reduction = PyQt5.QtWidgets.QGridLayout()
    line_edit_reduction = PyQt5.QtWidgets.QLineEdit()
    push_button_add_reduction = PyQt5.QtWidgets.QPushButton()
    push_button_remove_reduction = PyQt5.QtWidgets.QPushButton()

    group_box_labeling_control.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_labeling_control.setLayout(layout_labeling_control)
    group_box_labeling_control.setTitle("Labeling Control")
    group_box_reduction.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_reduction.setLayout(layout_reduction)
    group_box_reduction.setTitle("Reduction")
    group_box_reduction.setHidden(not header.label_enable_weight)

    layout_labeling_control.addLayout(layout_dataset)
    layout_labeling_control.addWidget(group_box_reduction)
    layout_reduction.addWidget(combo_box_reduction_labeling_control, 0, 0)
    layout_reduction.addWidget(line_edit_reduction, 0, 1)
    layout_reduction.addWidget(push_button_add_reduction, 0, 2)
    layout_reduction.addWidget(push_button_remove_reduction, 0, 3)
    line_edit_reduction.setFixedWidth(header.label_line_edit_width)
    push_button_add_reduction.clicked.connect(functools.partial(pushButtonAddReductionSlot, combo_box_reduction_labeling_control, line_edit_reduction))
    push_button_add_reduction.setText("Add Reduction")
    push_button_remove_reduction.clicked.connect(functools.partial(pushButtonRemoveReductionSlot, combo_box_reduction_labeling_control))
    push_button_remove_reduction.setText("Remove Reduction")

    if "" not in label_config["reductions"]:
        label_config["reductions"].insert(0, "")
        updateLabelConfig()

    for reduction_text in label_config["reductions"]:
        combo_box_reduction_labeling_control.addItem(reduction_text)

    for (i, dataset) in enumerate(label_config["datasets"]):
        combo_box_label = PyQt5.QtWidgets.QComboBox()
        double_spin_box_weight = PyQt5.QtWidgets.QDoubleSpinBox()
        group_box_label = PyQt5.QtWidgets.QGroupBox()
        group_box_weight = PyQt5.QtWidgets.QGroupBox()
        layout_label = PyQt5.QtWidgets.QGridLayout()
        layout_weight = PyQt5.QtWidgets.QGridLayout()
        line_edit_label = PyQt5.QtWidgets.QLineEdit()
        push_button_add_label = PyQt5.QtWidgets.QPushButton()
        push_button_remove_label = PyQt5.QtWidgets.QPushButton()

        if "" not in dataset["labels"]:
            dataset["labels"].insert(0, "")
            updateLabelConfig()

        for label_text in dataset["labels"]:
            combo_box_label.addItem(label_text)

        combo_box_label.setFixedWidth(header.label_combo_box_width)
        combo_box_label.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
        double_spin_box_weight.setMinimum(-1 * sys.float_info.max)
        group_box_label.setLayout(layout_label)
        group_box_label.setTitle("Label for \"" + dataset["name"] + "\"")
        group_box_weight.setLayout(layout_weight)
        group_box_weight.setTitle("Weight for \"" + dataset["name"] + "\"")
        group_box_weight.setHidden(not header.label_enable_weight)
        layout_label.addWidget(combo_box_label, 0, 0)
        layout_label.addWidget(line_edit_label, 0, 1)
        layout_label.addWidget(push_button_add_label, 0, 2)
        layout_label.addWidget(push_button_remove_label, 0, 3)
        layout_dataset.addWidget(group_box_label, i, 0)
        layout_dataset.addWidget(group_box_weight, i, 1)
        layout_weight.addWidget(double_spin_box_weight)
        line_edit_label.setFixedWidth(header.label_line_edit_width)
        line_edit_label.setText(dataset["name"] + "--")
        push_button_add_label.clicked.connect(functools.partial(pushButtonAddLabelSlot, dataset["name"], combo_box_label, line_edit_label))
        push_button_add_label.setText("Add Label")
        push_button_remove_label.clicked.connect(functools.partial(pushButtonRemoveLabelSlot, dataset["name"], combo_box_label))
        push_button_remove_label.setText("Remove Label")

        combo_boxes_label_labeling_control[dataset["name"]] = combo_box_label
        double_spin_boxes_weight_labeling_control[dataset["name"]] = double_spin_box_weight

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

def main():
    window = PyQt5.QtWidgets.QWidget()

    window.setLayout(createWindowLayout())
    window.setWindowTitle("Mapillary Dataset Labeling Tool")

    comboBoxApplicationControlSlot()

    window.show()
    window.setFixedSize(window.size())

    exit(application.exec())

if __name__ == "__main__":
    main()
