import cv2
import numpy as np

class HistogramMixin:
    def compute_histogram_data(self):
        if self.current_image is None: return None
        img = self.current_image
        result = {}

        if self.is_gray or len(img.shape) == 2:
            gray = img if len(img.shape) == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
            cdf  = np.cumsum(hist) / gray.size
            result['gray'] = {'hist': hist, 'cdf': cdf, 'label': 'Grayscale', 'color': '#555555'}
        else:
            channels = {'b': (0, '#2979FF'), 'g': (1, '#00C853'), 'r': (2, '#FF1744')}
            for name, (idx, color) in channels.items():
                hist = cv2.calcHist([img], [idx], None, [256], [0, 256]).flatten()
                cdf  = np.cumsum(hist) / (img.shape[0] * img.shape[1])
                result[name] = {'hist': hist, 'cdf': cdf, 'label': name.upper(), 'color': color}
        return result

    def apply_histogram_equalization(self):
        if self.original_image is None: return None, None
        before_data = self.compute_histogram_data()

        if self.is_gray or len(self.original_image.shape) == 2:
            gray = self.original_image if len(self.original_image.shape) == 2 else cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            self.current_image = cv2.equalizeHist(gray)
            self.is_gray = True
        else:
            ycrcb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2YCrCb)
            ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
            self.current_image = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
            self.is_gray = False

        after_data = self.compute_histogram_data()
        return self.get_display_image(), {'before': before_data, 'after': after_data}

    def apply_normalization(self, new_min=0, new_max=255):
        if self.original_image is None: return None
        img = self.original_image.astype(np.float32)

        if self.is_gray or len(img.shape) == 2:
            i_min, i_max = img.min(), img.max()
            if i_max == i_min:
                normalized = np.zeros_like(img)
            else:
                normalized = (img - i_min) / (i_max - i_min) * (new_max - new_min) + new_min
            self.current_image = normalized.astype(np.uint8)
            self.is_gray = True
        else:
            normalized = np.zeros_like(img)
            for c in range(img.shape[2]):
                ch = img[:, :, c]
                i_min, i_max = ch.min(), ch.max()
                if i_max == i_min:
                    normalized[:, :, c] = 0
                else:
                    normalized[:, :, c] = (ch - i_min) / (i_max - i_min) * (new_max - new_min) + new_min
            self.current_image = normalized.astype(np.uint8)
            self.is_gray = False

        return self.get_display_image()