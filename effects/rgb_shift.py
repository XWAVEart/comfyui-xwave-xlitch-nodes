"""
RGB Channel Shift effects for ComfyUI XWAVE Nodes.
Standalone implementation without external dependencies.
"""

import numpy as np
from PIL import Image


def split_and_shift_channels(image, shift_amount, direction, centered_channel, mode='shift'):
    """
    Split an RGB image into its channels, shift or mirror the channels based on mode,
    and recombine into a new image. Memory efficient implementation.

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
    
    # Get image dimensions
    width, height = image.size
    
    # Create new image for result
    result = Image.new('RGB', (width, height))
    
    # Process each channel separately to minimize memory usage
    for channel_idx, channel_name in enumerate(['R', 'G', 'B']):
        # Extract single channel
        channel_data = np.array(image)[:, :, channel_idx]
        
        if channel_name == centered_channel.upper()[0]:
            # Keep centered channel unchanged
            result.putchannel(channel_data, channel_idx)
            continue
        
        if mode == 'shift':
            # Create shifted channel
            shifted = np.zeros_like(channel_data)
            if direction == 'horizontal':
                if channel_name == 'R':
                    # Shift right
                    shifted[:, shift_amount:] = channel_data[:, :-shift_amount]
                else:  # B channel
                    # Shift left
                    shifted[:, :-shift_amount] = channel_data[:, shift_amount:]
            else:  # vertical
                if channel_name == 'R':
                    # Shift down
                    shifted[shift_amount:, :] = channel_data[:-shift_amount, :]
                else:  # B channel
                    # Shift up
                    shifted[:-shift_amount, :] = channel_data[shift_amount:, :]
        else:  # mirror mode
            # Create mirrored channel
            if direction == 'horizontal':
                shifted = np.fliplr(channel_data)
            else:  # vertical
                shifted = np.flipud(channel_data)
        
        # Put processed channel into result
        result.putchannel(shifted, channel_idx)
    
    return result


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