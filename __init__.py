"""
ComfyUI XWAVE Nodes
A collection of artistic glitch and image manipulation nodes for ComfyUI.
"""

# Import node classes
from .nodes.color.noise_effect import NoiseEffectNode

# Node class mappings - ComfyUI uses this to register nodes
NODE_CLASS_MAPPINGS = {
    "XWaveNoiseEffect": NoiseEffectNode,
}

# Display name mappings - how nodes appear in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveNoiseEffect": "XWAVE Noise Effect",
}

# Version info
__version__ = "1.0.0"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"] 