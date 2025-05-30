"""
RGB Channel Shift Node for ComfyUI XWAVE Nodes
Split and shift RGB channels for chromatic aberration effects.
"""

import torch
import numpy as np
from PIL import Image
import sys
import os

# Add parent directory to path to enable imports of effects
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
from effects.rgb_shift import rgb_channel_shift


class RGBChannelShiftNode:
    """
    Split RGB channels and shift or mirror them for artistic chromatic effects.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mode": (["shift", "mirror"],),
                "shift_amount": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "direction": (["horizontal", "vertical"],),
                "centered_channel": (["R", "G", "B"],),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, mode, shift_amount, direction, centered_channel):
        """
        Process the image with rgb channel shift effect.
        
        Args:
image: Input image tensor
            mode: 'shift' to shift channels or 'mirror' to mirror them
            shift_amount: Number of pixels to shift (ignored in mirror mode)
            direction: Direction of shift ('horizontal' or 'vertical')
            centered_channel: Which channel stays centered ('R', 'G', or 'B')
        
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
            processed_img = rgb_channel_shift(
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