from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QGroupBox, QLabel, QSpinBox, QDoubleSpinBox, 
                             QComboBox, QSplitter, QScrollArea) # <--- Added QScrollArea
from PyQt5.QtCore import Qt
from collapsible_box import CollapsibleBox
from image_viewer import ImageViewer

class SpatialTab(QWidget):
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
        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # ── Scroll Area Setup ─────────────────────────────────────────────
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True) # Very important: allows inner widget to expand
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        # ── Left panel (Inside the Scroll Area) ───────────────────────────
        left_panel = QWidget() # Removed self here, scroll_area will take ownership
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignTop)
        
        # Image Input
        input_group = QGroupBox("Image Input", self)
        input_layout = QVBoxLayout()
        
        btn_layout = QHBoxLayout()
        self.btn_load_color = QPushButton("Load Color")
        self.btn_load_gray = QPushButton("Load Grayscale")
        btn_layout.addWidget(self.btn_load_color)
        btn_layout.addWidget(self.btn_load_gray)
        input_layout.addLayout(btn_layout)
        
        self.btn_rgb_to_gray = QPushButton("RGB → Grayscale Conversion")
        input_layout.addWidget(self.btn_rgb_to_gray)
        
        self.btn_restore = QPushButton("↺ RESTORE ORIGINAL IMAGE")
        self.btn_restore.setStyleSheet(self.accent_btn_style)
        input_layout.addWidget(self.btn_restore)
        input_group.setLayout(input_layout)
        left_layout.addWidget(input_group)
        
        # ── 1. Noise Addition ─────────────────────────────────────────────
        noise_collapsible = CollapsibleBox("▶ Noise Addition", self)
        noise_widget = QWidget(self)
        noise_layout = QVBoxLayout(noise_widget)
        
        uniform_layout = QHBoxLayout()
        self.btn_uniform = QPushButton("Uniform Noise")
        uniform_layout.addWidget(self.btn_uniform)
        uniform_layout.addWidget(QLabel("Intensity:"))
        self.uniform_intensity = QSpinBox()
        self.uniform_intensity.setRange(1, 100)
        self.uniform_intensity.setValue(50)
        uniform_layout.addWidget(self.uniform_intensity)
        noise_layout.addLayout(uniform_layout)
        
        gaussian_layout = QHBoxLayout()
        self.btn_gaussian = QPushButton("Gaussian Noise")
        gaussian_layout.addWidget(self.btn_gaussian)
        gaussian_layout.addWidget(QLabel("Sigma:"))
        self.sigma_spin = QDoubleSpinBox()
        self.sigma_spin.setRange(1, 100)
        self.sigma_spin.setValue(25)
        self.sigma_spin.setSingleStep(5)
        gaussian_layout.addWidget(self.sigma_spin)
        noise_layout.addLayout(gaussian_layout)
        
        sp_layout = QHBoxLayout()
        self.btn_sp = QPushButton("S&P Noise")
        sp_layout.addWidget(self.btn_sp)
        sp_layout.addWidget(QLabel("Ratio:"))
        self.sp_ratio_spin = QDoubleSpinBox()
        self.sp_ratio_spin.setRange(0.01, 0.5)
        self.sp_ratio_spin.setValue(0.05)
        self.sp_ratio_spin.setSingleStep(0.01)
        self.sp_ratio_spin.setDecimals(2)
        sp_layout.addWidget(self.sp_ratio_spin)
        noise_layout.addLayout(sp_layout)
        
        note_label = QLabel("⚠️ Each operation is applied to the original image")
        note_label.setStyleSheet("color: #98c1d9; font-size: 11px; font-style: italic; padding: 5px;")
        note_label.setAlignment(Qt.AlignCenter)
        noise_layout.addWidget(note_label)

        self.btn_save_noisy = QPushButton("💾 Save Current Image")
        self.btn_save_noisy.setStyleSheet(self.accent_btn_style)
        noise_layout.addWidget(self.btn_save_noisy)
        noise_collapsible.addWidget(noise_widget)
        left_layout.addWidget(noise_collapsible)
        
        # ── 2. Noise Filtering ────────────────────────────────────────────
        filter_collapsible = CollapsibleBox("▶ Noise Filtering (Low-Pass)", self)
        filter_widget = QWidget(self)
        filter_layout = QVBoxLayout(filter_widget)
        
        avg_layout = QHBoxLayout()
        self.btn_avg = QPushButton("Average Filter")
        avg_layout.addWidget(self.btn_avg)
        avg_layout.addWidget(QLabel("Kernel:"))
        self.avg_kernel = QComboBox()
        self.avg_kernel.addItems(["3", "5", "7"])
        avg_layout.addWidget(self.avg_kernel)
        filter_layout.addLayout(avg_layout)
        
        gaussian_filter_layout = QHBoxLayout()
        self.btn_gaussian_filter = QPushButton("Gaussian Filter")
        gaussian_filter_layout.addWidget(self.btn_gaussian_filter)
        gaussian_filter_layout.addWidget(QLabel("K:"))
        self.gaussian_kernel = QComboBox()
        self.gaussian_kernel.addItems(["3", "5", "7"])
        gaussian_filter_layout.addWidget(self.gaussian_kernel)
        gaussian_filter_layout.addWidget(QLabel("σ:"))
        self.gaussian_sigma = QDoubleSpinBox()
        self.gaussian_sigma.setRange(0.1, 5)
        self.gaussian_sigma.setValue(1)
        self.gaussian_sigma.setSingleStep(0.1)
        gaussian_filter_layout.addWidget(self.gaussian_sigma)
        filter_layout.addLayout(gaussian_filter_layout)
        
        median_layout = QHBoxLayout()
        self.btn_median = QPushButton("Median Filter")
        median_layout.addWidget(self.btn_median)
        median_layout.addWidget(QLabel("Kernel:"))
        self.median_kernel = QComboBox()
        self.median_kernel.addItems(["3", "5", "7"])
        median_layout.addWidget(self.median_kernel)
        filter_layout.addLayout(median_layout)
        
        filter_collapsible.addWidget(filter_widget)
        left_layout.addWidget(filter_collapsible)
        
        # ── 3. Edge Detection ─────────────────────────────────────────────
        edge_collapsible = CollapsibleBox("▶ Edge Detection", self)
        edge_widget = QWidget(self)
        edge_layout = QVBoxLayout(edge_widget)
        
        self.btn_sobel = QPushButton("Sobel")
        self.btn_roberts = QPushButton("Roberts")
        self.btn_prewitt = QPushButton("Prewitt")
        edge_layout.addWidget(self.btn_sobel)
        edge_layout.addWidget(self.btn_roberts)
        edge_layout.addWidget(self.btn_prewitt)
        
        canny_layout = QHBoxLayout()
        self.btn_canny = QPushButton("Canny")
        canny_layout.addWidget(self.btn_canny)
        canny_layout.addWidget(QLabel("T1:"))
        self.canny_th1 = QSpinBox()
        self.canny_th1.setRange(0, 255)
        self.canny_th1.setValue(100)
        canny_layout.addWidget(self.canny_th1)
        canny_layout.addWidget(QLabel("T2:"))
        self.canny_th2 = QSpinBox()
        self.canny_th2.setRange(0, 255)
        self.canny_th2.setValue(200)
        canny_layout.addWidget(self.canny_th2)
        edge_layout.addLayout(canny_layout)
        
        edge_collapsible.addWidget(edge_widget)
        left_layout.addWidget(edge_collapsible)

        # ── 4. Histogram Analysis ─────────────────────────────────────────
        hist_collapsible = CollapsibleBox("▶ Histogram Analysis", self)
        hist_widget = QWidget(self)
        hist_layout = QVBoxLayout(hist_widget)

        hist_info = QLabel("Plots the histogram and CDF of the current image.")
        hist_info.setStyleSheet("color: #98c1d9; font-size: 11px; font-style: italic;")
        hist_info.setWordWrap(True)
        hist_layout.addWidget(hist_info)

        self.btn_show_histogram = QPushButton("📊 Show Histogram & CDF")
        self.btn_show_histogram.setStyleSheet(self.accent_btn_style)
        hist_layout.addWidget(self.btn_show_histogram)

        hist_collapsible.addWidget(hist_widget)
        left_layout.addWidget(hist_collapsible)

        # ── 5. Histogram Equalization ─────────────────────────────────────
        eq_collapsible = CollapsibleBox("▶ Histogram Equalization", self)
        eq_widget = QWidget(self)
        eq_layout = QVBoxLayout(eq_widget)

        eq_info = QLabel("Enhances contrast of low-contrast images by redistributing intensity values. Works on grayscale or color (Y channel).")
        eq_info.setStyleSheet("color: #98c1d9; font-size: 11px; font-style: italic;")
        eq_info.setWordWrap(True)
        eq_layout.addWidget(eq_info)

        self.btn_equalize = QPushButton("⚖️ Apply Histogram Equalization")
        self.btn_equalize.setStyleSheet(self.accent_btn_style)
        eq_layout.addWidget(self.btn_equalize)

        eq_collapsible.addWidget(eq_widget)
        left_layout.addWidget(eq_collapsible)

        # ── 6. Image Normalization ────────────────────────────────────────
        norm_collapsible = CollapsibleBox("▶ Image Normalization", self)
        norm_widget = QWidget(self)
        norm_layout = QVBoxLayout(norm_widget)

        norm_info = QLabel("Stretches pixel intensities so the darkest pixel maps to the minimum and the brightest to the maximum (min-max normalization).")
        norm_info.setStyleSheet("color: #98c1d9; font-size: 11px; font-style: italic;")
        norm_info.setWordWrap(True)
        norm_layout.addWidget(norm_info)

        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("Output Min:"))
        self.norm_min = QSpinBox()
        self.norm_min.setRange(0, 254)
        self.norm_min.setValue(0)
        range_layout.addWidget(self.norm_min)
        range_layout.addWidget(QLabel("Max:"))
        self.norm_max = QSpinBox()
        self.norm_max.setRange(1, 255)
        self.norm_max.setValue(255)
        range_layout.addWidget(self.norm_max)
        norm_layout.addLayout(range_layout)

        self.btn_normalize = QPushButton("🎚️ Apply Normalization")
        self.btn_normalize.setStyleSheet(self.accent_btn_style)
        norm_layout.addWidget(self.btn_normalize)

        norm_collapsible.addWidget(norm_widget)
        left_layout.addWidget(norm_collapsible)

        left_layout.addStretch()
        
        # ── Wrap the panel in the scroll area ─────────────────────────────
        scroll_area.setWidget(left_panel) # <--- Put the populated panel inside the scroll area
        
        # ── Right panel ───────────────────────────────────────────────────
        right_panel = QWidget(self)
        right_layout = QVBoxLayout(right_panel)
        
        self.image_viewer = ImageViewer()
        right_layout.addWidget(self.image_viewer)
        
        self.status_label = QLabel("No image loaded")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            background-color: #3d5a80; /* Dusk Blue */
            color: #e0fbfc; /* Light Cyan */
            padding: 8px; border-radius: 3px; font-weight: bold;
        """)
        right_layout.addWidget(self.status_label)
        
        # ── Assemble Splitter ─────────────────────────────────────────────
        splitter.addWidget(scroll_area) # <--- Add the scroll area instead of left_panel directly
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 1000])