import cv2
import numpy as np

def _create_gaussian_mask(rows, cols, D0, filter_type):
    """Helper function to create a vectorized Gaussian filter mask instantly."""
    crow, ccol = rows / 2, cols / 2
    y, x = np.ogrid[-crow:rows-crow, -ccol:cols-ccol]
    
    # Calculate distance squared from the center
    dist_sq = x**2 + y**2
    
    # Gaussian Low-Pass formula
    mask = np.exp(-dist_sq / (2 * D0**2))
    
    # If High-Pass, invert the mask
    if filter_type == 'HPF':
        mask = 1 - mask
        
    return mask

def get_magnitude_spectrum(image):
    """Computes the magnitude spectrum of an image for visualization."""
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    
    # Add 1 to avoid log(0)
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
    
    # Normalize to 0-255 for standard 8-bit display
    magnitude_display = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return cv2.cvtColor(magnitude_display, cv2.COLOR_GRAY2BGR)

def apply_filter(image, filter_type, D0):
    """
    Applies a Gaussian Low-Pass (LPF) or High-Pass (HPF) filter in the frequency domain.
    Returns the display-ready image and the raw float data for hybrid generation.
    """
    rows, cols = image.shape
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    
    # Create the Gaussian filter mask
    mask = _create_gaussian_mask(rows, cols, D0, filter_type)
        
    # Apply mask and inverse FFT
    fshift_filtered = fshift * mask
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    
    # Get the magnitude
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
        
    # Combine the magnitudes of the low frequencies and high frequencies
    hybrid = np.abs(img1_float) + np.abs(img2_float)
    
    # Normalize the final hybrid image to 0-255 for display
    hybrid_display = cv2.normalize(hybrid, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return cv2.cvtColor(hybrid_display, cv2.COLOR_GRAY2BGR)