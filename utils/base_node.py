"""
Base node class for ComfyUI XWAVE Nodes.
Provides common functionality for all glitch effect nodes.
"""

import torch
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
    
    def clear_memory(self):
        """Clear CUDA cache and unused memory."""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    def process_batch(self, tensor, effect_function, **kwargs):
        """
        Process a batch of images with the given effect function.
        Memory efficient implementation that processes one image at a time.
        
        Args:
            tensor: Input tensor in BHWC format
            effect_function: Function to apply to each PIL image
            **kwargs: Arguments to pass to the effect function
        
        Returns:
            torch.Tensor: Processed batch tensor
        """
        batch_size = tensor.shape[0]
        processed_images = []
        
        try:
            # Process each image individually to minimize memory usage
            for i in range(batch_size):
                # Convert single image to PIL
                img = tensor_to_pil(tensor[i:i+1])
                
                # Process the image
                processed_img = effect_function(img, **kwargs)
                processed_images.append(processed_img)
                
                # Clear memory after each image
                if i % 4 == 0:  # Clear every 4 images to balance performance
                    self.clear_memory()
            
            # Convert back to tensor batch
            result = pil_list_to_tensor_batch(processed_images)
            
            # Final memory cleanup
            self.clear_memory()
            
            return result
            
        except Exception as e:
            # Ensure memory is cleared even if an error occurs
            self.clear_memory()
            raise e
    
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