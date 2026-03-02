from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QGroupBox, QLabel, QComboBox, QSpinBox
from image_viewer import ImageViewer

class FrequencyTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.accent_btn_style = """
            QPushButton {
                background-color: #bc4749; color: #e0fbfc;
                font-weight: bold; font-size: 13px;
                padding: 10px; border-radius: 5px;
            }
            QPushButton:hover { background-color: #98c1d9; color: #293241; }
        """
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)
        
        # --- Image 1 Panel ---
        group_img1 = QGroupBox("Image 1 (Frequency Filter)", self)
        layout_img1 = QVBoxLayout(group_img1)
        
        ctrl_layout1 = QHBoxLayout()
        self.btn_load_f1 = QPushButton("Load Image 1")
        self.combo_filter1 = QComboBox()
        self.combo_filter1.addItems(["LPF", "HPF"])
        self.spin_radius1 = QSpinBox()
        self.spin_radius1.setRange(1, 1000)
        self.spin_radius1.setValue(30)
        self.btn_apply_f1 = QPushButton("Apply Filter")
        
        ctrl_layout1.addWidget(self.btn_load_f1)
        ctrl_layout1.addWidget(QLabel("Filter:"))
        ctrl_layout1.addWidget(self.combo_filter1)
        ctrl_layout1.addWidget(QLabel("Radius:"))
        ctrl_layout1.addWidget(self.spin_radius1)
        ctrl_layout1.addWidget(self.btn_apply_f1)
        
        self.viewer_f1_orig = ImageViewer()
        self.viewer_f1_filt = ImageViewer()
        
        layout_img1.addLayout(ctrl_layout1)
        layout_img1.addWidget(QLabel("Original / Magnitude Spectrum:"))
        layout_img1.addWidget(self.viewer_f1_orig)
        layout_img1.addWidget(QLabel("Filtered Result:"))
        layout_img1.addWidget(self.viewer_f1_filt)
        
        # --- Image 2 Panel ---
        group_img2 = QGroupBox("Image 2 (Frequency Filter)", self)
        layout_img2 = QVBoxLayout(group_img2)
        
        ctrl_layout2 = QHBoxLayout()
        self.btn_load_f2 = QPushButton("Load Image 2")
        self.combo_filter2 = QComboBox()
        self.combo_filter2.addItems(["HPF", "LPF"]) # Default to HPF
        self.spin_radius2 = QSpinBox()
        self.spin_radius2.setRange(1, 1000)
        self.spin_radius2.setValue(30)
        self.btn_apply_f2 = QPushButton("Apply Filter")
        
        ctrl_layout2.addWidget(self.btn_load_f2)
        ctrl_layout2.addWidget(QLabel("Filter:"))
        ctrl_layout2.addWidget(self.combo_filter2)
        ctrl_layout2.addWidget(QLabel("Radius:"))
        ctrl_layout2.addWidget(self.spin_radius2)
        ctrl_layout2.addWidget(self.btn_apply_f2)
        
        self.viewer_f2_orig = ImageViewer()
        self.viewer_f2_filt = ImageViewer()
        
        layout_img2.addLayout(ctrl_layout2)
        layout_img2.addWidget(QLabel("Original / Magnitude Spectrum:"))
        layout_img2.addWidget(self.viewer_f2_orig)
        layout_img2.addWidget(QLabel("Filtered Result:"))
        layout_img2.addWidget(self.viewer_f2_filt)
        
        # --- Hybrid Result Panel ---
        group_hybrid = QGroupBox("Hybrid Result", self)
        layout_hybrid = QVBoxLayout(group_hybrid)
        
        self.btn_generate_hybrid = QPushButton("Generate Hybrid Image")
        self.btn_generate_hybrid.setStyleSheet(self.accent_btn_style)
        self.viewer_hybrid = ImageViewer()
        
        layout_hybrid.addWidget(self.btn_generate_hybrid)
        layout_hybrid.addWidget(self.viewer_hybrid)
        
        # Add to Grid
        layout.addWidget(group_img1, 0, 0)
        layout.addWidget(group_img2, 0, 1)
        layout.addWidget(group_hybrid, 0, 2)