# -*- coding: utf-8 -*-
#!/usr/bin/python
# package/PYM_ViewerWidget.py
"""
    ViewerWidget
    ~~~~~~~~~~~~~~~~~~

    Image Viewer widget designed for frameless UI in PySide2.
    Accepts files or directories with text/icon and optional frame display.

    :Author: Michal Rutkowski
    :Created: 2019/02/26
    :Python Version: 3.7
"""

import PySide2
from PySide2 import QtWidgets, QtCore, QtSql, QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PIL.ImageQt import ImageQt


class ViewerWidget(QtWidgets.QGraphicsView):
    imageClicked = Signal(QtCore.QPoint)

    def __init__(self, parent):
        super(ViewerWidget, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._image = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._image)
        self.rawImage = None
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(53, 53, 53)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setAcceptDrops(True)

    def hasImage(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._image.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasImage():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setImage(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._image.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._image.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def setFromPilImage(self, image):
        print("Setting viewer from pil image")
        data = image.tobytes("raw", "RGB")
        qimage = QtGui.QImage(data, image.size[0], image.size[1], QtGui.QImage.Format_RGB888)
        #qimage = ImageQt(image)
        print("Converted pil image to qimage")
        pixmap = QtGui.QPixmap.fromImage(qimage)
        print("Got pixmap from qimage")
        self.setImage(pixmap)

    def setViewerFromRawImage(self, item):
        imageData = item.getPixmap()
        #print("Got imagePath " + imagePath)
        self.setImage(imageData)
        self.rawImage = item

    def setViewerFromThumbnail(self, thumbnail):
        print("Set viewer from thumbnail called with", thumbnail)
        imageData = thumbnail.getRawImage().getPixmap()
        self.setImage(imageData)
        self.rawImage = thumbnail.getRawImage()

    def getRawImage(self):
        return self.rawImage

    def wheelEvent(self, event):
        if self.hasImage():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._image.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._image.isUnderMouse():
            self.imageClicked.emit(QtCore.QPoint(event.pos()))
        super(ViewerWidget, self).mousePressEvent(event)
