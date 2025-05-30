"""
ComfyUI XWAVE Nodes
A collection of artistic glitch and image manipulation nodes for ComfyUI.
"""

import os
import importlib

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Get the directory path
node_directory = os.path.dirname(os.path.realpath(__file__))

# List of node files to import (without .py extension)
node_list = [
    "nodes.color.chromatic_aberration",
    "nodes.color.color_channel_manipulation", 
    "nodes.color.color_filter",
    "nodes.color.color_shift_expansion",
    "nodes.color.curved_hue_shift",
    "nodes.color.gaussian_blur",
    "nodes.color.histogram_glitch",
    "nodes.color.jpeg_artifacts",
    "nodes.color.noise_effect",
    "nodes.color.posterize",
    "nodes.color.rgb_channel_shift",
    "nodes.color.sharpen",
    "nodes.pixelate.pixelate_node",
]

# Import each node
for node_module in node_list:
    try:
        # Import the module
        module = importlib.import_module(f".{node_module}", package=__name__)
        
        # Get the mappings if they exist
        if hasattr(module, "NODE_CLASS_MAPPINGS"):
            NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
        
        if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
            NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
            
    except Exception as e:
        print(f"Failed to import {node_module}: {e}")

# ComfyUI uses this to detect the extension
WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"] 