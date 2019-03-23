# -*- coding: utf-8 -*-
#!/usr/bin/python
# package/PYM_SideNavWidget.py
"""
    SideNavWidget
    ~~~~~~~~~~~~~~~~~~

    Side Navigation widget designed for frameless UI in PySide2.
    Includes switching QStackedLayout tabs functionality.

    :Author: Michal Rutkowski
    :Created: 2019/03/13
    :Python Version: 3.7
"""

import os
import sys

# qt modules
import PySide2
from PySide2 import QtWidgets, QtCore, QtSql, QtGui

Action_Style = ("""
    QPushButton { font-size: 12px; border: 0px; background-color: #353535; color : #E6E6E6;}
    QPushButton:hover { font-size: 12px; border: 0px; background-color: #3f3f3f; color : #E6E6E6;}
    QPushButton:checked { font-size: 12px; border: 0px; background-color: #3f3f3f; color : #E6E6E6;}
        """)

class SideNavButton(QtWidgets.QPushButton):
    """
    Side Navigation button (inherits from QPushButton)
    """

    def __init__(self, label):
        super(SideNavButton, self).__init__(label)


class SideNavWidget(QtWidgets.QWidget):
    """
    Side Navigation widget written using PySide2 (inherits from QWidget)
    """
    def __init__(self, stackedLayout=None):
        super(SideNavWidget, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        mainLayout = QtWidgets.QHBoxLayout(self)
        mainLayout.setSpacing(0)
        mainLayout.setMargin(0)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        tabWidget = QtWidgets.QFrame()
        tabWidget.setObjectName('SideNavWidget')
        tabWidget.setStyleSheet("#SideNavWidget {background-color: #353535;}")
        tabWidget.setLayout(self.layout)
        mainLayout.addWidget(tabWidget)
        self.stackedLayout = stackedLayout

    def addTab(self, label, icon, layoutIndex):
        button = SideNavButton(label)
        button.setIcon(QtGui.QPixmap(icon))
        button.setStyleSheet(Action_Style)
        button.setFlat(True)
        button.setCheckable(True)
        button.setFixedSize(50, 50)
        button.setIconSize(QtCore.QSize(25, 25))
        #button.clicked.connect(self.switchToTab, layoutIndex)
        self.layout.addWidget(button)

    def switchToTab(self, index):
        self.stackedLayout.setCurrentIndex(index)
