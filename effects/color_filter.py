"""
Color filter effects for ComfyUI XWAVE Nodes.
Apply color filters with various blend modes and filter types.
"""

import numpy as np
from PIL import Image


def hex_to_rgb(hex_color):
    """
    Convert hex color string to RGB tuple.
    
    Args:
        hex_color (str): Hex color string (e.g., '#FF0000')
    
    Returns:
        tuple: RGB color tuple (0-255)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def create_gradient(width, height, start_color, end_color, angle=0):
    """
    Create a gradient image from start to end color.
    
    Args:
        width (int): Width of the gradient
        height (int): Height of the gradient
        start_color (tuple): RGB start color (0-255)
        end_color (tuple): RGB end color (0-255)
        angle (float): Gradient angle in degrees (0-360)
    
    Returns:
        ndarray: Gradient image array
    """
    # Create coordinate grids
    y_coords, x_coords = np.mgrid[0:height, 0:width]
    
    # Convert angle to radians
    angle_rad = np.radians(angle)
    
    # Normalize coordinates to [-1, 1] range
    x_norm = (x_coords - width / 2) / (width / 2)
    y_norm = (y_coords - height / 2) / (height / 2)
    
    # Rotate coordinates
    x_rot = x_norm * np.cos(angle_rad) - y_norm * np.sin(angle_rad)
    
    # Create gradient values from -1 to 1
    gradient_values = x_rot
    
    # Normalize to [0, 1] range
    gradient_values = (gradient_values + 1) / 2
    gradient_values = np.clip(gradient_values, 0, 1)
    
    # Convert colors to numpy arrays
    start_color = np.array(start_color, dtype=np.float32) / 255.0
    end_color = np.array(end_color, dtype=np.float32) / 255.0
    
    # Create gradient for each channel
    gradient = np.zeros((height, width, 3), dtype=np.float32)
    for i in range(3):
        gradient[:, :, i] = (
            gradient_values * start_color[i] + 
            (1 - gradient_values) * end_color[i]
        )
    
    return gradient


def apply_blend_mode(base, blend, mode, opacity=1.0):
    """
    Apply blend mode to two images.
    
    Args:
        base (ndarray): Base image array (0-1)
        blend (ndarray): Blend image array (0-1)
        mode (str): Blend mode
        opacity (float): Blend opacity (0-1)
    
    Returns:
        ndarray: Blended image array
    """
    if mode == 'overlay':
        # Original overlay blend mode
        result = np.where(
            base < 0.5,
            2 * base * blend,
            1 - 2 * (1 - base) * (1 - blend)
        )
    elif mode == 'soft_light':
        # Original soft light blend mode
        result = np.where(
            blend <= 0.5,
            base - (1 - 2 * blend) * base * (1 - base),
            base + (2 * blend - 1) * (
                np.where(base <= 0.25, 
                        ((16 * base - 12) * base + 4) * base,
                        np.sqrt(base)) - base
            )
        )
    else:
        # Additional blend modes from our implementation
        if mode == 'normal':
            result = blend
        elif mode == 'multiply':
            result = base * blend
        elif mode == 'screen':
            result = 1 - (1 - base) * (1 - blend)
        elif mode == 'hard_light':
            mask = blend > 0.5
            result = np.where(mask,
                             1 - 2 * (1 - base) * (1 - blend),
                             2 * base * blend)
        elif mode == 'color_dodge':
            result = np.minimum(1, base / (1 - blend + 1e-6))
        elif mode == 'color_burn':
            result = 1 - np.minimum(1, (1 - base) / (blend + 1e-6))
        elif mode == 'linear_dodge':
            result = np.minimum(1, base + blend)
        elif mode == 'linear_burn':
            result = np.maximum(0, base + blend - 1)
        elif mode == 'vivid_light':
            mask = blend > 0.5
            result = np.where(mask,
                             np.minimum(1, base / (2 * (1 - blend) + 1e-6)),
                             1 - np.minimum(1, (1 - base) / (2 * blend + 1e-6)))
        else:  # default to normal
            result = blend
    
    # Apply opacity
    result = base * (1 - opacity) + result * opacity
    return np.clip(result, 0, 1)


def color_filter(image, filter_type='solid', color='#FF0000', blend_mode='overlay', opacity=0.5,
                gradient_color2='#0000FF', gradient_angle=0, custom_gradient=None):
    """
    Apply a color filter to an image with various blend modes.
    
    Args:
        image (Image): PIL Image object to process.
        filter_type (str): Type of filter ('solid', 'gradient', 'custom').
        color (str): Primary filter color in hex format (e.g., '#FF0000').
        blend_mode (str): Blend mode to use.
        opacity (float): Filter opacity (0.0-1.0).
        gradient_color2 (str): Secondary color for gradient filter in hex format.
        gradient_angle (float): Gradient rotation angle in degrees (0-360).
        custom_gradient (Image): Custom gradient image for 'custom' filter type.
    
    Returns:
        Image: Processed image with color filter applied.
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert image to numpy array
    img_array = np.array(image, dtype=np.float32) / 255.0
    
    # Convert hex colors to RGB
    color_rgb = hex_to_rgb(color)
    
    # Create filter based on type
    if filter_type == 'solid':
        filter_array = np.full_like(img_array, np.array(color_rgb, dtype=np.float32) / 255.0)
    elif filter_type == 'gradient':
        gradient_color2_rgb = hex_to_rgb(gradient_color2)
        filter_array = create_gradient(
            image.width, image.height,
            color_rgb, gradient_color2_rgb,
            gradient_angle
        )
    else:  # custom gradient
        if custom_gradient is None:
            raise ValueError("Custom gradient image is required for 'custom' filter type")
        
        # Convert custom gradient to RGB and resize
        if custom_gradient.mode != 'RGB':
            custom_gradient = custom_gradient.convert('RGB')
        custom_gradient = custom_gradient.resize((image.width, image.height), Image.Resampling.LANCZOS)
        filter_array = np.array(custom_gradient, dtype=np.float32) / 255.0
    
    # Apply blend mode
    result = apply_blend_mode(img_array, filter_array, blend_mode, opacity)
    
    # Convert back to uint8 and create image
    result = (result * 255.0).astype(np.uint8)
    return Image.fromarray(result) 