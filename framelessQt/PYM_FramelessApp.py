# -*- coding: utf-8 -*-
#!/usr/bin/python
# package/PYM_FramelessApp.py
"""
    FramelessApp
    ~~~~~~~~~~~~~~~~~~

    Main application class designed for frameless UI in PySide2.

    :Author: Michal Rutkowski
    :Created: 2019/03/26
    :Python Version: 3.7
"""

import os
import sys
import platform

# qt modules
import PySide2
from PySide2 import QtWidgets, QtCore, QtSql, QtGui

import framelessQt.PYM_QDarkPalette as QDarkPalette
import framelessQt.PYM_MenuBarWidget as MenuBarWidget
import framelessQt.PYM_FooterWidget as FooterWidget

class FramelessApp(QtWidgets.QApplication):
    """
    Main application class designed for frameless UI in PySide2.
    """
    def __init__(self):
        super(FramelessApp, self).__init__()

        fontStyle = ("QLabel {font-size: 13px;}")
        self.setStyleSheet(fontStyle)

        darkPalette = QDarkPalette.QDarkPalette()
        darkPalette.set_app(self)
        self.setPalette(darkPalette)


    def createWindow(self, title, width, height, widget=None):
        """
        Creates window of size (width, height) and given title and immediately draws it.

        :param title: Window title displayed in menu bar
        :param width: Window width
        :param height: Window height
        :param widget: Optional widget to use instead of default empty widget
        :returns:
        """
        screen_resolution = self.desktop().screenGeometry()
        screenWidth, screenHeight = screen_resolution.width(), screen_resolution.height()

        mainWidget = QtWidgets.QWidget()
        mainWidget.setWindowTitle(title)
        mainWidget.setGeometry(0.5*(screenWidth - width), 0.5*(screenHeight-height), width, height)

        mainLayout = QtWidgets.QVBoxLayout()
        modulePath = os.path.dirname(__file__)
        print("Module path is ", modulePath)
        self.sharedResources = os.path.abspath(os.path.join(modulePath, "resources"))
        print("Resources path is ", self.sharedResources)
        self.iconPath = os.path.join(self.sharedResources, "icons/close_icon.png")
        menuBarWidget = MenuBarWidget.MenuBarWidget(mainWidget, title, self.sharedResources, self.iconPath)

        showRam = True
        showDisk = False
        footerWidget = FooterWidget.FooterWidget(self.sharedResources, showRam, showDisk)

        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        self.setWindowIcon(QtGui.QIcon(self.iconPath))

        # set qt flags required for frameless look
        self.setFramelessParams(mainWidget, title)

        # main window content area
        contentLayout = QtWidgets.QHBoxLayout()

        mainLayout.addWidget(menuBarWidget)
        mainLayout.addLayout(contentLayout)
        mainLayout.addWidget(footerWidget)

        mainWidget.setLayout(mainLayout)
        mainWidget.show()
        sys.exit(self.exec_())

        return contentLayout

    def setFramelessParams(self, widget, title):
        widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        widget.setContentsMargins(0, 0, 0, 0)

        if os.name == 'nt':
            # This is needed to display the app icon on the taskbar on Windows 7
            import ctypes
            myappid = title
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
