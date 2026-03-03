import cv2
import numpy as np

class BaseProcessor:
    def __init__(self):
        self.original_image = None
        self.current_image = None
        self.image_path = None
        self.is_gray = False
        
    def _resize_if_needed(self, img, max_size, force_even):
        """Internal helper to shrink massive images and fix odd dimensions."""
        if img is None: return None
        h, w = img.shape[:2]
        
        # 1. Shrink if too large
        if max_size and max(h, w) > max_size:
            scale = max_size / float(max(h, w))
            new_w, new_h = int(w * scale), int(h * scale)
            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            h, w = img.shape[:2] # Update sizes
            
        # 2. Force Even Dimensions (Required for FFT)
        if force_even and (h % 2 != 0 or w % 2 != 0):
            new_h = h - (h % 2)
            new_w = w - (w % 2)
            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
            
        return img

   

    def load_image(self, image_path, max_size=None, force_even=False):
        """
        SMART LOADER: Automatically detects if the image is color or grayscale.
        Even detects "fake" grayscale images saved as RGB.
        """
        self.image_path = image_path
        
        # Load unchanged to preserve original file properties if possible
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            return None, False
            
        # Drop alpha channel if it's a 4-channel PNG
        if len(img.shape) == 3 and img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # The "Fake Grayscale" Check
        if len(img.shape) == 3:
            b, g, r = cv2.split(img)
            # If all channels are identical, it's actually a grayscale image!
            if np.array_equal(b, g) and np.array_equal(g, r):
                img = b # Discard the redundant channels
                self.is_gray = True
            else:
                self.is_gray = False
        else:
            self.is_gray = True

        # Resize if necessary
        img = self._resize_if_needed(img, max_size, force_even)
            
        self.original_image = img
        self.current_image = self.original_image.copy()
        
        return self.current_image, True


    
    @staticmethod
    def load_frequency_image(image_path, max_size=512):
        """
        Stateless read function strictly for Frequency Domain.
        Reads as grayscale, resizes, and ensures even dimensions without 
        overwriting the Spatial Tab's current/original image variables.
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None, False
            
        h, w = img.shape[:2]
        if max_size and max(h, w) > max_size:
            scale = max_size / float(max(h, w))
            new_w, new_h = int(w * scale), int(h * scale)
            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            h, w = img.shape[:2]
            
        if h % 2 != 0 or w % 2 != 0:
            new_h = h - (h % 2)
            new_w = w - (w % 2)
            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
            
        return img, True

    def restore_original(self):
        if self.original_image is None:
            return None
        
        if len(self.original_image.shape) == 2:
            self.is_gray = True
        else:
            self.is_gray = False
        
        self.current_image = self.original_image.copy()
        return self.get_display_image()
    
    def convert_to_grayscale(self):
        if self.original_image is None:
            return None
        
        if self.is_gray:
            return self.get_display_image()
        
        if len(self.original_image.shape) == 3:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            self.current_image = gray
            self.is_gray = True
        else:
            self.current_image = self.original_image.copy()
            self.is_gray = True
        
        return self.get_display_image()
    
    # FIXED FUNCTION
    def get_display_image(self):
        if self.current_image is None:
            return None
        
        return self.current_image.copy()