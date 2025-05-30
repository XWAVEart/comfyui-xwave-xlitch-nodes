"""
Noise Effect Node for ComfyUI XWAVE Nodes
Adds various types of noise effects to images.
"""

import torch
import numpy as np
from PIL import Image
import sys
import os

# Add parent directory to path to enable imports of effects
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
from effects.noise import noise_effect


class NoiseEffectNode:
    """
    Add various types of noise effects to an image.
    Supports film grain, digital noise, colored noise, salt & pepper, and gaussian noise.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "noise_type": (["film_grain", "digital", "colored", "salt_pepper", "gaussian"],),
                "intensity": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "grain_size": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 5.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "color_variation": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "blend_mode": (["overlay", "add", "multiply", "screen"],),
                "pattern": (["random", "perlin", "cellular"],),
            },
            "optional": {
                "noise_color": ("STRING", {
                    "default": "#FFFFFF",
                    "multiline": False
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 4294967295
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, noise_type, intensity, grain_size, color_variation, 
                blend_mode, pattern, noise_color="#FFFFFF", seed=0):
        """
        Process the image with noise effect effect.
        
        Args:
image: Input image tensor
            noise_type: Type of noise to apply
            intensity: Overall noise intensity (0.0 to 1.0)
            grain_size: Size of noise particles (0.5 to 5.0)
            color_variation: Amount of color variation in noise (0.0 to 1.0)
            blend_mode: How to blend noise with image
            pattern: Noise pattern type
            noise_color: Base color for colored noise in hex format
            seed: Random seed (0 for random)
        
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
            
            # Apply noise effect effect
            processed_img = noise_effect(
                pil_img,
                noise_type=noise_type,

                            intensity=intensity,

                            grain_size=grain_size,

                            color_variation=color_variation,

                            noise_color=noise_color,

                            blend_mode=blend_mode,

                            pattern=pattern,

                            seed=seed
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveNoiseEffect": NoiseEffectNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveNoiseEffect": "XWAVE Noise Effect"
} 