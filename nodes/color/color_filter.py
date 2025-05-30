"""
Color Filter Node for ComfyUI XWAVE Nodes
Apply color filters with various blend modes and filter types.
"""

from ...utils.base_node import XWaveNodeBase
from ...effects.color_filter import color_filter


class ColorFilterNode(XWaveNodeBase):
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
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
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
        # Process the image batch
        result = self.process_batch(
            image,
            color_filter,
            filter_type=filter_type,
            color=color,
            blend_mode=blend_mode,
            opacity=opacity,
            gradient_color2=gradient_color2,
            gradient_angle=gradient_angle,
            custom_gradient=custom_gradient
        )
        
        return (result,)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveColorFilter": ColorFilterNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveColorFilter": "XWAVE Color Filter"
} 