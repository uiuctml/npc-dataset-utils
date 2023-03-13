#!/usr/bin/env python3

import header
import json
import os
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets

application = PyQt5.QtWidgets.QApplication([])
combo_box_label_application_control = PyQt5.QtWidgets.QComboBox()
combo_box_key_application_control = PyQt5.QtWidgets.QComboBox()
group_box_viewer = PyQt5.QtWidgets.QGroupBox()

file_config_group = open(os.path.join(header.config_dir, header.group_config_file_name), "r")
config_group = json.load(file_config_group)
file_config_group.close()

def updateConfigGroup():
    with open(os.path.join(header.config_dir, header.group_config_file_name), "w") as file_config_group:
        json.dump(config_group, file_config_group, indent = 4)

    return

def updateApplicationControlWidget():
    return

def updateViewerWidget():
    label_text = combo_box_application_control.currentText()
    file_path_images = os.path.join(header.group_dataset_dir_images, label_text)

    if not os.path.isdir(file_path_images):
        for i in range(0, header.group_viewer_count):
            label = group_box_viewer.layout().itemAt(i).widget()
            pixmap = PyQt5.QtGui.QPixmap(header.group_viewer_side_width, header.group_viewer_side_height)
            pixmap.fill(PyQt5.QtCore.Qt.black)
            label.setPixmap(pixmap)

        return

    file_names_images = sorted(os.listdir(file_path_images))

    for file_name_images in file_names_images:
        file_path_image = os.path.join(header.group_dataset_dir_images, label_text, file_name_images)

        if not os.path.isfile(file_path_image):
            file_names_images.remove(file_path_image)

    for i in range(0, group_box_viewer.layout().count()):
        label = group_box_viewer.layout().itemAt(i).widget()

        if i < len(file_names_images):
            file_path_image = os.path.join(header.group_dataset_dir_images, label_text, file_names_images[i])
            pixmap = PyQt5.QtGui.QPixmap(file_path_image)
            label.setPixmap(pixmap.scaled(header.group_viewer_side_width, header.group_viewer_side_height, PyQt5.QtCore.Qt.IgnoreAspectRatio))
        else:
            pixmap = PyQt5.QtGui.QPixmap(header.group_viewer_side_width, header.group_viewer_side_height)
            pixmap.fill(PyQt5.QtCore.Qt.black)
            label.setPixmap(pixmap)

    return

def slotComboBoxApplicationControl():
    updateApplicationControlWidget()
    # updateViewerWidget()

    return

def slotPushButtonSave():
    # updateConfigGroup()

    return

def slotPushButtonSaveAndLast():
    slotPushButtonSave()

    return

def slotPushButtonSaveAndNext():
    slotPushButtonSave()

    return

def createApplicationControlWidget():
    group_box_application_control = PyQt5.QtWidgets.QGroupBox()
    layout_application_control = PyQt5.QtWidgets.QHBoxLayout()
    push_button_save_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_save_and_last_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_save_and_next_application_control = PyQt5.QtWidgets.QPushButton()

    for label_text in config_group.keys():
        combo_box_label_application_control.addItem(label_text)

    combo_box_label_application_control.currentIndexChanged.connect(slotComboBoxApplicationControl)
    combo_box_label_application_control.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
    group_box_application_control.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_application_control.setLayout(layout_application_control)
    group_box_application_control.setTitle("Application Control")
    layout_application_control.addWidget(push_button_save_and_last_application_control)
    layout_application_control.addWidget(combo_box_label_application_control)
    layout_application_control.addWidget(combo_box_key_application_control)
    layout_application_control.addWidget(push_button_save_application_control)
    layout_application_control.addWidget(push_button_save_and_next_application_control)
    # push_button_reload_viewer_application_control.clicked.connect(updateViewerWidget)
    push_button_save_application_control.clicked.connect(slotPushButtonSave)
    push_button_save_application_control.setText("Save")
    push_button_save_and_last_application_control.clicked.connect(slotPushButtonSaveAndLast)
    push_button_save_and_last_application_control.setText("Save && Last")
    push_button_save_and_next_application_control.clicked.connect(slotPushButtonSaveAndNext)
    push_button_save_and_next_application_control.setText("Save && Next")

    return group_box_application_control

def createViewerWidget():
    count_viewer = header.group_viewer_side_count * 2 + 1
    layout_radio_button_viewer = PyQt5.QtWidgets.QHBoxLayout()
    layout_viewer = PyQt5.QtWidgets.QGridLayout()
    radio_button_testing_viewer = PyQt5.QtWidgets.QRadioButton()
    radio_button_training_viewer = PyQt5.QtWidgets.QRadioButton()

    group_box_viewer.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_viewer.setLayout(layout_viewer)
    group_box_viewer.setTitle("Viewer")
    layout_radio_button_viewer.addWidget(radio_button_training_viewer)
    layout_radio_button_viewer.addWidget(radio_button_testing_viewer)
    radio_button_testing_viewer.setSizePolicy(PyQt5.QtWidgets.QSizePolicy.Fixed, PyQt5.QtWidgets.QSizePolicy.Fixed)
    radio_button_testing_viewer.setText("Testing")
    radio_button_training_viewer.setSizePolicy(PyQt5.QtWidgets.QSizePolicy.Fixed, PyQt5.QtWidgets.QSizePolicy.Fixed)
    radio_button_training_viewer.setText("Training && Validation")

    for i in range(0, count_viewer):
        label = PyQt5.QtWidgets.QLabel()

        if i == header.group_viewer_side_count:
            pixmap = PyQt5.QtGui.QPixmap(header.group_viewer_center_width, header.group_viewer_center_height)
            label.setCursor(PyQt5.QtCore.Qt.PointingHandCursor)
            layout_viewer.addLayout(layout_radio_button_viewer, 1, i)
        else:
            pixmap = PyQt5.QtGui.QPixmap(header.group_viewer_side_width, header.group_viewer_side_height)

        pixmap.fill(PyQt5.QtCore.Qt.black)
        label.setPixmap(pixmap)
        layout_viewer.addWidget(label, 0, i)
        layout_viewer.setAlignment(label, PyQt5.QtCore.Qt.AlignBottom)

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
    window.setWindowTitle("Mapillary Dataset Grouping Tool")

    slotComboBoxApplicationControl()

    window.show()
    window.setFixedSize(window.size())

    exit(application.exec())

if __name__ == "__main__":
    main()
