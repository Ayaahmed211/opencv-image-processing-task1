import cv2
import numpy as np

class EdgeMixin:

    # ✅ FIXED VERSION (no dependency on is_gray flag)
    def _get_gray_from_original(self):
        if self.original_image is None:
            return None

        # If already grayscale
        if len(self.original_image.shape) == 2:
            return self.original_image.copy()

        # If color → convert to grayscale
        return cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)

    # ────────────────────────────────────────────────

    def sobel_edge_detection(self):
        if self.original_image is None:
            return None

        gray = self._get_gray_from_original()

        sobel_x = np.array([[-1, 0, 1],
                            [-2, 0, 2],
                            [-1, 0, 1]], dtype=np.float32)

        sobel_y = np.array([[-1, -2, -1],
                            [0,  0,  0],
                            [1,  2,  1]], dtype=np.float32)

        grad_x = cv2.filter2D(gray.astype(np.float32), -1, sobel_x)
        grad_y = cv2.filter2D(gray.astype(np.float32), -1, sobel_y)

        magnitude = np.sqrt(grad_x**2 + grad_y**2)

        self.current_image = np.clip(magnitude, 0, 255).astype(np.uint8)

        return self.get_display_image()

    # ────────────────────────────────────────────────

    def roberts_edge_detection(self):
        if self.original_image is None:
            return None

        gray = self._get_gray_from_original().astype(np.float32)

        roberts_x = np.array([[1, 0],
                              [0, -1]], dtype=np.float32)

        roberts_y = np.array([[0, 1],
                              [-1, 0]], dtype=np.float32)

        grad_x = cv2.filter2D(gray, -1, roberts_x)
        grad_y = cv2.filter2D(gray, -1, roberts_y)

        magnitude = np.sqrt(grad_x**2 + grad_y**2)

        self.current_image = np.clip(magnitude, 0, 255).astype(np.uint8)

        return self.get_display_image()

    # ────────────────────────────────────────────────

    def prewitt_edge_detection(self):
        if self.original_image is None:
            return None

        gray = self._get_gray_from_original()

        prewitt_x = np.array([[-1, 0, 1],
                              [-1, 0, 1],
                              [-1, 0, 1]], dtype=np.float32)

        prewitt_y = np.array([[-1, -1, -1],
                              [ 0,  0,  0],
                              [ 1,  1,  1]], dtype=np.float32)

        grad_x = cv2.filter2D(gray.astype(np.float32), -1, prewitt_x)
        grad_y = cv2.filter2D(gray.astype(np.float32), -1, prewitt_y)

        magnitude = np.sqrt(grad_x**2 + grad_y**2)

        self.current_image = np.clip(magnitude, 0, 255).astype(np.uint8)

        return self.get_display_image()

    # ────────────────────────────────────────────────

    def canny_edge_detection(self, threshold1=150, threshold2=250):
        if self.original_image is None:
            return None

        gray = self._get_gray_from_original()

        self.current_image = cv2.Canny(gray, threshold1, threshold2)

        return self.get_display_image()