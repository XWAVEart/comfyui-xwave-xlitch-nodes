"""
JPEG Artifacts Node for ComfyUI XWAVE Nodes
Simulates JPEG compression artifacts for glitch effects.
"""

from ...utils.base_node import XWaveNodeBase
from ...effects.jpeg_artifacts import simulate_jpeg_artifacts


class JPEGArtifactsNode(XWaveNodeBase):
    """
    Simulate JPEG compression artifacts by repeatedly compressing the image at low quality.
    Perfect for creating glitchy, lo-fi effects.
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
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Color"
    
    def process(self, image, intensity):
        """
        Process the image with JPEG artifacts.
        
        Args:
            image: Input image tensor
            intensity: Intensity of artifacts (0.0 to 1.0)
                      0 = minimal artifacts, 1 = extreme artifacts
        
        Returns:
            tuple: (processed_image_tensor,)
        """
        # Process the image batch
        result = self.process_batch(
            image,
            simulate_jpeg_artifacts,
            intensity=intensity
        )
        
        return (result,)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveJPEGArtifacts": JPEGArtifactsNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveJPEGArtifacts": "XWAVE JPEG Artifacts"
} 