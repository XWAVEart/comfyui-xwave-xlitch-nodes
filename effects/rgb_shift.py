"""
RGB Channel Shift effects for ComfyUI XWAVE Nodes.
Standalone implementation without external dependencies.
"""

import numpy as np
from PIL import Image


def split_and_shift_channels(image, shift_amount, direction, centered_channel, mode='shift'):
    """
    Split an RGB image into its channels, shift or mirror the channels based on mode,
    and recombine into a new image.

    Args:
        image (Image): PIL Image object in RGB mode.
        shift_amount (int): Number of pixels to shift the non-centered channels (for shift mode).
        direction (str): 'horizontal' or 'vertical' for shift mode (ignored in mirror mode).
        centered_channel (str): 'R', 'G', or 'B' to specify which channel stays centered/unchanged.
        mode (str): 'shift' to shift channels away or 'mirror' to mirror channels.

    Returns:
        Image: New PIL Image with shifted/mirrored channels.
    """
    # Convert to RGB mode if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
        
    # Convert image to numpy array
    pixels = np.array(image)
    
    # Extract channels
    R = pixels[:, :, 0]
    G = pixels[:, :, 1]
    B = pixels[:, :, 2]
    
    # Map the centered_channel string to the appropriate channel variable
    channel_dict = {'R': R, 'G': G, 'B': B}
    centered_channel = centered_channel.upper()[0]  # Convert 'red' to 'R', etc.
    
    if mode == 'shift':
        # Define shifts: centered channel stays at 0, others shift by -X and +X
        if centered_channel == 'R':
            shifts = {'R': 0, 'G': -shift_amount, 'B': shift_amount}
        elif centered_channel == 'G':
            shifts = {'R': -shift_amount, 'G': 0, 'B': shift_amount}
        elif centered_channel == 'B':
            shifts = {'R': -shift_amount, 'G': shift_amount, 'B': 0}
        
        # Apply shifts to each channel
        R_processed = shift_channel(R, shifts['R'], direction)
        G_processed = shift_channel(G, shifts['G'], direction)
        B_processed = shift_channel(B, shifts['B'], direction)
    
    elif mode == 'mirror':
        # Always mirror horizontally and vertically regardless of direction parameter
        # Define which channels to mirror
        if centered_channel == 'R':
            # R stays the same, G mirrors horizontally, B mirrors vertically
            R_processed = R.copy()
            G_processed = mirror_channel(G, 'horizontal')
            B_processed = mirror_channel(B, 'vertical')
        elif centered_channel == 'G':
            # G stays the same, R mirrors horizontally, B mirrors vertically
            R_processed = mirror_channel(R, 'horizontal')
            G_processed = G.copy()
            B_processed = mirror_channel(B, 'vertical')
        elif centered_channel == 'B':
            # B stays the same, R mirrors horizontally, G mirrors vertically
            R_processed = mirror_channel(R, 'horizontal')
            G_processed = mirror_channel(G, 'vertical')
            B_processed = B.copy()
    else:
        raise ValueError("Mode must be 'shift' or 'mirror'.")

    # Combine processed channels
    processed_pixels = np.stack([R_processed, G_processed, B_processed], axis=2)

    # Convert back to PIL Image
    processed_image = Image.fromarray(processed_pixels)

    return processed_image


def shift_channel(channel, shift, direction):
    """
    Shift a 2D array (channel) in a specified direction.

    Args:
        channel (numpy.ndarray): The channel to shift.
        shift (int): Number of pixels to shift (can be negative).
        direction (str): 'horizontal' or 'vertical'.

    Returns:
        numpy.ndarray: The shifted channel.
    """
    height, width = channel.shape
    shifted = np.zeros_like(channel)
    
    if direction == 'horizontal':
        if shift < 0:
            shifted[:, :width+shift] = channel[:, -shift:]
        elif shift > 0:
            shifted[:, shift:] = channel[:, :width-shift]
        else:
            shifted = channel.copy()
    elif direction == 'vertical':
        if shift < 0:
            shifted[:height+shift, :] = channel[-shift:, :]
        elif shift > 0:
            shifted[shift:, :] = channel[:height-shift, :]
        else:
            shifted = channel.copy()
    else:
        raise ValueError("Direction must be 'horizontal' or 'vertical'.")

    return shifted


def mirror_channel(channel, direction):
    """
    Mirror a 2D array (channel) horizontally or vertically.

    Args:
        channel (numpy.ndarray): The channel to mirror.
        direction (str): 'horizontal' or 'vertical'.

    Returns:
        numpy.ndarray: The mirrored channel.
    """
    if direction == 'horizontal':
        return np.fliplr(channel)
    elif direction == 'vertical':
        return np.flipud(channel)
    else:
        raise ValueError("Direction must be 'horizontal' or 'vertical'.") 