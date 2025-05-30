"""
Sharpen Node for ComfyUI XWAVE Nodes
Self-contained implementation with all effects included.
"""

import torch
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage


class SharpenNode:
    """
    Apply various sharpening effects to enhance image details.
    Supports unsharp mask, high-pass, edge enhancement, and custom kernels.
    """

    def __init__(self):
        pass

    
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
                    "step": 0.01,
                    "display": "slider"
                }),
                "radius": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "threshold": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "display": "slider"
                }),
                "edge_enhancement": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "high_pass_radius": ("FLOAT", {
                    "default": 3.0,
                    "min": 1.0,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "slider"
                }),
                "custom_kernel": (["laplacian", "sobel", "prewitt", "simple"],),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def sharpen_effect(self, image, method='unsharp_mask', intensity=1.0, radius=1.0, threshold=0,
                       edge_enhancement=0.0, high_pass_radius=3.0, custom_kernel=None):
        """
        Apply various sharpening effects to an image.
        
        Args:
            image (Image): PIL Image object to process.
            method (str): Sharpening method ('unsharp_mask', 'high_pass', 'edge_enhance', 'custom').
            intensity (float): Sharpening intensity/amount (0.0 to 5.0).
            radius (float): Radius for blur operations in unsharp mask (0.1 to 10.0).
            threshold (int): Threshold for unsharp mask (0 to 255).
            edge_enhancement (float): Additional edge enhancement (0.0 to 2.0).
            high_pass_radius (float): Radius for high-pass filter (1.0 to 10.0).
            custom_kernel (str): Custom convolution kernel type ('laplacian', 'sobel', 'prewitt').
        
        Returns:
            Image: Sharpened image.
        """
        if image.mode not in ['RGB', 'RGBA', 'L']:
            image = image.convert('RGB')
        
        # Ensure parameters are in valid ranges
        intensity = max(0.0, min(5.0, intensity))
        radius = max(0.1, min(10.0, radius))
        threshold = max(0, min(255, threshold))
        edge_enhancement = max(0.0, min(2.0, edge_enhancement))
        high_pass_radius = max(1.0, min(10.0, high_pass_radius))
        
        img_array = np.array(image, dtype=np.float32)
        
        if method == 'unsharp_mask':
            # Classic unsharp mask sharpening
            # 1. Create blurred version
            blurred = image.filter(ImageFilter.GaussianBlur(radius=radius))
            blurred_array = np.array(blurred, dtype=np.float32)
            
            # 2. Calculate difference (mask)
            mask = img_array - blurred_array
            
            # 3. Apply threshold if specified
            if threshold > 0:
                # Only sharpen where the difference exceeds threshold
                if len(mask.shape) == 3:  # Color image
                    mask_magnitude = np.sqrt(np.sum(mask**2, axis=2, keepdims=True))
                else:  # Grayscale
                    mask_magnitude = np.abs(mask).reshape(mask.shape[0], mask.shape[1], 1)
                threshold_mask = mask_magnitude > threshold
                mask = mask * threshold_mask
            
            # 4. Add scaled mask back to original
            result = img_array + mask * intensity
            
        elif method == 'high_pass':
            # High-pass filter sharpening
            # Create a strong blur and subtract from original
            heavily_blurred = image.filter(ImageFilter.GaussianBlur(radius=high_pass_radius))
            heavily_blurred_array = np.array(heavily_blurred, dtype=np.float32)
            
            # High-pass = original - low-pass
            high_pass = img_array - heavily_blurred_array
            
            # Add high-pass back to original with intensity scaling
            result = img_array + high_pass * intensity
            
        elif method == 'edge_enhance':
            # Use PIL's built-in edge enhancement as base
            if intensity <= 1.0:
                # Use smooth edge enhancement for subtle effects
                enhanced = image.filter(ImageFilter.EDGE_ENHANCE)
            else:
                # Use more aggressive edge enhancement
                enhanced = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            
            enhanced_array = np.array(enhanced, dtype=np.float32)
            
            # Blend between original and enhanced based on intensity
            blend_factor = min(1.0, intensity)
            result = img_array * (1 - blend_factor) + enhanced_array * blend_factor
            
            # If intensity > 1.0, apply additional sharpening
            if intensity > 1.0:
                extra_intensity = intensity - 1.0
                # Apply unsharp mask for additional sharpening
                blurred = Image.fromarray(np.clip(result, 0, 255).astype(np.uint8)).filter(
                    ImageFilter.GaussianBlur(radius=1.0)
                )
                blurred_array = np.array(blurred, dtype=np.float32)
                mask = result - blurred_array
                result = result + mask * extra_intensity
        
        elif method == 'custom':
            # Custom convolution kernel sharpening
            if custom_kernel == 'laplacian':
                # Laplacian kernel for edge detection/sharpening
                kernel = np.array([
                    [0, -1, 0],
                    [-1, 4, -1],
                    [0, -1, 0]
                ], dtype=np.float32)
            elif custom_kernel == 'sobel':
                # Sobel-based sharpening (combine X and Y)
                sobel_x = np.array([
                    [-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]
                ], dtype=np.float32)
                sobel_y = np.array([
                    [-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]
                ], dtype=np.float32)
                # Combine Sobel X and Y for omnidirectional edge detection
                kernel = sobel_x + sobel_y
            elif custom_kernel == 'prewitt':
                # Prewitt operator
                prewitt_x = np.array([
                    [-1, 0, 1],
                    [-1, 0, 1],
                    [-1, 0, 1]
                ], dtype=np.float32)
                prewitt_y = np.array([
                    [-1, -1, -1],
                    [0, 0, 0],
                    [1, 1, 1]
                ], dtype=np.float32)
                kernel = prewitt_x + prewitt_y
            else:  # Default to a simple sharpening kernel
                kernel = np.array([
                    [0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]
                ], dtype=np.float32)
            
            # Apply convolution to each channel
            if len(img_array.shape) == 3:  # Color image
                result = np.zeros_like(img_array)
                for i in range(img_array.shape[2]):
                    convolved = ndimage.convolve(img_array[:, :, i], kernel, mode='reflect')
                    result[:, :, i] = img_array[:, :, i] + convolved * intensity
            else:  # Grayscale
                convolved = ndimage.convolve(img_array, kernel, mode='reflect')
                result = img_array + convolved * intensity
        
        else:
            # Fallback to simple sharpening
            result = img_array
        
        # Apply additional edge enhancement if requested
        if edge_enhancement > 0:
            # Use Laplacian for edge detection
            edge_kernel = np.array([
                [0, -1, 0],
                [-1, 4, -1],
                [0, -1, 0]
            ], dtype=np.float32)
            
            if len(result.shape) == 3:  # Color image
                for i in range(result.shape[2]):
                    edges = ndimage.convolve(result[:, :, i], edge_kernel, mode='reflect')
                    result[:, :, i] += edges * edge_enhancement
            else:  # Grayscale
                edges = ndimage.convolve(result, edge_kernel, mode='reflect')
                result += edges * edge_enhancement
        
        # Ensure values are in valid range
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result)
    
    def process(self, image, method, intensity, radius, threshold,
                edge_enhancement, high_pass_radius, custom_kernel):
        """
        Process the image with sharpening effect.
        
        Args:
            image: Input image tensor
            method: Sharpening method to use
            intensity: Sharpening intensity/amount
            radius: Radius for blur operations in unsharp mask
            threshold: Threshold for unsharp mask
            edge_enhancement: Additional edge enhancement
            high_pass_radius: Radius for high-pass filter
            custom_kernel: Custom convolution kernel type
        
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
            
            # Apply sharpen effect
            processed_img = self.sharpen_effect(
                pil_img,
                method=method,
                intensity=intensity,
                radius=radius,
                threshold=threshold,
                edge_enhancement=edge_enhancement,
                high_pass_radius=high_pass_radius,
                custom_kernel=custom_kernel
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveSharpen": SharpenNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveSharpen": "XWAVE Sharpen"
} 