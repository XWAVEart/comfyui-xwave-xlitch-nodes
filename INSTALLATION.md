# Installation Guide for ComfyUI XWAVE Nodes

## Prerequisites

- ComfyUI installed and working
- Python 3.8 or higher
- Git (for cloning the repository)

## Installation Methods

### Method 1: Using ComfyUI Manager (Easiest - Coming Soon)

Once published to the ComfyUI Manager registry, you'll be able to:
1. Open ComfyUI
2. Go to Manager → Install Custom Nodes
3. Search for "XWAVE"
4. Click Install
5. Restart ComfyUI

### Method 2: Git Clone (Recommended)

1. **Open a terminal/command prompt**

2. **Navigate to your ComfyUI custom_nodes folder:**
   ```bash
   # Windows example:
   cd C:\ComfyUI\custom_nodes
   
   # Mac/Linux example:
   cd ~/ComfyUI/custom_nodes
   ```

3. **Clone this repository:**
   ```bash
   git clone https://github.com/XWAVEart/comfyui-xwave-nodes
   ```

4. **Install dependencies:**
   ```bash
   cd comfyui-xwave-nodes
   pip install -r requirements.txt
   ```

5. **Restart ComfyUI**

### Method 3: Manual Download

1. **Download the repository:**
   - Go to https://github.com/XWAVEart/comfyui-xwave-nodes
   - Click "Code" → "Download ZIP"

2. **Extract the ZIP file:**
   - Extract the contents to your `ComfyUI/custom_nodes` folder
   - Rename the extracted folder to `comfyui-xwave-nodes` (remove any `-main` suffix)

3. **Install dependencies:**
   - Open terminal/command prompt
   - Navigate to the extracted folder:
     ```bash
     cd /path/to/ComfyUI/custom_nodes/comfyui-xwave-nodes
     pip install -r requirements.txt
     ```

4. **Restart ComfyUI**

## Verifying Installation

1. Start ComfyUI
2. Right-click in the workflow area
3. Look for "XWAVE" category in the node menu
4. You should see "XWAVE Noise Effect" under "XWAVE/Color"

## Updating

### If installed via Git:
```bash
cd ComfyUI/custom_nodes/comfyui-xwave-nodes
git pull
pip install -r requirements.txt --upgrade
```

### If installed manually:
- Re-download and replace the folder
- Run `pip install -r requirements.txt --upgrade`

## Troubleshooting

### Nodes don't appear
1. Check the ComfyUI console for error messages
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Make sure the folder is named exactly `comfyui-xwave-nodes`
4. Restart ComfyUI completely

### Import errors
- Install missing dependencies: `pip install numpy scipy pillow`
- Make sure you're using the same Python environment as ComfyUI

### Performance issues
- The noise effects are CPU-based and may be slower on large images
- Consider reducing image size before applying effects

## Support

- GitHub Issues: https://github.com/XWAVEart/comfyui-xwave-nodes/issues
- Discord: Coming soon 