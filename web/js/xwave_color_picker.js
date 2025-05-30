/**
 * XWAVE Color Picker Extension for ComfyUI
 * Adds color picker widgets to string inputs that are meant for colors
 */

import { app } from "../../scripts/app.js";

console.log("[XWAVE] Color picker extension loading...");

app.registerExtension({
    name: "XWAVE.ColorPicker",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Only process XWAVE nodes
        if (!nodeData.name.startsWith("XWave")) {
            return;
        }
        
        console.log("[XWAVE] Processing node:", nodeData.name);

        // Store original getExtraMenuOptions if it exists
        const origGetExtraMenuOptions = nodeType.prototype.getExtraMenuOptions;

        // Override node creation
        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function() {
            const result = onNodeCreated?.apply(this, arguments);
            
            console.log("[XWAVE] Node created:", this.type, "Widgets:", this.widgets?.length);
            
            // Look for color inputs in widgets
            if (this.widgets) {
                for (const widget of this.widgets) {
                    console.log("[XWAVE] Widget:", widget.name, "Type:", widget.type, "Value:", widget.value);
                    
                    // Check if this is a color input (string widget with 'color' in name or hex color default)
                    // In ComfyUI, STRING inputs typically have type "customtext" or sometimes just the value type
                    if ((widget.type === "text" || widget.type === "customtext" || widget.type === "string" || !widget.type) && 
                        (widget.name.toLowerCase().includes("color") || 
                         (widget.value && typeof widget.value === "string" && widget.value.match(/^#[0-9A-Fa-f]{6}$/)))) {
                        
                        console.log("[XWAVE] Found color widget:", widget.name);
                        
                        // Override widget drawing to include color preview
                        const originalDraw = widget.draw;
                        widget.draw = function(ctx, node, widgetWidth, y, height) {
                            // Draw the original widget first
                            const originalResult = originalDraw?.apply(this, arguments);
                            
                            // Draw color preview box on the right side
                            const previewSize = height - 6;
                            const previewX = widgetWidth - previewSize - 5;
                            const previewY = y + 3;
                            
                            // Draw border
                            ctx.strokeStyle = "#666";
                            ctx.lineWidth = 1;
                            ctx.strokeRect(previewX, previewY, previewSize, previewSize);
                            
                            // Draw color if valid
                            if (this.value && typeof this.value === "string" && this.value.match(/^#?[0-9A-Fa-f]{6}$/)) {
                                const hexValue = this.value.startsWith("#") ? this.value : "#" + this.value;
                                ctx.fillStyle = hexValue;
                                ctx.fillRect(previewX + 1, previewY + 1, previewSize - 2, previewSize - 2);
                            } else {
                                // Draw checkerboard for invalid/no color
                                ctx.fillStyle = "#333";
                                ctx.fillRect(previewX + 1, previewY + 1, previewSize - 2, previewSize - 2);
                                ctx.fillStyle = "#555";
                                const halfSize = (previewSize - 2) / 2;
                                ctx.fillRect(previewX + 1, previewY + 1, halfSize, halfSize);
                                ctx.fillRect(previewX + 1 + halfSize, previewY + 1 + halfSize, halfSize, halfSize);
                            }
                            
                            return originalResult;
                        };
                        
                        // Store original callback
                        const originalCallback = widget.callback;
                        widget.callback = function(value) {
                            console.log("[XWAVE] Color widget value changed:", value);
                            return originalCallback?.apply(this, arguments);
                        };
                    }
                }
            }
            
            return result;
        };

        // Add color picker to extra menu options
        nodeType.prototype.getExtraMenuOptions = function(canvas, options) {
            const result = origGetExtraMenuOptions?.apply(this, arguments) || [];
            
            console.log("[XWAVE] Getting extra menu options for:", this.type);
            
            // Add color picker options for color widgets
            if (this.widgets) {
                for (const widget of this.widgets) {
                    if ((widget.type === "text" || widget.type === "customtext" || widget.type === "string" || !widget.type) && 
                        (widget.name.toLowerCase().includes("color") || 
                         (widget.value && typeof widget.value === "string" && widget.value.match(/^#[0-9A-Fa-f]{6}$/)))) {
                        
                        result.push({
                            content: `🎨 Pick color for ${widget.name}`,
                            callback: () => {
                                console.log("[XWAVE] Opening color picker for:", widget.name);
                                
                                // Create temporary color input
                                const input = document.createElement("input");
                                input.type = "color";
                                input.value = widget.value || "#000000";
                                input.style.position = "fixed";
                                input.style.left = "50%";
                                input.style.top = "50%";
                                input.style.transform = "translate(-50%, -50%)";
                                input.style.zIndex = "9999";
                                document.body.appendChild(input);
                                
                                // Handle color selection
                                const handleChange = (e) => {
                                    console.log("[XWAVE] Color selected:", e.target.value);
                                    widget.value = e.target.value.toUpperCase();
                                    widget.callback?.(widget.value);
                                    app.graph.setDirtyCanvas(true);
                                };
                                
                                const handleClose = () => {
                                    input.removeEventListener("change", handleChange);
                                    input.removeEventListener("blur", handleClose);
                                    document.body.removeChild(input);
                                };
                                
                                input.addEventListener("change", handleChange);
                                input.addEventListener("blur", handleClose);
                                
                                // Trigger click to open color picker
                                setTimeout(() => input.click(), 10);
                            }
                        });
                    }
                }
            }
            
            return result;
        };
    }
});

console.log("[XWAVE] Color picker extension loaded!"); 