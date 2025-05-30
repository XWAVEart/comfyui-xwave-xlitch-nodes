"""
Gaussian Blur Node for ComfyUI XWAVE Nodes
Applies Gaussian blur to images.
"""

import sys
import os
# Add parent directory to path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))


from utils.base_node import XWaveNodeBase
from effects.gaussian_blur import gaussian_blur


class GaussianBlurNode(XWaveNodeBase):
    """
    Apply Gaussian blur to an image for softening or creating depth of field effects.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "radius": ("FLOAT", {
                    "default": 5.0,
                    "min": 0.1,
                    "max": 50.0,
                    "step": 0.1,
                    "display": "slider"
                }),
            },
            "optional": {
                "sigma": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 20.0,
                    "step": 0.1,
                    "display": "slider"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, radius, sigma=0.0):
        """
        Process the image with Gaussian blur.
        
        Args:
            image: Input image tensor
            radius: Blur radius in pixels (0.1 to 50.0)
            sigma: Standard deviation for Gaussian kernel (0 uses radius/3.0)
        
        Returns:
            tuple: (processed_image_tensor,)
        """
        # sigma=0.0 means None will be passed to use default calculation
        sigma_value = None if sigma == 0.0 else sigma
        
        # Process the image batch
        result = self.process_batch(
            image,
            gaussian_blur,
            radius=radius,
            sigma=sigma_value
        )
        
        return (result,)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveGaussianBlur": GaussianBlurNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveGaussianBlur": "XWAVE Gaussian Blur"
} 