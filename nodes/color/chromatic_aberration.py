"""
Advanced Chromatic Aberration Node for ComfyUI XWAVE Nodes
Create realistic and artistic chromatic aberration effects.
"""

import torch
import numpy as np
from PIL import Image


class ChromaticAberrationNode:
    """
    Apply advanced chromatic aberration effects to images.
    Supports radial, linear, barrel, and custom patterns with various controls.
    """

    def __init__(self):
        pass

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
    
    def apply_displacement(self, channel, disp_x, disp_y, width, height):
        """
        Apply displacement to a channel using bilinear interpolation.
        
        Args:
            channel (ndarray): Channel to displace
            disp_x (ndarray): X displacement
            disp_y (ndarray): Y displacement
            width (int): Image width
            height (int): Image height
        
        Returns:
            ndarray: Displaced channel
        """
        # Create coordinate grids
        y_coords, x_coords = np.mgrid[0:height, 0:width]
        
        # Calculate new coordinates
        new_x = x_coords + disp_x
        new_y = y_coords + disp_y
        
        # Clip coordinates to image bounds
        new_x = np.clip(new_x, 0, width - 1)
        new_y = np.clip(new_y, 0, height - 1)
        
        # Get integer and fractional parts
        x0 = np.floor(new_x).astype(int)
        x1 = np.minimum(x0 + 1, width - 1)
        y0 = np.floor(new_y).astype(int)
        y1 = np.minimum(y0 + 1, height - 1)
        
        # Calculate interpolation weights
        wx = new_x - x0
        wy = new_y - y0
        
        # Bilinear interpolation
        interpolated = (
            channel[y0, x0] * (1 - wx) * (1 - wy) +
            channel[y0, x1] * wx * (1 - wy) +
            channel[y1, x0] * (1 - wx) * wy +
            channel[y1, x1] * wx * wy
        )
        
        return interpolated
    
    def chromatic_aberration(self, image, intensity=5.0, pattern='radial', red_shift_x=0.0, red_shift_y=0.0,
                            blue_shift_x=0.0, blue_shift_y=0.0, center_x=0.5, center_y=0.5,
                            falloff='quadratic', edge_enhancement=0.0, color_boost=1.0, seed=None):
        """
        Apply chromatic aberration effect to simulate lens color fringing.
    
        Args:
            image (Image): PIL Image object to process.
            intensity (float): Overall aberration intensity (0.0 to 50.0).
            pattern (str): Aberration pattern ('radial', 'linear', 'barrel', 'custom').
            red_shift_x (float): Manual red channel X displacement (-20.0 to 20.0).
            red_shift_y (float): Manual red channel Y displacement (-20.0 to 20.0).
            blue_shift_x (float): Manual blue channel X displacement (-20.0 to 20.0).
            blue_shift_y (float): Manual blue channel Y displacement (-20.0 to 20.0).
            center_x (float): Aberration center X position (0.0 to 1.0).
            center_y (float): Aberration center Y position (0.0 to 1.0).
            falloff (str): Distance falloff type ('linear', 'quadratic', 'cubic').
            edge_enhancement (float): Enhance edge contrast (0.0 to 1.0).
            color_boost (float): Boost color saturation (0.5 to 2.0).
            seed (int, optional): Random seed for pattern variations.
    
        Returns:
            Image: Image with chromatic aberration effect applied.
        """
        if image.mode != 'RGB':
            image = image.convert('RGB')
    
        if seed is not None:
            np.random.seed(seed)
    
        img_array = np.array(image, dtype=np.float32)
        height, width, channels = img_array.shape
    
        # Extract color channels
        red_channel = img_array[:, :, 0]
        green_channel = img_array[:, :, 1]
        blue_channel = img_array[:, :, 2]
    
        # Create coordinate grids
        y_coords, x_coords = np.mgrid[0:height, 0:width]
    
        # Normalize coordinates to [-1, 1] range centered on aberration center
        center_x_px = center_x * width
        center_y_px = center_y * height
        x_norm = (x_coords - center_x_px) / (width / 2)
        y_norm = (y_coords - center_y_px) / (height / 2)
    
        # Calculate distance from center
        distance = np.sqrt(x_norm**2 + y_norm**2)
    
        # Apply falloff function
        if falloff == 'linear':
            falloff_factor = distance
        elif falloff == 'cubic':
            falloff_factor = distance**3
        else:  # quadratic (default)
            falloff_factor = distance**2
    
        # Calculate displacement based on pattern
        if pattern == 'radial':
            # Classic radial chromatic aberration
            # Red channel moves outward, blue moves inward
            red_disp_x = x_norm * falloff_factor * intensity * 0.1
            red_disp_y = y_norm * falloff_factor * intensity * 0.1
            blue_disp_x = -x_norm * falloff_factor * intensity * 0.1
            blue_disp_y = -y_norm * falloff_factor * intensity * 0.1
        
        elif pattern == 'linear':
            # Linear aberration (like prism effect)
            red_disp_x = np.full_like(x_coords, intensity * 0.2, dtype=np.float32)
            red_disp_y = np.zeros_like(y_coords, dtype=np.float32)
            blue_disp_x = np.full_like(x_coords, -intensity * 0.2, dtype=np.float32)
            blue_disp_y = np.zeros_like(y_coords, dtype=np.float32)
        
        elif pattern == 'barrel':
            # Barrel distortion-like aberration
            angle = np.arctan2(y_norm, x_norm)
            radial_factor = falloff_factor * intensity * 0.1
            red_disp_x = np.cos(angle) * radial_factor * 1.2
            red_disp_y = np.sin(angle) * radial_factor * 1.2
            blue_disp_x = np.cos(angle) * radial_factor * 0.8
            blue_disp_y = np.sin(angle) * radial_factor * 0.8
        
        else:  # custom
            # Use manual displacement values with some distance modulation
            distance_mod = 1.0 + falloff_factor * 0.5
            red_disp_x = np.full_like(x_coords, red_shift_x * distance_mod, dtype=np.float32)
            red_disp_y = np.full_like(y_coords, red_shift_y * distance_mod, dtype=np.float32)
            blue_disp_x = np.full_like(x_coords, blue_shift_x * distance_mod, dtype=np.float32)
            blue_disp_y = np.full_like(y_coords, blue_shift_y * distance_mod, dtype=np.float32)
    
        # Add manual shifts to pattern-based displacement
        if pattern != 'custom':
            red_disp_x += red_shift_x
            red_disp_y += red_shift_y
            blue_disp_x += blue_shift_x
            blue_disp_y += blue_shift_y
    
        # Apply displacements
        red_displaced = self.apply_displacement(red_channel, red_disp_x, red_disp_y, width, height)
        blue_displaced = self.apply_displacement(blue_channel, blue_disp_x, blue_disp_y, width, height)
    
        # Green channel stays in place (or minimal displacement)
        green_displaced = green_channel.copy()
    
        # Combine channels
        result = np.stack([red_displaced, green_displaced, blue_displaced], axis=2)
    
        # Apply edge enhancement if requested
        if edge_enhancement > 0:
            try:
                from scipy import ndimage
                # Create edge detection kernel
                edge_kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
            
                # Apply edge detection to each channel
                for i in range(3):
                    edges = ndimage.convolve(result[:, :, i], edge_kernel, mode='reflect')
                    result[:, :, i] += edges * edge_enhancement * 0.1
            except ImportError:
                # Skip edge enhancement if scipy is not available
                pass
    
        # Apply color boost
        if color_boost != 1.0:
            # Convert to HSV for saturation boost
            result_uint8 = np.clip(result, 0, 255).astype(np.uint8)
            result_pil = Image.fromarray(result_uint8)
        
            # Simple saturation boost by scaling color channels relative to luminance
            luminance = 0.299 * result[:, :, 0] + 0.587 * result[:, :, 1] + 0.114 * result[:, :, 2]
            for i in range(3):
                # Boost color relative to luminance
                color_diff = result[:, :, i] - luminance
                result[:, :, i] = luminance + color_diff * color_boost
    
        # Ensure values are in valid range
        result = np.clip(result, 0, 255).astype(np.uint8)
    
        return Image.fromarray(result)
    
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
            processed_img = self.chromatic_aberration(
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