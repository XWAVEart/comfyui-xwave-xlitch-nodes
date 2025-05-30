"""
RGB Channel Shift Node for ComfyUI XWAVE Nodes
Split and shift RGB channels for chromatic aberration effects.
"""

import sys
import os
# Add parent directory to path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))


from utils.base_node import XWaveNodeBase
from effects.rgb_shift import split_and_shift_channels


class RGBChannelShiftNode(XWaveNodeBase):
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
        Process the image with RGB channel shift effect.
        
        Args:
            image: Input image tensor
            mode: 'shift' to shift channels or 'mirror' to mirror them
            shift_amount: Number of pixels to shift (ignored in mirror mode)
            direction: Direction of shift ('horizontal' or 'vertical')
            centered_channel: Which channel stays centered ('R', 'G', or 'B')
        
        Returns:
            tuple: (processed_image_tensor,)
        """
        # Process the image batch
        result = self.process_batch(
            image,
            split_and_shift_channels,
            shift_amount=shift_amount,
            direction=direction,
            centered_channel=centered_channel,
            mode=mode
        )
        
        return (result,)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveRGBChannelShift": RGBChannelShiftNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveRGBChannelShift": "XWAVE RGB Channel Shift"
} 