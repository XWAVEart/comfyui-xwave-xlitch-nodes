# ComfyUI Custom Node Development Guide (for LLMs)

This document outlines the essential structure and components required to create a custom node for ComfyUI, designed to guide an LLM in generating correctly formatted Python code.

## Important Notes

### Repository Location
- All node development should be done in `/Volumes/T7/VibeCoding/comfyui-xwave-nodes/`
- This is the main repository for XWAVE ComfyUI nodes

### Seed Values
- All seed parameters in ComfyUI nodes MUST be between 0 and 2**32 - 1 (4294967295)
- This is a ComfyUI requirement for reproducibility and compatibility
- Never use negative values for seeds
- When implementing random seeds, ensure they stay within this range

### Import Handling for Custom Node Packages
- **CRITICAL**: ComfyUI loads each node .py file individually, NOT as part of a package structure
- This means relative imports (e.g., `from ...utils.base_node import XWaveNodeBase`) will FAIL
- When creating nodes that share common utilities or base classes:
  1. Add the parent directory to sys.path at the beginning of each node file
  2. Use absolute imports instead of relative imports
  3. Each node file must be self-contained and independently loadable

Example of correct import handling for nodes with shared utilities:
```python
"""
Example Node for ComfyUI XWAVE Nodes
"""

import sys
import os
# Add parent directory to path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

# Now use absolute imports (not relative)
from utils.base_node import XWaveNodeBase
from effects.my_effect import my_effect_function

class MyNode(XWaveNodeBase):
    # ... node implementation ...

# Each node file must have its own registration
NODE_CLASS_MAPPINGS = {
    "MyNodeInternalName": MyNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MyNodeInternalName": "My Node Display Name"
}
```

## 1. File Structure and Location

*   Custom nodes must reside within the **`ComfyUI/custom_nodes`** directory [1, 2].
*   Nodes can be organized into subdirectories within `custom_nodes` [1, 2].
*   Python files for nodes must have the **`.py` extension** [3-5].
*   A subdirectory intended as a package should contain an **`__init__.py`** file [3, 6, 7]. This file can be empty or contain package-level code [6, 7]. It is essential for ComfyUI to recognize the directory as a custom node package [7].
*   Filenames and directory names often use **underscores (`_`)** instead of hyphens (`-`) at lower levels [8]. Python doesn't like hyphens very much, so using underscores is safer [8]. Avoiding both altogether is also an option [8].

## 2. Core Node Definition: The Python Class

Each custom node is typically defined as a **Python `class`** [9-11]. It is good practice to name the class the same as the main node file [12].

```python
class MyCustomNode:
    # Class attributes and methods go here
    pass # Placeholder for basic structure
```

### 2.1. Essential Class Members
The class must contain specific attributes and methods that ComfyUI looks for to understand the node's behavior.

• **`__init__(self)` (Optional Method)**:
  - The constructor for the class.
  - Defined as `def __init__(self):`.
  - Often contains just `pass` if no special initialization is needed.

• **`@classmethod INPUT_TYPES(s)` (Required Method)**:
  - Must be decorated with `@classmethod`.
  - Must be named `INPUT_TYPES` (all caps) - NOT `input_types`.
  - Defines the inputs the node accepts.
  - Must return a dictionary.
  - This dictionary contains keys for input groups: "required", "optional", "hidden". At least "required" must be present and its value must be a dictionary.
  - The value for each group key ("required", etc.) is another dictionary.
  - The keys of this inner dictionary are the input field names (strings). These names must match the parameter names in the main logic method exactly.
  - The values for each input field name are tuples.
  - The first element of the tuple is the input type:
    * ComfyUI Types: "IMAGE", "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT". These types determine noodle connections and colors.
    * Python Primitive Types: "INT" (integer), "FLOAT" (decimal), "STRING" (text).
    * List of Strings: ["option1", "option2", ...] for dropdown selections.
  - The second element of the tuple (optional) is a configuration dictionary for primitive types ("INT", "FLOAT", "STRING").
    * Config keys include: "default", "min", "max", "step" (for "INT", "FLOAT"), "display" ("text", "multiline", "slider") (for "STRING").
    * For seed parameters, always set:
      - "min": 0
      - "max": 4294967295 (2**32 - 1)
      - "default": 0 or a random value within range
  - Important Tuple Syntax: A tuple with a single element must have a trailing comma (e.g., ("IMAGE",) instead of ("IMAGE")).

• **`RETURN_TYPES` (Required Attribute)**:
  - Defines the types of the outputs.
  - An attribute, not a method.
  - A tuple of strings, where each string is a type name (matching the types used in INPUT_TYPES).

