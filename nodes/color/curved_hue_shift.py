"""
Curved hue shift node for ComfyUI XWAVE Nodes.
Apply non-linear hue transformations using exponential curves.
"""

import sys
import os
# Add parent directory to path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))


from utils.base_node import XWaveNodeBase
from effects.curved_hue_shift import curved_hue_shift


class CurvedHueShiftNode(XWaveNodeBase):
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
        Process the image with curved hue shift.
        
        Args:
            image: Input image tensor
            curve_value: Curve value from 1 to 360, controlling the shift curve
            shift_amount: Total shift amount in degrees
            
        Returns:
            Processed image tensor
        """
        result = self.process_batch(image, curved_hue_shift, curve_value=curve_value, shift_amount=shift_amount)
        return (result,)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveCurvedHueShift": CurvedHueShiftNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveCurvedHueShift": "XWAVE Curved Hue Shift"
} 