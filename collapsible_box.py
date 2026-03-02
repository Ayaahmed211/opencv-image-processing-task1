from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolButton
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)
        
        self.toggle_button = QToolButton(self)
        self.toggle_button.setText(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.setStyleSheet("""
            QToolButton { 
                border: none; 
                font-weight: bold; 
                font-size: 14px; 
                color: #e0fbfc; /* Light Cyan */
                text-align: left;
            }
            QToolButton:hover { color: #bc4749; /* Burnt Peach */ }
        """)
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.toggled.connect(self.on_toggle)
        
        self.content_area = QWidget(self)
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)
        self.content_area.setVisible(False)
        
        # Define layout once during init to prevent garbage collection issues
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 5, 10, 5)
        
        self.animation = QPropertyAnimation(self.content_area, b"maximumHeight", self)
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(self.on_animation_finished)
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.content_area)
        
        self._expanding = False
    
    def on_toggle(self, checked):
        self.toggle_button.setArrowType(Qt.DownArrow if checked else Qt.RightArrow)
        self.animation.stop()
        
        if checked:
            self._expanding = True
            self.content_area.setVisible(True)
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.content_area.sizeHint().height())
        else:
            self._expanding = False
            self.animation.setStartValue(self.content_area.height())
            self.animation.setEndValue(0)
        
        self.animation.start()
    
    def on_animation_finished(self):
        if not self._expanding:
            self.content_area.setVisible(False)
    
    def addWidget(self, widget):
        self.content_layout.addWidget(widget)