"""
Color Channel Manipulation Node for ComfyUI XWAVE Nodes
Manipulate image color channels through various operations.
"""

from ...utils.base_node import XWaveNodeBase
from ...effects.color_channel import color_channel_manipulation


class ColorChannelManipulationNode(XWaveNodeBase):
    """
    Manipulate image color channels with swap, invert, adjust, and negative operations.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "operation": (["swap", "invert", "adjust", "negative"],),
                "intensity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "slider"
                }),
            },
            "optional": {
                "channels": ("STRING", {
                    "default": "RG",
                    "multiline": False
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, operation, intensity, channels="RG"):
        """
        Process the image with color channel manipulation.
        
        Args:
            image: Input image tensor
            operation: Type of manipulation (swap, invert, adjust, negative)
            intensity: Adjustment factor for certain operations
            channels: Channels to manipulate (e.g., "RG" for red-green, "R" for red)
        
        Returns:
            tuple: (processed_image_tensor,)
        """
        # Map channel string to appropriate format for the effect function
        channel_map = {
            "RG": "red-green",
            "RB": "red-blue", 
            "GB": "green-blue",
            "R": "red",
            "G": "green",
            "B": "blue",
            "red-green": "red-green",
            "red-blue": "red-blue",
            "green-blue": "green-blue",
            "red": "red",
            "green": "green",
            "blue": "blue"
        }
        
        # Convert channels to lowercase and map to appropriate format
        mapped_channels = channel_map.get(channels.upper(), channels.lower())
        
        # For adjust operation, use intensity as factor
        # For other operations, factor is not needed
        factor = intensity if operation == "adjust" else None
        
        # Process the image batch
        result = self.process_batch(
            image,
            color_channel_manipulation,
            manipulation_type=operation,
            choice=mapped_channels,
            factor=factor
        )
        
        return (result,)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveColorChannelManipulation": ColorChannelManipulationNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveColorChannelManipulation": "XWAVE Color Channel Manipulation"
} 