"""
JPEG Artifacts Node for ComfyUI XWAVE Nodes
Simulates JPEG compression artifacts for glitch effects.
"""

import torch
import numpy as np
from PIL import Image
import sys
import os

# Add parent directory to path to enable imports of effects
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
from effects.jpeg_artifacts import jpeg_artifacts


class JPEGArtifactsNode:
    """
    Simulate JPEG compression artifacts by repeatedly compressing the image at low quality.
    Perfect for creating glitchy, lo-fi effects.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "intensity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, intensity):
        """
        Process the image with jpeg artifacts effect.
        
        Args:
image: Input image tensor
            intensity: Intensity of artifacts (0.0 to 1.0)
                      0 = minimal artifacts, 1 = extreme artifacts
        
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
            
            # Apply jpeg artifacts effect
            processed_img = jpeg_artifacts(
                pil_img,
                intensity=intensity
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveJPEGArtifacts": JPEGArtifactsNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveJPEGArtifacts": "XWAVE JPEG Artifacts"
} 