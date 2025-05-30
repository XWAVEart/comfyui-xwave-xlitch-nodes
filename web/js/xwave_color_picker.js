/**
 * XWAVE Color Picker Extension for ComfyUI
 * Adds color picker widgets to string inputs that are meant for colors
 */

import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
    name: "XWAVE.ColorPicker",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Only process XWAVE nodes
        if (!nodeData.name.startsWith("XWave")) {
            return;
        }

        // Store original getExtraMenuOptions if it exists
        const origGetExtraMenuOptions = nodeType.prototype.getExtraMenuOptions;

        // Override node creation
        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function() {
            const result = onNodeCreated?.apply(this, arguments);
            
            // Look for color inputs in widgets
            if (this.widgets) {
                for (const widget of this.widgets) {
                    // Check if this is a color input (string widget with 'color' in name or hex color default)
                    if (widget.type === "text" && 
                        (widget.name.toLowerCase().includes("color") || 
                         (widget.value && widget.value.match(/^#[0-9A-Fa-f]{6}$/)))) {
                        
                        // Add color picker button
                        const colorButton = document.createElement("input");
                        colorButton.type = "color";
                        colorButton.value = widget.value || "#000000";
                        colorButton.style.marginLeft = "5px";
                        colorButton.style.cursor = "pointer";
                        colorButton.style.width = "40px";
                        colorButton.style.height = "20px";
                        colorButton.style.border = "1px solid #666";
                        colorButton.style.borderRadius = "3px";
                        
                        // Store reference to color picker on widget
                        widget.colorPicker = colorButton;
                        
                        // Update text input when color picker changes
                        colorButton.addEventListener("change", (e) => {
                            widget.value = e.target.value.toUpperCase();
                            widget.callback?.(widget.value);
                        });
                        
                        // Update color picker when text input changes
                        const originalCallback = widget.callback;
                        widget.callback = function(value) {
                            // Validate hex color
                            if (value.match(/^#?[0-9A-Fa-f]{6}$/)) {
                                const hexValue = value.startsWith("#") ? value : "#" + value;
                                widget.colorPicker.value = hexValue;
                            }
                            originalCallback?.call(this, value);
                        };
                        
                        // Override widget drawing to include color preview
                        const originalDraw = widget.draw;
                        widget.draw = function(ctx, node, width, y, height) {
                            // Call original draw
                            if (originalDraw) {
                                originalDraw.call(this, ctx, node, width, y, height);
                            } else {
                                // Default text widget drawing
                                ctx.fillStyle = "#222";
                                ctx.fillRect(0, y, width, height);
                                ctx.fillStyle = "#fff";
                                ctx.font = "12px Arial";
                                ctx.textAlign = "left";
                                ctx.fillText(this.value || "", 10, y + height * 0.7);
                            }
                            
                            // Draw color preview box
                            const previewSize = height - 6;
                            const previewX = width - previewSize - 5;
                            const previewY = y + 3;
                            
                            // Draw border
                            ctx.strokeStyle = "#666";
                            ctx.lineWidth = 1;
                            ctx.strokeRect(previewX, previewY, previewSize, previewSize);
                            
                            // Draw color
                            if (this.value && this.value.match(/^#?[0-9A-Fa-f]{6}$/)) {
                                const hexValue = this.value.startsWith("#") ? this.value : "#" + this.value;
                                ctx.fillStyle = hexValue;
                                ctx.fillRect(previewX + 1, previewY + 1, previewSize - 2, previewSize - 2);
                            }
                        };
                    }
                }
            }
            
            return result;
        };

        // Add color picker to extra menu options
        nodeType.prototype.getExtraMenuOptions = function(canvas, options) {
            const result = origGetExtraMenuOptions?.apply(this, arguments) || [];
            
            // Add color picker options for color widgets
            if (this.widgets) {
                for (const widget of this.widgets) {
                    if (widget.type === "text" && 
                        (widget.name.toLowerCase().includes("color") || 
                         (widget.value && widget.value.match(/^#[0-9A-Fa-f]{6}$/)))) {
                        
                        result.push({
                            content: `Pick color for ${widget.name}`,
                            callback: () => {
                                // Create temporary color input
                                const input = document.createElement("input");
                                input.type = "color";
                                input.value = widget.value || "#000000";
                                input.style.position = "absolute";
                                input.style.left = "-9999px";
                                document.body.appendChild(input);
                                
                                input.addEventListener("change", (e) => {
                                    widget.value = e.target.value.toUpperCase();
                                    widget.callback?.(widget.value);
                                    document.body.removeChild(input);
                                });
                                
                                // Trigger click to open color picker
                                input.click();
                            }
                        });
                    }
                }
            }
            
            return result;
        };
    }
}); 