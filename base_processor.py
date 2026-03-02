import cv2

class BaseProcessor:
    def __init__(self):
        self.original_image = None
        self.current_image = None
        self.image_path = None
        self.is_gray = False
    
    def read_image(self, image_path):
        self.image_path = image_path
        self.original_image = cv2.imread(image_path)
        if self.original_image is None:
            return None, False
        self.current_image = self.original_image.copy()
        self.is_gray = False
        return self.current_image, True
    
    def read_grayscale(self, image_path):
        self.image_path = image_path
        self.original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if self.original_image is None:
            return None, False
        self.current_image = self.original_image.copy()
        self.is_gray = True
        return self.current_image, True   # ✅ Removed GRAY2BGR conversion
    
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
    
    # ✅ FIXED FUNCTION
    def get_display_image(self):
        if self.current_image is None:
            return None
        
        return self.current_image.copy()