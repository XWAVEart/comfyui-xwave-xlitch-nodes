"""
JPEG artifacts effect for ComfyUI XWAVE Nodes.
Simulates JPEG compression artifacts for glitch effects.
"""

from PIL import Image
import numpy as np
from io import BytesIO


def simulate_jpeg_artifacts(image, intensity):
    """
    Simulate JPEG compression artifacts by repeatedly compressing the image at low quality.

    Args:
        image (PIL.Image): The original image to process.
        intensity (float): A value between 0 and 1 controlling the intensity of the effect.
                           0 for minimal artifacts, 1 for extreme artifacts.

    Returns:
        PIL.Image: The image with simulated JPEG artifacts.
    """
    if not 0 <= intensity <= 1:
        raise ValueError("Intensity must be between 0 and 1.")

    # Map intensity to number of iterations and quality
    # More extreme - up to 30 iterations
    iterations = int(1 + 29 * intensity)  # 1 to 30 iterations
    # Allow quality to go down to 1
    quality = int(90 - 89 * intensity)    # 90 to 1 quality

    # Convert to RGB mode if the image has an alpha channel or is in a different mode
    if image.mode != 'RGB':
        # Create a white background for RGBA images
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            # Paste the image on the background using the alpha channel as mask
            background.paste(image, mask=image.split()[3])
            current_image = background
        else:
            current_image = image.convert('RGB')
    else:
        current_image = image.copy()

    for _ in range(iterations):
        # Save the image to a BytesIO object with the specified quality
        buffer = BytesIO()
        current_image.save(buffer, format="JPEG", quality=quality)
        # Reload the image from the buffer
        buffer.seek(0)
        current_image = Image.open(buffer)
        current_image.load()  # Make sure the image data is loaded

    return current_image 