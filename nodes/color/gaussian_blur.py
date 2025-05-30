"""
Gaussian Blur Node for ComfyUI XWAVE Nodes
Applies Gaussian blur effects to images.
"""

import torch
import numpy as np
from PIL import Image, ImageFilter


class GaussianBlurNode:
    """
    Apply Gaussian blur to images with adjustable radius.
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
    
    def gaussian_blur(self, image, radius=5.0, sigma=None):
        """
        Apply Gaussian blur to an image.
        
        Args:
            image (Image): PIL Image object to process.
            radius (float): Blur radius in pixels (0.1 to 50.0).
            sigma (float, optional): Standard deviation for Gaussian kernel. 
                                    If None, sigma = radius / 3.0 (common approximation).
        
        Returns:
            Image: Blurred image.
        """
        if image.mode not in ['RGB', 'RGBA', 'L']:
            image = image.convert('RGB')
        
        # If sigma is not provided, use the common approximation
        if sigma is None:
            sigma = radius / 3.0
        
        # Ensure minimum values to prevent errors
        radius = max(0.1, radius)
        sigma = max(0.1, sigma)
        
        # Apply Gaussian blur using PIL's ImageFilter
        # PIL's GaussianBlur uses radius parameter
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=radius))
        
        return blurred_image
    
    def process(self, image, radius, sigma):
        """
        Process the image with Gaussian blur effect.
        
        Args:
            image: Input image tensor
            radius: Blur radius in pixels
            sigma: Standard deviation for Gaussian kernel (0 for auto)
        
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
            processed_img = self.gaussian_blur(
                pil_img,
                radius=radius,
                sigma=sigma if sigma > 0 else None
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