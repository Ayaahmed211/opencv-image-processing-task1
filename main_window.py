import os
import cv2
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QFileDialog, QMessageBox
from image_processor import ImageProcessor
from histogram_dialog import HistogramDialog
import frequency_domain
import numpy as np

# Import the new UI components
from spatial_tab import SpatialTab
from frequency_tab import FrequencyTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.processor = ImageProcessor()
        self.dataset_path = "dataset_images"
        
        # State variables for frequency domain
        self.freq_img1_orig = None
        self.freq_img2_orig = None
        self.freq_img1_float = None
        self.freq_img2_float = None
        
        self.initUI()
        self.connect_signals()
        
    def initUI(self):
        self.setWindowTitle('Image Processing Application')
        self.setGeometry(100, 100, 1400, 800)
        
        # --- GLOBAL APPLICATION THEME (DARK MODE) ---
        self.setStyleSheet("""
            QWidget {
                background-color: #293241; /* Jet Black */
                color: #e0fbfc; /* Light Cyan */
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel { background-color: transparent; }
            QTabWidget::pane {
                border: 2px solid #3d5a80; /* Dusk Blue */
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #3d5a80; color: #e0fbfc; padding: 10px 20px;
                border-top-left-radius: 5px; border-top-right-radius: 5px;
                font-weight: bold; margin-right: 2px;
            }
            QTabBar::tab:selected { background: #98c1d9; color: #293241; }
            QTabBar::tab:hover:!selected { background: #bc4749; color: #293241; }
            QGroupBox {
                border: 2px solid #3d5a80; border-radius: 6px;
                margin-top: 15px; font-weight: bold;
                color: #98c1d9; background-color: transparent;
            }
            QGroupBox::title {
                subcontrol-origin: margin; subcontrol-position: top left;
                padding: 0 5px; left: 10px;
            }
            QPushButton {
                background-color: #3d5a80; color: #e0fbfc;
                border: none; border-radius: 4px; padding: 8px 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #98c1d9; color: #293241; }
            QPushButton:pressed {
                background-color: #293241; color: #98c1d9; border: 1px solid #98c1d9;
            }
            QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #3d5a80; border: 1px solid #98c1d9;
                border-radius: 3px; padding: 4px; color: #e0fbfc;
            }
            QComboBox::drop-down { border-left: 1px solid #98c1d9; }
            QSplitter::handle {
                background-color: #3d5a80; width: 3px; margin: 4px 0px;
            }
        """)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Initialize Tabs
        self.spatial_tab = SpatialTab()
        self.tabs.addTab(self.spatial_tab, "Spatial Domain")
        
        self.freq_tab = FrequencyTab()
        self.tabs.addTab(self.freq_tab, "Frequency Domain")

    def connect_signals(self):
        """Wire all buttons to their respective controller logic."""
        st = self.spatial_tab
        # Spatial Domain - I/O (UPDATED to use the single smart load button)
        st.btn_load_image.clicked.connect(self.load_image)
        st.btn_rgb_to_gray.clicked.connect(self.convert_rgb_to_grayscale)
        st.btn_restore.clicked.connect(self.restore_original)
        st.btn_save_noisy.clicked.connect(self.save_current_image)
        
        # Spatial Domain - Noise
        st.btn_uniform.clicked.connect(self.add_uniform_noise)
        st.btn_gaussian.clicked.connect(self.add_gaussian_noise)
        st.btn_sp.clicked.connect(self.add_salt_pepper_noise)
        
        # Spatial Domain - Filtering
        st.btn_avg.clicked.connect(self.apply_average_filter)
        st.btn_gaussian_filter.clicked.connect(self.apply_gaussian_filter)
        st.btn_median.clicked.connect(self.apply_median_filter)
        
        # Spatial Domain - Edges
        st.btn_sobel.clicked.connect(self.apply_sobel)
        st.btn_roberts.clicked.connect(self.apply_roberts)
        st.btn_prewitt.clicked.connect(self.apply_prewitt)
        st.btn_canny.clicked.connect(self.apply_canny)
        
        # Spatial Domain - Histogram & Normalization
        st.btn_show_histogram.clicked.connect(self.show_histogram)
        st.btn_equalize.clicked.connect(self.apply_histogram_equalization)
        st.btn_normalize.clicked.connect(self.apply_normalization)

        ft = self.freq_tab
        # Frequency Domain
        ft.btn_load_f1.clicked.connect(lambda: self.load_freq_image(1))
        ft.btn_load_f2.clicked.connect(lambda: self.load_freq_image(2))
        ft.btn_apply_f1.clicked.connect(lambda: self.apply_freq_filter(1))
        ft.btn_apply_f2.clicked.connect(lambda: self.apply_freq_filter(2))
        ft.btn_generate_hybrid.clicked.connect(self.generate_hybrid_image)

    # =========================================================================
    # Spatial Domain Functions
    # =========================================================================
    
    def load_image(self):
        """Smart loader that handles both Color and Grayscale automatically."""
        if not os.path.exists(self.dataset_path):
            return QMessageBox.warning(self, "Warning", f"Folder '{self.dataset_path}' not found!")
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", self.dataset_path, "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            img, success = self.processor.load_image(file_path)
            if success:
                self.spatial_tab.image_viewer.setImage(img)
                h, w = img.shape[:2]
                # Dynamically update label based on the smart loader's finding
                mode = "Grayscale" if self.processor.is_gray else "Color"
                self.spatial_tab.status_label.setText(f"Loaded: {os.path.basename(file_path)} ({mode}) | Size: {w}x{h}")
            else:
                QMessageBox.critical(self, "Error", "Failed to load image!")

    def convert_rgb_to_grayscale(self):
        if self.processor.original_image is None:
            return QMessageBox.warning(self, "Warning", "Please load an image first!")
        if self.processor.is_gray:
            return QMessageBox.information(self, "Info", "Image is already grayscale!")
        gray_img = self.processor.convert_to_grayscale()
        self.spatial_tab.image_viewer.setImage(gray_img)
        self.spatial_tab.status_label.setText("Converted RGB to Grayscale")
    
    def restore_original(self):
        if self.processor.original_image is None:
            return QMessageBox.warning(self, "Warning", "No image loaded!")
        img = self.processor.restore_original()
        if img is not None:
            self.spatial_tab.image_viewer.setImage(img)
            self.spatial_tab.status_label.setText("Restored original image")
    
    def save_current_image(self):
        if self.processor.current_image is None:
            return QMessageBox.warning(self, "Warning", "No image to save! Apply noise first.")
        if not os.path.exists(self.dataset_path):
            os.makedirs(self.dataset_path)
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Current Image", self.dataset_path, "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg);;BMP Image (*.bmp)"
        )
        if file_path:
            success = cv2.imwrite(file_path, self.processor.current_image)
            if success:
                QMessageBox.information(self, "Saved", f"Image saved:\n{file_path}")
                self.spatial_tab.status_label.setText(f"Saved: {os.path.basename(file_path)}")
            else:
                QMessageBox.critical(self, "Error", "Failed to save image!")

    def add_uniform_noise(self):
        if self.processor.original_image is None:
            return QMessageBox.warning(self, "Warning", "Please load an image first!")
        intensity = self.spatial_tab.uniform_intensity.value()
        img = self.processor.add_uniform_noise(intensity)
        self.spatial_tab.image_viewer.setImage(img)
        self.spatial_tab.status_label.setText(f"Added Uniform Noise (intensity={intensity})")
    
    def add_gaussian_noise(self):
        if self.processor.original_image is None:
            return QMessageBox.warning(self, "Warning", "Please load an image first!")
        sigma = self.spatial_tab.sigma_spin.value()
        img = self.processor.add_gaussian_noise(sigma)
        self.spatial_tab.image_viewer.setImage(img)
        self.spatial_tab.status_label.setText(f"Added Gaussian Noise (σ={sigma})")
    
    def add_salt_pepper_noise(self):
        if self.processor.original_image is None:
            return QMessageBox.warning(self, "Warning", "Please load an image first!")
        ratio = self.spatial_tab.sp_ratio_spin.value()
        img = self.processor.add_salt_pepper_noise(ratio)
        self.spatial_tab.image_viewer.setImage(img)
        self.spatial_tab.status_label.setText(f"Added Salt & Pepper Noise (ratio={ratio})")

    def apply_average_filter(self):
        if self.processor.original_image is None: return
        kernel = int(self.spatial_tab.avg_kernel.currentText())
        img = self.processor.apply_average_filter(kernel)
        self.spatial_tab.image_viewer.setImage(img)
    
    def apply_gaussian_filter(self):
        if self.processor.original_image is None: return
        kernel = int(self.spatial_tab.gaussian_kernel.currentText())
        sigma = self.spatial_tab.gaussian_sigma.value()
        img = self.processor.apply_gaussian_filter(kernel, sigma)
        self.spatial_tab.image_viewer.setImage(img)
    
    def apply_median_filter(self):
        if self.processor.original_image is None: return
        kernel = int(self.spatial_tab.median_kernel.currentText())
        img = self.processor.apply_median_filter(kernel)
        self.spatial_tab.image_viewer.setImage(img)

    def apply_sobel(self):
        if self.processor.original_image is None: return
        edges = self.processor.sobel_edge_detection()
        self.spatial_tab.image_viewer.setImage(edges)
    
    def apply_roberts(self):
        if self.processor.original_image is None: return
        edges = self.processor.roberts_edge_detection()
        self.spatial_tab.image_viewer.setImage(edges)
    
    def apply_prewitt(self):
        if self.processor.original_image is None: return
        edges = self.processor.prewitt_edge_detection()
        self.spatial_tab.image_viewer.setImage(edges)
    
    def apply_canny(self):
        if self.processor.original_image is None: return
        th1 = self.spatial_tab.canny_th1.value()
        th2 = self.spatial_tab.canny_th2.value()
        edges = self.processor.canny_edge_detection(th1, th2)
        self.spatial_tab.image_viewer.setImage(edges)

    def show_histogram(self):
        if self.processor.current_image is None: return
        hist_data = self.processor.compute_histogram_data()
        if hist_data is None: return
        dlg = HistogramDialog(hist_data, title="Histogram Analysis", parent=self)
        dlg.exec_()

    def apply_histogram_equalization(self):
        if self.processor.original_image is None: return
        before_img = self.processor.get_display_image()
        img, eq_data = self.processor.apply_histogram_equalization()
        if img is None: return
        self.spatial_tab.image_viewer.setImage(img)
        dlg = HistogramDialog(eq_data['after'], title="Histogram Equalization", equalization_data=eq_data, before_image=before_img, after_image=img, parent=self)
        dlg.exec_()

    def apply_normalization(self):
        if self.processor.original_image is None: return
        new_min = self.spatial_tab.norm_min.value()
        new_max = self.spatial_tab.norm_max.value()
        if new_min >= new_max: return QMessageBox.warning(self, "Warning", "Min >= Max!")
        img = self.processor.apply_normalization(new_min, new_max)
        if img is not None: self.spatial_tab.image_viewer.setImage(img)

    # =========================================================================
    # Frequency Domain & Hybrid Functions
    # =========================================================================

    def load_freq_image(self, img_num):
        file_path, _ = QFileDialog.getOpenFileName(self, f"Select Image {img_num}", self.dataset_path, "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if not file_path: return
        
        img, success = self.processor.load_frequency_image(file_path)
        
        if success:
            display_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            if img_num == 1:
                self.freq_img1_orig = img
                self.freq_tab.viewer_f1_orig.setImage(display_img)
            else:
                self.freq_img2_orig = img
                self.freq_tab.viewer_f2_orig.setImage(display_img)
        else:
            QMessageBox.critical(self, "Error", "Failed to load image!")

    def apply_freq_filter(self, img_num):
        """Applies frequency filter and avoids code repetition."""
        # 1. Dynamically set variables based on which image is being processed
        if img_num == 1:
            if self.freq_img1_orig is None:
                return QMessageBox.warning(self, "Warning", "Load Image 1 first!")
            img = self.freq_img1_orig
            f_type = self.freq_tab.combo_filter1.currentText()
            d0 = self.freq_tab.spin_d0_1.value()
            viewer = self.freq_tab.viewer_f1_filt
        else:
            if self.freq_img2_orig is None:
                return QMessageBox.warning(self, "Warning", "Load Image 2 first!")
            img = self.freq_img2_orig
            f_type = self.freq_tab.combo_filter2.currentText()
            d0 = self.freq_tab.spin_d0_2.value()
            viewer = self.freq_tab.viewer_f2_filt
            
        # 2. Call the C++ backend exactly once
        display_img, float_data = frequency_domain.apply_filter(img, f_type, d0)
        
        # 3. Save the float data to the correct state variable
        if img_num == 1:
            self.freq_img1_float = float_data
        else:
            self.freq_img2_float = float_data
            
        # 4. Update the UI
        viewer.setImage(display_img)

    def generate_hybrid_image(self):
        if self.freq_img1_float is None or self.freq_img2_float is None:
            return QMessageBox.warning(self, "Warning", "Please apply filters to BOTH images first!")
            
        hybrid_img = frequency_domain.generate_hybrid(self.freq_img1_float, self.freq_img2_float)
        self.freq_tab.viewer_hybrid.setImage(hybrid_img)