import cv2
import numpy as np

class FilterMixin:
    def apply_average_filter(self, kernel_size=3):
        if self.original_image is None:
            return None
        if kernel_size % 2 == 0: kernel_size += 1
        img = self.original_image.copy()
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size**2)
        filtered = cv2.filter2D(img, -1, kernel)
        self.current_image = filtered
        return self.get_display_image()
    
    def apply_gaussian_filter(self, kernel_size=3, sigma=1):
        if self.original_image is None:
            return None
        if kernel_size % 2 == 0: kernel_size += 1
        img = self.original_image.copy()
        filtered = cv2.GaussianBlur(img, (kernel_size, kernel_size), sigma)
        self.current_image = filtered
        return self.get_display_image()
    
    def apply_median_filter(self, kernel_size=3):
        if self.original_image is None:
            return None
        if kernel_size % 2 == 0: kernel_size += 1
        img = self.original_image.copy()
        filtered = cv2.medianBlur(img, kernel_size)
        self.current_image = filtered
        return self.get_display_image()