
Self-contained implementation with all effects included.
"""

Histogram Glitch Node for ComfyUI XWAVE Nodes
Apply different histogram-based transformations to each color channel.
"""

import torch
import numpy as np
from PIL import Image


class HistogramGlitchNode:
    """
    Apply different transformations to each color channel based on histogram analysis.
    Supports solarize, log, gamma, and normal transformations.
    """

    def __init__(self):
        pass

    
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
    
    
        def histogram_glitch(image, r_mode='solarize', g_mode='log', b_mode='gamma', 
                         r_freq=1.0, r_phase=0.0, g_freq=1.0, g_phase=0.0, 
                         b_freq=1.0, b_phase=0.0, gamma_val=0.5):
        """
        Apply different transformations to each color channel based on its histogram.
    
        Args:
            image (PIL.Image): Input image.
            r_mode (str): Transformation for red channel ('solarize', 'log', 'gamma', 'normal').
            g_mode (str): Transformation for green channel ('solarize', 'log', 'gamma', 'normal').
            b_mode (str): Transformation for blue channel ('solarize', 'log', 'gamma', 'normal').
            r_freq (float): Frequency for red channel solarization (0.1-10.0).
            r_phase (float): Phase for red channel solarization (0.0-6.28).
            g_freq (float): Frequency for green channel solarization (0.1-10.0).
            g_phase (float): Phase for green channel solarization (0.0-6.28).
            b_freq (float): Frequency for blue channel solarization (0.1-10.0).
            b_phase (float): Phase for blue channel solarization (0.0-6.28).
            gamma_val (float): Gamma value for gamma transformation (0.1-3.0).
    
        Returns:
            PIL.Image: Processed image with transformed color channels.
        """
        # Convert to RGB mode if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
    
        # Convert PIL image to numpy array
        img_array = np.array(image)
    
        # Normalize the image data to 0-1 range
        img_float = img_array.astype(np.float32) / 255.0
    
        # Define helper FUNCTION to select transformation
        def get_transform(mode, freq, phase, gamma):
            if mode == 'solarize':
                return lambda x: solarize(x, freq, phase)
            elif mode == 'log':
                return log_transform
            elif mode == 'gamma':
                return lambda x: gamma_transform(x, gamma)
            else:  # 'normal'
                return lambda x: x
    
        # Get transform functions for each channel
        r_transform = get_transform(r_mode, r_freq, r_phase, gamma_val)
        g_transform = get_transform(g_mode, g_freq, g_phase, gamma_val)
        b_transform = get_transform(b_mode, b_freq, b_phase, gamma_val)
    
        # Apply transforms to each channel
        img_float[:, :, 0] = r_transform(img_float[:, :, 0])
        img_float[:, :, 1] = g_transform(img_float[:, :, 1])
        img_float[:, :, 2] = b_transform(img_float[:, :, 2])
    
        # Convert back to 0-255 range, clip values, and convert back to uint8
        img_array = np.clip(img_float * 255.0, 0, 255).astype(np.uint8)
    
        # Convert back to PIL Image
        return Image.fromarray(img_array)


    def solarize(x, freq=1, phase=0):
        """
        Apply a sine-based solarization transformation to a pixel value.

        Args:
            x (int or np.ndarray): Pixel value (0-1.0) or array of pixel values.
            freq (float): Frequency of the sine wave (controls inversion frequency).
            phase (float): Phase shift of the sine wave (shifts the inversion point).

        Returns:
            int or np.ndarray: Transformed pixel value(s) (0-1.0).
        """
        return 0.5 + 0.5 * np.sin(freq * np.pi * x + phase)


    def log_transform(x):
        """
        Apply a logarithmic transformation to compress the dynamic range.

        Args:
            x (int or np.ndarray): Pixel value (0-1.0) or array of pixel values.

        Returns:
            int or np.ndarray: Transformed pixel value(s) (0-1.0).
        """
        return np.log(1 + x) / np.log(2)  # Normalize to approximately 0-1 range


    def gamma_transform(x, gamma):
        """
        Apply a power-law (gamma) transformation to adjust brightness/contrast.

        Args:
            x (int or np.ndarray): Pixel value (0-1.0) or array of pixel values.
            gamma (float): Gamma value (e.g., <1 brightens, >1 darkens).

        Returns:
            int or np.ndarray: Transformed pixel value(s) (0-1.0).
        """
        # Handle both single values and arrays
        return np.power(x, gamma) 
    
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
            processed_img = self.histogram_glitch(
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