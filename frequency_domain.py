import cv2
import numpy as np

def read_image(file_path, max_size=512):
    """Loads an image, resizes it if it's too large, and ensures it is in grayscale."""
    img = cv2.imread(file_path)
    if img is None:
        return None, False
        
    # Shrink large images to fit the screen and make FFT math lightning fast
    h, w = img.shape[:2]
    if max(h, w) > max_size:
        scale = max_size / float(max(h, w))
        new_w, new_h = int(w * scale), int(h * scale)
        # INTER_AREA is the best interpolation method for shrinking images down
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
        
    return gray, True

def _create_distance_matrix(rows, cols):
    """Helper function to create a matrix of distances from the center."""
    crow, ccol = rows // 2, cols // 2
    y, x = np.ogrid[-crow:rows-crow, -ccol:cols-ccol]
    return np.sqrt(x**2 + y**2)

def get_magnitude_spectrum(image):
    """Computes the magnitude spectrum of an image for visualization."""
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    
    # Add 1 to avoid log(0)
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
    
    # Normalize to 0-255 for standard 8-bit display
    magnitude_display = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return cv2.cvtColor(magnitude_display, cv2.COLOR_GRAY2BGR)

def apply_filter(image, filter_type, radius):
    """
    Applies an Ideal Low-Pass (LPF) or High-Pass (HPF) filter.
    Returns the display-ready image and the raw float data for hybrid generation.
    """
    rows, cols = image.shape
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    
    # Create the filter mask
    d_matrix = _create_distance_matrix(rows, cols)
    mask = np.zeros((rows, cols), np.uint8)
    
    if filter_type == 'LPF':
        mask[d_matrix <= radius] = 1
    elif filter_type == 'HPF':
        mask[d_matrix > radius] = 1
        
    # Apply mask and inverse FFT
    fshift_filtered = fshift * mask
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    # Normalize for display
    img_display = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    img_display = cv2.cvtColor(img_display, cv2.COLOR_GRAY2BGR)
    
    return img_display, img_back

def generate_hybrid(img1_float, img2_float):
    """Combines two frequency-filtered float images into a hybrid image."""
    h1, w1 = img1_float.shape[:2]
    h2, w2 = img2_float.shape[:2]
    
    # Ensure images are the exact same size before combining
    # We resize img2 to match img1 using INTER_CUBIC, which is better for float data
    if (h1, w1) != (h2, w2):
        img2_float = cv2.resize(img2_float, (w1, h1), interpolation=cv2.INTER_CUBIC)
        
    # Combine the low frequencies and high frequencies
    hybrid = img1_float + img2_float
    
    # Clip negative values before normalization to prevent inversion artifacts
    hybrid = np.clip(hybrid, 0, None)
    
    # Normalize the final hybrid image to 0-255 for display
    hybrid_display = cv2.normalize(hybrid, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return cv2.cvtColor(hybrid_display, cv2.COLOR_GRAY2BGR)