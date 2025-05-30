"""
Curved hue shift node for ComfyUI XWAVE Nodes.
Apply non-linear hue transformations using exponential curves.
"""

import torch
import numpy as np
from PIL import Image
import sys
import os

# Add parent directory to path to enable imports of effects
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
from effects.curved_hue_shift import curved_hue_shift


class CurvedHueShiftNode:
    """Apply curved hue shift effects using exponential curves."""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "curve_value": ("FLOAT", {
                    "default": 180.0,
                    "min": 1.0,
                    "max": 360.0,
                    "step": 1.0,
                    "display": "slider"
                }),
                "shift_amount": ("FLOAT", {
                    "default": 30.0,
                    "min": -180.0,
                    "max": 180.0,
                    "step": 1.0,
                    "display": "slider"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, curve_value, shift_amount):
        """
        Process the image with curved hue shift effect.
        
        Args:
image: Input image tensor
            curve_value: Curve value from 1 to 360, controlling the shift curve
            shift_amount: Total shift amount in degrees
        
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
            
            # Apply curved hue shift effect
            processed_img = curved_hue_shift(
                pil_img,
                curve_value=curve_value,
                 shift_amount=shift_amount
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveCurvedHueShift": CurvedHueShiftNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveCurvedHueShift": "XWAVE Curved Hue Shift"
} 