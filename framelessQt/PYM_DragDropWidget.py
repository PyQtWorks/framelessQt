# -*- coding: utf-8 -*-
#!/usr/bin/python
# package/PYM_DragDropWidget.py
"""
    DragDropWidget
    ~~~~~~~~~~~~~~~~~~

    Drag & drop widget designed for frameless UI in PySide2.
    Accepts files or directories with text/icon and optional frame display.

    :Author: Michal Rutkowski
    :Created: 2019/02/26
    :Python Version: 3.7
"""

import PySide2
from PySide2 import QtWidgets, QtCore, QtSql, QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *

import platform
import ntpath
import os

# Use NSURL as a workaround to pyside/Qt4 behaviour for dragging and dropping on OSx
op_sys = platform.system()
if op_sys == 'Darwin':
    from Foundation import NSURL

Action_Style = ("""
    QPushButton { font-size: 16px; border: 0px; font-family: Source Sans Pro;background-color: transparent;color : #E6E6E6; }
    QPushButton:hover { font-size: 16px; border: 0px; font-family: Source Sans Pro;background-color: transparent;color : #E6E6E6; }
        """)

class DragDropWidget(QtWidgets.QWidget):
    def __init__(self, label, maximumSize, drawFrame=False, resourcesPath=None, stackedLayout=None, customDropCallback=None):
        super(DragDropWidget, self).__init__()
        self.stackedLayout = stackedLayout
        self.text = label
        self.drawFrame = drawFrame
        self.resourcesPath = resourcesPath
        self.width, self.height = maximumSize
        self.customDropCallback = customDropCallback
        self.setMaximumSize(QSize(self.width, self.height))
        self.drawDragDropLayout()

    def drawDragDropLayout(self):
        self.label = QtWidgets.QLabel(self.text)
        self.label.setAlignment(Qt.AlignCenter)
        self.dragDropLayout = QtWidgets.QHBoxLayout(self)

        if (self.drawFrame and self.resourcesPath):
            frameIcon = QtGui.QPixmap(os.path.join(self.resourcesPath, "icons/bracket2.png"))

            self.frameLeft = QtWidgets.QPushButton("")
            self.frameLeft.setIcon(QIcon(frameIcon))
            self.frameLeft.setIconSize(QSize(self.height/3, self.height))
            self.frameLeft.setStyleSheet(Action_Style)

            self.frameRight = QtWidgets.QPushButton("")
            self.frameRight.setIcon(QIcon(frameIcon.transformed(QTransform().scale(-1, 1))))
            self.frameRight.setIconSize(QSize(self.height/3, self.height))
            self.frameRight.setStyleSheet(Action_Style)

            self.frameLeft.setMaximumHeight(self.height)
            self.frameRight.setMaximumHeight(self.height)
            self.dragDropLayout.addWidget(self.frameLeft)
            self.dragDropLayout.addWidget(self.label)
            self.dragDropLayout.addWidget(self.frameRight)
        else:
            self.dragDropLayout.addWidget(self.label)

        self.dragDropLayout.setAlignment(QtCore.Qt.AlignHCenter)
        # Enable dragging and dropping onto the GUI
        self.setAcceptDrops(True)

    # The following three methods set up dragging and dropping for the app
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        Drop files directly onto the widget
        File locations are stored in fname
        :param e:
        :return:
        """
        if e.mimeData().hasUrls:
            e.setDropAction(QtCore.Qt.CopyAction)
            e.accept()
            # Workaround for OSx dragging and dropping
            for url in e.mimeData().urls():
                if op_sys == 'Darwin':
                    fname = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
                else:
                    #if not os.path.isdir(str(url.toLocalFile())):
                    #    print("Please drag & drop a directory onto the main window")
                    #    return
                    fname = str(url.toLocalFile())
            if (self.customDropCallback is not None):
                self.customDropCallback(fname)
            else:
                self.imageFolder = fname
                self.folderWasSet()
        else:
            e.ignore()

    def folderWasSet(self):
        self.stackedLayout.setCurrentIndex(0)
        self.stackedLayout.widget(0).onEnabled(self.imageFolder)
