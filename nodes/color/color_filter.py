
Self-contained implementation with all effects included.
"""

Color Filter Node for ComfyUI XWAVE Nodes
Apply color filters with various blend modes and filter types.
"""

import torch
import numpy as np
from PIL import Image


class ColorFilterNode:
    """
    Apply color filters to images with various blend modes and filter types.
    Supports solid colors, gradients, and custom gradient images.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "filter_type": (["solid", "gradient", "custom"],),
                "color": ("STRING", {
                    "default": "#FF0000",
                    "multiline": False
                }),
                "blend_mode": (["normal", "multiply", "screen", "overlay", "soft_light", "hard_light",
                               "color_dodge", "color_burn", "linear_dodge", "linear_burn", "vivid_light"],),
                "opacity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
                "gradient_color2": ("STRING", {
                    "default": "#0000FF",
                    "multiline": False
                }),
                "gradient_angle": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 360.0,
                    "step": 1.0,
                    "display": "slider"
                }),
                "custom_gradient": ("IMAGE", {"default": None}),
            }
        }
    
    return_types = ("IMAGE",)
    function = "process"
    category = "XWAVE/Color"
    
    
        def color_filter(image, filter_type='solid', color='#FF0000', blend_mode='overlay', opacity=0.5,
                    gradient_color2='#0000FF', gradient_angle=0, custom_gradient=None):
        """
        Apply a color filter to an image with various blend modes.
    
        Args:
            image (Image): PIL Image object to process.
            filter_type (str): Type of filter ('solid', 'gradient', 'custom').
            color (str): Primary filter color in hex format (e.g., '#FF0000').
            blend_mode (str): Blend mode to use.
            opacity (float): Filter opacity (0.0-1.0).
            gradient_color2 (str): Secondary color for gradient filter in hex format.
            gradient_angle (float): Gradient rotation angle in degrees (0-360).
            custom_gradient (Image): Custom gradient image for 'custom' filter type.
    
        Returns:
            Image: Processed image with color filter applied.
        """
        if image.mode != 'RGB':
            image = image.convert('RGB')
    
        # Convert image to numpy array
        img_array = np.array(image, dtype=np.float32) / 255.0
    
        # Convert hex colors to RGB
        color_rgb = hex_to_rgb(color)
    
        # Create filter based on type
        if filter_type == 'solid':
            filter_array = np.full_like(img_array, np.array(color_rgb, dtype=np.float32) / 255.0)
        elif filter_type == 'gradient':
            gradient_color2_rgb = hex_to_rgb(gradient_color2)
            filter_array = create_gradient(
                image.width, image.height,
                color_rgb, gradient_color2_rgb,
                gradient_angle
            )
        else:  # custom gradient
            if custom_gradient is None:
                raise ValueError("Custom gradient image is required for 'custom' filter type")
        
            # Convert custom gradient to RGB and resize
            if custom_gradient.mode != 'RGB':
                custom_gradient = custom_gradient.convert('RGB')
            custom_gradient = custom_gradient.resize((image.width, image.height), Image.Resampling.LANCZOS)
            filter_array = np.array(custom_gradient, dtype=np.float32) / 255.0
    
        # Apply blend mode
        result = apply_blend_mode(img_array, filter_array, blend_mode, opacity)
    
        # Convert back to uint8 and create image
        result = (result * 255.0).astype(np.uint8)
        return Image.fromarray(result) 
    
        def process(self, image, filter_type, color, blend_mode, opacity,
                gradient_color2, gradient_angle, custom_gradient):
        """
        Process the image with color filter effect.
        
        Args:
image: Input image tensor
            filter_type: Type of filter (solid, gradient, custom)
            color: Primary filter color in hex format
            blend_mode: Blend mode to use
            opacity: Filter opacity (0.0-1.0)
            gradient_color2: Secondary color for gradient in hex format
            gradient_angle: Gradient rotation angle in degrees
            custom_gradient: Custom gradient image for 'custom' filter type
        
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

                            gradient_angle=gradient_angle,

                            custom_gradient=custom_gradient
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