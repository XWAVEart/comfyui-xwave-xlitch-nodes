"""
Gaussian blur effect for ComfyUI XWAVE Nodes.
Applies various blur effects to images.
"""

from PIL import Image, ImageFilter
import numpy as np


def gaussian_blur(image, radius=5.0, sigma=None):
    """
    Apply Gaussian blur to an image.
    
    Args:
        image (Image): PIL Image object to process.
        radius (float): Blur radius in pixels (0.1 to 50.0).
        sigma (float, optional): Standard deviation for Gaussian kernel. 
                                If None, sigma = radius / 3.0 (common approximation).
    
    Returns:
        Image: Blurred image.
    """
    if image.mode not in ['RGB', 'RGBA', 'L']:
        image = image.convert('RGB')
    
    # If sigma is not provided, use the common approximation
    if sigma is None:
        sigma = radius / 3.0
    
    # Ensure minimum values to prevent errors
    radius = max(0.1, radius)
    sigma = max(0.1, sigma)
    
    # Apply Gaussian blur using PIL's ImageFilter
    # PIL's GaussianBlur uses radius parameter
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=radius))
    
    return blurred_image 