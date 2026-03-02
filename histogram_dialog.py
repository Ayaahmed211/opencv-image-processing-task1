from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTabWidget, QWidget, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
import cv2

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class HistogramCanvas(FigureCanvas):
    def __init__(self, width=7, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1e1e2e')
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()


class HistogramDialog(QDialog):
    BG   = '#1e1e2e'
    GRID = '#313244'
    TEXT = '#cdd6f4'

    def __init__(self, hist_data, title="Histogram Analysis",
                 equalization_data=None,
                 before_image=None, after_image=None,
                 parent=None):
        """
        Parameters
        ----------
        hist_data         : dict  – compute_histogram_data() for current image
        equalization_data : dict or None – {'before': ..., 'after': ...}
        before_image      : np.ndarray or None – BGR image before equalization
        after_image       : np.ndarray or None – BGR image after equalization
        """
        super().__init__(parent)
        self.hist_data         = hist_data
        self.equalization_data = equalization_data
        self.before_image      = before_image
        self.after_image       = after_image

        self.setWindowTitle(title)
        self.setMinimumSize(920, 620)
        self.setStyleSheet(f"""
            QDialog   {{ background: {self.BG}; color: {self.TEXT}; }}
            QTabWidget::pane {{ border: 1px solid #45475a; border-radius: 6px; }}
            QTabBar::tab {{
                background: #313244; color: {self.TEXT};
                padding: 8px 18px; border-radius: 4px 4px 0 0; margin-right: 3px;
            }}
            QTabBar::tab:selected {{ background: #89b4fa; color: #1e1e2e; font-weight: bold; }}
            QPushButton {{
                background: #89b4fa; color: #1e1e2e;
                padding: 7px 22px; border-radius: 5px;
                font-weight: bold; font-size: 13px;
            }}
            QPushButton:hover {{ background: #b4d0fa; }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.tabs.addTab(self._make_histogram_tab(), "📊 Histogram")
        self.tabs.addTab(self._make_cdf_tab(),       "📈 CDF")

        if equalization_data and before_image is not None and after_image is not None:
            self.tabs.addTab(self._make_image_comparison_tab(), "🖼️ Image Comparison")
            self.tabs.addTab(self._make_before_after_hist_tab(), "⚖️ Histogram Comparison")
            self.tabs.setCurrentIndex(2)   # open on image comparison

        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.accept)
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(btn_close)
        layout.addLayout(row)

    # ── helpers ───────────────────────────────────────────────────────────

    def _style_ax(self, ax, title, xlabel="Intensity (0–255)", ylabel=""):
        ax.set_facecolor(self.BG)
        ax.set_title(title, color=self.TEXT, fontsize=12, pad=10)
        ax.set_xlabel(xlabel, color=self.TEXT, fontsize=9)
        ax.set_ylabel(ylabel, color=self.TEXT, fontsize=9)
        ax.tick_params(colors=self.TEXT, labelsize=8)
        ax.set_xlim(0, 255)
        for spine in ax.spines.values():
            spine.set_edgecolor(self.GRID)
        ax.grid(True, color=self.GRID, linewidth=0.5, alpha=0.6)

    def _plot_hist(self, ax, channel_data, alpha=0.75):
        x = np.arange(256)
        for info in channel_data.values():
            ax.fill_between(x, info['hist'], alpha=alpha,
                            color=info['color'], label=info['label'])
            ax.plot(x, info['hist'], color=info['color'], linewidth=0.8)
        ax.legend(facecolor='#313244', edgecolor='none',
                  labelcolor=self.TEXT, fontsize=9)

    def _plot_cdf(self, ax, channel_data):
        x = np.arange(256)
        for info in channel_data.values():
            ax.plot(x, info['cdf'], color=info['color'],
                    linewidth=2, label=info['label'])
            ax.fill_between(x, info['cdf'], alpha=0.12, color=info['color'])
        ax.set_ylim(0, 1.05)
        ax.legend(facecolor='#313244', edgecolor='none',
                  labelcolor=self.TEXT, fontsize=9)

    @staticmethod
    def _cv_to_pixmap(cv_img):
        if cv_img is None:
            return QPixmap()
        if len(cv_img.shape) == 2:
            h, w = cv_img.shape
            qimg = QImage(cv_img.data, w, h, w, QImage.Format_Grayscale8)
        else:
            h, w, _ = cv_img.shape
            rgb  = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            qimg = QImage(rgb.data, w, h, 3 * w, QImage.Format_RGB888)
        return QPixmap.fromImage(qimg)

    def _image_panel(self, cv_img, caption):
        """A dark card with a caption and the image scaled to fit."""
        card = QWidget()
        card.setStyleSheet("background:#181825; border-radius:8px;")
        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(8, 8, 8, 8)
        vbox.setSpacing(6)

        lbl_cap = QLabel(caption)
        lbl_cap.setAlignment(Qt.AlignCenter)
        lbl_cap.setStyleSheet("color:#89b4fa; font-weight:bold; font-size:13px;")
        vbox.addWidget(lbl_cap)

        lbl_img = QLabel()
        lbl_img.setAlignment(Qt.AlignCenter)
        lbl_img.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pixmap = self._cv_to_pixmap(cv_img)
        lbl_img.setPixmap(
            pixmap.scaled(420, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        vbox.addWidget(lbl_img)
        return card

    # ── tabs ──────────────────────────────────────────────────────────────

    def _make_histogram_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(4, 4, 4, 4)
        canvas = HistogramCanvas(7, 3.8)
        ax = canvas.fig.add_subplot(111)
        self._style_ax(ax, "Pixel Intensity Histogram", ylabel="Pixel Count")
        self._plot_hist(ax, self.hist_data)
        canvas.fig.tight_layout()
        lay.addWidget(canvas)
        return w

    def _make_cdf_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(4, 4, 4, 4)
        canvas = HistogramCanvas(7, 3.8)
        ax = canvas.fig.add_subplot(111)
        self._style_ax(ax, "Cumulative Distribution Function (CDF)",
                       ylabel="Cumulative Probability")
        self._plot_cdf(ax, self.hist_data)
        canvas.fig.tight_layout()
        lay.addWidget(canvas)
        return w

    def _make_image_comparison_tab(self):
        """Side-by-side before / after images."""
        w = QWidget()
        w.setStyleSheet(f"background:{self.BG};")
        hbox = QHBoxLayout(w)
        hbox.setContentsMargins(12, 12, 12, 12)
        hbox.setSpacing(14)

        hbox.addWidget(self._image_panel(self.before_image, "⬅  Before Equalization"))

        arrow = QLabel("▶")
        arrow.setStyleSheet("color:#89b4fa; font-size:30px;")
        arrow.setAlignment(Qt.AlignCenter)
        hbox.addWidget(arrow)

        hbox.addWidget(self._image_panel(self.after_image,  "After Equalization  ➡"))
        return w

    def _make_before_after_hist_tab(self):
        """2×2 grid: histograms and CDFs before + after equalization."""
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(4, 4, 4, 4)
        canvas = HistogramCanvas(9, 5)
        axes = canvas.fig.subplots(2, 2)

        before = self.equalization_data['before']
        after  = self.equalization_data['after']

        self._style_ax(axes[0, 0], "Histogram — Before", ylabel="Pixel Count")
        self._plot_hist(axes[0, 0], before)

        self._style_ax(axes[0, 1], "Histogram — After",  ylabel="Pixel Count")
        self._plot_hist(axes[0, 1], after)

        self._style_ax(axes[1, 0], "CDF — Before", ylabel="Cumulative Probability")
        self._plot_cdf(axes[1, 0], before)

        self._style_ax(axes[1, 1], "CDF — After",  ylabel="Cumulative Probability")
        self._plot_cdf(axes[1, 1], after)

        canvas.fig.tight_layout(pad=2.5)
        lay.addWidget(canvas)
        return w