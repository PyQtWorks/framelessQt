# -*- coding: utf-8 -*-
#!/usr/bin/python
# package/PYM_MenuBarWidget.py
"""
    MenuBarWidget
    ~~~~~~~~~~~~~~~~~~

    Menu Bar widget designed for frameless UI in PySide2.
    Displays app icon, title and window commands (minimize and close)

    :Author: Michal Rutkowski
    :Created: 2019/03/10
    :Python Version: 3.7
"""

import os
import shutil

# qt modules
import PySide2
from PySide2 import QtWidgets, QtCore, QtSql, QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *

import framelessQt.PYM_MoveableWidget as MoveableWidget

Action_Style = ("""
    QPushButton { font-size: 16px; border: 0px; font-family: Source Sans Pro;background-color: transparent;color : #E6E6E6; }
    QPushButton:hover { font-size: 16px; border: 0px; font-family: Source Sans Pro;background-color: transparent;color : #E6E6E6; }
        """)


class QBaseButton(QtWidgets.QPushButton):
    def __init__(self, request, resourcesPath):
        super(QBaseButton, self).__init__(None)
        self.request = request
        self.iconsPath = os.path.join(resourcesPath, "icons")
        self.setIcon(QIcon(QPixmap(os.path.join(self.iconsPath, self.request + '_icon.png'))))
        self.setIconSize(QSize(22, 22))
        self.setStyleSheet(Action_Style)
        self.setMinimumHeight(22)
        # self.clicked.connect(self.cancel)

    def enterEvent(self, event):
        self.setIcon(QIcon(QPixmap(os.path.join(self.iconsPath, self.request + '_hover_icon.png'))))
        self.setIconSize(QSize(22, 22))

    def leaveEvent(self, event):
        self.setIcon(QIcon(QPixmap(os.path.join(self.iconsPath, self.request + '_icon.png'))))
        self.setIconSize(QSize(22, 22))


class MenuBarWidget(MoveableWidget.MoveableWidget):
    def __init__(self, app, title, resourcesPath, iconPath):
        super(MenuBarWidget, self).__init__(app)
        # Set the top layout
        self.menuBarLayout = QtWidgets.QHBoxLayout()
        self.menuBarLayout.setAlignment(Qt.AlignTop)
        #self.MainLayout.addLayout(self.menuBarLayout)
        self.menuBarLayout.setSpacing(8)

        self.logoIconLayout = QtWidgets.QHBoxLayout()
        self.menuBarLayout.addLayout(self.logoIconLayout)
        self.logoIconLayout.setAlignment(Qt.AlignLeft)
        self.logoIconLayout.setSpacing(8)

        self.logoButton = QtWidgets.QPushButton("")
        self.logoButton.setIcon(QIcon(QPixmap(os.path.join(resourcesPath, iconPath))))
        self.logoButton.setIconSize(QSize(35, 35))
        self.logoButton.setStyleSheet(Action_Style)
        self.logoIconLayout.addWidget(self.logoButton)
        self.titleLabel = QtWidgets.QLabel(title)
        self.logoIconLayout.addWidget(self.titleLabel)

        self.closeMinimizeLayout = QtWidgets.QHBoxLayout()
        self.menuBarLayout.addLayout(self.closeMinimizeLayout)
        self.closeMinimizeLayout.setAlignment(Qt.AlignRight)
        self.closeMinimizeLayout.setSpacing(8)

        self.minimizeButton = QBaseButton("minimize", resourcesPath)
        self.closeMinimizeLayout.addWidget(self.minimizeButton)
        self.minimizeButton.clicked.connect(lambda: self.app.showMinimized())

        self.close_ui = QBaseButton("close", resourcesPath)
        self.closeMinimizeLayout.addWidget(self.close_ui)
        self.close_ui.clicked.connect(self.cancel)

        self.menuBarLayout.addLayout(self.closeMinimizeLayout)

        self.setLayout(self.menuBarLayout)

        self.mouseLock = False

    def cancel(self):
        self.app.close()
        '''
        folder = "cache"
        # remove cache folder contents
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        '''
