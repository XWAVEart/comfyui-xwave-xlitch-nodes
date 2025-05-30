"""
ComfyUI XWAVE Nodes
A collection of artistic glitch and image manipulation nodes for ComfyUI.
"""

# Import node classes
from .nodes.color.noise_effect import NoiseEffectNode
from .nodes.color.color_channel_manipulation import ColorChannelManipulationNode
from .nodes.color.rgb_channel_shift import RGBChannelShiftNode
from .nodes.color.histogram_glitch import HistogramGlitchNode

# Node class mappings - ComfyUI uses this to register nodes
NODE_CLASS_MAPPINGS = {
    "XWaveNoiseEffect": NoiseEffectNode,
    "XWaveColorChannelManipulation": ColorChannelManipulationNode,
    "XWaveRGBChannelShift": RGBChannelShiftNode,
    "XWaveHistogramGlitch": HistogramGlitchNode,
}

# Display name mappings - how nodes appear in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveNoiseEffect": "XWAVE Noise Effect",
    "XWaveColorChannelManipulation": "XWAVE Color Channel Manipulation",
    "XWaveRGBChannelShift": "XWAVE RGB Channel Shift",
    "XWaveHistogramGlitch": "XWAVE Histogram Glitch",
}

# Version info
__version__ = "1.0.0"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"] 