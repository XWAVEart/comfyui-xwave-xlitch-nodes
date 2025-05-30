# ComfyUI XWAVE Nodes

A collection of artistic glitch and image manipulation nodes for ComfyUI, featuring advanced noise effects, color manipulations, distortions, and more.

## Installation

### Method 1: ComfyUI Manager (Recommended)
1. Install [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)
2. Search for "XWAVE" in the manager
3. Install "ComfyUI XWAVE Nodes"
4. Restart ComfyUI

### Method 2: Manual Installation
1. Navigate to your ComfyUI's `custom_nodes` directory:
```bash
cd /path/to/ComfyUI/custom_nodes
```

2. Clone this repository:
```bash
git clone https://github.com/XWAVEart/comfyui-xwave-nodes
```

3. Install dependencies:
```bash
cd comfyui-xwave-nodes
pip install -r requirements.txt
```

4. Restart ComfyUI

### Method 3: Direct Copy
1. Download this repository as a ZIP file
2. Extract the `comfyui-xwave-nodes` folder into your `ComfyUI/custom_nodes` directory
3. Install dependencies:
```bash
cd ComfyUI/custom_nodes/comfyui-xwave-nodes
pip install -r requirements.txt
```
4. Restart ComfyUI

## Available Nodes

All nodes can be found under the "XWAVE" category in the node menu.

### 🎨 Color Effects

#### XWAVE Noise Effect
Adds various types of noise to images with extensive customization options.

**Features:**
- 5 noise types: Film Grain, Digital, Colored, Salt & Pepper, Gaussian
- 4 blend modes: Overlay, Add, Multiply, Screen
- 3 patterns: Random, Perlin, Cellular
- Customizable grain size and color variation
- Seed control for reproducible results

**Inputs:**
- `image`: Input image
- `noise_type`: Type of noise effect
- `intensity`: Overall noise strength (0.0-1.0)
- `grain_size`: Size of noise particles (0.5-5.0)
- `color_variation`: Amount of color variation (0.0-1.0)
- `blend_mode`: How to blend noise with the image
- `pattern`: Noise generation pattern
- `noise_color`: Base color for colored noise (hex format)
- `seed`: Random seed (-1 for random)

## Usage Example

1. Add an image loader node
2. Find "XWAVE Noise Effect" under "XWAVE/Color" category
3. Connect image output to noise effect input
4. Adjust parameters to taste
5. Connect to preview or save node

## Workflow Examples

Example workflows can be found in the `examples/` directory.

## Tips for Best Results

### Noise Effect Tips:
- **Film Grain**: Use low intensity (0.1-0.3) for realistic film look
- **Digital Noise**: Works well with higher intensities
- **Pattern Selection**:
  - `random`: Classic noise
  - `perlin`: Organic, cloud-like patterns
  - `cellular`: Unique structured patterns
- **Blend Modes**:
  - `overlay`: Preserves image details
  - `add`: Brightens the image
  - `multiply`: Creates texture effects
  - `screen`: Lighter, ethereal effect

## Coming Soon

- **Color Manipulation**: Channel swapping, histogram effects, color filters
- **Pixel Sorting**: Advanced sorting algorithms with multiple modes
- **Distortion Effects**: Wave, ripple, and displacement effects
- **Glitch Effects**: Databending, bit manipulation, corruption effects
- **Pattern Generation**: Voronoi, concentric shapes, masked merges
- **And many more!**

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- ComfyUI community for the amazing platform
- Inspired by classic glitch art techniques and modern digital art

## Support

For questions, issues, or feature requests:
- Open an issue on [GitHub](https://github.com/XWAVEart/comfyui-xwave-xlitch-nodes)

---

Made with ❤️ by XWAVE 