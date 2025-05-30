"""
Jpeg Artifacts Node for ComfyUI XWAVE Nodes
Self-contained implementation with all effects included.
"""

import torch
import numpy as np
from PIL import Image
from io import BytesIO


class JPEGArtifactsNode:
    """
    Simulate JPEG compression artifacts for glitch effects.
    Produces authentic JPEG artifacts by actual compression.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "intensity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "slider"
                }),
            }
        }
    
    return_types = ("IMAGE",)
    function = "process"
    category = "XWAVE/Color"
    
    def simulate_jpeg_artifacts(self, image, intensity):
        """
        Simulate JPEG compression artifacts by repeatedly compressing the image at low quality.

        Args:
            image (PIL.Image): The original image to process.
            intensity (float): A value between 0 and 1 controlling the intensity of the effect.
                               0 for minimal artifacts, 1 for extreme artifacts.

        Returns:
            PIL.Image: The image with simulated JPEG artifacts.
        """
        if not 0 <= intensity <= 1:
            raise ValueError("Intensity must be between 0 and 1.")

        # Map intensity to number of iterations and quality
        # More extreme - up to 30 iterations
        iterations = int(1 + 29 * intensity)  # 1 to 30 iterations
        # Allow quality to go down to 1
        quality = int(90 - 89 * intensity)    # 90 to 1 quality

        # Convert to RGB mode if the image has an alpha channel or is in a different mode
        if image.mode != 'RGB':
            # Create a white background for RGBA images
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                # Paste the image on the background using the alpha channel as mask
                background.paste(image, mask=image.split()[3])
                current_image = background
            else:
                current_image = image.convert('RGB')
        else:
            current_image = image.copy()

        for _ in range(iterations):
            # Save the image to a BytesIO object with the specified quality
            buffer = BytesIO()
            current_image.save(buffer, format="JPEG", quality=quality)
            # Reload the image from the buffer
            buffer.seek(0)
            current_image = Image.open(buffer)
            current_image.load()  # Make sure the image data is loaded

        return current_image
    
    def process(self, image, intensity):
        """
        Process the image with JPEG artifacts effect.
        
        Args:
            image: Input image tensor
            intensity: JPEG compression intensity
        
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
            
            # Apply jpeg artifacts effect
            processed_img = self.simulate_jpeg_artifacts(
                pil_img,
                intensity=intensity
            )
            
            # Convert back to tensor format
            result_array = np.array(processed_img).astype(np.float32) / 255.0
            result.append(result_array)
        
        # Stack results and convert to tensor
        result = np.stack(result)
        return (torch.from_numpy(result),)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveJPEGArtifacts": JPEGArtifactsNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveJPEGArtifacts": "XWAVE JPEG Artifacts"
} 