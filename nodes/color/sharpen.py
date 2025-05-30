"""
Sharpen Effect Node for ComfyUI XWAVE Nodes
Various sharpening methods for image enhancement.
"""

import sys
import os
# Add parent directory to path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))


from utils.base_node import XWaveNodeBase
from effects.sharpen import sharpen_effect


class SharpenEffectNode(XWaveNodeBase):
    """
    Apply various sharpening effects to enhance image detail and clarity.
    Supports multiple sharpening algorithms and custom kernels.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "method": (["unsharp_mask", "high_pass", "edge_enhance", "custom"],),
                "intensity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "radius": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "slider"
                }),
            },
            "optional": {
                "threshold": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 255,
                    "step": 1
                }),
                "edge_enhancement": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "high_pass_radius": ("FLOAT", {
                    "default": 3.0,
                    "min": 1.0,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "custom_kernel": (["laplacian", "sobel", "prewitt"],),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, method, intensity, radius, threshold=0,
                edge_enhancement=0.0, high_pass_radius=3.0, custom_kernel="laplacian"):
        """
        Process the image with sharpening effect.
        
        Args:
            image: Input image tensor
            method: Sharpening method ('unsharp_mask', 'high_pass', 'edge_enhance', 'custom')
            intensity: Sharpening intensity/amount (0.0 to 5.0)
            radius: Radius for blur operations in unsharp mask (0.1 to 10.0)
            threshold: Threshold for unsharp mask (0 to 255)
            edge_enhancement: Additional edge enhancement (0.0 to 2.0)
            high_pass_radius: Radius for high-pass filter (1.0 to 10.0)
            custom_kernel: Custom convolution kernel type
        
        Returns:
            tuple: (processed_image_tensor,)
        """
        # Process the image batch
        result = self.process_batch(
            image,
            sharpen_effect,
            method=method,
            intensity=intensity,
            radius=radius,
            threshold=threshold,
            edge_enhancement=edge_enhancement,
            high_pass_radius=high_pass_radius,
            custom_kernel=custom_kernel
        )
        
        return (result,)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveSharpenEffect": SharpenEffectNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveSharpenEffect": "XWAVE Sharpen Effect"
} 