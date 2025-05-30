"""
Advanced Chromatic Aberration Node for ComfyUI XWAVE Nodes
Create realistic and artistic chromatic aberration effects.
"""

import torch
import numpy as np
from PIL import Image
import sys
import os

# Add parent directory to path to enable imports of effects
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
from effects.chromatic_aberration import chromatic_aberration


class ChromaticAberrationNode:
    """
    Apply advanced chromatic aberration effects to images.
    Supports radial, linear, barrel, and custom patterns with various controls.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "intensity": ("FLOAT", {
                    "default": 5.0,
                    "min": 0.0,
                    "max": 50.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "pattern": (["radial", "linear", "barrel", "custom"],),
                "red_shift_x": ("FLOAT", {
                    "default": 0.0,
                    "min": -20.0,
                    "max": 20.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "red_shift_y": ("FLOAT", {
                    "default": 0.0,
                    "min": -20.0,
                    "max": 20.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "blue_shift_x": ("FLOAT", {
                    "default": 0.0,
                    "min": -20.0,
                    "max": 20.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "blue_shift_y": ("FLOAT", {
                    "default": 0.0,
                    "min": -20.0,
                    "max": 20.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "center_x": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "center_y": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "falloff": (["linear", "quadratic", "cubic"],),
                "edge_enhancement": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "color_boost": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 4294967295,
                    "step": 1
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, intensity, pattern, red_shift_x, red_shift_y,
                blue_shift_x, blue_shift_y, center_x, center_y, falloff,
                edge_enhancement, color_boost, seed):
        """
        Process the image with chromatic aberration effect.
        
        Args:
            image: Input image tensor
            intensity: Overall aberration intensity
            pattern: Aberration pattern
            red_shift_x: Red channel X displacement
            red_shift_y: Red channel Y displacement
            blue_shift_x: Blue channel X displacement
            blue_shift_y: Blue channel Y displacement
            center_x: Aberration center X position
            center_y: Aberration center Y position
            falloff: Distance falloff type
            edge_enhancement: Edge contrast enhancement
            color_boost: Color saturation boost
            seed: Random seed for pattern variations
        
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
            
            # Apply chromatic aberration effect
            processed_img = chromatic_aberration(
                pil_img,
                intensity=intensity,
                pattern=pattern,
                red_shift_x=red_shift_x,
                red_shift_y=red_shift_y,
                blue_shift_x=blue_shift_x,
                blue_shift_y=blue_shift_y,
                center_x=center_x,
                center_y=center_y,
                falloff=falloff,
                edge_enhancement=edge_enhancement,
                color_boost=color_boost,
                seed=seed if seed > 0 else None
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveChromaticAberration": ChromaticAberrationNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveChromaticAberration": "XWAVE Chromatic Aberration"
} 