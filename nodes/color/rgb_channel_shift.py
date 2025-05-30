"""
Rgb Channel Shift Node for ComfyUI XWAVE Nodes
Self-contained implementation with all effects included.
"""

import torch
import numpy as np
from PIL import Image


class RGBChannelShiftNode:
    """
    Apply RGB channel shifting effects for color separation glitches.
    Creates analog video-style color misalignment effects.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "shift_amount": ("INT", {
                    "default": 10,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "direction": (["horizontal", "vertical"],),
                "centered_channel": (["R", "G", "B"],),
                "mode": (["shift", "mirror"],),
            }
        }
    
    return_types = ("IMAGE",)
    function = "process"
    category = "XWAVE/Color"
    
    def rgb_channel_shift(self, image, shift_amount, direction, centered_channel, mode='shift'):
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
        
        # Split into channels
        r, g, b = image.split()
        channels = {'R': r, 'G': g, 'B': b}
        
        # Process each channel
        processed_channels = {}
        for channel_name, channel in channels.items():
            if channel_name == centered_channel.upper()[0]:
                # Keep centered channel unchanged
                processed_channels[channel_name] = channel
                continue
            
            # Convert to numpy array for processing
            channel_array = np.array(channel)
            
            if mode == 'shift':
                # Create shifted channel
                shifted = np.zeros_like(channel_array)
                if direction == 'horizontal':
                    if channel_name == 'R':
                        # Shift right
                        if shift_amount < width:
                            shifted[:, shift_amount:] = channel_array[:, :-shift_amount]
                    else:  # B channel
                        # Shift left
                        if shift_amount < width:
                            shifted[:, :-shift_amount] = channel_array[:, shift_amount:]
                else:  # vertical
                    if channel_name == 'R':
                        # Shift down
                        if shift_amount < height:
                            shifted[shift_amount:, :] = channel_array[:-shift_amount, :]
                    else:  # B channel
                        # Shift up
                        if shift_amount < height:
                            shifted[:-shift_amount, :] = channel_array[shift_amount:, :]
                processed_channels[channel_name] = Image.fromarray(shifted)
            else:  # mirror mode
                # Create mirrored channel
                if direction == 'horizontal':
                    mirrored = np.fliplr(channel_array)
                else:  # vertical
                    mirrored = np.flipud(channel_array)
                processed_channels[channel_name] = Image.fromarray(mirrored)
        
        # Merge channels back together
        result = Image.merge('RGB', (processed_channels['R'], processed_channels['G'], processed_channels['B']))
        return result
    
    def process(self, image, shift_amount, direction, centered_channel, mode):
        """
        Process the image with RGB channel shift effect.
        
        Args:
            image: Input image tensor
            shift_amount: Number of pixels to shift
            direction: Shift direction (horizontal/vertical)
            centered_channel: Which channel to keep centered
            mode: Effect mode (shift/mirror)
        
        Returns:
            tuple: (processed_image_tensor,)
        """
        # Convert from ComfyUI tensor format to PIL Images
        batch_size = image.shape[0]
        result = []
        
        for i in range(batch_size):
            # Convert to PIL Image
            img_array = (image[i].cpu().numpy() * 255).astype(np.uint8)
            pil_img = Image.fromarray(img_array, mode='RGB')
            
            # Apply rgb channel shift effect
            processed_img = self.rgb_channel_shift(
                pil_img,
                shift_amount=shift_amount,
                direction=direction,
                centered_channel=centered_channel,
                mode=mode
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveRGBChannelShift": RGBChannelShiftNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveRGBChannelShift": "XWAVE RGB Channel Shift"
} 