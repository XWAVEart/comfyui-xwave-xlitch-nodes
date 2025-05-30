# ComfyUI Node Conversion Plan for XWAVE Glitch Art Generator

## Overview

This document outlines the process for converting the XWAVE Glitch Art Generator effects into ComfyUI custom nodes. This conversion will enable users to integrate these powerful glitch effects into ComfyUI workflows for advanced image manipulation and artistic creation. 

THE GLITCH ART REPO IS LOCATED AT: /Volumes/T7/VibeCoding/glitch_art_app
We will be duplicating the effects found in the glitch art app into standalone comfy nodes. Do not modify the original files in glitch_art_app. 
All new code goes in this dir: comfyui-xwave-nodes
Make sure the modules are in the correct subdirs.
When possible make sure we are using the same default parameters from the original glitch_art_app
Keep in mind that we are testing on a separate machine and will not be able to import torch on this dev laptop.

## ComfyUI Node Architecture Overview

### Basic ComfyUI Node Structure
- **INPUT_TYPES**: Defines input parameters and their types
- **RETURN_TYPES**: Defines output types
- **FUNCTION**: The main execution function name
- **CATEGORY**: Node category in the UI
- **OUTPUT_NODE**: Whether the node produces output

### Key ComfyUI Concepts
1. **Tensor Format**: ComfyUI uses PyTorch tensors (BHWC format: Batch, Height, Width, Channels)
2. **Image Format**: Images are float32 tensors with values 0-1
3. **Node Registration**: Nodes must be registered in `NODE_CLASS_MAPPINGS`

## ComfyUI Node Development Standards (Updated)

Based on the official ComfyUI node development guide, here are critical standards to follow:

### 1. File and Directory Structure
- Custom nodes MUST reside in `ComfyUI/custom_nodes` directory
- Use **underscores** instead of hyphens in file/directory names
- Subdirectories must contain `__init__.py` files
- Python files must have `.py` extension

### 2. Class Definition Requirements
Each node class MUST have:
- `@classmethod INPUT_TYPES(cls)` - Returns dict with at minimum "required" key
- `RETURN_TYPES` - Tuple attribute (NOT a method) with trailing comma for single elements
- `FUNCTION` - String attribute naming the main logic method
- `CATEGORY` - String attribute for menu path (e.g., "Glitch Art/Color")
- Main logic method with name matching FUNCTION attribute

Optional attributes:
- `RETURN_NAMES` - Tuple of strings for output labels
- `OUTPUT_NODE` - Boolean (default False)

### 3. INPUT_TYPES Dictionary Structure
```python
{
    "required": {
        "field_name": ("TYPE",),  # Single element tuple needs comma
        "field_name2": ("TYPE", {config_dict}),  # With configuration
        "dropdown": (["option1", "option2"],),  # List for dropdown
    },
    "optional": {
        # Same structure as required
    },
    "hidden": {
        # For hidden inputs
    }
}
```

### 4. Type Specifications
**ComfyUI Types** (uppercase strings):
- "IMAGE", "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT"

**Primitive Types**:
- "INT" - Integer with optional min, max, step, default
- "FLOAT" - Float with optional min, max, step, default, display ("slider" or "number")
- "STRING" - String with optional default, multiline, display ("text" or "multi_line")

### 5. Critical Syntax Rules
- **Trailing commas** required for single-element tuples: `("IMAGE",)` not `("IMAGE")`
- **Case sensitivity**: Types must be uppercase, attributes must be exact
- **Parameter matching**: Input field names MUST match method parameter names exactly
- **No indentation** for NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS

### 6. Node Registration
```python
# At module level (no indentation)
NODE_CLASS_MAPPINGS = {
    "UniqueInternalName": ClassName
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UniqueInternalName": "Display Name in UI"
}
```

## Project Structure

```
comfyui_glitch_nodes/
├── __init__.py                    # Node registration
├── requirements.txt               # Dependencies
├── README.md                      # Documentation
├── utils/
│   ├── image_converter.py         # PIL <-> Tensor conversion utilities
│   ├── parameter_validation.py    # Input validation helpers
│   └── common_inputs.py           # Reusable input type definitions
├── nodes/
│   ├── color/                     # Color manipulation nodes
│   ├── distortion/                # Spatial distortion nodes
│   ├── glitch/                    # Glitch effect nodes
│   ├── noise/                     # Noise-based nodes
│   ├── patterns/                  # Pattern generation nodes
│   ├── sorting/                   # Pixel sorting nodes
│   ├── pixelate/                  # Pixelation effect nodes
│   ├── blend/                     # Image blending nodes
│   └── contour/                   # Contour effect nodes
└── examples/
    └── workflows/                 # Example ComfyUI workflows
```

