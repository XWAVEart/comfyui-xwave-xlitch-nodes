"""
Noise effects for ComfyUI XWAVE Nodes.
Standalone implementation without external dependencies.
"""

import numpy as np
import random
from PIL import Image
from scipy import ndimage


def noise_effect(image, noise_type='film_grain', intensity=0.3, grain_size=1.0, 
                color_variation=0.2, noise_color='#FFFFFF', blend_mode='overlay', 
                pattern='random', seed=None):
    """
    Add various types of noise effects to an image.
    
    Args:
        image (Image): PIL Image object to process.
        noise_type (str): Type of noise ('film_grain', 'digital', 'colored', 'salt_pepper', 'gaussian').
        intensity (float): Overall noise intensity (0.0 to 1.0).
        grain_size (float): Size of noise particles (0.5 to 5.0).
        color_variation (float): Amount of color variation in noise (0.0 to 1.0).
        noise_color (str): Base color for colored noise in hex format.
        blend_mode (str): How to blend noise ('overlay', 'add', 'multiply', 'screen').
        pattern (str): Noise pattern ('random', 'perlin', 'cellular').
        seed (int, optional): Random seed for reproducible results. 0 or None for random.
    
    Returns:
        Image: Image with noise effect applied.
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Handle seed - 0 means random, any other value is used as seed
    if seed is not None and seed != 0:
        np.random.seed(seed)
        random.seed(seed)
    
    img_array = np.array(image, dtype=np.float32)
    height, width, channels = img_array.shape
    
    # Convert hex color to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    base_color = hex_to_rgb(noise_color)
    
    # Generate base noise pattern
    if pattern == 'perlin':
        # Simple Perlin-like noise using multiple octaves
        noise_base = np.zeros((height, width))
        for octave in range(3):
            scale = 0.1 * (2 ** octave) * grain_size
            y_coords, x_coords = np.mgrid[0:height, 0:width]
            noise_octave = np.sin(x_coords * scale) * np.cos(y_coords * scale)
            noise_base += noise_octave / (2 ** octave)
        noise_base = (noise_base + 1) / 2  # Normalize to 0-1
    elif pattern == 'cellular':
        # Cellular automata-like pattern
        noise_base = np.random.random((height, width))
        # Apply cellular automata rules
        for _ in range(2):
            kernel = np.ones((3, 3)) / 9
            noise_base = ndimage.convolve(noise_base, kernel, mode='wrap')
            noise_base = (noise_base > 0.5).astype(float)
    else:  # random
        noise_base = np.random.random((height, width))
    
    # Scale noise by grain size
    if grain_size != 1.0:
        # Resize noise pattern
        scale_factor = 1.0 / grain_size
        small_height = max(1, int(height * scale_factor))
        small_width = max(1, int(width * scale_factor))
        
        # Generate smaller noise and scale up
        if pattern == 'random':
            small_noise = np.random.random((small_height, small_width))
        else:
            small_noise = noise_base[:small_height, :small_width]
        
        # Resize back to original size
        noise_base = ndimage.zoom(small_noise, (height/small_height, width/small_width), order=1)
    
    # Create noise based on type
    if noise_type == 'film_grain':
        # Simulate film grain with luminance-dependent noise
        luminance = 0.299 * img_array[:,:,0] + 0.587 * img_array[:,:,1] + 0.114 * img_array[:,:,2]
        luminance_norm = luminance / 255.0
        
        # More grain in mid-tones, less in shadows and highlights
        grain_mask = 4 * luminance_norm * (1 - luminance_norm)
        
        # Generate colored grain
        noise_r = (noise_base - 0.5) * intensity * grain_mask
        noise_g = (np.random.random((height, width)) - 0.5) * intensity * grain_mask * color_variation
        noise_b = (np.random.random((height, width)) - 0.5) * intensity * grain_mask * color_variation
        
        noise_array = np.stack([noise_r, noise_g, noise_b], axis=2) * 255
        
    elif noise_type == 'digital':
        # Sharp digital noise
        noise_base = (noise_base > (1 - intensity)).astype(float)
        noise_array = np.stack([noise_base] * 3, axis=2) * 255
        
        # Add color variation
        if color_variation > 0:
            for i in range(3):
                color_noise = (np.random.random((height, width)) - 0.5) * color_variation * 255
                noise_array[:,:,i] += color_noise
    
    elif noise_type == 'colored':
        # Colored noise based on base color
        noise_r = (noise_base - 0.5) * intensity * (base_color[0] / 255.0) * 255
        noise_g = (noise_base - 0.5) * intensity * (base_color[1] / 255.0) * 255
        noise_b = (noise_base - 0.5) * intensity * (base_color[2] / 255.0) * 255
        
        # Add color variation
        if color_variation > 0:
            noise_r += (np.random.random((height, width)) - 0.5) * color_variation * 255
            noise_g += (np.random.random((height, width)) - 0.5) * color_variation * 255
            noise_b += (np.random.random((height, width)) - 0.5) * color_variation * 255
        
        noise_array = np.stack([noise_r, noise_g, noise_b], axis=2)
    
    elif noise_type == 'salt_pepper':
        # Salt and pepper noise
        salt_pepper = np.random.random((height, width))
        salt_mask = salt_pepper > (1 - intensity/2)
        pepper_mask = salt_pepper < (intensity/2)
        
        noise_array = np.zeros((height, width, 3))
        noise_array[salt_mask] = 255  # Salt (white)
        noise_array[pepper_mask] = -255  # Pepper (black)
    
    else:  # gaussian
        # Gaussian noise
        noise_r = np.random.normal(0, intensity * 255, (height, width))
        noise_g = np.random.normal(0, intensity * 255 * color_variation, (height, width))
        noise_b = np.random.normal(0, intensity * 255 * color_variation, (height, width))
        
        noise_array = np.stack([noise_r, noise_g, noise_b], axis=2)
    
    # Apply blend mode
    if blend_mode == 'add':
        result = img_array + noise_array
    elif blend_mode == 'multiply':
        noise_norm = (noise_array + 255) / 510  # Normalize to 0-1 range
        result = img_array * noise_norm
    elif blend_mode == 'screen':
        img_norm = img_array / 255.0
        noise_norm = (noise_array + 255) / 510
        result = (1 - (1 - img_norm) * (1 - noise_norm)) * 255
    else:  # overlay (default)
        noise_norm = noise_array / 255.0
        img_norm = img_array / 255.0
        
        result = np.where(
            img_norm < 0.5,
            2 * img_norm * (noise_norm + 0.5),
            1 - 2 * (1 - img_norm) * (0.5 - noise_norm)
        ) * 255
    
    # Ensure values are in valid range
    result = np.clip(result, 0, 255).astype(np.uint8)
    
    return Image.fromarray(result) 