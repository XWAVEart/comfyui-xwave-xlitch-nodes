"""
Histogram Glitch Node for ComfyUI XWAVE Nodes
Apply different histogram-based transformations to each color channel.
"""

import torch
import numpy as np
from PIL import Image
import sys
import os

# Add parent directory to path to enable imports of effects
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
from effects.histogram import histogram_glitch


class HistogramGlitchNode:
    """
    Apply different transformations to each color channel based on histogram analysis.
    Supports solarize, log, gamma, and normal transformations.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "r_mode": (["solarize", "log", "gamma", "normal"], {"default": "solarize"}),
                "g_mode": (["solarize", "log", "gamma", "normal"], {"default": "log"}),
                "b_mode": (["solarize", "log", "gamma", "normal"], {"default": "gamma"}),
                "r_freq": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "g_freq": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "b_freq": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "r_phase": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 6.28,
                    "step": 0.01,
                    "display": "slider"
                }),
                "g_phase": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 6.28,
                    "step": 0.01,
                    "display": "slider"
                }),
                "b_phase": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 6.28,
                    "step": 0.01,
                    "display": "slider"
                }),
                "gamma_val": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.1,
                    "max": 3.0,
                    "step": 0.01,
                    "display": "slider"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, r_mode, g_mode, b_mode, r_freq, g_freq, b_freq,
                r_phase, g_phase, b_phase, gamma_val):
        """
        Process the image with histogram glitch effect.
        
        Args:
image: Input image tensor
            r_mode: Transformation for red channel
            g_mode: Transformation for green channel
            b_mode: Transformation for blue channel
            r_freq: Frequency for red channel solarization
            g_freq: Frequency for green channel solarization
            b_freq: Frequency for blue channel solarization
            r_phase: Phase for red channel solarization
            g_phase: Phase for green channel solarization
            b_phase: Phase for blue channel solarization
            gamma_val: Gamma value for gamma transformation
        
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
            
            # Apply histogram glitch effect
            processed_img = histogram_glitch(
                pil_img,
                r_mode=r_mode,

                            g_mode=g_mode,

                            b_mode=b_mode,

                            r_freq=r_freq,

                            r_phase=r_phase,

                            g_freq=g_freq,

                            g_phase=g_phase,

                            b_freq=b_freq,

                            b_phase=b_phase,

                            gamma_val=gamma_val
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveHistogramGlitch": HistogramGlitchNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveHistogramGlitch": "XWAVE Histogram Glitch"
} 