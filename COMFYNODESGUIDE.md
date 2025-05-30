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


# ComfyUI Custom Node Development Guide (for LLMs)

This document outlines the essential structure and components required to create a custom node for ComfyUI, designed to guide an LLM in generating correctly formatted Python code.


## 1. File Structure and Location

*   Custom nodes must reside within the **`ComfyUI/custom_nodes`** directory [1, 2].
*   Nodes can be organized into subdirectories within `custom_nodes` [1, 2].
*   Python files for nodes must have the **`.py` extension** [3-5].
*   A subdirectory intended as a package should contain an **`__init__.py`** file [3, 6, 7]. This file can be empty or contain package-level code [6, 7]. It is essential for ComfyUI to recognize the directory as a custom node package [7].
*   Filenames and directory names often use **underscores (`_`)** instead of hyphens (`-`) at lower levels [8]. Python doesn't like hyphens very much, so using underscores is safer [8]. Avoiding both altogether is also an option [8].
◦ The second element of the tuple (optional) is a configuration dictionary for primitive types ("INT", "FLOAT", "STRING").
▪ Config keys include: "default", "min", "max", "step" (for "INT", "FLOAT"), "display" ("text", "multi_line") (for "STRING").
▪ For seed parameters, always set:
  - "min": 0
  - "max": 4294967295 (2**32 - 1)
  - "default": 0 or a random value within range
◦ Important Tuple Syntax: A tuple with a single element must have a trailing comma (e.g., ("IMAGE",) instead of ("IMAGE")). This is a technical requirement for Python to distinguish it from a simple parenthesized expression. 

## 2. Core Node Definition: The Python Class

Each custom node is typically defined as a **Python `class`** [9-11]. It is good practice to name the class the same as the main node file [12].

