"""
Histogram-based transformation effects for ComfyUI XWAVE Nodes.
Standalone implementation without external dependencies.
"""

import numpy as np
from PIL import Image


def histogram_glitch(image, r_mode='solarize', g_mode='log', b_mode='gamma', 
                     r_freq=1.0, r_phase=0.0, g_freq=1.0, g_phase=0.0, 
                     b_freq=1.0, b_phase=0.0, gamma_val=0.5):
    """
    Apply different transformations to each color channel based on its histogram.
    
    Args:
        image (PIL.Image): Input image.
        r_mode (str): Transformation for red channel ('solarize', 'log', 'gamma', 'normal').
        g_mode (str): Transformation for green channel ('solarize', 'log', 'gamma', 'normal').
        b_mode (str): Transformation for blue channel ('solarize', 'log', 'gamma', 'normal').
        r_freq (float): Frequency for red channel solarization (0.1-10.0).
        r_phase (float): Phase for red channel solarization (0.0-6.28).
        g_freq (float): Frequency for green channel solarization (0.1-10.0).
        g_phase (float): Phase for green channel solarization (0.0-6.28).
        b_freq (float): Frequency for blue channel solarization (0.1-10.0).
        b_phase (float): Phase for blue channel solarization (0.0-6.28).
        gamma_val (float): Gamma value for gamma transformation (0.1-3.0).
    
    Returns:
        PIL.Image: Processed image with transformed color channels.
    """
    # Convert to RGB mode if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert PIL image to numpy array
    img_array = np.array(image)
    
    # Normalize the image data to 0-1 range
    img_float = img_array.astype(np.float32) / 255.0
    
    # Define helper function to select transformation
    def get_transform(mode, freq, phase, gamma):
        if mode == 'solarize':
            return lambda x: solarize(x, freq, phase)
        elif mode == 'log':
            return log_transform
        elif mode == 'gamma':
            return lambda x: gamma_transform(x, gamma)
        else:  # 'normal'
            return lambda x: x
    
    # Get transform functions for each channel
    r_transform = get_transform(r_mode, r_freq, r_phase, gamma_val)
    g_transform = get_transform(g_mode, g_freq, g_phase, gamma_val)
    b_transform = get_transform(b_mode, b_freq, b_phase, gamma_val)
    
    # Apply transforms to each channel
    img_float[:, :, 0] = r_transform(img_float[:, :, 0])
    img_float[:, :, 1] = g_transform(img_float[:, :, 1])
    img_float[:, :, 2] = b_transform(img_float[:, :, 2])
    
    # Convert back to 0-255 range, clip values, and convert back to uint8
    img_array = np.clip(img_float * 255.0, 0, 255).astype(np.uint8)
    
    # Convert back to PIL Image
    return Image.fromarray(img_array)


def solarize(x, freq=1, phase=0):
    """
    Apply a sine-based solarization transformation to a pixel value.

    Args:
        x (int or np.ndarray): Pixel value (0-1.0) or array of pixel values.
        freq (float): Frequency of the sine wave (controls inversion frequency).
        phase (float): Phase shift of the sine wave (shifts the inversion point).

    Returns:
        int or np.ndarray: Transformed pixel value(s) (0-1.0).
    """
    return 0.5 + 0.5 * np.sin(freq * np.pi * x + phase)


def log_transform(x):
    """
    Apply a logarithmic transformation to compress the dynamic range.

    Args:
        x (int or np.ndarray): Pixel value (0-1.0) or array of pixel values.

    Returns:
        int or np.ndarray: Transformed pixel value(s) (0-1.0).
    """
    return np.log(1 + x) / np.log(2)  # Normalize to approximately 0-1 range


def gamma_transform(x, gamma):
    """
    Apply a power-law (gamma) transformation to adjust brightness/contrast.

    Args:
        x (int or np.ndarray): Pixel value (0-1.0) or array of pixel values.
        gamma (float): Gamma value (e.g., <1 brightens, >1 darkens).

    Returns:
        int or np.ndarray: Transformed pixel value(s) (0-1.0).
    """
    # Handle both single values and arrays
    return np.power(x, gamma) 