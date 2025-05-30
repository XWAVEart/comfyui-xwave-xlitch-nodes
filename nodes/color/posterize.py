"""
Posterize Node for ComfyUI XWAVE Nodes
Reduce color levels with optional dithering.
"""

import torch
import numpy as np
from PIL import Image
import sys
import os

# Add parent directory to path to enable imports of effects
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
from effects.posterize import posterize


class PosterizeNode:
    """
    Reduce the number of colors in an image with optional dithering.
    Supports multiple color spaces and dithering methods.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "levels": ("INT", {
                    "default": 8,
                    "min": 2,
                    "max": 256,
                    "step": 1,
                    "display": "slider"
                }),
                "dither": (["none", "floyd-steinberg", "atkinson", "ordered"],),
                "color_space": (["rgb", "hsv", "lab"],),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, levels, dither, color_space):
        """
        Process the image with posterize effect.
        
        Args:
image: Input image tensor
            levels: Number of color levels per channel (2-256)
            dither: Dithering method
            color_space: Color space for posterization
        
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
            
            # Apply posterize effect
            processed_img = posterize(
                pil_img,
                levels=levels,

                            dither=dither,

                            color_space=color_space
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWavePosterize": PosterizeNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWavePosterize": "XWAVE Posterize"
} 