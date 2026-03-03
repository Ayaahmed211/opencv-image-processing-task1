import numpy as np

class NoiseMixin:

    # -----------------------------
    # Uniform Noise
    # -----------------------------
    def add_uniform_noise(self, intensity=50):
        if self.original_image is None:
            return None

        img = self.original_image.copy()

        # Generate uniform noise
        noise = np.random.uniform(-intensity, intensity, img.shape)

        # Add noise and clip values
        noisy_img = np.clip(
            img.astype(np.float32) + noise,
            0, 255
        ).astype(np.uint8)

        self.current_image = noisy_img
        return self.get_display_image()

    # -----------------------------
    # Gaussian Noise
    # -----------------------------
    def add_gaussian_noise(self, sigma=25):
        if self.original_image is None:
            return None

        img = self.original_image.copy()

        # Generate Gaussian noise
        noise = np.random.normal(0, sigma, img.shape)

        # Add noise and clip values
        noisy_img = np.clip(
            img.astype(np.float32) + noise,
            0, 255
        ).astype(np.uint8)

        self.current_image = noisy_img
        return self.get_display_image()

    # -----------------------------
    # Salt & Pepper Noise (FIXED)
    # -----------------------------
    def add_salt_pepper_noise(self, noise_ratio=0.05):
        if self.original_image is None:
            return None

        img = self.original_image.copy()

        # Total number of pixels to modify
        if len(img.shape) == 2:  # Grayscale
            h, w = img.shape
            num_pixels = int(noise_ratio * h * w)

            # Salt (white)
            coords = [np.random.randint(0, i, num_pixels // 2) for i in (h, w)]
            img[coords[0], coords[1]] = 255

            # Pepper (black)
            coords = [np.random.randint(0, i, num_pixels // 2) for i in (h, w)]
            img[coords[0], coords[1]] = 0

        else:  # Color image
            h, w, c = img.shape
            num_pixels = int(noise_ratio * h * w)

            # Salt (white pixels)
            coords = [np.random.randint(0, i, num_pixels // 2) for i in (h, w)]
            img[coords[0], coords[1]] = [255, 255, 255]

            # Pepper (black pixels)
            coords = [np.random.randint(0, i, num_pixels // 2) for i in (h, w)]
            img[coords[0], coords[1]] = [0, 0, 0]

        self.current_image = img
        return self.get_display_image()
