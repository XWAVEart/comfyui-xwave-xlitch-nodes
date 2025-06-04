# Cellular Noise Node for ComfyUI

This node adds cellular noise patterns to images in ComfyUI. It creates a pattern of circles with customizable noise inside each circle, which can be blended with the original image using various blend modes.

## Features

- Multiple noise types: RGB, Grayscale, Palette, and Gaussian
- Two layout options: Grid and Hexagonal
- Various blend modes: Overlay, Add, Multiply, Screen, Soft Light, Hard Light, Color Dodge, Color Burn, Linear Dodge, Linear Burn, and Difference
- Adjustable circle size (8-128 pixels)
- Customizable noise intensity at center and edges
- Linear or radial gradient options
- Optional antialiasing for smoother circle edges
- Support for custom color palettes

## Installation

1. Place the `cellular_noise` folder in your ComfyUI's `custom_nodes` directory
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Restart ComfyUI

## Usage

1. Add the "Cellular Noise" node to your workflow
2. Connect an image input
3. Adjust the parameters to achieve the desired effect:
   - Circle Size: Controls the size of each noise cell
   - Layout: Choose between grid or hexagonal patterns
   - Noise Type: Select the type of noise to generate
   - Blend Mode: Choose how the noise blends with the original image
   - Center/Edge Noise: Control noise intensity at different positions
   - Gradient Type: Choose between linear or radial gradients
   - Reverse Gradient: Invert the gradient direction
   - Antialias: Enable for smoother circle edges

### Palette Mode

When using the "palette" noise type, you need to provide a palette file. The palette file should be a text file with one RGB color per line, formatted as:
```
R G B
R G B
...
```
Where R, G, and B are integers between 0 and 255.

## Example

A typical workflow might look like:
1. Load Image
2. Cellular Noise (with desired settings)
3. Save Image

## Dependencies

- numpy
- Pillow
- scipy

## License

This project is licensed under the MIT License - see the LICENSE file for details. 