"""
Color Shift Expansion Node for ComfyUI XWAVE Nodes
Apply color shift expansion effects with customizable patterns and themes.
"""

import sys
import os
# Add parent directory to path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))


from utils.base_node import XWaveNodeBase
from effects.color_shift_expansion import color_shift_expansion


class ColorShiftExpansionNode(XWaveNodeBase):
    """
    Apply color shift expansion effects to images.
    Expands colored shapes from various points with customizable patterns and themes.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "num_points": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 50,
                    "step": 1,
                    "display": "slider"
                }),
                "shift_amount": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 20,
                    "step": 1,
                    "display": "slider"
                }),
                "expansion_type": (["square", "circle", "diamond"],),
                "mode": (["xtreme", "subtle", "mono"],),
                "saturation_boost": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "value_boost": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "pattern_type": (["random", "grid", "edges"],),
                "color_theme": (["full-spectrum", "warm", "cool", "pastel"],),
                "decay_factor": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2**32 - 1,
                    "step": 1
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, num_points, shift_amount, expansion_type, mode,
                saturation_boost, value_boost, pattern_type, color_theme,
                decay_factor, seed):
        """
        Process the image with color shift expansion effect.
        
        Args:
            image: Input image tensor
            num_points: Number of expansion points
            shift_amount: Amount of color shifting (0-20)
            expansion_type: Shape of expansion ('square', 'circle', 'diamond')
            mode: Mode of color application ('xtreme', 'subtle', 'mono')
            saturation_boost: Amount to boost saturation (0.0-1.0)
            value_boost: Amount to boost brightness (0.0-1.0)
            pattern_type: Pattern of color point placement ('random', 'grid', 'edges')
            color_theme: Color theme to use ('full-spectrum', 'warm', 'cool', 'pastel')
            decay_factor: How quickly effect fades with distance (0.0-1.0)
            seed: Seed for random number generation
        
        Returns:
            tuple: (processed_image_tensor,)
        """
        # Process the image batch
        result = self.process_batch(
            image,
            color_shift_expansion,
            num_points=num_points,
            shift_amount=shift_amount,
            expansion_type=expansion_type,
            mode=mode,
            saturation_boost=saturation_boost,
            value_boost=value_boost,
            pattern_type=pattern_type,
            color_theme=color_theme,
            decay_factor=decay_factor,
            seed=seed
        )
        
        return (result,)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveColorShiftExpansion": ColorShiftExpansionNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveColorShiftExpansion": "XWAVE Color Shift Expansion"
} 