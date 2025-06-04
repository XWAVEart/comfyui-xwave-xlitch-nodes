from .cellular_noise_node import CellularNoiseNode

NODE_CLASS_MAPPINGS = {
    "CellularNoiseNode": CellularNoiseNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CellularNoiseNode": "Cellular Noise"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"] 