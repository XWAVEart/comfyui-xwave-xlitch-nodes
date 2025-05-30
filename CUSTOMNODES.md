Creating your own custom nodes in ComfyUI involves defining Python classes and organizing them within specific directories so ComfyUI can discover and load them.
ComfyUI Node Lifecycle and Structure
When ComfyUI starts, it scans the custom_nodes directory for Python modules. A Python module is typically a directory containing an __init__.py file. For a module to be recognized as containing custom nodes, its __init__.py file must export NODE_CLASS_MAPPINGS. This file is executed when ComfyUI attempts to import the module. If there's an error during import, ComfyUI will report the module as failed to load, but will continue starting.
The __init__.py file can be very simple, primarily importing node classes from other Python files within the module and defining NODE_CLASS_MAPPINGS. For example:
from .python_file import MyCustomNode
NODE_CLASS_MAPPINGS = { "My Custom Node" : MyCustomNode }
__all__ = ["NODE_CLASS_MAPPINGS"]
Here, NODE_CLASS_MAPPINGS must be a dictionary where the keys are the unique names for your custom nodes (unique across the entire ComfyUI installation), and the values are the corresponding node classes.
Optionally, the __init__.py file can also export NODE_DISPLAY_NAME_MAPPINGS. This is another dictionary that maps the unique node names to a display name for the node in the UI. If this mapping is not provided, ComfyUI will use the unique name from NODE_CLASS_MAPPINGS as the display name.
If your custom node includes client-side JavaScript code, you'll typically place these .js files in a subdirectory (conventionally named js) relative to your module directory. You need to export the path to this directory (relative to the module) by defining WEB_DIRECTORY in your __init__.py. Only .js files will be served this way. Older methods of copying JavaScript files should not be used anymore.
Structure of a Custom Node Class
Every custom node is defined as a Python class. This class serves as a blueprint for the node object in the ComfyUI graph. Key properties are defined as class attributes or methods within this class:
•
CATEGORY: A string that determines where the node will appear in the "Add Node" menu in the ComfyUI UI. You can specify submenus using a path format like examples/trivial. If not specified, ComfyUI may assign a default category based on the folder name.
•
INPUT_TYPES: This is a @classmethod that defines the inputs for the node. It must return a dictionary. The top-level keys of this dictionary can be required, optional, and hidden. A node class must have at least the required key.
◦
The values associated with required, optional, or hidden keys are themselves dictionaries.
◦
In these inner dictionaries, keys are the names of the input fields (which must match the parameter names in the node's FUNCTION method), and values are tuples.
◦
The first element of the input tuple is a string indicating the data type of the field (e.g., "IMAGE", "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "INT", "STRING", "FLOAT"). It can also be a list of strings for a dropdown selection.
◦
The second element of the input tuple is an optional dictionary for additional configuration parameters for specific types like "INT", "STRING", or "FLOAT" (e.g., "default", "min", "max", "step", "multiline", "display").
◦
The @classmethod decorator is used for INPUT_TYPES so that ComfyUI can compute dynamic options at runtime.
•
RETURN_TYPES: A tuple of strings defining the data types returned by the node (e.g., ("IMAGE",)). If the node has multiple outputs, list their types in order. If there's only one output, remember the trailing comma ("IMAGE",) to ensure it's recognized as a tuple. If the node has no outputs, use an empty tuple ().
•
RETURN_NAMES: An optional tuple of strings providing names for the outputs. If omitted, ComfyUI will use the lowercase versions of the types defined in RETURN_TYPES. The order must match RETURN_TYPES.
•
FUNCTION: A string that specifies the name of the Python method within the class that will be called when the node is executed. This method serves as the entry point for the node's logic.
The Main Function (defined by FUNCTION)
The method specified by the FUNCTION attribute is where the node's core processing logic resides.
•
It receives inputs defined in INPUT_TYPES as named arguments. Required and hidden inputs are always passed. Optional inputs are only passed if they are connected to another node's output. It's good practice to provide default values for optional inputs in the function signature or capture them with **kwargs.
•
The method performs calculations or operations based on the inputs.
•
It must return a tuple whose elements correspond to the data types defined in RETURN_TYPES. Again, for a single output, remember the trailing comma (result,). Even if nothing is returned, you must return an empty tuple ().
Optional Node Properties
•
OUTPUT_NODE: A boolean attribute. Set to True if this node is considered an output node (like SaveImage), which tells ComfyUI to start tracing the graph backward from these nodes during execution. Defaults to False.
•
IS_CHANGED: An optional @classmethod used to control when a node is re-executed, even if its direct inputs haven't changed (e.g., if it uses a random number or loads an external file). It receives the same arguments as the FUNCTION method. It should return a Python object; if this object differs from the one returned in the previous run, the node is re-executed. Returning float("NaN") forces the node to always re-execute. Do not return True or False from this method, as True == True and False == False would prevent re-execution based on the comparison logic.
•
DEPRECATED: A boolean attribute. If True, the node is hidden in the UI by default but remains functional for existing workflows.
•
EXPERIMENTAL: A boolean attribute. If True, the node is marked as experimental in the UI, indicating it might change or be removed in the future.
•
INPUT_IS_LIST and OUTPUT_IS_LIST: Used to control sequential processing of data.
•
VALIDATE_INPUTS: An optional @classmethod called before workflow execution. It can validate inputs, particularly constants defined within the workflow. It receives arguments for the inputs it requests. It should return True if inputs are valid or a string message describing the error to prevent execution. If it takes an input_types argument, it receives a dictionary mapping connected input names to their types, and default type validation is skipped.
Development Environment and Debugging
A standard setup involves installing ComfyUI and using a code editor like Visual Studio Code. When developing, using a clean ComfyUI installation (perhaps a separate one) is recommended to avoid library conflicts with other custom nodes, which can complicate debugging.
When creating a new node file (.py), ComfyUI loads it on startup. Any changes require restarting the ComfyUI server for them to take effect.
Errors during node loading or execution are typically reported in the terminal where ComfyUI is running or potentially in the web browser console. Debugging involves reading these error messages carefully. They often provide clues like the type of error and the file/line number where it occurred. Starting with small changes and testing frequently can make debugging easier.
Getting Started Steps
A common way to start creating a custom node:
1.
Navigate to the ComfyUI/custom_nodes directory.
2.
Create a new folder for your node module (conventionally using hyphens, but underscores are safer for Python compatibility, or avoid separators if unsure, checking what other developers do).
3.
Inside the new folder, create an __init__.py file.
4.
Create another Python file (e.g., nodes.py or a descriptive name) within the module folder to define your node class(es).
5.
Define your node class with the required CATEGORY, INPUT_TYPES, RETURN_TYPES, and FUNCTION attributes/methods.
6.
Define the function specified by FUNCTION to handle the node's logic.
7.
In __init__.py, import your node class and define NODE_CLASS_MAPPINGS to export your node(s).
8.
Restart ComfyUI.
9.
Check the terminal for import success or failure messages. If successful, the node should appear in the "Add Node" menu under the specified CATEGORY.
Alternatively, some tools like comfy-cli provide scaffolding commands (comfy node scaffold) to help set up the initial directory structure and files based on prompts.