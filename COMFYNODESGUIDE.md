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

## 1. File Structure and Location

◦ The second element of the tuple (optional) is a configuration dictionary for primitive types ("INT", "FLOAT", "STRING").
▪ Config keys include: "default", "min", "max", "step" (for "INT", "FLOAT"), "display" ("text", "multi_line") (for "STRING").
▪ For seed parameters, always set:
  - "min": 0
  - "max": 4294967295 (2**32 - 1)
  - "default": 0 or a random value within range
◦ Important Tuple Syntax: A tuple with a single element must have a trailing comma (e.g., ("IMAGE",) instead of ("IMAGE")). This is a technical requirement for Python to distinguish it from a simple parenthesized expression.

// ... existing code ... 