## Phase 1: Foundation Setup (Week 1)

### 1.1 Create Base Infrastructure
- [x] Set up ComfyUI custom node package structure
- [x] Create image format conversion utilities (PIL ↔ Tensor)
- [x] Implement parameter validation framework
- [x] Create common input type definitions
- [ ] Set up testing framework

### 1.2 Base Node Class
```python
class GlitchNodeBase:
    """Base class for all glitch effect nodes"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "Glitch Art"
    
    def tensor_to_pil(self, tensor):
        """Convert ComfyUI tensor to PIL Image"""
        pass
    
    def pil_to_tensor(self, pil_image):
        """Convert PIL Image to ComfyUI tensor"""
        pass
```

## Phase 2: Node Categories Implementation

### 2.1 Color Manipulation Nodes (Week 2)

#### Nodes to Implement:
1. **ColorChannelManipulation**
   - Inputs: image, operation, channels, factor, seed
   - Complex parameter mapping for different operations

2. **RGBChannelShift**
   - Inputs: image, shift_r, shift_g, shift_b, wrap_mode

3. **HistogramGlitch**
   - Inputs: image, intensity, channel_mode, equalize

4. **ColorShiftExpansion**
   - Inputs: image, expansion_factor, pattern, direction

5. **Posterize**
   - Inputs: image, levels, dither, color_space

6. **CurvedHueShift**
   - Inputs: image, intensity, curve_type, preserve_luminance

7. **ColorFilter**
   - Inputs: image, filter_color, intensity, blend_mode

8. **ChromaticAberration**
   - Inputs: image, strength, direction, falloff

9. **VHSEffect**
   - Inputs: image, tracking_error, color_bleed, noise_amount, scan_lines

10. **NoiseEffect** ✅ (Completed)
    - Fully implemented with all parameters

### 2.2 Pixel Sorting Nodes (Week 3)

#### Nodes to Implement:
1. **AdvancedPixelSorting**
   - Inputs: image, algorithm, chunk_size, sort_by, reverse, parameters
   - Sub-algorithms: chunk, full_frame, spiral, polar, wrapped, perlin, voronoi

2. **PixelSortingClassic**
   - Inputs: image, mode, chunk_width, chunk_height, sort_by, reverse

3. **FullFrameSort**
   - Inputs: image, direction, sort_by, reverse

4. **SpiralSort**
   - Inputs: image, chunk_size, direction, sort_by

5. **PolarSorting**
   - Inputs: image, center_x, center_y, sort_mode, sort_by

### 2.3 Distortion Nodes (Week 4)

#### Nodes to Implement:
1. **PixelDrift**
   - Inputs: image, drift_amount, band_size, direction, color_shift

2. **PerlinDisplacement**
   - Inputs: image, scale, amplitude, octaves, seed

3. **WaveDistortion**
   - Inputs: image, wave_type, frequency, amplitude, phase

4. **RippleEffect**
   - Inputs: image, center_x, center_y, wavelength, amplitude, damping

5. **PixelScatter**
   - Inputs: image, scatter_amount, attribute, pattern, seed

6. **SliceOperations**
   - Inputs: image, operation, slice_size, direction, parameters

### 2.4 Glitch & Corruption Nodes (Week 5)

#### Nodes to Implement:
1. **BitManipulation**
   - Inputs: image, operation, chunk_size, skip_chunks, bit_range

2. **DataMoshBlocks**
   - Inputs: image, block_size, corruption_rate, mode, seed

3. **Databending**
   - Inputs: image, method, intensity, preserve_header

### 2.5 Additional Effect Nodes (Week 6)

#### Pattern Nodes:
1. **VoronoiEffects**
   - Inputs: image, num_points, effect_type, parameters

2. **ConcentricShapes**
   - Inputs: image, shape, center, size, count, color_mode

3. **MaskedMerge**
   - Inputs: image1, image2, mask_type, parameters

#### Utility Nodes:
1. **NoiseGenerator**
   - Inputs: image, noise_type, amount, parameters

2. **BlurSharpen**
   - Inputs: image, operation, kernel_size, strength

3. **ContourExtraction**
   - Inputs: image, mode, thickness, color, parameters

## Phase 3: Advanced Features (Week 7-8)

### 3.1 Batch Processing Support
- Implement batch processing for all nodes
- Handle multiple images in tensor format
- Optimize performance for batch operations

