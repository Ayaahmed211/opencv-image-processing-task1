from PyQt5.QtWidgets import QLabel, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
import cv2
import numpy as np

class ImageViewer(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        
        self.setWidget(self.imageLabel)
        self.setWidgetResizable(True)
        
        self.pixmap = None
        self.scale_factor = 1.0
        
    def setImage(self, cv_image):
        """Set image from OpenCV format"""
        if cv_image is None:
            return
        
        # Convert OpenCV BGR to RGB
        if len(cv_image.shape) == 3:
            height, width, channel = cv_image.shape
            bytes_per_line = 3 * width
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            q_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        else:
            height, width = cv_image.shape
            bytes_per_line = width
            q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        
        self.pixmap = QPixmap.fromImage(q_image)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.resize(self.pixmap.size())
        
    def clear(self):
        """Clear the image"""
        self.imageLabel.clear()
        self.pixmap = None