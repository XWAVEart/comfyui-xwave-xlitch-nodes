
Self-contained implementation with all effects included.
"""

Curved hue shift node for ComfyUI XWAVE Nodes.
Apply non-linear hue transformations using exponential curves.
"""

import torch
import numpy as np
from PIL import Image


class CurvedHueShiftNode:
    """Apply curved hue shift effects using exponential curves."""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "curve_value": ("FLOAT", {
                    "default": 180.0,
                    "min": 1.0,
                    "max": 360.0,
                    "step": 1.0,
                    "display": "slider"
                }),
                "shift_amount": ("FLOAT", {
                    "default": 30.0,
                    "min": -180.0,
                    "max": 180.0,
                    "step": 1.0,
                    "display": "slider"
                }),
            }
        }
    
    return_types = ("IMAGE",)
    function = "process"
    category = "XWAVE/Color"
    
    
        def curved_hue_shift(image, curve_value=180.0, shift_amount=30.0):
        """
        Applies a curved hue shift to an image using exponential curves.
    
        Args:
            image (PIL.Image): The input image.
            curve_value (float): Curve value from 1 to 360, controlling the shift curve.
            shift_amount (float): Total shift amount in degrees.
    
        Returns:
            PIL.Image: The image with the curved hue shift applied.
        """
        # Validate inputs
        if not 1 <= curve_value <= 360:
            raise ValueError("Curve parameter must be between 1 and 360")
    
        original_mode = image.mode
        if image.mode not in ['RGB', 'RGBA']:
            image = image.convert('RGB') # Fallback to RGB if not directly convertible to HSV from original
        elif image.mode == 'RGBA':
            # Store alpha channel if present
            alpha = image.split()[-1] if image.mode == 'RGBA' else None
            image = image.convert('RGB') # Work with RGB for HSV conversion
        else: # Already RGB
            alpha = None

        # Convert to HSV using PIL
        hsv_image = image.convert('HSV')
        h_channel, s_channel, v_channel = hsv_image.split()

        # Convert H channel to NumPy array and normalize to 0-1 range
        h_array_pil = np.array(h_channel, dtype=np.float32)
        h_norm = h_array_pil / 255.0  # Normalized H (0.0 - 1.0)

        # Curve parameter p (normalized curve_value to -1 to 1)
        p_curve = (curve_value - 180.0) / 180.0

        # Calculate shift amount for each pixel
        shift_factor_rad = p_curve * (h_norm - 0.5)  # This term provides the curve based on original hue
        s_shift_degrees = shift_amount * np.exp(shift_factor_rad)

        # Current hue in degrees
        current_h_degrees = h_norm * 360.0

        # New hue in degrees
        new_h_degrees = (current_h_degrees + s_shift_degrees) % 360.0

        # Convert new H back to PIL's 0-255 scale for 'L' mode channel
        new_h_pil_scale = (new_h_degrees / 360.0) * 255.0
        shifted_h_array = np.clip(new_h_pil_scale, 0, 255).astype(np.uint8)
    
        shifted_h_channel_pil = Image.fromarray(shifted_h_array, mode='L')

        # Merge channels and convert back to RGB
        final_hsv_image = Image.merge('HSV', (shifted_h_channel_pil, s_channel, v_channel))
        final_rgb_image = final_hsv_image.convert('RGB')

        # If original image had alpha, re-apply it
        if alpha:
            final_rgb_image.putalpha(alpha)

        return final_rgb_image 
    
        def process(self, image, curve_value, shift_amount):
        """
        Process the image with curved hue shift effect.
        
        Args:
image: Input image tensor
            curve_value: Curve value from 1 to 360, controlling the shift curve
            shift_amount: Total shift amount in degrees
        
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
            
            # Apply curved hue shift effect
            processed_img = self.curved_hue_shift(
                pil_img,
                curve_value=curve_value,
                 shift_amount=shift_amount
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)



# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveCurvedHueShift": CurvedHueShiftNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveCurvedHueShift": "XWAVE Curved Hue Shift"
} 