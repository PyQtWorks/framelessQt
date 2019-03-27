# -*- coding: utf-8 -*-
#!/usr/bin/python
# package/PYM_MoveableWidget.py
"""
    MoveableWidget
    ~~~~~~~~~~~~~~~~~~

    Moveable widget designed for frameless UI in PySide2.

    :Author: Michal Rutkowski
    :Created: 2019/03/26
    :Python Version: 3.7
"""

import os
import sys

# qt modules
import PySide2
from PySide2 import QtWidgets, QtCore, QtSql, QtGui


class MoveableWidget(QtWidgets.QWidget):
    """
    Moveable widget designed for frameless UI in PySide2.
    """
    def __init__(self, app):
        super(MoveableWidget, self).__init__()
        self.app = app
        self.mouselock = None

    def widgetUnderCursor(self, pos):
        print("Widget found under cursor")
        widgets = []
        widget_at = self.app.widgetAt(pos)

        while widget_at:
            widgets.append(widget_at)
            # Make widget invisible to further enquiries
            widget_at.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
            widget_at = self.app.widgetAt(pos)

        # Restore attribute
        for widget in widgets:
            widget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)

        return widgets

    def mousePressEvent(self, event):
        print("Selected widget is ", self.widgetUnderCursor(QtGui.QCursor.pos())[0])
        try:
            self.mouselock = None
            moveableWidgets = [self]
            if self.widgetUnderCursor(QtGui.QCursor.pos())[0] in moveableWidgets:
                print("Start moving widget")
                self.mouselock = True
                self.offset = event.pos()
            else:
                self.mouseReleaseEvent(event)
        except:
            pass

    def mouseMoveEvent(self, event):
        print("Moving mouse, mouselock value is ", self.mouselock)
        try:
            if (self.mouselock is True):
                x = event.globalX()
                y = event.globalY()
                x_w = self.offset.x()
                y_w = self.offset.y()
                self.move(x-x_w, y-y_w)
                self.update()
        except:
            print("Moving window failed")
            pass

    def mouseReleaseEvent(self, event):
        try:
            self.mouselock = None
            self.offset = event.pos()
        except:
            pass
