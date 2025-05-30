"""
Posterize Node for ComfyUI XWAVE Nodes
Self-contained implementation with all effects included.
"""

import torch
import numpy as np
from PIL import Image


class PosterizeNode:
    """
    Reduce the number of colors in an image for artistic effect.
    Supports multiple dithering methods and color spaces.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "levels": ("INT", {
                    "default": 8,
                    "min": 2,
                    "max": 256,
                    "step": 1,
                    "display": "slider"
                }),
                "dither": (["none", "floyd-steinberg", "atkinson", "ordered"],),
                "color_space": (["rgb", "hsv", "lab"],),
            }
        }
    
    return_types = ("IMAGE",)
    function = "process"
    category = "XWAVE/Color"
    
    def posterize(self, image, levels=8, dither='none', color_space='rgb'):
        """
        Reduce the number of colors in an image with optional dithering.
        
        Args:
            image (Image): PIL Image object to process.
            levels (int): Number of color levels per channel (2-256).
            dither (str): Dithering method ('none', 'floyd-steinberg', 'atkinson', 'ordered').
            color_space (str): Color space for posterization ('rgb', 'hsv', 'lab').
        
        Returns:
            Image: Processed image with reduced color levels.
        """
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        img_array = np.array(image, dtype=np.float32)
        
        # Convert to specified color space
        if color_space == 'hsv':
            # Convert RGB to HSV
            r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
            maxc = np.maximum(np.maximum(r, g), b)
            minc = np.minimum(np.minimum(r, g), b)
            v = maxc
            s = np.where(maxc != 0, (maxc - minc) / maxc, 0)
            h = np.zeros_like(maxc)
            
            # Calculate hue
            rc = (maxc - r) / (maxc - minc + 1e-6)
            gc = (maxc - g) / (maxc - minc + 1e-6)
            bc = (maxc - b) / (maxc - minc + 1e-6)
            
            h = np.where(maxc == r, bc - gc, h)
            h = np.where(maxc == g, 2.0 + rc - bc, h)
            h = np.where(maxc == b, 4.0 + gc - rc, h)
            h = (h / 6.0) % 1.0
            
            img_array = np.stack([h, s, v], axis=2)
            
        elif color_space == 'lab':
            # Convert RGB to LAB (simplified version)
            r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
            
            # Convert to XYZ
            x = 0.412453 * r + 0.357580 * g + 0.180423 * b
            y = 0.212671 * r + 0.715160 * g + 0.072169 * b
            z = 0.019334 * r + 0.119193 * g + 0.950227 * b
            
            # Convert to LAB
            x = x / 0.950456
            z = z / 1.088754
            
            # Calculate L
            l = np.where(y > 0.008856,
                         116.0 * np.power(y, 1.0/3.0) - 16.0,
                         903.3 * y)
            
            # Calculate a and b
            a = 500.0 * (np.power(x, 1.0/3.0) - np.power(y, 1.0/3.0))
            b = 200.0 * (np.power(y, 1.0/3.0) - np.power(z, 1.0/3.0))
            
            # Normalize
            l = l / 100.0
            a = (a + 128.0) / 255.0
            b = (b + 128.0) / 255.0
            
            img_array = np.stack([l, a, b], axis=2)
        
        # Calculate step size for quantization
        step = 255.0 / (levels - 1)
        
        # Apply dithering if specified
        if dither != 'none':
            height, width = img_array.shape[:2]
            
            if dither == 'floyd-steinberg':
                # Floyd-Steinberg dithering
                for y in range(height):
                    for x in range(width):
                        old_pixel = img_array[y, x].copy()
                        new_pixel = np.round(old_pixel / step) * step
                        img_array[y, x] = new_pixel
                        
                        error = old_pixel - new_pixel
                        
                        if x + 1 < width:
                            img_array[y, x + 1] += error * 7/16
                        if y + 1 < height:
                            if x > 0:
                                img_array[y + 1, x - 1] += error * 3/16
                            img_array[y + 1, x] += error * 5/16
                            if x + 1 < width:
                                img_array[y + 1, x + 1] += error * 1/16
                                
            elif dither == 'atkinson':
                # Atkinson dithering
                for y in range(height):
                    for x in range(width):
                        old_pixel = img_array[y, x].copy()
                        new_pixel = np.round(old_pixel / step) * step
                        img_array[y, x] = new_pixel
                        
                        error = (old_pixel - new_pixel) / 8
                        
                        # Distribute error to neighboring pixels
                        for dy, dx, factor in [(0, 1, 1), (0, 2, 1), (1, -1, 1), (1, 0, 1),
                                             (1, 1, 1), (2, 0, 1)]:
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < height and 0 <= nx < width:
                                img_array[ny, nx] += error * factor
                                
            else:  # ordered dithering
                # Create Bayer matrix for ordered dithering
                bayer = np.array([[0, 8, 2, 10],
                                [12, 4, 14, 6],
                                [3, 11, 1, 9],
                                [15, 7, 13, 5]]) / 16.0
                
                # Tile the Bayer matrix to match image size
                bayer = np.tile(bayer, (height//4 + 1, width//4 + 1))[:height, :width]
                
                # Add dithering pattern
                img_array = img_array + (bayer[:, :, np.newaxis] - 0.5) * step
        
        # Quantize colors
        img_array = np.round(img_array / step) * step
        
        # Convert back to RGB if needed
        if color_space == 'hsv':
            # Convert HSV back to RGB
            h, s, v = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
            
            h = h * 6.0
            i = np.floor(h)
            f = h - i
            p = v * (1.0 - s)
            q = v * (1.0 - s * f)
            t = v * (1.0 - s * (1.0 - f))
            
            i = i % 6
            r = np.where(i == 0, v, np.where(i == 1, q, np.where(i == 2, p,
                    np.where(i == 3, p, np.where(i == 4, t, v)))))
            g = np.where(i == 0, t, np.where(i == 1, v, np.where(i == 2, v,
                    np.where(i == 3, q, np.where(i == 4, p, p)))))
            b = np.where(i == 0, p, np.where(i == 1, p, np.where(i == 2, t,
                    np.where(i == 3, v, np.where(i == 4, v, q)))))
            
            img_array = np.stack([r, g, b], axis=2) * 255.0
            
        elif color_space == 'lab':
            # Convert LAB back to RGB (simplified version)
            l, a, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
            
            # Denormalize
            l = l * 100.0
            a = (a * 255.0) - 128.0
            b = (b * 255.0) - 128.0
            
            # Convert to XYZ
            y = np.power((l + 16.0) / 116.0, 3.0)
            x = y + (a / 500.0)
            z = y - (b / 200.0)
            
            # Convert to RGB
            r = 3.240479 * x - 1.537150 * y - 0.498535 * z
            g = -0.969256 * x + 1.875992 * y + 0.041556 * z
            b = 0.055648 * x - 0.204043 * y + 1.057311 * z
            
            img_array = np.stack([r, g, b], axis=2) * 255.0
        
        # Ensure values are in valid range
        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        
        return Image.fromarray(img_array)
    
    def process(self, image, levels, dither, color_space):
        """
        Process the image with posterize effect.
        
        Args:
            image: Input image tensor
            levels: Number of color levels per channel
            dither: Dithering method to use
            color_space: Color space for posterization
        
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
            
            # Apply posterize effect
            processed_img = self.posterize(
                pil_img,
                levels=levels,
                dither=dither,
                color_space=color_space
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWavePosterize": PosterizeNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWavePosterize": "XWAVE Posterize"
} 