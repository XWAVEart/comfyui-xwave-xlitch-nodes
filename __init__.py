"""
ComfyUI XWAVE Nodes
A collection of artistic glitch and image manipulation nodes for ComfyUI.
"""

# Import node classes
from .nodes.color.noise_effect import NoiseEffectNode
from .nodes.color.color_channel_manipulation import ColorChannelManipulationNode
from .nodes.color.rgb_channel_shift import RGBChannelShiftNode
from .nodes.color.histogram_glitch import HistogramGlitchNode
from .nodes.color.color_shift_expansion import ColorShiftExpansionNode
from .nodes.color.posterize import PosterizeNode
from .nodes.color.curved_hue_shift import CurvedHueShiftNode
from .nodes.color.color_filter import ColorFilterNode
from .nodes.color.chromatic_aberration import ChromaticAberrationNode
from .nodes.color.gaussian_blur import GaussianBlurNode
from .nodes.color.jpeg_artifacts import JPEGArtifactsNode
from .nodes.color.sharpen import SharpenEffectNode

# Node class mappings - ComfyUI uses this to register nodes
NODE_CLASS_MAPPINGS = {
    "XWaveNoiseEffect": NoiseEffectNode,
    "XWaveColorChannelManipulation": ColorChannelManipulationNode,
    "XWaveRGBChannelShift": RGBChannelShiftNode,
    "XWaveHistogramGlitch": HistogramGlitchNode,
    "XWaveColorShiftExpansion": ColorShiftExpansionNode,
    "XWavePosterize": PosterizeNode,
    "XWaveCurvedHueShift": CurvedHueShiftNode,
    "XWaveColorFilter": ColorFilterNode,
    "XWaveChromaticAberration": ChromaticAberrationNode,
    "XWaveGaussianBlur": GaussianBlurNode,
    "XWaveJPEGArtifacts": JPEGArtifactsNode,
    "XWaveSharpenEffect": SharpenEffectNode,
}

# Display name mappings - how nodes appear in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveNoiseEffect": "XWAVE Noise Effect",
    "XWaveColorChannelManipulation": "XWAVE Color Channel Manipulation",
    "XWaveRGBChannelShift": "XWAVE RGB Channel Shift",
    "XWaveHistogramGlitch": "XWAVE Histogram Glitch",
    "XWaveColorShiftExpansion": "XWAVE Color Shift Expansion",
    "XWavePosterize": "XWAVE Posterize",
    "XWaveCurvedHueShift": "XWAVE Curved Hue Shift",
    "XWaveColorFilter": "XWAVE Color Filter",
    "XWaveChromaticAberration": "XWAVE Chromatic Aberration",
    "XWaveGaussianBlur": "XWAVE Gaussian Blur",
    "XWaveJPEGArtifacts": "XWAVE JPEG Artifacts",
    "XWaveSharpenEffect": "XWAVE Sharpen Effect",
}

# Version info
__version__ = "1.0.0"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"] 