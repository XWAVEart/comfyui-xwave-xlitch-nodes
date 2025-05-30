"""
Image conversion utilities for ComfyUI Glitch Nodes.
Handles conversion between ComfyUI tensor format and PIL Image format.
"""

import torch
import numpy as np
from PIL import Image


def tensor_to_pil(tensor):
    """
    Convert ComfyUI tensor (BHWC format) to PIL Image.
    
    Args:
        tensor: PyTorch tensor in BHWC format (Batch, Height, Width, Channels)
                Values should be in range [0, 1] as float32
    
    Returns:
        PIL.Image: RGB image
    """
    # Handle batch dimension - take first image if batch
    if len(tensor.shape) == 4:
        tensor = tensor[0]
    
    # Ensure tensor is on CPU
    if tensor.is_cuda:
        tensor = tensor.cpu()
    
    # Convert from 0-1 float to 0-255 uint8
    tensor_255 = (tensor * 255).clamp(0, 255).to(torch.uint8)
    
    # Convert to numpy array
    np_array = tensor_255.numpy()
    
    # Handle different channel counts
    if np_array.shape[2] == 1:  # Grayscale
        np_array = np_array.squeeze(2)
        return Image.fromarray(np_array, mode='L')
    elif np_array.shape[2] == 3:  # RGB
        return Image.fromarray(np_array, mode='RGB')
    elif np_array.shape[2] == 4:  # RGBA
        return Image.fromarray(np_array, mode='RGBA')
    else:
        raise ValueError(f"Unsupported number of channels: {np_array.shape[2]}")


def pil_to_tensor(pil_image):
    """
    Convert PIL Image to ComfyUI tensor (BHWC format).
    
    Args:
        pil_image: PIL.Image object
    
    Returns:
        torch.Tensor: Tensor in BHWC format with values in [0, 1]
    """
    # Convert to RGB if not already (handles RGBA, L, etc.)
    if pil_image.mode not in ['RGB', 'RGBA']:
        pil_image = pil_image.convert('RGB')
    
    # Convert to numpy array
    np_image = np.array(pil_image).astype(np.float32) / 255.0
    
    # Add batch dimension and convert to tensor
    tensor = torch.from_numpy(np_image).unsqueeze(0)
    
    return tensor


def tensor_batch_to_pil_list(tensor):
    """
    Convert a batch of ComfyUI tensors to a list of PIL Images.
    
    Args:
        tensor: PyTorch tensor in BHWC format
    
    Returns:
        list: List of PIL.Image objects
    """
    batch_size = tensor.shape[0]
    return [tensor_to_pil(tensor[i:i+1]) for i in range(batch_size)]


def pil_list_to_tensor_batch(pil_images):
    """
    Convert a list of PIL Images to a batch tensor.
    
    Args:
        pil_images: List of PIL.Image objects
    
    Returns:
        torch.Tensor: Batch tensor in BHWC format
    """
    if not pil_images:
        raise ValueError("Empty image list provided")
    
    tensors = [pil_to_tensor(img) for img in pil_images]
    return torch.cat(tensors, dim=0)


def ensure_rgb(pil_image):
    """
    Ensure PIL image is in RGB format.
    
    Args:
        pil_image: PIL.Image object
    
    Returns:
        PIL.Image: RGB image
    """
    if pil_image.mode != 'RGB':
        return pil_image.convert('RGB')
    return pil_image 