"""
Color Channel Manipulation effects for ComfyUI XWAVE Nodes.
Standalone implementation without external dependencies.
"""

import numpy as np
from PIL import Image


def color_channel_manipulation(image, manipulation_type, choice, factor=None):
    """
    Manipulate the image's color channels (swap, invert, adjust intensity, or create negative).
    
    Args:
        image (Image): PIL Image object to process.
        manipulation_type (str): 'swap', 'invert', 'adjust', or 'negative'.
        choice (str): Specific channel or swap pair (e.g., 'red-green', 'red').
                     Not used for 'negative' type.
        factor (float, optional): Intensity adjustment factor (required for 'adjust').
    
    Returns:
        Image: Processed image with modified color channels.
    """
    if image.mode not in ['RGB', 'RGBA']:
        image = image.convert('RGB')
    elif image.mode == 'RGBA':  # Convert RGBA to RGB by discarding alpha
        image = image.convert('RGB')

    img_array = np.array(image)
    
    if manipulation_type == 'swap':
        if choice == 'red-green':
            # R, G, B -> G, R, B
            img_array = img_array[:, :, [1, 0, 2]]
        elif choice == 'red-blue':
            # R, G, B -> B, G, R
            img_array = img_array[:, :, [2, 1, 0]]
        elif choice == 'green-blue':
            # R, G, B -> R, B, G
            img_array = img_array[:, :, [0, 2, 1]]
    elif manipulation_type == 'invert':
        if choice == 'red':
            img_array[:, :, 0] = 255 - img_array[:, :, 0]
        elif choice == 'green':
            img_array[:, :, 1] = 255 - img_array[:, :, 1]
        elif choice == 'blue':
            img_array[:, :, 2] = 255 - img_array[:, :, 2]
    elif manipulation_type == 'negative':
        img_array = 255 - img_array
    elif manipulation_type == 'adjust':
        if factor is None:
            raise ValueError("Factor is required for adjust manipulation")
        
        # Ensure factor is positive; negative factors would invert and are better handled by 'invert'
        # Clamping to 0 to avoid issues with large negative factors if not strictly positive.
        safe_factor = max(0, factor)

        if choice == 'red':
            img_array[:, :, 0] = np.clip(img_array[:, :, 0] * safe_factor, 0, 255).astype(np.uint8)
        elif choice == 'green':
            img_array[:, :, 1] = np.clip(img_array[:, :, 1] * safe_factor, 0, 255).astype(np.uint8)
        elif choice == 'blue':
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] * safe_factor, 0, 255).astype(np.uint8)

    return Image.fromarray(img_array) 