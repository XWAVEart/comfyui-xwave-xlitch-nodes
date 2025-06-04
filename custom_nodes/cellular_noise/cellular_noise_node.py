import numpy as np
from PIL import Image
from scipy.stats import norm

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
                "antialias": ("BOOLEAN", {"default": False})
            },
            "optional": {
                "palette_path": ("STRING", {"default": ""})
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_cellular_noise"
    CATEGORY = "image/postprocessing"

    def blend(self, original, noise, mask, mode='overlay'):
        """Blend noise into original image using specified mode."""
        # Normalize mask to 0-1 range
        mask = mask / 255.0
        
        if mode == 'overlay':
            return original * (1 - mask) + noise * mask
        elif mode == 'add':
            return np.clip(original + noise * mask, 0, 255)
        elif mode == 'multiply':
            return np.clip(original * (1 + noise * mask / 255), 0, 255)
        elif mode == 'screen':
            return 255 - (255 - original) * (255 - (noise * mask)) / 255
        elif mode == 'soft_light':
            return np.where(original < 128,
                           2 * original * noise * mask / 255 + original * (1 - mask),
                           255 - 2 * (255 - original) * (255 - noise * mask) / 255)
        elif mode == 'hard_light':
            return np.where(noise * mask < 128,
                           2 * original * noise * mask / 255,
                           255 - 2 * (255 - original) * (255 - noise * mask) / 255)
        elif mode == 'color_dodge':
            return np.clip(original / (1 - (noise * mask / 255) + 1e-6), 0, 255)
        elif mode == 'color_burn':
            return np.clip(255 - (255 - original) / ((noise * mask / 255) + 1e-6), 0, 255)
        elif mode == 'linear_dodge':
            return np.clip(original + noise * mask, 0, 255)
        elif mode == 'linear_burn':
            return np.clip(original + noise * mask - 255, 0, 255)
        elif mode == 'difference':
            return np.abs(original - noise * mask)
        else:
            raise ValueError(f"Unknown blend mode: {mode}")

    def generate_noise(self, shape, noise_type, palette=None):
        if noise_type == 'rgb':
            return np.random.randint(0, 256, size=(*shape, 3), dtype=np.uint8)
        elif noise_type == 'grayscale':
            gray = np.random.randint(0, 256, size=shape, dtype=np.uint8)
            return np.stack([gray] * 3, axis=-1)
        elif noise_type == 'palette':
            if palette is None:
                raise ValueError("Palette must be provided for palette noise")
            palette_colors = np.array(palette)
            idx = np.random.randint(0, len(palette_colors), size=shape)
            return palette_colors[idx]
        elif noise_type == 'gaussian':
            return np.clip(norm.rvs(loc=127, scale=40, size=(*shape, 3)), 0, 255).astype(np.uint8)
        else:
            raise ValueError(f'Unknown noise_type {noise_type}')

    def circle_mask(self, h, w, cx, cy, radius, antialias=False):
        y, x = np.ogrid[:h, :w]
        dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        mask = (dist <= radius).astype(np.float32)
        if antialias:
            aa_zone = (dist > radius - 1) & (dist <= radius)
            mask[aa_zone] = 1 - (dist[aa_zone] - (radius - 1))
        return mask

    def gradient_profile(self, dist, radius, center_val, edge_val, grad_type, reverse):
        if grad_type == 'radial':
            grad = dist / radius
        else:  # linear
            grad = dist / radius
        grad = np.clip(grad, 0, 1)
        if reverse:
            grad = 1 - grad
        return center_val + (edge_val - center_val) * grad

    def load_palette(self, palette_path):
        if not palette_path:
            return None
        palette = []
        with open(palette_path, 'r') as f:
            for line in f:
                vals = line.strip().split()
                if len(vals) == 3:
                    palette.append(tuple(map(int, vals)))
        return palette

    def process_block(self, result, x0, y0, circle_size, noise_type, palette, blend_mode, 
                     center_noise, edge_noise, gradient_type, reverse_gradient, antialias, w, h):
        """Process a single block of the image."""
        x1 = min(x0 + circle_size, w)
        y1 = min(y0 + circle_size, h)
        if x1 <= 0 or y1 <= 0 or x0 >= w or y0 >= h:
            return
        x0 = max(0, x0)
        y0 = max(0, y0)
        cx = x0 + (x1 - x0) // 2
        cy = y0 + (y1 - y0) // 2
        region = result[y0:y1, x0:x1]
        yy, xx = np.ogrid[y0:y1, x0:x1]
        dist = np.sqrt((xx - cx)**2 + (yy - cy)**2)
        noise_amt = self.gradient_profile(
            dist, circle_size // 2,
            center_noise, edge_noise,
            gradient_type, reverse_gradient
        )
        noise = self.generate_noise(region.shape[:2], noise_type, palette)
        for c in range(3):
            region[..., c] = self.blend(region[..., c], noise[..., c], noise_amt, mode=blend_mode)
        result[y0:y1, x0:x1] = region

    def apply_cellular_noise(self, image, circle_size, layout, noise_type, blend_mode, 
                           center_noise, edge_noise, gradient_type, reverse_gradient, 
                           antialias, palette_path=""):
        # Convert image to numpy array if it isn't already
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Load palette if needed
        palette = None
        if noise_type == 'palette':
            palette = self.load_palette(palette_path)
            if palette is None:
                raise ValueError("Palette path must be provided for palette noise")

        result = image.copy()
        h, w = result.shape[:2]
        
        if layout == 'grid':
            for y0 in range(0, h, circle_size):
                for x0 in range(0, w, circle_size):
                    self.process_block(result, x0, y0, circle_size, noise_type, palette,
                                     blend_mode, center_noise, edge_noise, gradient_type,
                                     reverse_gradient, antialias, w, h)
        else:  # hex layout
            row_height = int(circle_size * 0.866)  # sqrt(3)/2
            for row, y0 in enumerate(range(0, h, row_height)):
                x_offset = circle_size // 2 if row % 2 else 0
                for x0 in range(-x_offset, w, circle_size):
                    self.process_block(result, x0, y0, circle_size, noise_type, palette,
                                     blend_mode, center_noise, edge_noise, gradient_type,
                                     reverse_gradient, antialias, w, h)

        return (result,) 