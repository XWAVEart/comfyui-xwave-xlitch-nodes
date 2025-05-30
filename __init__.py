"""
ComfyUI XWAVE Nodes
A collection of artistic glitch and image manipulation nodes for ComfyUI.
"""

import os
import importlib.util
import sys

__version__ = "1.0.0"

# Initialize the mappings
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Get the directory of this file
node_dir = os.path.dirname(os.path.realpath(__file__))

# List of subdirectories containing nodes
node_subdirs = ['color', 'distortion', 'glitch', 'noise', 'patterns', 'sorting', 'pixelate', 'blend', 'contour']

# Iterate through each subdirectory
for subdir in node_subdirs:
    subdir_path = os.path.join(node_dir, 'nodes', subdir)
    
    # Check if the subdirectory exists
    if os.path.exists(subdir_path):
        # List all Python files in the subdirectory
        for filename in os.listdir(subdir_path):
            if filename.endswith('.py') and not filename.startswith('_'):
                # Construct the full path to the file
                file_path = os.path.join(subdir_path, filename)
                module_name = f"nodes.{subdir}.{filename[:-3]}"
                
                try:
                    # Import the module dynamically
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    
                    # Add parent directory to path before executing to handle imports
                    sys.path.insert(0, node_dir)
                    spec.loader.exec_module(module)
                    sys.path.pop(0)
                    
                    # Check if the module has the required mappings
                    if hasattr(module, 'NODE_CLASS_MAPPINGS'):
                        NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
                    
                    if hasattr(module, 'NODE_DISPLAY_NAME_MAPPINGS'):
                        NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
                        
                except Exception as e:
                    print(f"Failed to load node from {file_path}: {e}")
                    import traceback
                    traceback.print_exc()

# Print summary of loaded nodes
print(f"XWAVE Nodes: Loaded {len(NODE_CLASS_MAPPINGS)} nodes") 