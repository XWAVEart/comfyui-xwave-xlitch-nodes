"""
Base node class for ComfyUI XWAVE Nodes.
Provides common functionality for all glitch effect nodes.
"""

from .image_converter import tensor_to_pil, pil_to_tensor, tensor_batch_to_pil_list, pil_list_to_tensor_batch


class XWaveNodeBase:
    """Base class for all XWAVE glitch effect nodes."""
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        Define input types. Should be overridden by subclasses.
        """
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "XWAVE/Glitch"
    
    def tensor_to_pil(self, tensor):
        """Convert ComfyUI tensor to PIL Image."""
        return tensor_to_pil(tensor)
    
    def pil_to_tensor(self, pil_image):
        """Convert PIL Image to ComfyUI tensor."""
        return pil_to_tensor(pil_image)
    
    def process_batch(self, tensor, effect_function, **kwargs):
        """
        Process a batch of images with the given effect function.
        
        Args:
            tensor: Input tensor in BHWC format
            effect_function: Function to apply to each PIL image
            **kwargs: Arguments to pass to the effect function
        
        Returns:
            torch.Tensor: Processed batch tensor
        """
        # Convert batch to PIL images
        pil_images = tensor_batch_to_pil_list(tensor)
        
        # Process each image
        processed_images = []
        for img in pil_images:
            processed_img = effect_function(img, **kwargs)
            processed_images.append(processed_img)
        
        # Convert back to tensor batch
        return pil_list_to_tensor_batch(processed_images)
    
    def process(self, image, **kwargs):
        """
        Main processing function. Should be overridden by subclasses.
        
        Args:
            image: Input image tensor
            **kwargs: Additional parameters
        
        Returns:
            tuple: (processed_image_tensor,)
        """
        raise NotImplementedError("Subclasses must implement the process method") 