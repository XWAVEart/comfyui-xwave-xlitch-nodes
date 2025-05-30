"""
Sharpen effect for ComfyUI XWAVE Nodes.
Various sharpening methods for image enhancement.
"""

from PIL import Image, ImageFilter
import numpy as np


def sharpen_effect(image, method='unsharp_mask', intensity=1.0, radius=1.0, threshold=0,
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
        from scipy import ndimage
        
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
        from scipy import ndimage
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