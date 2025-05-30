"""
Color Filter Node for ComfyUI XWAVE Nodes
Apply color filters with various blend modes and filter types.
"""

import torch
import numpy as np
from PIL import Image
import math


class ColorFilterNode:
    """
    Apply color filters to images with various blend modes and filter types.
    Supports solid colors, gradients, and custom gradient images.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "filter_type": (["solid", "gradient"], {"default": "solid"}),
                "color": ("STRING", {
                    "default": "#FF0000",
                    "multiline": False,
                    "tooltip": "Primary filter color in hex format (e.g., #FF0000 for red)",
                    "display": "color"  # Hint for UI to show color picker
                }),
                "blend_mode": (["overlay", "multiply", "screen", "soft_light", "hard_light",
                               "color_dodge", "color_burn", "linear_dodge", "linear_burn", 
                               "vivid_light", "normal"], {"default": "overlay"}),
                "opacity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
            },
            "optional": {
                "gradient_color2": ("STRING", {
                    "default": "#0000FF",
                    "multiline": False,
                    "tooltip": "Secondary color for gradient filter in hex format (e.g., #0000FF for blue)",
                    "display": "color"  # Hint for UI to show color picker
                }),
                "gradient_angle": ("INT", {
                    "default": 45,
                    "min": 0,
                    "max": 360,
                    "step": 1,
                    "display": "slider"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_gradient(self, width, height, color1_rgb, color2_rgb, angle):
        """Create a gradient array."""
        # Create coordinate grids
        x = np.arange(width)
        y = np.arange(height)
        X, Y = np.meshgrid(x, y)
        
        # Convert angle to radians
        angle_rad = math.radians(angle)
        
        # Calculate gradient direction
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        
        # Project coordinates onto gradient direction
        proj = (X - width/2) * cos_angle + (Y - height/2) * sin_angle
        
        # Normalize projection to 0-1 range
        proj_min = proj.min()
        proj_max = proj.max()
        if proj_max > proj_min:
            proj_norm = (proj - proj_min) / (proj_max - proj_min)
        else:
            proj_norm = np.zeros_like(proj)
        
        # Create gradient
        gradient = np.zeros((height, width, 3), dtype=np.float32)
        for i in range(3):
            gradient[:, :, i] = (1 - proj_norm) * (color1_rgb[i] / 255.0) + proj_norm * (color2_rgb[i] / 255.0)
        
        return gradient
    
    def apply_blend_mode(self, base, overlay, mode, opacity):
        """Apply blend mode between base and overlay images."""
        if mode == 'normal':
            result = overlay
        elif mode == 'multiply':
            result = base * overlay
        elif mode == 'screen':
            result = 1 - (1 - base) * (1 - overlay)
        elif mode == 'overlay':
            result = np.where(base < 0.5,
                            2 * base * overlay,
                            1 - 2 * (1 - base) * (1 - overlay))
        elif mode == 'soft_light':
            result = np.where(overlay < 0.5,
                            base - (1 - 2 * overlay) * base * (1 - base),
                            base + (2 * overlay - 1) * (np.sqrt(base) - base))
        elif mode == 'hard_light':
            result = np.where(overlay < 0.5,
                            2 * base * overlay,
                            1 - 2 * (1 - base) * (1 - overlay))
        elif mode == 'color_dodge':
            result = np.where(overlay < 1, base / (1 - overlay + 1e-10), 1)
        elif mode == 'color_burn':
            result = np.where(overlay > 0, 1 - (1 - base) / (overlay + 1e-10), 0)
        elif mode == 'linear_dodge':
            result = base + overlay
        elif mode == 'linear_burn':
            result = base + overlay - 1
        elif mode == 'vivid_light':
            result = np.where(overlay < 0.5,
                            1 - (1 - base) / (2 * overlay + 1e-10),
                            base / (2 * (1 - overlay) + 1e-10))
        else:
            result = overlay
        
        # Clamp result
        result = np.clip(result, 0, 1)
        
        # Apply opacity
        final_result = base * (1 - opacity) + result * opacity
        return np.clip(final_result, 0, 1)
    
    def color_filter(self, image, filter_type='solid', color='#FF0000', blend_mode='overlay', opacity=0.5,
                     gradient_color2='#0000FF', gradient_angle=45):
        """
        Apply a color filter to an image with various blend modes.
    
        Args:
            image (Image): PIL Image object to process.
            filter_type (str): Type of filter ('solid', 'gradient').
            color (str): Primary filter color in hex format (e.g., '#FF0000').
            blend_mode (str): Blend mode to use.
            opacity (float): Filter opacity (0.0-1.0).
            gradient_color2 (str): Secondary color for gradient filter in hex format.
            gradient_angle (int): Gradient rotation angle in degrees (0-360).
    
        Returns:
            Image: Processed image with color filter applied.
        """
        if image.mode != 'RGB':
            image = image.convert('RGB')
    
        # Convert image to numpy array
        img_array = np.array(image, dtype=np.float32) / 255.0
    
        # Convert hex colors to RGB
        color_rgb = self.hex_to_rgb(color)
    
        # Create filter based on type
        if filter_type == 'solid':
            filter_array = np.full_like(img_array, np.array(color_rgb, dtype=np.float32) / 255.0)
        else:  # gradient
            gradient_color2_rgb = self.hex_to_rgb(gradient_color2)
            filter_array = self.create_gradient(
                image.width, image.height,
                color_rgb, gradient_color2_rgb,
                gradient_angle
            )
    
        # Apply blend mode
        result = self.apply_blend_mode(img_array, filter_array, blend_mode, opacity)
    
        # Convert back to uint8 and create image
        result = (result * 255.0).astype(np.uint8)
        return Image.fromarray(result)
    
    def process(self, image, filter_type, color, blend_mode, opacity,
                gradient_color2="#0000FF", gradient_angle=45):
        """
        Process the image with color filter effect.
        
        Args:
            image: Input image tensor
            filter_type: Type of filter (solid, gradient)
            color: Primary filter color in hex format
            blend_mode: Blend mode to use
            opacity: Filter opacity (0.0-1.0)
            gradient_color2: Secondary color for gradient in hex format
            gradient_angle: Gradient rotation angle in degrees
        
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
            
            # Apply color filter effect
            processed_img = self.color_filter(
                pil_img,
                filter_type=filter_type,
                color=color,
                blend_mode=blend_mode,
                opacity=opacity,
                gradient_color2=gradient_color2,
                gradient_angle=gradient_angle
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveColorFilter": ColorFilterNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveColorFilter": "XWAVE Color Filter"
} 