```python
class MyCustomNode:
    # Class attributes and methods go here
    pass # Placeholder for basic structure
2.1. Essential Class Members
The class must contain specific attributes and methods that ComfyUI looks for to understand the node's behavior.
•
__init__(self) (Optional Method):
◦
The constructor for the class.
◦
Defined as def __init__(self):.
◦
Often contains just pass if no special initialization is needed.
•
@classmethod input_types(s) (Required Method):
◦
Must be decorated with @classmethod.
◦
Defines the inputs the node accepts.
◦
Must return a dictionary.
◦
This dictionary contains keys for input groups: "required", "optional", "hidden". At least "required" must be present and its value must be a dictionary.
◦
The value for each group key ("required", etc.) is another dictionary.
◦
The keys of this inner dictionary are the input field names (strings). These names must match the parameter names in the main logic method exactly.
◦
The values for each input field name are tuples.
◦
The first element of the tuple is the input type. This is specified as a string or a list of strings:
▪
ComfyUI Types: "IMAGE", "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT". These types determine noodle connections and colors.
▪
Python Primitive Types: "INT" (integer), "FLOAT" (decimal), "STRING" (text). These are often referred to as Primitives.
▪
List of Strings: ["option1", "option2", ...] for dropdown selections.
◦
The second element of the tuple (optional) is a configuration dictionary for primitive types ("INT", "FLOAT", "STRING").
▪
Config keys include: "default", "min", "max", "step" (for "INT", "FLOAT"), "display" ("text", "multi_line") (for "STRING").
◦
Important Tuple Syntax: A tuple with a single element must have a trailing comma (e.g., ("IMAGE",) instead of ("IMAGE")). This is a technical requirement for Python to distinguish it from a simple parenthesized expression.
•
return_types (Required Attribute):
◦
Defines the types of the outputs.
◦
An attribute, not a method.
◦
A tuple of strings, where each string is a type name (matching the types used in input_types). The order matters. The returned value must be of the type declared here.
•
return_names (Optional Attribute):
◦
Provides human-readable names for the outputs in the UI.
◦
An attribute.
◦
A tuple of strings, where each string is a name for the corresponding type in return_types. The order must match return_types. Useful when returning multiple outputs, especially of the same type.
•
function (Required Attribute):
◦
Specifies the name of the Python method within the class that ComfyUI will call to execute the node's main logic.
◦
A string attribute (e.g., function = "run"). The actual method definition must use this exact name. This is the "main sort of a function" for the node.
•
output_node (Optional Attribute):
◦
Designates whether the node is a final output node. ComfyUI traces workflows backward from output nodes designated this way.
◦
A Boolean attribute (True or False). Default is False.
•
category (Recommended Attribute):
◦
Determines the menu path in the "Add Node" context menu.
◦
A string attribute (e.g., category = "MyNodes/Image"). If omitted, ComfyUI may place it in a default category like "SD".
•
Main Logic Method (Required Method):
◦
The method whose name is specified by the function attribute.
◦
Defined using def (e.g., def run(self, ...):). It is technically a method as it's part of a class.
◦
Takes self as the first parameter.
◦
Takes additional parameters corresponding to the input field names defined in the input_types dictionary. The order of these parameters should ideally match the order in input_types for clarity.
◦
Contains the core logic to process inputs and generate outputs.
◦
Must return a tuple containing the outputs, matching the order and types specified in return_types and return_names.
3. Node Registration
Outside the class definition (at the top level of the .py file, no indentation), you must register your node with ComfyUI using two dictionaries:
•
NODE_CLASS_MAPPINGS (Required Dictionary):
◦
Maps the internal node name (string key) to the Python class object (value) that defines the node.
◦
Example: NODE_CLASS_MAPPINGS = {"MyAwesomeNodeInternalName": MyCustomNode}.
◦
The key (internal name) must be globally unique across all installed custom nodes. You can prefix it with initials or package names to help ensure uniqueness.
◦
The value is the name of the class defined earlier in the file.
•
NODE_DISPLAY_NAME_MAPPINGS (Required Dictionary):
◦
Maps the internal node name (string key) to the human-readable name displayed in the ComfyUI UI.
◦
Example: NODE_DISPLAY_NAME_MAPPINGS = {"MyAwesomeNodeInternalName": "My Awesome Node"}.
◦
The key must exactly match the key used in NODE_CLASS_MAPPINGS.
◦
The value is the name users see in the "Add Node" menu. Spaces are allowed in this display name.
# Example registration outside the class

# Map internal node name to the class
NODE_CLASS_MAPPINGS = {
    "MyAwesomeNodeInternalName": MyCustomNode
}

# Map internal node name to the UI display name
NODE_DISPLAY_NAME_MAPPINGS = {
    "MyAwesomeNodeInternalName": "My Awesome Node"
}
4. Syntax and Code Style Notes
•
Indentation: Python uses indentation (spaces, conventionally 4) to define code blocks. Correct indentation is critical and incorrect indentation is a common source of errors. Registration dictionaries are not indented relative to the class. Visual Studio Code often defaults to 4 spaces per tab.
•
Case Sensitivity: Python is case-sensitive. Keywords, variable names, attribute names (like return_types), and method names (input_types, the function specified by function) must be spelled with correct capitalization. ComfyUI types are typically uppercase strings (e.g., "IMAGE", "INT").
•
Strings: Strings are enclosed in single ('...') or double ("...") quotes. Attributes like function and category, type names, and display names are strings.
•
Comments: Start a line comment with #. Multi-line comments or docstrings use triple quotes """...""". Comments are ignored by the Python interpreter.
•
Dictionaries: Key-value pairs enclosed in curly braces {}. Keys must be unique. Values can be of any data type, including other dictionaries (nested dictionaries). Used extensively for node inputs and configuration.
•
Tuples: Ordered sets of elements enclosed in round parentheses (). The order of elements matters. Used for specifying input types and output types/names. A tuple with a single element requires a trailing comma.
•
Attributes vs. Methods: Methods are defined using def and perform actions (often taking inputs and returning outputs). Attributes are defined using =, store values, and don't typically perform complex calculations. ComfyUI nodes use both (e.g., input_types is a method, return_types is an attribute).
5. Workflow and Debugging
•
After creating or modifying a custom node file, restart ComfyUI to load the changes. ComfyUI scans the custom_nodes directory on startup and attempts to load .py files with the required headers.
•
Read error messages in the ComfyUI console/terminal. Error messages often indicate the type of error, file name, and line number.
•
Check the web browser console for client-side errors.
•
Common errors include incorrect indentation, typos in attribute/method names, mismatched parameter/input names, incorrect types in return_types, and missing or incorrect registration mappings.
•
Creating a clean installation of ComfyUI without many other custom nodes can help avoid conflicts and simplify debugging when starting.
This structure provides the necessary blueprint for generating a functional ComfyUI custom node. The logic within the main method (defined by the function attribute) can be any valid Python code.
# Full structure example for clarity

# Class definition
class MyAwesomeNode:
    # Optional init
    # def __init__(self):
    #     pass

    @classmethod
    def input_types(s):
        return {
            "required": {
                "my_image_input": ("IMAGE",), # ComfyUI type
                "my_string_input": ("STRING", {"default": "Default text", "display": "text"}), # Python primitive with config
                "my_selection_input": (["Option1", "Option2"],), # List for selection
            },
            "optional": {
                 "optional_number": ("INT", {"default": 0}),
            }
        }

    # Required attributes
    return_types = ("IMAGE", "STRING") # Outputs an Image and a String
    return_names = ("Processed Image", "Status Message") # Names for the outputs
    function = "run_logic" # Name of the method that runs the node

    # Optional attributes
    output_node = False # Not a final output node
    category = "MyCustomNodes" # Category in the Add Node menu

    # Main logic method - name matches 'function' attribute
    def run_logic(self, my_image_input, my_string_input, my_selection_input, optional_number=0):
        # --- Your node's processing logic goes here ---
        # Access inputs via parameters: my_image_input, my_string_input, etc.
        # Perform operations...
        # Generate outputs...

        processed_image_output = my_image_input # Example: pass image through
        status_message_output = f"Processed with selection: {my_selection_input} and text: {my_string_input}"

        # --- End of processing logic ---

        # Return a tuple of outputs, matching return_types and return_names order
        return (processed_image_output, status_message_output)

# Required registration dictionaries (NO INDENTATION)
NODE_CLASS_MAPPINGS = {
    "MyAwesomeNodeInternalName": MyAwesomeNode # Map internal name to the Class object
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MyAwesomeNodeInternalName": "My Awesome Node" # Map internal name to the display name
}