# -*- coding: utf-8 -*-
#!/usr/bin/python
# package/PYM_FooterWidget.py
"""
    FooterWidget
    ~~~~~~~~~~~~~~~~~~

    Footer widget designed for frameless UI in PySide2.
    Optionally displays app memory and disk usage and progress bar.

    :Author: Michal Rutkowski
    :Created: 2019/03/11
    :Python Version: 3.7
"""

import os

# qt modules
import PySide2
import datetime
import os
import psutil

from PySide2 import QtWidgets, QtCore, QtSql, QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *

iconsFolder = "resources/icons/"

Action_Style = ("""
    QPushButton { font-size: 16px; border: 0px; font-family: Source Sans Pro;background-color: transparent;color : #E6E6E6; }
    QPushButton:hover { font-size: 16px; border: 0px; font-family: Source Sans Pro;background-color: transparent;color : #E6E6E6; }
        """)

ProgressBarStyle = ("""
    QProgressBar { font-size: 8px; border-radius: 3px; background-color: #383838; color : #383838; text-align: center }
    QProgressBar::chunk { font-size: 8px; border-radius: 3px; background-color: #d9b834; color : #383838; text-align: center }
        """)

class FooterWidget(QtWidgets.QWidget):
    def __init__(self, resourcesPath, showRamUsage=True, showDiskUsage=False):
        super(FooterWidget, self).__init__()
        self.showRamUsage = showRamUsage
        self.showDiskUsage = showDiskUsage
        # Set the top layout
        self.footerLayout = QtWidgets.QHBoxLayout()
        self.footerLayout.setAlignment(Qt.AlignBottom)
        self.footerLayout.setSpacing(8)

        self.statsLayout = QtWidgets.QHBoxLayout()
        self.footerLayout.addLayout(self.statsLayout)
        self.statsLayout.setAlignment(Qt.AlignLeft)
        self.statsLayout.setSpacing(8)

        newfont = QtGui.QFont("Tahoma", 5, QtGui.QFont.Light)

        if (showRamUsage):
            self.memoryIcon = QtWidgets.QPushButton("")
            self.memoryIcon.setIcon(QIcon(QPixmap(os.path.join(resourcesPath, "icons/memory-1-w.png"))))
            self.memoryIcon.setIconSize(QSize(12, 12))
            self.memoryIcon.setStyleSheet(Action_Style)
            self.statsLayout.addWidget(self.memoryIcon)
            self.memoryLabel = QtWidgets.QLabel("0 mb")
            self.statsLayout.addWidget(self.memoryLabel)
            self.memoryLabel.setFont(newfont)

        if (showDiskUsage):
            self.cacheSizeIcon = QtWidgets.QPushButton("")
            self.cacheSizeIcon.setIcon(QIcon(os.path.join(resourcesPath, "icons/disk-2-w.png")))
            self.cacheSizeIcon.setIconSize(QSize(12, 12))
            self.cacheSizeIcon.setStyleSheet(Action_Style)
            self.cacheSizeLabel = QtWidgets.QLabel("0 mb")
            self.statsLayout.addWidget(self.cacheSizeIcon)
            self.statsLayout.addWidget(self.cacheSizeLabel)
            self.cacheSizeLabel.setFont(newfont)

        self.progressLayout = QtWidgets.QHBoxLayout()
        self.progressBar = QtWidgets.QProgressBar()
        #self.progressBar.setMaximumHeight(10)
        self.progressBar.setFixedSize(100, 12)
        self.progressBar.setStyleSheet(ProgressBarStyle)
        self.progressLayout.setAlignment(QtCore.Qt.AlignRight)
        self.progressLayout.addWidget(self.progressBar)
        self.footerLayout.addLayout(self.progressLayout)

        self.setLayout(self.footerLayout)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1)

    def refresh(self):
        # ram usage
        if (self.showRamUsage):
            process = psutil.Process(os.getpid())
            time = datetime.datetime.now()
            currentTime = str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)
            currentMemory = round((process.memory_info().rss/(1024*1024)), 1)
            self.memoryLabel.setText(str(currentMemory) + " mb")

        if (self.showDiskUsage):
            # cache size
            cacheFolder = "cache/"
            cacheSize = sum(os.path.getsize(cacheFolder+f) for f in os.listdir(cacheFolder) if os.path.isfile(cacheFolder+f))/(1024*1024)
            self.cacheSizeLabel.setText(str(round(cacheSize, 1)) + " mb")

    def resetProgressBar(self):
        self.progressBar.setValue(0)

    def setProgressSteps(self, value):
        self.progressBar.setRange(0, value)

    def incrementProgressBar(self):
        self.progressBar.setValue(self.progressBar.value() + 1)
