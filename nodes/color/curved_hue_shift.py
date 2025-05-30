"""
Curved hue shift node for ComfyUI XWAVE Nodes.
Apply non-linear hue transformations using exponential curves.
"""

from ..base import XWaveNodeBase
from ...effects.curved_hue_shift import curved_hue_shift


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
        return (self.apply_effect(curved_hue_shift, image, curve_value=curve_value, shift_amount=shift_amount),)


NODE_CLASS_MAPPINGS = {
    "CurvedHueShiftNode": "XWAVE Curved Hue Shift"
} 