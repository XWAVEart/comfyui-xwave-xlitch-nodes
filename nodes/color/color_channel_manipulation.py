
Self-contained implementation with all effects included.
"""

Color Channel Manipulation Node for ComfyUI XWAVE Nodes
Manipulate image color channels through various operations.
"""

import torch
import numpy as np
from PIL import Image


class ColorChannelManipulationNode:
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
    
    return_types = ("IMAGE",)
    function = "process"
    category = "XWAVE/Color"
    
    
        def color_channel_manipulation(image, manipulation_type, choice, factor=None):
        """
        Manipulate the image's color channels (swap, invert, adjust intensity, or create negative).
    
        Args:
            image (Image): PIL Image object to process.
            manipulation_type (str): 'swap', 'invert', 'adjust', or 'negative'.
            choice (str): Specific channel or swap pair (e.g., 'red-green', 'red').
                         Not used for 'negative' type.
            factor (float, optional): Intensity adjustment factor (required for 'adjust').
    
        Returns:
            Image: Processed image with modified color channels.
        """
        if image.mode not in ['RGB', 'RGBA']:
            image = image.convert('RGB')
        elif image.mode == 'RGBA':  # Convert RGBA to RGB by discarding alpha
            image = image.convert('RGB')

        img_array = np.array(image)
    
        if manipulation_type == 'swap':
            if choice == 'red-green':
                # R, G, B -> G, R, B
                img_array = img_array[:, :, [1, 0, 2]]
            elif choice == 'red-blue':
                # R, G, B -> B, G, R
                img_array = img_array[:, :, [2, 1, 0]]
            elif choice == 'green-blue':
                # R, G, B -> R, B, G
                img_array = img_array[:, :, [0, 2, 1]]
        elif manipulation_type == 'invert':
            if choice == 'red':
                img_array[:, :, 0] = 255 - img_array[:, :, 0]
            elif choice == 'green':
                img_array[:, :, 1] = 255 - img_array[:, :, 1]
            elif choice == 'blue':
                img_array[:, :, 2] = 255 - img_array[:, :, 2]
        elif manipulation_type == 'negative':
            img_array = 255 - img_array
        elif manipulation_type == 'adjust':
            if factor is None:
                raise ValueError("Factor is required for adjust manipulation")
        
            # Ensure factor is positive; negative factors would invert and are better handled by 'invert'
            # Clamping to 0 to avoid issues with large negative factors if not strictly positive.
            safe_factor = max(0, factor)

            if choice == 'red':
                img_array[:, :, 0] = np.clip(img_array[:, :, 0] * safe_factor, 0, 255).astype(np.uint8)
            elif choice == 'green':
                img_array[:, :, 1] = np.clip(img_array[:, :, 1] * safe_factor, 0, 255).astype(np.uint8)
            elif choice == 'blue':
                img_array[:, :, 2] = np.clip(img_array[:, :, 2] * safe_factor, 0, 255).astype(np.uint8)

        return Image.fromarray(img_array) 
    
        def process(self, image, operation, intensity, channels="RG"):
        """
        Process the image with color channel manipulation effect.
        
        Args:
image: Input image tensor
            operation: Type of manipulation (swap, invert, adjust, negative)
            intensity: Adjustment factor for certain operations
            channels: Channels to manipulate (e.g., "RG" for red-green, "R" for red)
        
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
            
            # Apply color channel manipulation effect
            processed_img = self.color_channel_manipulation(
                pil_img,
                manipulation_type=operation,

                            choice=mapped_channels,

                            factor=factor
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)



# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveColorChannelManipulation": ColorChannelManipulationNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveColorChannelManipulation": "XWAVE Color Channel Manipulation"
} 