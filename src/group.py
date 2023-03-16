#!/usr/bin/env python3

import gzip
import header
import json
import os
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
import type

application = PyQt5.QtWidgets.QApplication([])
combo_box_file_key_application_control = PyQt5.QtWidgets.QComboBox()
combo_box_label_application_control = PyQt5.QtWidgets.QComboBox()
group_box_viewer = PyQt5.QtWidgets.QGroupBox()
label_center_viewer_clicked = -1
radio_button_test_viewer = PyQt5.QtWidgets.QRadioButton()
radio_button_train_validate_viewer = PyQt5.QtWidgets.QRadioButton()

file_config_group = gzip.open(os.path.join(header.config_dir, header.group_config_file_name), "r")
config_group_json_encoded = file_config_group.read()
file_config_group.close()

config_group_json = config_group_json_encoded.decode("utf-8")
config_group = json.loads(config_group_json)

def updateComboBoxFileKeyApplicationControl():
    label_text = combo_box_label_application_control.currentText()
    file_path_images = os.path.join(header.group_dataset_dir_images, label_text)
    file_names_images = sorted(os.listdir(file_path_images))

    combo_box_file_key_application_control.clear()

    for file_name_images in file_names_images:
        file_key = file_name_images.split(header.dataset_file_extension_images)[0]
        combo_box_file_key_application_control.addItem(file_key)

    return

def updateConfigGroup():
    config_group_json = json.dumps(config_group, indent = 4)
    config_group_json_encoded = config_group_json.encode("utf-8")

    with gzip.open(os.path.join(header.config_dir, header.group_config_file_name), "w") as file_config_group:
        file_config_group.write(config_group_json_encoded)

    return

def updateViewerWidget():
    count_viewer = header.group_viewer_side_count * 2 + 1
    file_key = combo_box_file_key_application_control.currentText()
    file_key_index_current = combo_box_file_key_application_control.currentIndex()
    file_key_index_start = max(file_key_index_current - header.group_viewer_side_count, 0)
    file_key_index_end = min(file_key_index_current + header.group_viewer_side_count, combo_box_file_key_application_control.count() - 1)
    group = ""
    label_text = combo_box_label_application_control.currentText()

    if file_key in config_group[label_text].keys():
        group = config_group[label_text][file_key]

    if group == header.group_keyword_test:
        radio_button_test_viewer.setChecked(True)
    elif group == header.group_keyword_train_validate:
        radio_button_train_validate_viewer.setChecked(True)
    else:
        radio_button_test_viewer.setAutoExclusive(False)
        radio_button_test_viewer.setChecked(False)
        radio_button_train_validate_viewer.setChecked(False)
        radio_button_test_viewer.setAutoExclusive(True)

    for i in range(0, count_viewer):
        if i < header.group_viewer_side_count:
            label = group_box_viewer.layout().itemAt(i).widget()
        else:
            label = group_box_viewer.layout().itemAt(i + 1).widget()

        if i == header.group_viewer_side_count:
            pixmap = PyQt5.QtGui.QPixmap(header.group_viewer_center_width, header.group_viewer_center_height)
        else:
            pixmap = PyQt5.QtGui.QPixmap(header.group_viewer_side_width, header.group_viewer_side_height)

        pixmap.fill(PyQt5.QtCore.Qt.black)
        label.setPixmap(pixmap)

    for file_key_index in range(file_key_index_start, file_key_index_end + 1):
        viewer_index = file_key_index + (header.group_viewer_side_count - file_key_index_current)
        file_key = combo_box_file_key_application_control.itemText(file_key_index)
        file_path_image = os.path.join(header.group_dataset_dir_images, label_text, file_key)

        if viewer_index < header.group_viewer_side_count:
            label = group_box_viewer.layout().itemAt(viewer_index).widget()
        else:
            label = group_box_viewer.layout().itemAt(viewer_index + 1).widget()

        pixmap = PyQt5.QtGui.QPixmap(file_path_image)

        if viewer_index == header.group_viewer_side_count:
            label.setPixmap(pixmap.scaled(header.group_viewer_center_width, header.group_viewer_center_height, PyQt5.QtCore.Qt.IgnoreAspectRatio))
        else:
            label.setPixmap(pixmap.scaled(header.group_viewer_side_width, header.group_viewer_side_height, PyQt5.QtCore.Qt.IgnoreAspectRatio))

    return

def slotComboBoxFileKeyApplicationControl():
    updateViewerWidget()

    return

def slotComboBoxLabelApplicationControl():
    updateComboBoxFileKeyApplicationControl()
    updateViewerWidget()

    return

def slotPushButtonSaveApplicationControl():
    file_key = combo_box_file_key_application_control.currentText()
    group = ""
    label_text = combo_box_label_application_control.currentText()

    if radio_button_test_viewer.isChecked():
        group = header.group_keyword_test
    elif radio_button_train_validate_viewer.isChecked():
        group = header.group_keyword_train_validate

    config_group[label_text][file_key] = group

    updateConfigGroup()

    return