• **`RETURN_NAMES` (Optional Attribute)**:
  - Provides human-readable names for the outputs in the UI.
  - A tuple of strings, where each string is a name for the corresponding type in RETURN_TYPES.

• **`FUNCTION` (Required Attribute)**:
  - Specifies the name of the Python method within the class that ComfyUI will call to execute the node's main logic.
  - A string attribute (e.g., `FUNCTION = "process"`).

• **`OUTPUT_NODE` (Optional Attribute)**:
  - Designates whether the node is a final output node.
  - A Boolean attribute (True or False). Default is False.

• **`CATEGORY` (Recommended Attribute)**:
  - Determines the menu path in the "Add Node" context menu.
  - A string attribute (e.g., `CATEGORY = "XWAVE/Color"`).

• **Main Logic Method (Required Method)**:
  - The method whose name is specified by the FUNCTION attribute.
  - Takes `self` as the first parameter.
  - Takes additional parameters corresponding to the input field names defined in INPUT_TYPES.
  - Must return a tuple containing the outputs, matching the order and types specified in RETURN_TYPES.

## 3. Node Registration

Outside the class definition (at the top level of the .py file, no indentation), you must register your node with ComfyUI using two dictionaries:

• **`NODE_CLASS_MAPPINGS` (Required Dictionary)**:
  - Maps the internal node name (string key) to the Python class object (value).
  - Example: `NODE_CLASS_MAPPINGS = {"MyAwesomeNodeInternalName": MyCustomNode}`.
  - The key (internal name) must be globally unique across all installed custom nodes.

• **`NODE_DISPLAY_NAME_MAPPINGS` (Required Dictionary)**:
  - Maps the internal node name (string key) to the human-readable name displayed in the ComfyUI UI.
  - Example: `NODE_DISPLAY_NAME_MAPPINGS = {"MyAwesomeNodeInternalName": "My Awesome Node"}`.
  - The key must exactly match the key used in NODE_CLASS_MAPPINGS.

## 4. Syntax and Code Style Notes

• **Indentation**: Python uses indentation (spaces, conventionally 4) to define code blocks.
• **Case Sensitivity**: Python is case-sensitive. ComfyUI types are typically uppercase strings.
• **Strings**: Strings are enclosed in single ('...') or double ("...") quotes.
• **Dictionaries**: Key-value pairs enclosed in curly braces {}.
• **Tuples**: Ordered sets of elements enclosed in round parentheses ().

## 5. Workflow and Debugging

• After creating or modifying a custom node file, restart ComfyUI to load the changes.
• ComfyUI scans the custom_nodes directory on startup and attempts to load .py files with the required headers.
• Read error messages in the ComfyUI console/terminal.
• Common errors include incorrect indentation, typos in attribute/method names, mismatched parameter/input names.

## Full Structure Example

```python
"""
Example Node for ComfyUI XWAVE Nodes
Description of what this node does.
"""

import sys
import os
# Add parent directory to path to enable imports (if using shared utilities)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

# Import any shared utilities or effect functions
from utils.base_node import XWaveNodeBase
from effects.my_effect import my_effect_function

class MyAwesomeNode(XWaveNodeBase):  # or just 'object' if not using base class
    """
    Detailed description of the node functionality.
    """
    
    @classmethod
    def INPUT_TYPES(cls):  # Must be INPUT_TYPES, not input_types
        return {
            "required": {
                "image": ("IMAGE",),  # ComfyUI type with trailing comma
                "my_string_input": ("STRING", {
                    "default": "Default text",
                    "multiline": False
                }),
                "my_selection": (["option1", "option2", "option3"],),
                "intensity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.01,
                    "display": "slider"
                }),
            },
            "optional": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 4294967295
                }),
            }
        }

    # Required attributes
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("processed_image",)
    FUNCTION = "process"  # Name of the method that runs the node
    CATEGORY = "XWAVE/Effects"  # Where it appears in the menu

    def process(self, image, my_string_input, my_selection, intensity, seed=0):
        """
        The main processing function.
        Parameter names must match those defined in INPUT_TYPES.
        """
        # Your processing logic here
        processed_image = image  # Example: pass through
        
        # Must return a tuple matching RETURN_TYPES
        return (processed_image,)


# Required registration dictionaries (NO INDENTATION)
NODE_CLASS_MAPPINGS = {
    "XWaveMyAwesomeNode": MyAwesomeNode  # Unique internal name -> Class
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "XWaveMyAwesomeNode": "XWAVE My Awesome Node"  # Internal name -> Display name
}
```

This structure provides the necessary blueprint for generating a functional ComfyUI custom node.