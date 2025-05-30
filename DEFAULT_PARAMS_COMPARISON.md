# Default Parameters Comparison: glitch_art_app vs ComfyUI XWAVE Nodes

## Summary
This document compares the default parameter values between the original glitch_art_app forms and our ComfyUI XWAVE nodes implementation.

## Differences Found

### 1. **Chromatic Aberration**
✅ All defaults match:
- intensity: 5.0
- pattern: 'radial'
- red_shift_x/y: 0.0
- blue_shift_x/y: 0.0
- center_x/y: 0.5
- falloff: 'quadratic'
- edge_enhancement: 0.0
- color_boost: 1.0
- seed: 0

### 2. **RGB Channel Shift**
✅ All defaults match:
- shift_amount: 42
- direction: 'horizontal'
- center_channel: 'green'
- mode: 'shift'

### 3. **Histogram Glitch**
⚠️ Some differences in phase values:
- r_mode: 'solarize' ✅
- g_mode: 'solarize' → **'log'** ❌ (ComfyUI has 'log')
- b_mode: 'solarize' → **'gamma'** ❌ (ComfyUI has 'gamma')
- r_freq: 1.0 ✅
- g_freq: 1.0 ✅
- b_freq: 1.0 ✅
- **r_phase**: 0.4 → **0.0** ❌ (ComfyUI has 0.0)
- **g_phase**: 0.3 → **0.0** ❌ (ComfyUI has 0.0)
- **b_phase**: 0.2 → **0.0** ❌ (ComfyUI has 0.0)
- gamma_val: 0.5 ✅

### 4. **Color Shift Expansion**
✅ All defaults match:
- num_points: 7
- shift_amount: 20
- expansion_type: 'circle'
- pattern_type: 'random'
- color_theme: 'full-spectrum'
- saturation_boost: 0.5
- value_boost: 0.0
- decay_factor: 0.2

### 5. **Noise Effect**
✅ All defaults match:
- noise_type: 'film_grain'
- intensity: 0.3
- grain_size: 1.0
- color_variation: 0.2
- noise_color: '#FFFFFF'
- blend_mode: 'overlay'
- pattern: 'random'
- seed: 0

### 6. **Pixelate**
⚠️ Attribute default differs:
- width: 16 ✅
- height: 16 ✅
- **attribute**: 'hue' → **'color'** ❌ (ComfyUI has 'color')

### 7. **Posterize**
✅ All defaults match:
- levels: 4

### 8. **Curved Hue Shift**
✅ All defaults match:
- curve_value: 180
- shift_amount: 90

### 9. **Color Filter**
✅ All defaults match:
- filter_type: 'solid'
- blend_mode: 'overlay'
- opacity: 0.5
- color: '#FF0000'
- gradient_color2: '#0000FF'
- gradient_angle: 45

### 10. **Gaussian Blur**
✅ All defaults match:
- radius: 5.0
- sigma: 1.0

### 11. **Sharpen**
⚠️ Method default differs in ComfyUI:
- **method**: 'unsharp_mask' → **Not implemented in ComfyUI**
- intensity: 1.0 ✅

### 12. **JPEG Artifacts**
✅ All defaults match:
- intensity: 1.0

## Recommended Updates

Based on this comparison, the following nodes need their defaults updated to match the original:

1. **HistogramGlitchNode**:
   - Change `g_mode` default from 'log' to 'solarize'
   - Change `b_mode` default from 'gamma' to 'solarize'
   - Change `r_phase` default from 0.0 to 0.4
   - Change `g_phase` default from 0.0 to 0.3
   - Change `b_phase` default from 0.0 to 0.2

2. **PixelateNode**:
   - Change `attribute` default from 'color' to 'hue'

3. **SharpenNode** (if implemented):
   - Add `method` parameter with default 'unsharp_mask'

## Note on Missing Effects

Some effects from the original app are not yet implemented in ComfyUI nodes:
- Perlin Displacement
- Ripple Effect
- VHS Effect
- Wave Distortion
- Pixel Scatter
- Various sorting effects
- Slice and block manipulations
- Data mosh blocks
- Contour effect
- Concentric shapes
- Voronoi pixelate

These could be added in future updates to provide the full range of effects from the original application. 