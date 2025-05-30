
Self-contained implementation with all effects included.
"""

Color Shift Expansion Node for ComfyUI XWAVE Nodes
Apply color shift expansion effects with customizable patterns and themes.
"""

import torch
import numpy as np
from PIL import Image
import random
import colorsys


class ColorShiftExpansionNode:
    """
    Apply color shift expansion effects to images.
    Expands colored shapes from various points with customizable patterns and themes.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "num_points": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 50,
                    "step": 1,
                    "display": "slider"
                }),
                "shift_amount": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 20,
                    "step": 1,
                    "display": "slider"
                }),
                "expansion_type": (["square", "circle", "diamond"],),
                "mode": (["xtreme", "subtle", "mono"],),
                "saturation_boost": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "value_boost": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "pattern_type": (["random", "grid", "edges"],),
                "color_theme": (["full-spectrum", "warm", "cool", "pastel"],),
                "decay_factor": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2**32 - 1,
                    "step": 1
                }),
            }
        }
    
    return_types = ("IMAGE",)
    function = "process"
    category = "XWAVE/Color"
    
    
        def color_shift_expansion(image, num_points=5, shift_amount=5, expansion_type='square', mode='xtreme', 
                            saturation_boost=0.0, value_boost=0.0, pattern_type='random', 
                            color_theme='full-spectrum', decay_factor=0.0, seed=None):
        """
        Apply a color shift expansion effect expanding colored shapes from various points.
    
        Args:
            image (Image): PIL Image object to process.
            num_points (int): Number of expansion points.
            shift_amount (int): Amount of color shifting (0-20).
            expansion_type (str): Shape of expansion ('square', 'circle', 'diamond').
            mode (str): Mode of color application ('xtreme', 'subtle', 'mono').
            saturation_boost (float): Amount to boost saturation (0.0-1.0).
            value_boost (float): Amount to boost brightness (0.0-1.0).
            pattern_type (str): Pattern of color point placement ('random', 'grid', 'edges').
            color_theme (str): Color theme to use ('full-spectrum', 'warm', 'cool', 'pastel').
            decay_factor (float): How quickly effect fades with distance (0.0-1.0).
            seed (int, optional): Seed for random number generation. Defaults to None.
    
        Returns:
            Image: Processed image with color shift expansion effect.
        """
        # Convert to RGB mode if the image has an alpha channel or is in a different mode
        if image.mode != 'RGB':
            image = image.convert('RGB')

        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
    
        width, height = image.size
        image_np = np.array(image)
    
        # Create a blank canvas for our output
        output_np = np.zeros_like(image_np)
    
        # Ensure parameters are in valid ranges
        shift_amount = max(1, min(20, shift_amount))
        num_points = max(1, min(50, num_points))
        saturation_boost = max(0.0, min(1.0, saturation_boost))
        value_boost = max(0.0, min(1.0, value_boost))
        decay_factor = max(0.0, min(1.0, decay_factor))
    
        # Generate seed points based on pattern type
        seed_points = []
        if pattern_type == 'grid':
            # Create an evenly spaced grid of points
            cols = max(2, int(np.sqrt(num_points)))
            rows = max(2, num_points // cols)
            x_step = width // cols
            y_step = height // rows
            for i in range(rows):
                for j in range(cols):
                    x = j * x_step + x_step // 2
                    y = i * y_step + y_step // 2
                    if x < width and y < height:
                        seed_points.append((x, y))
        elif pattern_type == 'edges':
            # Points along the edges of the image
            edge_points = num_points
            # Distribute points along the edges
            for i in range(edge_points):
                if i % 4 == 0:  # Top edge
                    seed_points.append((int(width * (i / edge_points)), 0))
                elif i % 4 == 1:  # Right edge
                    seed_points.append((width - 1, int(height * (i / edge_points))))
                elif i % 4 == 2:  # Bottom edge
                    seed_points.append((int(width * (1 - i / edge_points)), height - 1))
                elif i % 4 == 3:  # Left edge
                    seed_points.append((0, int(height * (1 - i / edge_points))))
        else:  # random
            # Generate random points
            xs = np.random.randint(0, width, size=num_points)
            ys = np.random.randint(0, height, size=num_points)
            seed_points = list(zip(xs, ys))
    
        # Define the base colors for each theme
        seed_colors = []
        if color_theme == 'warm':
            # Warm colors (reds, oranges, yellows)
            for _ in range(num_points):
                h = random.uniform(0, 60) / 360  # Red to yellow
                s = random.uniform(0.6, 1.0)
                v = random.uniform(0.7, 1.0)
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                seed_colors.append((int(r * 255), int(g * 255), int(b * 255)))
        elif color_theme == 'cool':
            # Cool colors (blues, greens, purples)
            for _ in range(num_points):
                if random.random() < 0.5:
                    h = random.uniform(180, 300) / 360  # Cyan to purple
                else:
                    h = random.uniform(90, 180) / 360  # Yellow-green to cyan
                s = random.uniform(0.5, 1.0)
                v = random.uniform(0.6, 1.0)
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                seed_colors.append((int(r * 255), int(g * 255), int(b * 255)))
        elif color_theme == 'pastel':
            # Pastel colors (any hue but lower saturation)
            for _ in range(num_points):
                h = random.random()  # Any hue
                s = random.uniform(0.1, 0.5)  # Lower saturation
                v = random.uniform(0.8, 1.0)  # Higher value
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                seed_colors.append((int(r * 255), int(g * 255), int(b * 255)))
        else:  # 'full-spectrum'
            # Full spectrum of vibrant colors
            for i in range(num_points):
                h = i / num_points  # Evenly distributed hues
                s = random.uniform(0.7, 1.0)  # High saturation
                v = random.uniform(0.7, 1.0)  # Medium to high value
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                seed_colors.append((int(r * 255), int(g * 255), int(b * 255)))
    
        # Calculate the maximum possible distance (diagonal of the image)
        max_distance = np.sqrt(width**2 + height**2)
    
        # Create distance maps for each seed point (vectorized)
        yy, xx = np.mgrid[0:height, 0:width]
        distance_maps_list = []

        for point_idx, point_coords in enumerate(seed_points):
            x0, y0 = point_coords
            if expansion_type == 'square':
                # Chebyshev distance (L∞ norm)
                dist_map = np.maximum(np.abs(xx - x0), np.abs(yy - y0))
            elif expansion_type == 'diamond':
                # Manhattan distance (L1 norm)
                dist_map = np.abs(xx - x0) + np.abs(yy - y0)
            else:  # circle (default)
                # Euclidean distance (L2 norm)
                dist_map = np.sqrt((xx - x0)**2 + (yy - y0)**2)
            distance_maps_list.append(dist_map)
    
        # Stack distance maps into a 3D array for easier access: (num_points, height, width)
        if not distance_maps_list: # Handle case with no seed points if num_points could be 0
            # Fill output with original image if no points, though num_points is validated >= 1
            output_np = image_np.copy() 
        else:
            distance_maps_stack = np.stack(distance_maps_list, axis=0)

        # Process each pixel (still a loop, but distance calculation is now outside)
        # Further vectorization of this loop is complex due to per-pixel HSV conversions
        # and conditional logic, but the heaviest part (distance maps) is done.

        # Pre-calculate seed colors as a NumPy array for easier broadcasting later if possible
        seed_colors_np = np.array(seed_colors, dtype=np.float32) # num_points x 3

        # The main loop remains, but accesses pre-calculated distance_maps_stack
        for y in range(height):
            for x in range(width):
                original_r, original_g, original_b = image_np[y, x]
                h, s, v = colorsys.rgb_to_hsv(original_r / 255.0, original_g / 255.0, original_b / 255.0)
            
                if not distance_maps_list: # Should not happen due to num_points validation
                    output_np[y, x] = image_np[y, x]
                    continue

                # Get all distances for the current pixel (y,x) from all seed points
                pixel_distances = distance_maps_stack[:, y, x] # Shape: (num_points,)
            
                closest_idx = np.argmin(pixel_distances)
                min_dist = pixel_distances[closest_idx]
            
                influences = np.zeros(len(seed_points), dtype=float)
                if decay_factor > 0:
                    # Higher decay_factor means faster drop-off. Normalize distance by max_distance.
                    influences = np.maximum(0.0, 1.0 - (decay_factor * pixel_distances / max_distance))
                else:
                    # Inverse relationship (original was 1/(1 + (d/50)^2) )
                    # Avoid division by zero if distance is very small, though 1.0 + ... handles it.
                    influences = 1.0 / (1.0 + (pixel_distances / 50.0)**2) # 50.0 is a sensitivity factor

                total_influence = np.sum(influences)
            
                if total_influence < 0.001 or len(seed_colors_np) == 0:
                    output_np[y, x] = image_np[y, x]
                    continue
            
                normalized_influences = influences / total_influence # Shape: (num_points,)
            
                # Weighted blend of seed colors (RGB)
                # normalized_influences[:, np.newaxis] gives (num_points, 1)
                # seed_colors_np is (num_points, 3)
                # Result is (num_points, 3), then sum over axis 0
                blend_rgb = np.sum(normalized_influences[:, np.newaxis] * seed_colors_np, axis=0)
                blend_r, blend_g, blend_b = blend_rgb[0], blend_rgb[1], blend_rgb[2]
            
                blend_h, blend_s, blend_v = colorsys.rgb_to_hsv(
                    np.clip(blend_r / 255.0, 0, 1), 
                    np.clip(blend_g / 255.0, 0, 1), 
                    np.clip(blend_b / 255.0, 0, 1)
                )
            
                shift_weight = min(0.85, shift_amount / 12.0)
            
                final_h = h * (1 - shift_weight) + blend_h * shift_weight # Hue blending can be tricky, direct average here
                final_s = s * (1 - shift_weight) + (blend_s + saturation_boost) * shift_weight
                final_v = v * (1 - shift_weight) + (blend_v + value_boost) * shift_weight
            
                final_s = min(1.0, max(0.0, final_s))
                final_v = min(1.0, max(0.0, final_v))
                final_h = final_h % 1.0 # Ensure hue remains in [0,1)
            
                final_r_float, final_g_float, final_b_float = colorsys.hsv_to_rgb(final_h, final_s, final_v)
            
                output_np[y, x] = [
                    int(final_r_float * 255),
                    int(final_g_float * 255),
                    int(final_b_float * 255)
                ]
    
        # Convert back to PIL Image
        processed_image = Image.fromarray(output_np.astype(np.uint8))
        return processed_image 
    
        def process(self, image, num_points, shift_amount, expansion_type, mode,
                saturation_boost, value_boost, pattern_type, color_theme,
                decay_factor, seed):
        """
        Process the image with color shift expansion effect.
        
        Args:
image: Input image tensor
            num_points: Number of expansion points
            shift_amount: Amount of color shifting (0-20)
            expansion_type: Shape of expansion ('square', 'circle', 'diamond')
            mode: Mode of color application ('xtreme', 'subtle', 'mono')
            saturation_boost: Amount to boost saturation (0.0-1.0)
            value_boost: Amount to boost brightness (0.0-1.0)
            pattern_type: Pattern of color point placement ('random', 'grid', 'edges')
            color_theme: Color theme to use ('full-spectrum', 'warm', 'cool', 'pastel')
            decay_factor: How quickly effect fades with distance (0.0-1.0)
            seed: Seed for random number generation
        
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
            
            # Apply color shift expansion effect
            processed_img = self.color_shift_expansion(
                pil_img,
                num_points=num_points,

                            shift_amount=shift_amount,

                            expansion_type=expansion_type,

                            mode=mode,

                            saturation_boost=saturation_boost,

                            value_boost=value_boost,

                            pattern_type=pattern_type,

                            color_theme=color_theme,

                            decay_factor=decay_factor,

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
    "XWaveColorShiftExpansion": ColorShiftExpansionNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveColorShiftExpansion": "XWAVE Color Shift Expansion"
} 