import numpy as np
from PIL import Image
from scipy.stats import norm
import torch

class CellularNoiseNode:
    """
    A ComfyUI node that generates cellular noise patterns and applies them to images.
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "circle_size": ("INT", {
                    "default": 32,
                    "min": 8,
                    "max": 128,
                    "step": 1
                }),
                "layout": (["grid", "hex"], {"default": "grid"}),
                "noise_type": (["rgb", "grayscale", "palette", "gaussian"], {"default": "rgb"}),
                "blend_mode": (["overlay", "add", "multiply", "screen", "soft_light", "hard_light", 
                              "color_dodge", "color_burn", "linear_dodge", "linear_burn", "difference"], 
                             {"default": "overlay"}),
                "center_noise": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                "edge_noise": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                "gradient_type": (["linear", "radial"], {"default": "linear"}),
                "reverse_gradient": ("BOOLEAN", {"default": False}),
                "opacity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "antialias": ("BOOLEAN", {"default": False})
            },
            "optional": {
                "palette_path": ("STRING", {"default": ""})
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_cellular_noise"
    CATEGORY = "XWAVE/Noise"  # Updated category

    def blend(self, original, noise, mask, mode='overlay', opacity=1.0):
        if mask.ndim == 2 and original.ndim == 3:
            mask = mask[..., np.newaxis]
        if noise.ndim == 2 and original.ndim == 3: # If noise is grayscale for a color image
            noise = np.stack([noise]*original.shape[2], axis=-1)

        if mode == 'overlay':
            original_norm = original / 255.0
            noise_norm = noise / 255.0
            low = 2 * original_norm * noise_norm
            high = 1 - 2 * (1 - original_norm) * (1 - noise_norm)
            blended_norm = np.where(original_norm < 0.5, low, high)
            blended_0_255 = np.clip(blended_norm * 255.0, 0, 255)
            result = original * (1 - mask) + blended_0_255 * mask
        elif mode == 'add':
            result = np.clip(original + noise * mask, 0, 255)
        elif mode == 'multiply':
            original_norm = original / 255.0
            noise_norm = noise / 255.0
            blended_norm = original_norm * noise_norm
            blended_0_255 = np.clip(blended_norm * 255.0, 0, 255)
            result = original * (1-mask) + blended_0_255 * mask
        elif mode == 'screen':
            original_norm = original / 255.0
            noise_norm = noise / 255.0
            blended_norm = 1 - (1 - original_norm) * (1 - noise_norm)
            blended_0_255 = np.clip(blended_norm * 255.0, 0, 255)
            result = original * (1-mask) + blended_0_255 * mask
        elif mode == 'soft_light':
            original_norm = original / 255.0
            noise_norm = noise / 255.0
            # Using a common formula for soft light
            res = np.where(noise_norm < 0.5,
                           (2 * original_norm - 1) * (noise_norm - noise_norm**2) + original_norm,
                           (2 * original_norm - 1) * (np.sqrt(noise_norm) - noise_norm) + original_norm)
            blended_0_255 = np.clip(res * 255.0, 0, 255)
            result = original * (1-mask) + blended_0_255 * mask
        elif mode == 'hard_light':
            original_norm = original / 255.0
            noise_norm = noise / 255.0
            # Using a common formula for hard light (overlay with inputs swapped)
            res = np.where(noise_norm < 0.5, 
                           2 * original_norm * noise_norm, 
                           1 - 2 * (1 - original_norm) * (1 - noise_norm))
            blended_0_255 = np.clip(res * 255.0, 0, 255)
            result = original * (1 - mask) + blended_0_255 * mask
        elif mode == 'color_dodge':
            # Ensure noise*mask doesn't make denominator zero or negative
            dodge_factor = noise * mask / 255.0
            result = np.clip(original / (1.0 - dodge_factor + 1e-7), 0, 255)
        elif mode == 'color_burn':
            burn_factor = noise * mask / 255.0
            result = np.clip(255.0 - (255.0 - original) / (burn_factor + 1e-7), 0, 255)
        elif mode == 'linear_dodge': # Same as add
            result = np.clip(original + noise * mask, 0, 255)
        elif mode == 'linear_burn': # (A + B - 1) or (original + noise_masked - 255)
            result = np.clip(original + noise * mask - 255.0, 0, 255)
        elif mode == 'difference':
            result = np.clip(np.abs(original - noise * mask),0,255)
        else:
            raise ValueError(f"Unknown blend mode: {mode}")
        
        # Apply opacity: blend between original and result based on opacity
        return original * (1.0 - opacity) + result * opacity

    def generate_noise(self, shape, noise_type, palette=None):
        if noise_type == 'rgb':
            return np.random.randint(0, 256, size=(*shape, 3), dtype=np.uint8)
        elif noise_type == 'grayscale':
            # Grayscale noise is often applied to each channel identically or used as a base for color noise
            gray = np.random.randint(0, 256, size=shape, dtype=np.uint8)
            return np.stack([gray] * 3, axis=-1) # Return as 3-channel gray for easier blending
        elif noise_type == 'palette':
            if palette is None or len(palette) == 0:
                # This case should be handled by a fallback in apply_cellular_noise
                raise ValueError("Palette must be provided and be non-empty for palette noise")
            palette_colors = np.array(palette)
            idx = np.random.randint(0, len(palette_colors), size=shape)
            return palette_colors[idx]
        elif noise_type == 'gaussian':
            return np.clip(norm.rvs(loc=127, scale=40, size=(*shape, 3)), 0, 255).astype(np.uint8)
        else:
            raise ValueError(f'Unknown noise_type {noise_type}')

    def gradient_profile(self, dist, radius, center_val, edge_val, grad_type, reverse):
        if radius == 0: # Avoid division by zero
            return np.full_like(dist, center_val if not reverse else edge_val, dtype=np.float32)
        # Calculate gradient factor (0 at center, 1 at radius)
        grad_factor = dist / radius
        grad_factor = np.clip(grad_factor, 0, 1)
        if reverse:
            grad_factor = 1 - grad_factor
        # Interpolate between center_val and edge_val
        profile = center_val + (edge_val - center_val) * grad_factor
        
        # For distances beyond radius, gradually fade to zero to prevent hard edges
        beyond_radius = dist > radius
        if np.any(beyond_radius):
            fade_factor = np.maximum(0, 1 - (dist - radius) / (radius * 0.5))  # Fade over half-radius distance
            profile = np.where(beyond_radius, profile * fade_factor, profile)
        
        return profile

    def load_palette(self, palette_path):
        if not palette_path:
            return None
        try:
            palette = []
            with open(palette_path, 'r') as f:
                for line in f:
                    vals = line.strip().split()
                    if len(vals) == 3:
                        palette.append(tuple(map(int, vals)))
            return palette if palette else None
        except FileNotFoundError:
            print(f"Warning: Palette file not found at {palette_path}")
            return None
        except Exception as e:
            print(f"Warning: Error loading palette file {palette_path}: {e}")
            return None

    def process_block(self, result_slice, block_y_start, block_x_start, 
                      circle_center_x_in_image, circle_center_y_in_image, 
                      circle_radius, noise_type, palette, blend_mode, 
                      center_noise, edge_noise, gradient_type, reverse_gradient, opacity):
        # result_slice is the actual numpy array slice to modify.
        # block_y_start, block_x_start are the top-left coordinates of the block in the image
        
        block_h, block_w = result_slice.shape[:2]
        
        # Create coordinate grid for this specific block
        yy, xx = np.ogrid[block_y_start:block_y_start + block_h, 
                          block_x_start:block_x_start + block_w]
        
        # Calculate distance from each point in the block to the circle center
        dist = np.sqrt((xx - circle_center_x_in_image)**2 + 
                       (yy - circle_center_y_in_image)**2)
        
        noise_amount_profile = self.gradient_profile(
            dist, circle_radius,
            center_noise, edge_noise,
            gradient_type, reverse_gradient
        )
        
        # Generate noise for the exact region shape
        noise = self.generate_noise(result_slice.shape[:2], noise_type, palette)
        
        for c_idx in range(result_slice.shape[2]): # Iterate through channels
            result_slice[..., c_idx] = self.blend(
                result_slice[..., c_idx],
                noise[..., c_idx],
                noise_amount_profile, # This is the mask, should be 0-1
                mode=blend_mode,
                opacity=opacity
            )
        # Modification is done in-place on result_slice

    def apply_cellular_noise(self, image, circle_size, layout, noise_type, blend_mode, 
                           center_noise, edge_noise, gradient_type, reverse_gradient, 
                           opacity, antialias, palette_path=""):
        # antialias is not used in current backend logic, but kept for future
        processed_images = []
        if circle_size <= 0: 
            print("Warning: circle_size is invalid, defaulting to 32.")
            circle_size = 32 

        for i in range(image.shape[0]): # Batch loop
            img_tensor = image[i]
            # Convert to HWC, 0-255, float32 for processing
            img_np = np.clip(255. * img_tensor.cpu().numpy(), 0, 255).astype(np.float32)
            
            current_noise_type = noise_type
            palette = None
            if noise_type == 'palette':
                palette = self.load_palette(palette_path)
                if not palette:
                    print(f"Warning: Palette not loaded or empty from '{palette_path}'. Falling back to RGB noise.")
                    current_noise_type = 'rgb'
            
            result_np = img_np.copy()
            h, w = result_np.shape[:2]
            radius = circle_size // 2
            if radius <= 0: radius = 1

            if layout == 'grid':
                for y0 in range(0, h, circle_size): # y0 is top of the block
                    for x0 in range(0, w, circle_size): # x0 is left of the block
                        cx = x0 + radius # center of current circle
                        cy = y0 + radius # center of current circle

                        # Define block boundaries for slicing result_np
                        eff_x0, eff_y0 = max(0, x0), max(0, y0)
                        eff_x1, eff_y1 = min(w, x0 + circle_size), min(h, y0 + circle_size)
                        
                        if eff_x0 >= eff_x1 or eff_y0 >= eff_y1: continue # Skip if block is outside or zero-size

                        block_slice = result_np[eff_y0:eff_y1, eff_x0:eff_x1]
                        
                        self.process_block(block_slice, eff_y0, eff_x0,
                                         cx, cy, radius, current_noise_type, palette, blend_mode,
                                         center_noise, edge_noise, gradient_type, reverse_gradient, opacity)
            
            else:  # hex layout - ensure seamless coverage
                row_height = int(circle_size * 0.866)  # sqrt(3)/2 for hex packing
                if row_height == 0: row_height = 1 
                
                # Use smaller row_height to ensure overlap and prevent gaps
                row_height = max(1, int(row_height * 0.9))  # Reduce by 10% to ensure overlap

                # Process hex layout with overlapping coverage
                for row, y0 in enumerate(range(0, h + circle_size, row_height)):
                    x_offset = (circle_size // 2) if row % 2 else 0  # Hex offset for alternating rows
                    for x0 in range(-x_offset - radius, w + radius, circle_size):  # Extended range for better coverage
                        # Calculate circle center
                        cx = x0 + radius
                        cy = y0 + radius
                        
                        # Use larger processing blocks to ensure overlap
                        block_x0 = x0 - radius // 2  # Extend block beyond circle boundary
                        block_y0 = y0 - radius // 2
                        block_x1 = x0 + circle_size + radius // 2
                        block_y1 = y0 + circle_size + radius // 2
                        
                        # Clip to image boundaries
                        eff_x0, eff_y0 = max(0, block_x0), max(0, block_y0)
                        eff_x1, eff_y1 = min(w, block_x1), min(h, block_y1)
                        
                        if eff_x0 >= eff_x1 or eff_y0 >= eff_y1: continue

                        block_slice = result_np[eff_y0:eff_y1, eff_x0:eff_x1]
                        
                        self.process_block(block_slice, eff_y0, eff_x0,
                                         cx, cy, radius, current_noise_type, palette, blend_mode,
                                         center_noise, edge_noise, gradient_type, reverse_gradient, opacity)
            
            processed_images.append(result_np)

        # Convert list of processed NumPy arrays back to a torch tensor (0-1, float32)
        output_images = []
        for res_np_item in processed_images:
            res_np_float = res_np_item.astype(np.float32) / 255.0
            output_images.append(torch.from_numpy(res_np_float))
        
        final_tensor = torch.stack(output_images, dim=0) # B, H, W, C
        return (final_tensor,)

# Node Mappings - Must be at the top level of this Python file
NODE_CLASS_MAPPINGS = {
    "XWAVECellularNoiseNode": CellularNoiseNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "XWAVECellularNoiseNode": "XWAVE Cellular Noise"
} 