def slotPushButtonSaveAndLastApplicationControl():
    slotPushButtonSaveApplicationControl()

    if combo_box_file_key_application_control.currentIndex() <= 0:
        return

    combo_box_file_key_application_control.setCurrentIndex(combo_box_file_key_application_control.currentIndex() - 1)

    return

def slotPushButtonSaveAndNextApplicationControl():
    slotPushButtonSaveApplicationControl()

    if combo_box_file_key_application_control.currentIndex() >= combo_box_file_key_application_control.count() - 1:
        return

    combo_box_file_key_application_control.setCurrentIndex(combo_box_file_key_application_control.currentIndex() + 1)

    return

def slotLabelCenterViewerLeft():
    global label_center_viewer_clicked

    radio_button_train_validate_viewer.setChecked(True)

    if label_center_viewer_clicked == 0:
        label_center_viewer_clicked = -1
        slotPushButtonSaveAndNextApplicationControl()
    else:
        label_center_viewer_clicked = 0

    return

def slotLabelCenterViewerRight():
    global label_center_viewer_clicked

    radio_button_test_viewer.setChecked(True)

    if label_center_viewer_clicked == 1:
        label_center_viewer_clicked = -1
        slotPushButtonSaveAndNextApplicationControl()
    else:
        label_center_viewer_clicked = 1

    return

def createApplicationControlWidget():
    group_box_application_control = PyQt5.QtWidgets.QGroupBox()
    layout_application_control = PyQt5.QtWidgets.QHBoxLayout()
    push_button_save_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_save_and_last_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_save_and_next_application_control = PyQt5.QtWidgets.QPushButton()

    for label_text in config_group.keys():
        combo_box_label_application_control.addItem(label_text)

    updateComboBoxFileKeyApplicationControl()

    combo_box_file_key_application_control.currentIndexChanged.connect(slotComboBoxFileKeyApplicationControl)
    combo_box_file_key_application_control.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
    combo_box_label_application_control.currentIndexChanged.connect(slotComboBoxLabelApplicationControl)
    combo_box_label_application_control.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
    group_box_application_control.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_application_control.setLayout(layout_application_control)
    group_box_application_control.setTitle("Application Control")
    layout_application_control.addWidget(push_button_save_and_last_application_control)
    layout_application_control.addWidget(combo_box_label_application_control)
    layout_application_control.addWidget(combo_box_file_key_application_control)
    layout_application_control.addWidget(push_button_save_application_control)
    layout_application_control.addWidget(push_button_save_and_next_application_control)
    push_button_save_application_control.clicked.connect(slotPushButtonSaveApplicationControl)
    push_button_save_application_control.setText("Save")
    push_button_save_and_last_application_control.clicked.connect(slotPushButtonSaveAndLastApplicationControl)
    push_button_save_and_last_application_control.setText("Save && Last")
    push_button_save_and_next_application_control.clicked.connect(slotPushButtonSaveAndNextApplicationControl)
    push_button_save_and_next_application_control.setText("Save && Next")

    return group_box_application_control

def createViewerWidget():
    count_viewer = header.group_viewer_side_count * 2 + 1
    layout_radio_button_viewer = PyQt5.QtWidgets.QHBoxLayout()
    layout_viewer = PyQt5.QtWidgets.QGridLayout()

    group_box_viewer.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_viewer.setLayout(layout_viewer)
    group_box_viewer.setTitle("Viewer")
    layout_radio_button_viewer.addWidget(radio_button_train_validate_viewer)
    layout_radio_button_viewer.addWidget(radio_button_test_viewer)
    radio_button_test_viewer.setSizePolicy(PyQt5.QtWidgets.QSizePolicy.Fixed, PyQt5.QtWidgets.QSizePolicy.Fixed)
    radio_button_test_viewer.setText("Testing")
    radio_button_train_validate_viewer.setSizePolicy(PyQt5.QtWidgets.QSizePolicy.Fixed, PyQt5.QtWidgets.QSizePolicy.Fixed)
    radio_button_train_validate_viewer.setText("Training && Validation")

    for i in range(0, count_viewer):
        label = None

        if i == header.group_viewer_side_count:
            label = type.QLabelClickable()
            pixmap = PyQt5.QtGui.QPixmap(header.group_viewer_center_width, header.group_viewer_center_height)

            label.clicked_left.connect(slotLabelCenterViewerLeft)
            label.clicked_right.connect(slotLabelCenterViewerRight)
            label.setCursor(PyQt5.QtCore.Qt.PointingHandCursor)
            layout_viewer.addLayout(layout_radio_button_viewer, 1, i)
        else:
            label = PyQt5.QtWidgets.QLabel()
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

    slotComboBoxFileKeyApplicationControl()

    window.show()
    window.setFixedSize(window.size())

    exit(application.exec())

if __name__ == "__main__":
    main()