### 3.2 Parameter Presets
- Create preset system for common parameter combinations
- Implement preset loading/saving
- Add preset selector to nodes

### 3.3 Animation Support
- Add frame interpolation for parameters
- Support for animated sequences
- Keyframe-based parameter control

## Phase 4: Integration & Polish (Week 9-10)

### 4.1 ComfyUI Integration
- Register all nodes properly
- Create node icons/thumbnails
- Implement proper error handling
- Add progress callbacks

### 4.2 Documentation
- Create comprehensive node documentation
- Build example workflows
- Write usage tutorials
- Create video demonstrations

### 4.3 Testing & Optimization
- Unit tests for each node
- Performance benchmarking
- Memory usage optimization
- GPU acceleration where applicable

## Technical Considerations

### Image Format Conversion
```python
def tensor_to_pil(tensor):
    """Convert ComfyUI tensor (BHWC) to PIL Image"""
    # Handle batch dimension
    if len(tensor.shape) == 4:
        tensor = tensor[0]
    
    # Convert from 0-1 float to 0-255 uint8
    tensor = (tensor * 255).clamp(0, 255).to(torch.uint8)
    
    # Convert from HWC to PIL
    return Image.fromarray(tensor.cpu().numpy())

def pil_to_tensor(pil_image):
    """Convert PIL Image to ComfyUI tensor (BHWC)"""
    # Convert to numpy
    np_image = np.array(pil_image).astype(np.float32) / 255.0
    
    # Add batch dimension
    tensor = torch.from_numpy(np_image).unsqueeze(0)
    
    return tensor
```

### Parameter Mapping Strategy
1. **Enums**: Convert string choices to ComfyUI enum inputs (list of strings with trailing comma)
2. **Ranges**: Use INT/FLOAT with min/max/default/step values in config dict
3. **Colors**: Use STRING input type for hex colors
4. **Seeds**: Use INT input with special seed handling (-1 for random)
5. **Optional Parameters**: Use "optional" input category

### Common Input Configurations
```python
# Float slider
"parameter": ("FLOAT", {
    "default": 1.0,
    "min": 0.0,
    "max": 10.0,
    "step": 0.1,
    "display": "slider"
})

# Integer
"parameter": ("INT", {
    "default": 50,
    "min": 1,
    "max": 100
})

# String
"parameter": ("STRING", {
    "default": "default text",
    "multiline": False
})

# Dropdown
"parameter": (["option1", "option2", "option3"],)
```

### Memory Management
- Implement proper cleanup after processing
- Use context managers for large operations
- Consider streaming for very large images
- Implement tile-based processing for memory-intensive effects

## Example Node Implementation

```python
class ColorChannelManipulationNode(GlitchNodeBase):
    """Node for color channel manipulation effects"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "operation": (["swap", "invert", "adjust", "isolate", "mix"],),
                "channels": ("STRING", {"default": "RG"}),
                "factor": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "Glitch Art/Color"
    
    def process(self, image, operation, channels, factor, seed=-1):
        # Convert tensor to PIL
        pil_image = self.tensor_to_pil(image)
        
        # Apply effect
        result = color_channel_manipulation(
            pil_image, 
            operation, 
            channels, 
            factor,
            seed if seed != -1 else None
        )
        
        # Convert back to tensor
        return (self.pil_to_tensor(result),)
```

## Deployment Strategy

### 1. Package Distribution
- Create pip-installable package
- Submit to ComfyUI node registry
- Create GitHub repository with releases

### 2. Installation Process
```bash
# Clone into ComfyUI custom_nodes directory
cd ComfyUI/custom_nodes
git clone https://github.com/XWAVEart/comfyui-glitch-nodes
cd comfyui-glitch-nodes
pip install -r requirements.txt
```

### 3. Version Management
- Semantic versioning (MAJOR.MINOR.PATCH)
- Maintain compatibility with ComfyUI versions
- Document breaking changes

## Success Metrics
- [ ] All 40+ effects converted to nodes
- [ ] Comprehensive documentation
- [ ] Example workflows for each effect
- [ ] Performance benchmarks documented
- [ ] Community feedback incorporated
- [ ] Regular updates and bug fixes

## Timeline Summary
- **Weeks 1-2**: Foundation and Color nodes
- **Week 3**: Pixel Sorting nodes
- **Week 4**: Distortion nodes
- **Week 5**: Glitch nodes
- **Week 6**: Additional effects
- **Weeks 7-8**: Advanced features
- **Weeks 9-10**: Integration and polish

## Next Steps
1. Review and approve plan
2. Set up development environment
3. Create base node structure
4. Begin implementation of Phase 1 