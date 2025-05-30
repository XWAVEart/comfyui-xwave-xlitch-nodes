"""
Gaussian Blur Node for ComfyUI XWAVE Nodes
Applies Gaussian blur to images.
"""

import torch
import numpy as np
from PIL import Image
import sys
import os

# Add parent directory to path to enable imports of effects
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
from effects.gaussian_blur import gaussian_blur


class GaussianBlurNode:
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
        Process the image with gaussian blur effect.
        
        Args:
image: Input image tensor
            radius: Blur radius in pixels (0.1 to 50.0)
            sigma: Standard deviation for Gaussian kernel (0 uses radius/3.0)
        
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
            
            # Apply gaussian blur effect
            processed_img = gaussian_blur(
                pil_img,
                radius=radius,

                            sigma=sigma_value
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveGaussianBlur": GaussianBlurNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveGaussianBlur": "XWAVE Gaussian Blur"
} 