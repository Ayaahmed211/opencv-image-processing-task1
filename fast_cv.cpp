#include <cstdlib>

// extern "C" prevents C++ name mangling so Python can find the exact function name
extern "C" {
    // __declspec(dllexport) makes the function visible in a Windows DLL
    __declspec(dllexport) void apply_uniform_noise(unsigned char* img_data, int width, int height, int channels, int intensity) {
        
        int total_elements = width * height * channels;
        
        // Loop through every single pixel channel (R, G, B, or Grayscale)
        for (int i = 0; i < total_elements; i++) {
            // Generate noise between -intensity and +intensity
            int noise = (rand() % (2 * intensity + 1)) - intensity;
            int new_val = img_data[i] + noise;
            
            // Clamp values to valid 0-255 image range
            if (new_val > 255) new_val = 255;
            if (new_val < 0) new_val = 0;
            
            // Reassign back to memory
            img_data[i] = (unsigned char)new_val;
        }
    }
}