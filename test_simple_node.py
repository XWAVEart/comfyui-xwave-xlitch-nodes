"""
Simple Test Node for ComfyUI XWAVE Nodes
Testing if nodes at root level are found by ComfyUI
"""

import torch
import numpy as np
from PIL import Image


class XWaveTestNode:
    """
    A simple test node to verify ComfyUI loading
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "test_value": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "display": "slider"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Test"
    
    def process(self, image, test_value):
        """
        Simple test processing - just multiply image by test_value
        """
        # Simple operation - multiply image by test_value
        result = image * test_value
        # Clamp to valid range
        result = torch.clamp(result, 0.0, 1.0)
        return (result,)


# Node display name mapping
NODE_CLASS_MAPPINGS = {
    "XWaveTestNode": XWaveTestNode
}

# Display names for the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveTestNode": "XWAVE Test Node"
} 