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
group_box_viewer = PyQt5.QtWidgets.QGroupBox()

file_attribute_config = open(os.path.join(header.config_dir, header.attribute_config_file_name), "r")
attribute_config = json.load(file_attribute_config)
file_attribute_config.close()

def createApplicationControlWidget():
    combo_box_application_control_visual_attribute = PyQt5.QtWidgets.QComboBox()
    combo_box_application_control_label = PyQt5.QtWidgets.QComboBox()
    group_box_application_control = PyQt5.QtWidgets.QGroupBox()
    layout_application_control = PyQt5.QtWidgets.QHBoxLayout()
    push_button_reload_viewer_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_last_application_control = PyQt5.QtWidgets.QPushButton()
    push_button_next_application_control = PyQt5.QtWidgets.QPushButton()

    for attribute in attribute_config["attributes"]:
        combo_box_application_control_visual_attribute.addItem(attribute["name"])

    for attribute in attribute_config["attributes"]:
        if attribute["name"] == combo_box_application_control_visual_attribute.currentText():
            for label in attribute["labels"]:
                if label != "":
                    combo_box_application_control_label.addItem(label)

            break

    combo_box_application_control_visual_attribute.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
    combo_box_application_control_label.view().setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAsNeeded)
    group_box_application_control.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_application_control.setLayout(layout_application_control)
    group_box_application_control.setTitle("Application Control")
    layout_application_control.addWidget(push_button_last_application_control)
    layout_application_control.addWidget(combo_box_application_control_visual_attribute)
    layout_application_control.addWidget(combo_box_application_control_label)
    layout_application_control.addWidget(push_button_next_application_control)

    push_button_reload_viewer_application_control.setText("Reload Viewer")
    push_button_last_application_control.setText("Last")
    push_button_next_application_control.setText("Next")

    return group_box_application_control

def createViewerWidget():
    layout_viewer = PyQt5.QtWidgets.QGridLayout()

    group_box_viewer.setAlignment(PyQt5.QtCore.Qt.AlignHCenter)
    group_box_viewer.setLayout(layout_viewer)
    group_box_viewer.setTitle("Viewer")

    for i in range(0, header.attribute_viewer_count):
        label = PyQt5.QtWidgets.QLabel()
        pixmap = PyQt5.QtGui.QPixmap(header.attribute_viewer_width, header.attribute_viewer_height)
        pixmap.fill(PyQt5.QtCore.Qt.black)
        label.setPixmap(pixmap)
        layout_viewer.addWidget(label, i // header.attribute_viewer_count_col, i % header.attribute_viewer_count_col)

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

    exit(application.exec())

if __name__ == "__main__":
    main()
