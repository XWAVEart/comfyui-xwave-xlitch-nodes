import torch
import numpy as np
from PIL import Image

class XWAVEPixelateNode:
    """
    A ComfyUI node that applies pixelation effects to images.
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "pixel_width": ("INT", {
                    "default": 8,
                    "min": 1,
                    "max": 256,
                    "step": 1,
                    "display": "number"
                }),
                "pixel_height": ("INT", {
                    "default": 8,
                    "min": 1,
                    "max": 256,
                    "step": 1,
                    "display": "number"
                }),
                "attribute": (["color", "brightness", "hue", "saturation", "luminance"],),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "apply_pixelate"
    CATEGORY = "XWAVE/Effects"
    
    def apply_pixelate(self, image, pixel_width, pixel_height, attribute):
        # Convert from ComfyUI tensor format to numpy array
        # ComfyUI images are [batch, height, width, channels] with values 0-1
        batch_size = image.shape[0]
        result = []
        
        for i in range(batch_size):
            # Convert to PIL Image
            img_array = (image[i].cpu().numpy() * 255).astype(np.uint8)
            pil_img = Image.fromarray(img_array, mode='RGB')
            
            # Apply pixelation
            pixelated = self.pixelate_by_attribute(pil_img, pixel_width, pixel_height, attribute)
            
            # Convert back to tensor format
            result_array = np.array(pixelated).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)
    
    def pixelate_by_attribute(self, image, pixel_width=8, pixel_height=8, attribute='color'):
        """
        Apply pixelation grouping similar values from the specified attribute.
        """
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        img_array = np.array(image)
        height, width, _ = img_array.shape
        result_array = np.zeros_like(img_array)
        
        # Process each pixel block
        for y in range(0, height, pixel_height):
            for x in range(0, width, pixel_width):
                block_y_end = min(y + pixel_height, height)
                block_x_end = min(x + pixel_width, width)
                
                current_block_slice = img_array[y:block_y_end, x:block_x_end]
                if current_block_slice.size == 0:
                    continue
                
                fill_color = None
                
                if attribute == 'color':
                    # Reshape block to (num_pixels_in_block, 3)
                    flat_block = current_block_slice.reshape(-1, 3)
                    if flat_block.shape[0] == 0: 
                        continue
                    
                    # Find the most common color
                    unique_colors, counts = np.unique(flat_block, axis=0, return_counts=True)
                    most_common_color_idx = np.argmax(counts)
                    fill_color = unique_colors[most_common_color_idx]
                else:
                    # Calculate attribute for each pixel in the block
                    flat_block = current_block_slice.reshape(-1, 3)
                    if flat_block.shape[0] == 0: 
                        continue
                    
                    # Calculate attributes
                    attr_values = []
                    for pixel in flat_block:
                        if attribute == 'brightness':
                            val = np.mean(pixel)
                        elif attribute == 'hue':
                            # Convert RGB to HSV
                            r, g, b = pixel[0] / 255.0, pixel[1] / 255.0, pixel[2] / 255.0
                            max_val = max(r, g, b)
                            min_val = min(r, g, b)
                            diff = max_val - min_val
                            
                            if diff == 0:
                                hue = 0
                            elif max_val == r:
                                hue = ((g - b) / diff) % 6
                            elif max_val == g:
                                hue = (b - r) / diff + 2
                            else:
                                hue = (r - g) / diff + 4
                            
                            val = hue * 60  # Convert to degrees
                        elif attribute == 'saturation':
                            r, g, b = pixel[0] / 255.0, pixel[1] / 255.0, pixel[2] / 255.0
                            max_val = max(r, g, b)
                            min_val = min(r, g, b)
                            
                            if max_val == 0:
                                val = 0
                            else:
                                val = (max_val - min_val) / max_val
                        elif attribute == 'luminance':
                            # Using standard luminance formula
                            val = 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]
                        else:
                            val = np.mean(pixel)
                        
                        attr_values.append(val)
                    
                    attr_values = np.array(attr_values)
                    
                    if attr_values.size > 0:
                        avg_attr = np.mean(attr_values)
                        # Find the pixel with the attribute value closest to the average
                        closest_idx = np.argmin(np.abs(attr_values - avg_attr))
                        fill_color = flat_block[closest_idx]
                
                if fill_color is not None:
                    result_array[y:block_y_end, x:block_x_end] = fill_color
        
        return Image.fromarray(result_array)

# Node registration
NODE_CLASS_MAPPINGS = {
    "XWAVEPixelate": XWAVEPixelateNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "XWAVEPixelate": "XWAVE Pixelate"
} 