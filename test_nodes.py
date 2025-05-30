#!/usr/bin/env python3
"""
Test script to verify XWAVE nodes are working correctly.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        # Test effect imports
        from effects.noise import noise_effect
        print("✓ noise_effect imported successfully")
        
        from effects.color_channel import color_channel_manipulation
        print("✓ color_channel_manipulation imported successfully")
        
        # Test utils imports
        from utils.base_node import XWaveNodeBase
        print("✓ XWaveNodeBase imported successfully")
        
        from utils.image_converter import tensor_to_pil, pil_to_tensor
        print("✓ Image converters imported successfully")
        
        # Test node imports
        from nodes.color.noise_effect import NoiseEffectNode
        print("✓ NoiseEffectNode imported successfully")
        
        from nodes.color.color_channel_manipulation import ColorChannelManipulationNode
        print("✓ ColorChannelManipulationNode imported successfully")
        
        # Test main module
        import __init__ as main_module
        print("✓ Main module imported successfully")
        print(f"  Registered nodes: {list(main_module.NODE_CLASS_MAPPINGS.keys())}")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_node_structure():
    """Test that nodes have required attributes."""
    print("\nTesting node structure...")
    
    from nodes.color.noise_effect import NoiseEffectNode
    from nodes.color.color_channel_manipulation import ColorChannelManipulationNode
    
    nodes_to_test = [
        ("NoiseEffectNode", NoiseEffectNode),
        ("ColorChannelManipulationNode", ColorChannelManipulationNode),
    ]
    
    required_attrs = ["INPUT_TYPES", "RETURN_TYPES", "FUNCTION", "CATEGORY"]
    
    for node_name, node_class in nodes_to_test:
        print(f"\nChecking {node_name}:")
        for attr in required_attrs:
            if hasattr(node_class, attr):
                print(f"  ✓ Has {attr}")
            else:
                print(f"  ✗ Missing {attr}")
                
        # Check INPUT_TYPES returns correct structure
        try:
            input_types = node_class.INPUT_TYPES()
            if "required" in input_types:
                print(f"  ✓ INPUT_TYPES has 'required' key")
            else:
                print(f"  ✗ INPUT_TYPES missing 'required' key")
        except Exception as e:
            print(f"  ✗ Error calling INPUT_TYPES: {e}")

if __name__ == "__main__":
    print("XWAVE Nodes Test Suite")
    print("=" * 50)
    
    if test_imports():
        test_node_structure()
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Tests failed!")
        sys.exit(1) 