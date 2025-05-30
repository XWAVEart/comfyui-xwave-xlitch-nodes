"""
Posterize Node for ComfyUI XWAVE Nodes
Reduce color levels with optional dithering.
"""

import sys
import os
# Add parent directory to path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))


from utils.base_node import XWaveNodeBase
from effects.posterize import posterize


class PosterizeNode(XWaveNodeBase):
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
        # Process the image batch
        result = self.process_batch(
            image,
            posterize,
            levels=levels,
            dither=dither,
            color_space=color_space
        )
        
        return (result,)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWavePosterize": PosterizeNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWavePosterize": "XWAVE Posterize"
} 