"""
Color Channel Manipulation Node for ComfyUI XWAVE Nodes
Manipulate image color channels through various operations.
"""

import torch
import numpy as np
from PIL import Image
import sys
import os

# Add parent directory to path to enable imports of effects
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
from effects.color_channel import color_channel_manipulation


class ColorChannelManipulationNode:
    """
    Manipulate image color channels with swap, invert, adjust, and negative operations.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "operation": (["swap", "invert", "adjust", "negative"],),
                "intensity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "slider"
                }),
            },
            "optional": {
                "channels": ("STRING", {
                    "default": "RG",
                    "multiline": False
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, operation, intensity, channels="RG"):
        """
        Process the image with color channel manipulation effect.
        
        Args:
image: Input image tensor
            operation: Type of manipulation (swap, invert, adjust, negative)
            intensity: Adjustment factor for certain operations
            channels: Channels to manipulate (e.g., "RG" for red-green, "R" for red)
        
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
            
            # Apply color channel manipulation effect
            processed_img = color_channel_manipulation(
                pil_img,
                manipulation_type=operation,

                            choice=mapped_channels,

                            factor=factor
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveColorChannelManipulation": ColorChannelManipulationNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveColorChannelManipulation": "XWAVE Color Channel Manipulation"
} 