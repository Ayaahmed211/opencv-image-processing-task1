# import numpy as np

# class NoiseMixin:
#     def add_uniform_noise(self, intensity=50):
#         if self.original_image is None:
#             return None
#         img = self.original_image.copy()
#         noise = np.random.uniform(-intensity, intensity, img.shape)
#         noisy_img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
#         self.current_image = noisy_img
#         return self.get_display_image()
    
#     def add_gaussian_noise(self, sigma=25):
#         if self.original_image is None:
#             return None
#         img = self.original_image.copy()
#         noise = np.random.normal(0, sigma, img.shape)
#         noisy_img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
#         self.current_image = noisy_img
#         return self.get_display_image()
    
#     def add_salt_pepper_noise(self, noise_ratio=0.05):
#         if self.original_image is None:
#             return None
#         img = self.original_image.copy()
#         if len(img.shape) == 2:
#             h, w = img.shape
#             num_salt = int(noise_ratio * h * w / 2)
#             if num_salt > 0:
#                 salt_coords = [np.random.randint(0, i, num_salt) for i in [h, w]]
#                 img[salt_coords[0], salt_coords[1]] = 255
#             num_pepper = int(noise_ratio * h * w / 2)
#             if num_pepper > 0:
#                 pepper_coords = [np.random.randint(0, i, num_pepper) for i in [h, w]]
#                 img[pepper_coords[0], pepper_coords[1]] = 0
#         else:
#             h, w, c = img.shape
#             num_salt = int(noise_ratio * h * w * c / 2)
#             if num_salt > 0:
#                 salt_coords = [np.random.randint(0, i, num_salt) for i in [h, w, c]]
#                 img[salt_coords[0], salt_coords[1], salt_coords[2]] = 255
#             num_pepper = int(noise_ratio * h * w * c / 2)
#             if num_pepper > 0:
#                 pepper_coords = [np.random.randint(0, i, num_pepper) for i in [h, w, c]]
#                 img[pepper_coords[0], pepper_coords[1], pepper_coords[2]] = 0
        
#         self.current_image = img
#         return self.get_display_image()
    



import numpy as np
import ctypes
import os

# 1. Load the compiled C++ DLL
dll_path = os.path.join(os.path.dirname(__file__), 'fast_cv.dll')
fast_cv = ctypes.CDLL(dll_path)

# 2. Define the exact argument types the C++ function expects
fast_cv.apply_uniform_noise.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),  # img_data (pointer to unsigned char)
    ctypes.c_int,                    # width
    ctypes.c_int,                    # height
    ctypes.c_int,                    # channels
    ctypes.c_int                     # intensity
]

class NoiseMixin:
    def add_uniform_noise(self, intensity=50):
        if self.original_image is None: 
            return None
            
        # Create a copy so we don't overwrite the original
        img = self.original_image.copy()
        
        # Ensure the numpy array is stored as a continuous block in C-memory
        img = np.ascontiguousarray(img, dtype=np.uint8)
        
        # Get image dimensions
        height, width = img.shape[:2]
        channels = img.shape[2] if len(img.shape) == 3 else 1
        
        # Get the raw C pointer to the numpy array's memory
        img_ptr = img.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
        
        # Call the blazing fast C++ function!
        # It modifies the 'img' memory directly in-place.
        fast_cv.apply_uniform_noise(img_ptr, width, height, channels, intensity)
        
        self.current_image = img
        return self.get_display_image()
        
    # ... keep your other noise functions below ...
    
    def add_gaussian_noise(self, sigma=25):
        if self.original_image is None:
            return None
        img = self.original_image.copy()
        noise = np.random.normal(0, sigma, img.shape)
        noisy_img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        self.current_image = noisy_img
        return self.get_display_image()
    
    def add_salt_pepper_noise(self, noise_ratio=0.05):
        if self.original_image is None:
            return None
        img = self.original_image.copy()
        if len(img.shape) == 2:
            h, w = img.shape
            num_salt = int(noise_ratio * h * w / 2)
            if num_salt > 0:
                salt_coords = [np.random.randint(0, i, num_salt) for i in [h, w]]
                img[salt_coords[0], salt_coords[1]] = 255
            num_pepper = int(noise_ratio * h * w / 2)
            if num_pepper > 0:
                pepper_coords = [np.random.randint(0, i, num_pepper) for i in [h, w]]
                img[pepper_coords[0], pepper_coords[1]] = 0
        else:
            h, w, c = img.shape
            num_salt = int(noise_ratio * h * w * c / 2)
            if num_salt > 0:
                salt_coords = [np.random.randint(0, i, num_salt) for i in [h, w, c]]
                img[salt_coords[0], salt_coords[1], salt_coords[2]] = 255
            num_pepper = int(noise_ratio * h * w * c / 2)
            if num_pepper > 0:
                pepper_coords = [np.random.randint(0, i, num_pepper) for i in [h, w, c]]
                img[pepper_coords[0], pepper_coords[1], pepper_coords[2]] = 0
        
        self.current_image = img
        return self.get_display_image()