"""
ComfyUI XWAVE Nodes
A collection of artistic glitch and image manipulation nodes for ComfyUI.
"""

import os
import sys
from pathlib import Path

# Add the package directory to Python path
package_dir = Path(__file__).parent
if str(package_dir) not in sys.path:
    sys.path.insert(0, str(package_dir))

# Initialize node mappings
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Import nodes from subdirectories
# Since ComfyUI loads each file individually, we'll just make sure our structure is correct
# The actual loading happens when ComfyUI scans the directories

# Color nodes
color_node_files = [
    'nodes.color.chromatic_aberration',
    'nodes.color.color_channel_manipulation',
    'nodes.color.color_filter',
    'nodes.color.color_shift_expansion',
    'nodes.color.curved_hue_shift',
    'nodes.color.gaussian_blur',
    'nodes.color.histogram_glitch',
    'nodes.color.jpeg_artifacts',
    'nodes.color.noise_effect',
    'nodes.color.posterize',
    'nodes.color.rgb_channel_shift',
    'nodes.color.sharpen',
]

# Pixelate node
other_node_files = [
    'nodes.pixelate.pixelate_node',
]

all_node_files = color_node_files + other_node_files

# Try to import each node
for node_module in all_node_files:
    try:
        # Dynamic import
        parts = node_module.split('.')
        module = None
        
        # Try different import methods
        try:
            # Method 1: Direct import as submodule
            exec(f"from .{node_module} import NODE_CLASS_MAPPINGS as mappings, NODE_DISPLAY_NAME_MAPPINGS as display")
            NODE_CLASS_MAPPINGS.update(locals()['mappings'])
            NODE_DISPLAY_NAME_MAPPINGS.update(locals()['display'])
            print(f"Loaded {node_module}")
        except:
            # Method 2: Import from file path
            file_path = os.path.join(package_dir, *parts) + '.py'
            if os.path.exists(file_path):
                import importlib.util
                spec = importlib.util.spec_from_file_location(node_module, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'NODE_CLASS_MAPPINGS'):
                    NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
                if hasattr(module, 'NODE_DISPLAY_NAME_MAPPINGS'):
                    NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
                print(f"Loaded {node_module} via file import")
    except Exception as e:
        print(f"Failed to load {node_module}: {e}")
        import traceback
        traceback.print_exc()

print(f"Total nodes loaded: {len(NODE_CLASS_MAPPINGS)}")

# ComfyUI uses this to detect web extensions
WEB_DIRECTORY = "./web"

# Make sure we export the mappings
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY'] 